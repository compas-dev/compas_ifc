"""Verify transformation rectification by comparing global positions
between the old Model (direct IFC placement chains) and new BuildingModel
(rectified relative transforms composed via scene-graph)."""

from compas.geometry import Frame, Transformation, Point
from compas_ifc.model import Model
from compas_ifc.bim import BuildingInformationModel as BuildingModel

# Load with both APIs
old_model = Model("data/Duplex_A_20110907.ifc", verbose=False)
new_model = BuildingModel(filepath="data/Duplex_A_20110907.ifc")

# Compare global positions for all elements
mismatches = 0
checked = 0

for element in new_model.building_elements:
    if element.global_id is None:
        continue

    old_entity = old_model.get_entity_by_global_id(element.global_id)
    if old_entity is None or old_entity.frame is None:
        continue

    # Old model: global frame directly from IFC placement chain
    old_point = old_entity.frame.point

    # New model: composed transform from scene-graph (modeltransformation)
    new_frame = element.frame
    new_point = new_frame.point

    dist = old_point.distance_to_point(new_point)
    checked += 1

    if dist > 1e-6:
        mismatches += 1
        if mismatches <= 5:
            print(f"MISMATCH {element.ifc_type} '{element.name}':")
            print(f"  old: {old_point}")
            print(f"  new: {new_point}")
            print(f"  dist: {dist:.6e}")

if mismatches == 0:
    print(f"ALL {checked} elements match (tolerance 1e-6)")
else:
    print(f"\n{mismatches} / {checked} elements have mismatched global positions")
