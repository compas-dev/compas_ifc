"""Test bi-directional BIM model: programmatic creation and round-trip."""

import os
from compas.geometry import Box, Frame
from compas_ifc.bim import BuildingInformationModel

os.makedirs("temp", exist_ok=True)

# ========================================
# 1. Create from scratch
# ========================================
print("=== 1. Template creation ===")
model = BuildingInformationModel.template(storey_count=2, unit="mm")
model.print_hierarchy()

print(f"\nSchema: {model.schema_name}")
print(f"Unit: {model.unit}")
print(f"Elements: {len(list(model.elements()))}")
print(f"Sites: {len(model.sites)}")
print(f"Buildings: {len(model.buildings)}")
print(f"Storeys: {len(model.storeys)}")

# ========================================
# 2. Add elements with geometry
# ========================================
print("\n=== 2. Add elements ===")
storey = model.storeys[0]
print(f"Adding to storey: {storey.name}")

wall = model.create_wall(
    parent=storey,
    geometry=Box(1, 5, 3).to_mesh(),
    name="Test Wall",
)
print(f"Wall: {wall}")
print(f"  IFC entity: {wall._ifc_entity}")
print(f"  GlobalId: {wall.global_id}")
print(f"  Geometry: {wall.geometry}")

slab = model.create_slab(
    parent=storey,
    geometry=Box(10, 10, 0.3).to_mesh(),
    name="Test Slab",
)
print(f"Slab: {slab}")
print(f"  IFC entity: {slab._ifc_entity}")
print(f"  GlobalId: {slab.global_id}")

# Add to second storey too
storey2 = model.storeys[1]
wall2 = model.create_wall(
    parent=storey2,
    geometry=Box(1, 4, 3).to_mesh(),
    name="Upper Wall",
)
print(f"Upper wall: {wall2}")

print(f"\nTotal elements: {len(list(model.elements()))}")
print(f"Building elements: {len(model.building_elements)}")

# ========================================
# 3. Modify element
# ========================================
print("\n=== 3. Modify element ===")
wall.name = "Renamed Wall"
print(f"Wall name after rename: {wall.name}")
print(f"IFC Name after rename: {wall._ifc_entity.Name}")

# ========================================
# 4. Print final hierarchy
# ========================================
print("\n=== 4. Final hierarchy ===")
model.print_hierarchy()

# ========================================
# 5. Save
# ========================================
print("\n=== 5. Save ===")
output_path = "temp/creation_test.ifc"
model.save(output_path)
print(f"Saved to {output_path}")

# ========================================
# 6. Reload and verify round-trip
# ========================================
print("\n=== 6. Round-trip verification ===")
model2 = BuildingInformationModel(filepath=output_path)
model2.print_hierarchy()

print(f"\nElements: {len(list(model2.elements()))}")
walls = model2.get_elements_by_type("IfcWall")
print(f"Walls: {len(walls)}")
for w in walls:
    print(f"  {w.name} | GlobalId={w.global_id} | geometry={'yes' if w.geometry else 'no'}")

slabs = model2.get_elements_by_type("IfcSlab")
print(f"Slabs: {len(slabs)}")
for s in slabs:
    print(f"  {s.name} | GlobalId={s.global_id} | geometry={'yes' if s.geometry else 'no'}")

# ========================================
# 7. Import existing file still works
# ========================================
print("\n=== 7. Import existing file ===")
model3 = BuildingInformationModel(filepath="data/wall-with-opening-and-window.ifc")
model3.print_hierarchy(max_depth=3)
print(f"Elements: {len(list(model3.elements()))}")
walls3 = model3.get_elements_by_type("IfcWallStandardCase")
for w in walls3:
    print(f"  Wall: {w.name} | geometry={'yes' if w.geometry else 'no'}")

print("\nDone!")
