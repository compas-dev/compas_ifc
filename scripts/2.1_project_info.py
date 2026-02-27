from pprint import pprint
from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/wall-with-opening-and-window.ifc")

# High-level model properties
print("\n" + "*" * 53)
print("Project (high-level)")
print("*" * 53 + "\n")

print(f"Name:        {model.name}")
print(f"Description: {model.description}")
print(f"Schema:      {model.schema_name}")
print(f"Unit:        {model.unit}")
print(f"Sites:       {model.sites}")

# Low-level IFC entity access (escape hatch for deep introspection)
ifc_project = model._file.get_entities_by_type("IfcProject")[0]

print("\n" + "*" * 53)
print("IfcProject (low-level)")
print("*" * 53 + "\n")

print("\nAttributes")
print("=" * 53 + "\n")

pprint(ifc_project.to_dict())

ifc_project.print_attributes(max_depth=3)

print("\nRepresentation Contexts")
print("=" * 53 + "\n")

pprint(ifc_project.contexts)

print("\nUnits")
print("=" * 53 + "\n")

pprint(ifc_project.units)

print("\nModel Context")
print("=" * 53 + "\n")

print(f"Reference Frame: {ifc_project.frame}")
print(f"True North: {ifc_project.north}")

print()
