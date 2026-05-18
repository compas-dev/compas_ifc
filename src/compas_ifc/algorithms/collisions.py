"""Vectorized mesh-mesh collision detection via ray-casting.

Detects volumetric overlap between two meshes by checking whether any
vertex of mesh A lies inside mesh B, and vice versa.  This corresponds
to the IFC concept of *interference* (``IfcRelInterferesElements``).

The algorithm:

1. Fan-triangulate both meshes into ``(T, 3, 3)`` NumPy arrays.
2. For each vertex of mesh A, cast a ray along +Z and count
   intersections with the triangles of mesh B.  An odd count means
   the vertex is inside B.
3. Repeat with B's vertices against A's triangles.
4. If any vertex is inside the other mesh, the pair collides.

The ray-triangle intersection uses the Möller-Trumbore algorithm,
fully vectorized over the ``(P, T)`` point × triangle matrix.
"""

import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Point


def fast_mesh_mesh_collision_numpy(
    verts_a: np.ndarray,
    tris_a: np.ndarray,
    verts_b: np.ndarray,
    tris_b: np.ndarray,
    tolerance: float = 1e-6,
    min_depth: float = 1e-4,
) -> list[Point]:
    """Numpy-direct variant of :func:`fast_mesh_mesh_collision`.

    Bypasses the :class:`compas.datastructures.Mesh` round-trip — callers
    pass the vertex array and triangle-index array directly. Used by
    :meth:`compas_ifc.element.GenericElement.compute_collisions` with
    cached per-element arrays.

    Parameters
    ----------
    verts_a, verts_b : np.ndarray
        Shape ``(V, 3)`` — world-coord vertex arrays.
    tris_a, tris_b : np.ndarray
        Shape ``(F, 3)`` — triangle-vertex-index arrays (must already be
        triangulated; quads/n-gons should be fan-triangulated upstream).
    tolerance : float, optional
    min_depth : float, optional
        See :func:`fast_mesh_mesh_collision`.
    """
    if len(verts_a) == 0 or len(verts_b) == 0 or len(tris_a) == 0 or len(tris_b) == 0:
        return []

    a_tri_coords = verts_a[tris_a]  # (T, 3, 3)
    b_tri_coords = verts_b[tris_b]  # (T, 3, 3)

    penetrating = []
    for verts, tri_coords in ((verts_a, b_tri_coords), (verts_b, a_tri_coords)):
        inside, _ = _points_inside_mesh(verts, tri_coords, tolerance)
        if not np.any(inside):
            continue
        surf_dist = _min_surface_distance(verts[inside], tri_coords)
        for i, idx in enumerate(np.where(inside)[0]):
            if surf_dist[i] > min_depth:
                penetrating.append(Point(*verts[idx]))
    return penetrating


def fast_mesh_mesh_collision(
    a: Mesh,
    b: Mesh,
    tolerance: float = 1e-6,
    min_depth: float = 1e-4,
) -> list[Point]:
    """Detect volumetric collision between two meshes.

    Returns the world-space points that penetrate the other mesh.
    An empty list means no collision.

    Parameters
    ----------
    a : Mesh
        The first mesh.
    b : Mesh
        The second mesh.
    tolerance : float, optional
        Numerical tolerance for the ray-triangle intersection test.
    min_depth : float, optional
        Minimum penetration depth to count as a collision.  Vertices
        classified as "inside" but closer than *min_depth* to the mesh
        surface are excluded (these are touching, not penetrating).
        Default ``1e-4``.

    Returns
    -------
    list[Point]
        Vertices of A inside B and vertices of B inside A.

    """
    verts_a, tris_a = _mesh_to_numpy(a)
    verts_b, tris_b = _mesh_to_numpy(b)
    return fast_mesh_mesh_collision_numpy(verts_a, tris_a, verts_b, tris_b, tolerance, min_depth)


def _mesh_to_numpy(mesh: Mesh) -> tuple[np.ndarray, np.ndarray]:
    """Convert a compas Mesh to (vertices, triangle_indices) numpy arrays."""
    verts, faces = mesh.to_vertices_and_faces(triangulated=True)
    return (
        np.asarray(verts, dtype=np.float64),
        np.asarray(faces, dtype=np.int64) if faces else np.empty((0, 3), dtype=np.int64),
    )


