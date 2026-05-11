from pprint import pprint
from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/wall-with-opening-and-window.ifc")
window = model.get_elements_by_type("IfcWindow")[0]

# =============================================================================
# Info
# =============================================================================

print("\n" + "*" * 53)
print("Window")
print("*" * 53 + "\n")

print("\nAttributes")
print("=" * 53 + "\n")

pprint(window.to_dict())

print("\nProperties")
print("=" * 53 + "\n")

pprint(window.properties)
