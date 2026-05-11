"""Demonstrates unified properties on GenericElement.

IFC stores data in two separate places:
  1. Schema attributes (Name, Description, ObjectType, Tag, PredefinedType)
  2. Property sets (Pset_WallCommon, PSet_Revit_Constraints, ...)

GenericElement.properties merges both into a single flat dict,
so users never have to think about where data lives.
"""

from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

# Pick one wall
wall = model.get_elements_by_type("IfcWall")[0]

print(f"Element: {wall}")
print(f"IFC type: {wall.ifc_type}")
print(f"Name: {wall.name}")
print(f"GlobalId: {wall.global_id}")
print()

# --- Unified properties ---
props = wall.properties
print("=== All property keys ===")
for key in props:
    val = props[key]
    if isinstance(val, dict):
        print(f"  {key}: ({len(val)} sub-properties)")
    else:
        print(f"  {key}: {val}")

print()

# Schema attributes and property sets are accessed the same way
print("=== Direct access examples ===")
print(f"  ObjectType:  {props.get('ObjectType')}")
print(f"  Tag:         {props.get('Tag')}")
print(f"  IsExternal:  {props.get('Pset_WallCommon', {}).get('IsExternal')}")
print(f"  LoadBearing: {props.get('Pset_WallCommon', {}).get('LoadBearing')}")
print()

# Compare across element types
print("=== Properties across types ===")
for ifc_type in ["IfcWall", "IfcSlab", "IfcDoor", "IfcWindow", "IfcColumn"]:
    elements = model.get_elements_by_type(ifc_type)
    if elements:
        e = elements[0]
        pset_names = [k for k, v in e.properties.items() if isinstance(v, dict)]
        attr_names = [k for k, v in e.properties.items() if not isinstance(v, dict)]
        print(f"  {ifc_type} ({len(elements)} total)")
        print(f"    Schema attrs: {attr_names}")
        print(f"    Property sets: {pset_names}")
