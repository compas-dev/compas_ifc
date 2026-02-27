"""Test collision (interference) detection via ray-casting.

Part 1: Synthetic test with two overlapping box meshes to verify the
algorithm detects penetration correctly.

Part 2: Run on the Duplex model to check for real interferences among
all building elements.
"""

import time

import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Translation

from compas_ifc.algorithms.collisions import fast_mesh_mesh_collision

# ==========================================================================
# Part 1: Synthetic box-box collision test
# ==========================================================================

print("=" * 60)
print("PART 1: Synthetic box-box collision tests")
print("=" * 60)


def make_box_mesh(xmin, ymin, zmin, xmax, ymax, zmax):
    """Create an axis-aligned box mesh."""
    vertices = [
        [xmin, ymin, zmin],
        [xmax, ymin, zmin],
        [xmax, ymax, zmin],
        [xmin, ymax, zmin],
        [xmin, ymin, zmax],
        [xmax, ymin, zmax],
        [xmax, ymax, zmax],
        [xmin, ymax, zmax],
    ]
    faces = [
        [0, 3, 2, 1],  # bottom
        [4, 5, 6, 7],  # top
        [0, 1, 5, 4],  # front
        [1, 2, 6, 5],  # right
        [2, 3, 7, 6],  # back
        [3, 0, 4, 7],  # left
    ]
    return Mesh.from_vertices_and_faces(vertices, faces)


# Test 1: Overlapping boxes — should detect collision
print("\nTest 1: Overlapping boxes")
box_a = make_box_mesh(0, 0, 0, 2, 2, 2)
box_b = make_box_mesh(1, 1, 1, 3, 3, 3)  # overlaps in [1,2]^3

pts = fast_mesh_mesh_collision(box_a, box_b, tolerance=1e-9)
print(f"  Penetrating points: {len(pts)}")
assert len(pts) > 0, "Should detect collision between overlapping boxes"
print("  PASS")

# Test 2: Separated boxes — should NOT detect collision
print("\nTest 2: Separated boxes")
box_c = make_box_mesh(0, 0, 0, 1, 1, 1)
box_d = make_box_mesh(2, 2, 2, 3, 3, 3)  # no overlap

pts = fast_mesh_mesh_collision(box_c, box_d, tolerance=1e-9)
print(f"  Penetrating points: {len(pts)}")
assert len(pts) == 0, "Should NOT detect collision between separated boxes"
print("  PASS")

# Test 3: Touching boxes (shared face) — should NOT detect collision
# (touching is a connection, not a collision)
print("\nTest 3: Touching boxes (shared face)")
box_e = make_box_mesh(0, 0, 0, 1, 1, 1)
box_f = make_box_mesh(1, 0, 0, 2, 1, 1)  # shares face at x=1

pts = fast_mesh_mesh_collision(box_e, box_f, tolerance=1e-9)
print(f"  Penetrating points: {len(pts)}")
assert len(pts) == 0, "Should NOT detect collision between touching boxes"
print("  PASS")

# Test 4: One box fully inside another
print("\nTest 4: Box fully inside another")
box_g = make_box_mesh(0, 0, 0, 10, 10, 10)
box_h = make_box_mesh(2, 2, 2, 4, 4, 4)  # fully inside box_g

pts = fast_mesh_mesh_collision(box_g, box_h, tolerance=1e-9)
print(f"  Penetrating points: {len(pts)}")
assert len(pts) > 0, "Should detect collision when one box is inside another"
# All 8 vertices of box_h should be inside box_g
inside_count = sum(1 for p in pts if 2.0 <= p.x <= 4.0)
print(f"  Vertices of inner box detected inside: {inside_count}")
print("  PASS")

print(f"\nAll synthetic tests passed!")

# ==========================================================================
# Part 2: Duplex model collision detection
# ==========================================================================

print("\n" + "=" * 60)
print("PART 2: Duplex model collision detection")
print("=" * 60)

from compas_ifc.bim import BuildingInformationModel

print("\nLoading Duplex model...")
model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

# Check existing interferences from IFC file
existing = model.interferences
print(f"Existing IFC interferences: {len(existing)}")

# Run collision detection on all elements
print("\nRunning compute_collisions() on all elements...")
t0 = time.time()
new_count = model.compute_collisions(tolerance=1e-6)
elapsed = time.time() - t0

print(f"compute_collisions() found {new_count} collisions in {elapsed:.2f}s")

# Report results
collision_edges = model.interferences
print(f"\nTotal interference edges: {len(collision_edges)}")

if collision_edges:
    print("\nDetected interferences:")
    for i, edge in enumerate(collision_edges[:20]):
        a, b = model._edge_elements(edge)
        pts = model.graph.edge_attribute(edge, "penetrating_points") or []
        a_name = a.name or a.ifc_type
        b_name = b.name or b.ifc_type
        print(f"  [{i}] {a_name} <-> {b_name}  ({len(pts)} penetrating points)")
    if len(collision_edges) > 20:
        print(f"  ... and {len(collision_edges) - 20} more")
else:
    print("\nNo collisions detected (well-authored model).")

print(f"\n{'='*60}")
print("DONE")
print(f"{'='*60}")
