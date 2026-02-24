"""
13.1 Instancing Write Test
==========================

Test for Phase 3: creates multiple products sharing the same geometry
object, saves to IFC, reloads, and verifies that proper instancing
(IfcRepresentationMap + IfcMappedItem) was created.

Expected:
- 5 columns share one Cylinder -> 1 IfcRepresentationMap, 4 IfcMappedItem
- 3 beams share one Box       -> 1 IfcRepresentationMap, 2 IfcMappedItem
- 1 slab with unique Mesh     -> 0 maps, 0 mapped items (direct rep)
"""

import os

from compas.geometry import Box, Cylinder, Frame, Point, Vector
from compas.datastructures import Mesh
from compas_ifc.model import Model

# ------------------------------------------------------------------
# Create model
# ------------------------------------------------------------------

model = Model.template(schema="IFC4", unit="m")
storey = model.building_storeys[0]

# ------------------------------------------------------------------
# Shared geometry: 5 columns with the same Cylinder
# ------------------------------------------------------------------

column_geom = Cylinder(0.15, 3.0)  # single Python object

for i in range(5):
    frame = Frame(Point(i * 2.0, 0.0, 0.0), Vector.Xaxis(), Vector.Yaxis())
    model.create(
        "IfcColumn",
        geometry=column_geom,
        frame=frame,
        parent=storey,
        Name=f"Column_{i}",
    )

# ------------------------------------------------------------------
# Shared geometry: 3 beams with the same Box
# ------------------------------------------------------------------

beam_geom = Box(4.0, 0.2, 0.3)  # single Python object

for i in range(3):
    frame = Frame(Point(0.0, i * 3.0, 3.0), Vector.Xaxis(), Vector.Yaxis())
    model.create(
        "IfcBeam",
        geometry=beam_geom,
        frame=frame,
        parent=storey,
        Name=f"Beam_{i}",
    )

# ------------------------------------------------------------------
# Unique geometry: 1 slab with a unique Mesh
# ------------------------------------------------------------------

slab_geom = Mesh.from_meshgrid(10, 5, 10, 5)  # unique object

model.create(
    "IfcSlab",
    geometry=slab_geom,
    frame=Frame.worldXY(),
    parent=storey,
    Name="Slab_0",
)

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------

os.makedirs("temp", exist_ok=True)
output_path = "temp/instancing_test.ifc"
model.save(output_path)
print(f"Saved: {output_path}")

# ------------------------------------------------------------------
# Reload and verify
# ------------------------------------------------------------------

print()
print("=" * 60)
print("Verification: Reload and check instancing")
print("=" * 60)

model2 = Model(output_path)

# Count IFC entities
rep_maps = model2.get_entities_by_type("IfcRepresentationMap")
mapped_items = model2.get_entities_by_type("IfcMappedItem")

print(f"IfcRepresentationMap count: {len(rep_maps)}")
print(f"IfcMappedItem count:        {len(mapped_items)}")
print()

# Verify each map's usage
for i, rm in enumerate(rep_maps):
    try:
        usages = rm.entity.MapUsage  # inverse attribute on raw ifcopenshell entity
        usage_count = len(usages) if usages else 0
    except Exception:
        usage_count = "?"
    inner_type = rm.MappedRepresentation.RepresentationType if rm.MappedRepresentation else "?"
    print(f"  Map #{i}: inner type={inner_type}, instances={usage_count}")

print()

# Verify all products have geometry
products = model2.get_entities_by_type("IfcProduct")
geom_count = 0
for entity in products:
    if entity.is_a("IfcSpace") or entity.is_a("IfcSite") or entity.is_a("IfcBuilding") or entity.is_a("IfcBuildingStorey"):
        continue
    geom = entity.geometry
    if geom is not None:
        geom_count += 1
    name = getattr(entity, "Name", "") or ""
    status = "OK" if geom is not None else "MISSING"
    print(f"  [{entity.is_a()}] {name}: geometry={status}")

print()

# Summary
expected_maps = 2   # 1 for columns, 1 for beams
expected_mapped = 6  # 4 column instances + 2 beam instances

ok_maps = len(rep_maps) == expected_maps
ok_mapped = len(mapped_items) == expected_mapped
ok_geom = geom_count == 9  # 5 columns + 3 beams + 1 slab

print("=" * 60)
print("Results")
print("=" * 60)
print(f"RepresentationMaps: {len(rep_maps)} (expected {expected_maps}) {'PASS' if ok_maps else 'FAIL'}")
print(f"MappedItems:        {len(mapped_items)} (expected {expected_mapped}) {'PASS' if ok_mapped else 'FAIL'}")
print(f"Geometries parsed:  {geom_count} (expected 9) {'PASS' if ok_geom else 'FAIL'}")

if ok_maps and ok_mapped and ok_geom:
    print("\nSUCCESS: Instancing write + round-trip verified.")
else:
    print("\nWARNING: Some checks did not match expectations.")
