"""Verify transformation rectification is self-consistent: load a model
with rectified placements and check that each element's composed global
position (from modeltransformation) matches its IFC placement chain."""

from compas.geometry import Frame, Transformation, Point
from compas_ifc.bim import BuildingInformationModel
from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation

model = BuildingInformationModel(filepath="data/Duplex_A_20110907.ifc")

mismatches = 0
checked = 0

for element in model.building_elements:
    if element.global_id is None:
        continue

    ifc_entity = element._ifc_entity
    if ifc_entity is None or not hasattr(ifc_entity, "ObjectPlacement") or ifc_entity.ObjectPlacement is None:
        continue

    # IFC placement chain: global position from raw IFC data
    ifc_global = IfcLocalPlacement_to_transformation(ifc_entity.ObjectPlacement)
    ifc_frame = Frame.from_transformation(ifc_global)
    ifc_point = ifc_frame.point

    # Model tree: composed global position from scene-graph
    model_transform = element.modeltransformation
    model_frame = Frame.from_transformation(model_transform)
    model_point = model_frame.point

    dist = ifc_point.distance_to_point(model_point)
    checked += 1

    if dist > 1e-6:
        mismatches += 1
        if mismatches <= 5:
            print(f"MISMATCH {element.ifc_type} '{element.name}':")
            print(f"  ifc:   {ifc_point}")
            print(f"  model: {model_point}")
            print(f"  dist:  {dist:.6e}")

if mismatches == 0:
    print(f"ALL {checked} elements match (tolerance 1e-6)")
else:
    print(f"\n{mismatches} / {checked} elements have mismatched global positions")
