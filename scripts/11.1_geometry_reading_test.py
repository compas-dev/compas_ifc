"""
11.1 Geometry Reading Test
==========================

Demonstrates Phase 1 of the geometry reading pipeline:
``element.geometry`` now returns parsed COMPAS geometry objects
(Extrusion, Mesh, Box, etc.) instead of TessellatedBrep.

The ``visual_geometry`` property still provides the ifcopenshell-
evaluated tessellation for display purposes.
"""

from compas_ifc.model import Model
from compas_ifc.representations import Extrusion
from compas.geometry import Box, Sphere, Cone, Cylinder, Polygon, Circle
from compas.datastructures import Mesh

# ------------------------------------------------------------------
# 1. Read Duplex model and inspect parsed geometry types
# ------------------------------------------------------------------

model = Model("data/Duplex_A_20110907.ifc")

products = model.get_entities_by_type("IfcProduct")

type_counts = {}
total = 0

for entity in products:
    geom = entity.geometry
    if geom is None:
        continue
    total += 1
    type_name = type(geom).__name__
    type_counts[type_name] = type_counts.get(type_name, 0) + 1

print("=" * 60)
print("Geometry type distribution")
print("=" * 60)
print(f"Total elements with geometry: {total}\n")
for name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    pct = count / total * 100
    print(f"  {name:30s}  {count:4d}  ({pct:5.1f}%)")

# ------------------------------------------------------------------
# 2. Show a few example Extrusions with their parametric data
# ------------------------------------------------------------------

print("\n" + "=" * 60)
print("Example Extrusions")
print("=" * 60)

shown = 0
for entity in products:
    geom = entity.geometry
    if isinstance(geom, Extrusion):
        name = getattr(entity, "Name", "") or ""
        ifc_type = entity.is_a()
        profile = geom.profile

        if isinstance(profile, Polygon):
            profile_desc = f"Polygon({len(profile.points)} pts)"
        elif isinstance(profile, Circle):
            profile_desc = f"Circle(r={profile.radius:.3f})"
        elif isinstance(profile, tuple):
            n_voids = len(profile[1])
            profile_desc = f"ProfileWithVoids({n_voids} holes)"
        else:
            profile_desc = type(profile).__name__

        print(f"\n  {ifc_type} '{name}'")
        print(f"    Profile:   {profile_desc}")
        print(f"    Direction: {geom.direction}")
        print(f"    Depth:     {geom.depth:.3f}")
        print(f"    Frame:     {geom.frame}")

        shown += 1
        if shown >= 5:
            break

# ------------------------------------------------------------------
# 3. Verify visual_geometry is still independent
# ------------------------------------------------------------------

print("\n" + "=" * 60)
print("Visual geometry vs parsed geometry")
print("=" * 60)

entity = next(e for e in products if isinstance(e.geometry, Extrusion))
print(f"\n  Entity: {entity.is_a()} '{getattr(entity, 'Name', '')}'")
print(f"  .geometry       -> {type(entity.geometry).__name__}")
print(f"  .visual_geometry -> {type(entity.visual_geometry).__name__}")

# ------------------------------------------------------------------
# 4. Extrusion.to_mesh()
# ------------------------------------------------------------------

print("\n" + "=" * 60)
print("Extrusion.to_mesh()")
print("=" * 60)

mesh = entity.geometry.to_mesh()
print(f"\n  Vertices: {mesh.number_of_vertices()}")
print(f"  Faces:    {mesh.number_of_faces()}")
