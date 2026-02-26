"""Test placement rectification: rewrite IFC placements to align with spatial hierarchy."""

import os
from compas_ifc.bim import BuildingInformationModel

os.makedirs("temp", exist_ok=True)

# ========================================
# 1. Import Duplex with rectification + verbose
# ========================================
print("=== 1. Import Duplex with rectification (verbose) ===")
model = BuildingInformationModel(filepath="data/Duplex_A_20110907.ifc", load_geometries=False, rectify_verbose=True)
# model = BuildingInformationModel(filepath="temp/1072_HiLo_Model-Architecture.ifc", load_geometries=False, rectify_verbose=True)
print(f"Elements: {len(list(model.elements()))}")

# ========================================
# 2. Verify all placements are aligned
# ========================================
print("\n=== 2. Verify placement alignment ===")
misaligned = 0
total_with_placement = 0
for element in model.elements():
    if element.treenode is None:
        continue
    ifc = element.ifc_entity
    if not hasattr(ifc, "ObjectPlacement") or not ifc.ObjectPlacement:
        continue
    total_with_placement += 1

    placement = ifc.ObjectPlacement
    parent_elem = element.parent
    if parent_elem is None:
        expected = None
    else:
        parent_ifc = parent_elem.ifc_entity
        expected = getattr(parent_ifc, "ObjectPlacement", None) if parent_ifc else None

    actual = placement.PlacementRelTo
    if actual is not expected:
        misaligned += 1
        print(f"  MISALIGNED: {element.ifc_type} '{element.name}'")

print(f"Elements with placement: {total_with_placement}")
print(f"Misaligned: {misaligned}")

# ========================================
# 3. Save rectified file and reload
# ========================================
print("\n=== 3. Save rectified file and reload ===")
rectified_path = "temp/duplex_rectified.ifc"
model.save(rectified_path)
print(f"Saved to {rectified_path}")

model2 = BuildingInformationModel(filepath=rectified_path, load_geometries=False)
print(f"Elements: {len(list(model2.elements()))}")
# Should report 0 rectified since placements are already aligned
model2.print_hierarchy(max_depth=2)

# ========================================
# 4. Import without rectification
# ========================================
print("\n=== 4. Import without rectification ===")
model3 = BuildingInformationModel(filepath="data/Duplex_A_20110907.ifc", load_geometries=False, rectify_placements=False)
print(f"Elements: {len(list(model3.elements()))}")

# Count how many would need rectification
would_rectify = 0
for element in model3.elements():
    if element.treenode is None:
        continue
    ifc = element.ifc_entity
    if not hasattr(ifc, "ObjectPlacement") or not ifc.ObjectPlacement:
        continue
    placement = ifc.ObjectPlacement
    parent_elem = element.parent
    if parent_elem is None:
        expected = None
    else:
        parent_ifc = parent_elem.ifc_entity
        expected = getattr(parent_ifc, "ObjectPlacement", None) if parent_ifc else None
    if placement.PlacementRelTo is not expected:
        would_rectify += 1

print(f"Placements that would need rectification: {would_rectify}")

# ========================================
# 5. Small file test
# ========================================
print("\n=== 5. Small file test ===")
model4 = BuildingInformationModel(filepath="data/wall-with-opening-and-window.ifc")
print(f"Elements: {len(list(model4.elements()))}")

print("\nDone!")