def _min_surface_distance(
    points: np.ndarray,
    triangles: np.ndarray,
) -> np.ndarray:
    """Compute the minimum distance from each point to the mesh surface.

    For each point, computes the signed distance to every triangle plane
    and returns the minimum absolute distance.  This is a lower bound on
    the true point-to-surface distance (exact when the nearest surface
    point lies within a face, not on an edge or vertex).

    Parameters
    ----------
    points : np.ndarray
        Shape ``(P, 3)``.
    triangles : np.ndarray
        Shape ``(T, 3, 3)``.

    Returns
    -------
    np.ndarray
        Shape ``(P,)`` — minimum distance to the nearest face plane.

    """
    v0 = triangles[:, 0, :]  # (T, 3)
    e1 = triangles[:, 1, :] - v0  # (T, 3)
    e2 = triangles[:, 2, :] - v0  # (T, 3)

    normals = np.cross(e1, e2)  # (T, 3)
    norms = np.linalg.norm(normals, axis=1, keepdims=True)  # (T, 1)
    normals = normals / np.maximum(norms, 1e-12)  # (T, 3)

    P = points.shape[0]
    T = v0.shape[0]

    # Batch to limit memory: each batch produces (B, T) array
    BATCH = max(1, 2_000_000 // max(T, 1))
    min_dists = np.full(P, np.inf, dtype=np.float64)

    for start in range(0, P, BATCH):
        end = min(start + BATCH, P)
        diffs = points[start:end, np.newaxis, :] - v0[np.newaxis, :, :]  # (B, T, 3)
        signed = np.abs(np.einsum("btk,tk->bt", diffs, normals))  # (B, T)
        min_dists[start:end] = signed.min(axis=1)

    return min_dists


def _points_inside_mesh(
    points: np.ndarray,
    triangles: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Test which points lie inside a closed triangle mesh via ray casting.

    Casts a ray along +Z from each point and counts intersections with
    the triangle mesh.  Odd count → inside.  Also returns the minimum
    positive ray parameter *t* for each inside point — this is the
    distance to the nearest surface along +Z and serves as a proxy for
    penetration depth.

    Parameters
    ----------
    points : np.ndarray
        Shape ``(P, 3)``.
    triangles : np.ndarray
        Shape ``(T, 3, 3)``.
    tolerance : float
        Numerical tolerance.

    Returns
    -------
    inside : np.ndarray
        Boolean array of shape ``(P,)``.
    min_depths : np.ndarray
        Float array of shape ``(P,)``.  For inside points, the minimum
        positive *t* value (distance to nearest surface along +Z).
        For outside points, the value is 0.

    """
    # Perturb query points slightly in XY to avoid ray-edge/vertex
    # coincidences that cause double-counting on shared triangle edges.
    rng = np.random.RandomState(42)
    perturbation = rng.uniform(-1e-8, 1e-8, size=points.shape)
    perturbation[:, 2] = 0.0  # keep Z exact
    points = points + perturbation

    v0 = triangles[:, 0, :]  # (T, 3)
    v1 = triangles[:, 1, :]  # (T, 3)
    v2 = triangles[:, 2, :]  # (T, 3)

    # hits[i, j] = True if ray from points[i] along +Z hits triangles[j]
    # t_vals[i, j] = ray parameter t (distance along +Z) for the hit
    hits, t_vals = _ray_z_triangle_intersections(points, v0, v1, v2, tolerance)

    # Odd number of hits → inside
    counts = hits.sum(axis=1)  # (P,)
    inside = (counts % 2) == 1

    # Compute minimum positive t for inside points (penetration depth proxy)
    # Replace non-hit entries with inf so they don't affect the minimum
    t_masked = np.where(hits, t_vals, np.inf)
    min_depths = np.where(inside, t_masked.min(axis=1), 0.0)

    return inside, min_depths


def _ray_z_triangle_intersections(
    points: np.ndarray,
    v0: np.ndarray,
    v1: np.ndarray,
    v2: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized Möller-Trumbore ray-triangle intersection along +Z.

    For each point ``p`` in *points*, casts a ray ``(p, +Z)`` and tests
    intersection with every triangle defined by ``(v0, v1, v2)``.

    Parameters
    ----------
    points : np.ndarray
        Shape ``(P, 3)`` — ray origins.
    v0, v1, v2 : np.ndarray
        Shape ``(T, 3)`` — triangle vertex arrays.
    tolerance : float
        Numerical tolerance for parallel-ray and boundary checks.

    Returns
    -------
    hits : np.ndarray
        Boolean array of shape ``(P, T)``.
    t_vals : np.ndarray
        Float array of shape ``(P, T)`` — ray parameter *t* for each hit.
        Non-hit entries are 0.

    """
    P = points.shape[0]
    T = v0.shape[0]

    # Ray direction is (0, 0, 1) for all rays.
    # Möller-Trumbore with d = (0, 0, 1):
    #   edge1 = v1 - v0                          (T, 3)
    #   edge2 = v2 - v0                          (T, 3)
    #   h = cross(d, edge2) = (-edge2_y, edge2_x, 0)   (T, 3)
    #   a = dot(edge1, h) = -e1_x*e2_y + e1_y*e2_x     (T,)
    #   (this is the z-component of cross(edge1, edge2))

    edge1 = v1 - v0  # (T, 3)
    edge2 = v2 - v0  # (T, 3)

    # h = cross((0,0,1), edge2) = (-edge2_y, edge2_x, 0)
    h = np.empty_like(edge2)  # (T, 3)
    h[:, 0] = -edge2[:, 1]
    h[:, 1] = edge2[:, 0]
    h[:, 2] = 0.0

    # a = dot(edge1, h)  — determinant
    a = edge1[:, 0] * h[:, 0] + edge1[:, 1] * h[:, 1]  # (T,)

    # Mask out near-parallel triangles (ray parallel to triangle plane)
    valid = np.abs(a) > tolerance  # (T,)

    # Pre-allocate results
    result = np.zeros((P, T), dtype=bool)
    t_out = np.zeros((P, T), dtype=np.float64)

    if not np.any(valid):
        return result, t_out

    # Work only with valid triangles to save memory
    valid_idx = np.where(valid)[0]
    Tv = len(valid_idx)

    a_v = a[valid_idx]  # (Tv,)
    v0_v = v0[valid_idx]  # (Tv, 3)
    h_v = h[valid_idx]  # (Tv, 3)
    edge1_v = edge1[valid_idx]  # (Tv, 3)
    edge2_v = edge2[valid_idx]  # (Tv, 3)

    f = 1.0 / a_v  # (Tv,)

    # s = points - v0  →  (P, Tv, 3)
    # Use broadcasting: points[:, np.newaxis, :] - v0_v[np.newaxis, :, :]
    # For large P*Tv this can be memory-heavy; batch if needed.
    BATCH = max(1, 500_000 // max(Tv, 1))

    for start in range(0, P, BATCH):
        end = min(start + BATCH, P)
        p_batch = points[start:end]  # (B, 3)

        s = p_batch[:, np.newaxis, :] - v0_v[np.newaxis, :, :]  # (B, Tv, 3)

        # u = f * dot(s, h)
        u = f[np.newaxis, :] * np.einsum("btk,tk->bt", s, h_v)  # (B, Tv)

        # Mask: 0 <= u <= 1
        mask_u = (u >= -tolerance) & (u <= 1.0 + tolerance)

        # q = cross(s, edge1)  →  (B, Tv, 3)
        q = np.cross(s, edge1_v[np.newaxis, :, :])  # (B, Tv, 3)

        # v = f * dot(d, q) = f * q[:,:,2]  (since d = (0,0,1))
        v = f[np.newaxis, :] * q[:, :, 2]  # (B, Tv)

        # Mask: v >= 0 and u + v <= 1
        mask_v = (v >= -tolerance) & ((u + v) <= 1.0 + tolerance)

        # t = f * dot(edge2, q)
        t = f[np.newaxis, :] * np.einsum("tk,btk->bt", edge2_v, q)  # (B, Tv)

        # Mask: t > tolerance (intersection is in +Z direction, ahead of point)
        mask_t = t > tolerance

        # Combine all masks
        hit = mask_u & mask_v & mask_t  # (B, Tv)

        # Scatter back to full triangle indices
        result[start:end][:, valid_idx] = hit
        t_out[start:end][:, valid_idx] = np.where(hit, t, 0.0)

    return result, t_out
