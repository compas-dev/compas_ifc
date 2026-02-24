"""
Pipe geometry type for parametric IFC representation.
"""

import math

from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import Vector


class Pipe(Geometry):
    """A swept disk solid: circular cross-section swept along a directrix curve.

    Directly corresponds to ``IfcSweptDiskSolid``.  Preserves the parametric
    data (directrix path, radius) that is lost when ifcopenshell evaluates
    the shape into tessellated or OCC geometry.

    Parameters
    ----------
    directrix : :class:`Polyline`
        The 3D curve along which the circular disk is swept.
    radius : float
        Outer radius of the circular disk.
    inner_radius : float, optional
        Inner radius for hollow pipes (annular cross-section).
        ``None`` for solid pipes.
    name : str, optional
        Optional name for the pipe.

    Attributes
    ----------
    directrix : :class:`Polyline`
    radius : float
    inner_radius : float or None
    name : str or None
    """

    def __init__(self, directrix, radius, inner_radius=None, name=None):
        super().__init__()
        self.directrix = Polyline(directrix.points) if isinstance(directrix, Polyline) else Polyline(directrix)
        self.radius = float(radius)
        self.inner_radius = float(inner_radius) if inner_radius is not None else None
        self.name = name

    def __repr__(self):
        n_pts = len(self.directrix.points)
        hollow = f", inner_r={self.inner_radius:.3f}" if self.inner_radius else ""
        return f"<Pipe r={self.radius:.3f}{hollow} directrix={n_pts}pts>"

    # ------------------------------------------------------------------
    # Geometry interface
    # ------------------------------------------------------------------

    def transform(self, transformation):
        """Transform the pipe by transforming its directrix.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.
        """
        self.directrix.transform(transformation)

    def copy(self):
        """Return a deep copy of this pipe.

        Returns
        -------
        :class:`Pipe`
        """
        return Pipe(
            directrix=Polyline([Point(*p) for p in self.directrix.points]),
            radius=self.radius,
            inner_radius=self.inner_radius,
            name=self.name,
        )

    # ------------------------------------------------------------------
    # Mesh generation
    # ------------------------------------------------------------------

    def to_vertices_and_faces(self, n=16):
        """Discretise the pipe into vertices and faces.

        Generates a tube mesh by placing *n*-gon rings at each directrix
        point, oriented perpendicular to the local tangent.

        Parameters
        ----------
        n : int
            Number of vertices per circular cross-section ring.

        Returns
        -------
        tuple[list[list[float]], list[list[int]]]
            ``(vertices, faces)`` suitable for
            :meth:`Mesh.from_vertices_and_faces`.
        """
        pts = self.directrix.points
        if len(pts) < 2:
            return [], []

        vertices = []
        r = self.radius

        for idx, p in enumerate(pts):
            # Compute local tangent
            if idx == 0:
                tangent = Vector.from_start_end(pts[0], pts[1])
            elif idx == len(pts) - 1:
                tangent = Vector.from_start_end(pts[-2], pts[-1])
            else:
                tangent = Vector.from_start_end(pts[idx - 1], pts[idx + 1])
            tangent.unitize()

            # Build a local frame perpendicular to the tangent
            # Choose a reference vector not parallel to tangent
            if abs(tangent.dot(Vector(0, 0, 1))) < 0.9:
                ref = Vector(0, 0, 1)
            else:
                ref = Vector(1, 0, 0)
            u = tangent.cross(ref)
            u.unitize()
            v = tangent.cross(u)
            v.unitize()

            # Generate ring points
            for i in range(n):
                theta = 2.0 * math.pi * i / n
                offset_x = r * math.cos(theta)
                offset_y = r * math.sin(theta)
                vx = p.x + u.x * offset_x + v.x * offset_y
                vy = p.y + u.y * offset_x + v.y * offset_y
                vz = p.z + u.z * offset_x + v.z * offset_y
                vertices.append([vx, vy, vz])

        # Build faces (quad strips between consecutive rings)
        faces = []
        n_rings = len(pts)
        for j in range(n_rings - 1):
            for i in range(n):
                i_next = (i + 1) % n
                faces.append([
                    j * n + i,
                    j * n + i_next,
                    (j + 1) * n + i_next,
                    (j + 1) * n + i,
                ])

        return vertices, faces

    def to_mesh(self, n=16):
        """Convert the pipe to a :class:`compas.datastructures.Mesh`.

        Parameters
        ----------
        n : int
            Number of vertices per circular cross-section ring.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(n=n)
        if not vertices:
            return None
        return Mesh.from_vertices_and_faces(vertices, faces)
