from pprint import pprint
from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")
window = model.get_entities_by_type("IfcWindow")[0]
window.print_spatial_hierarchy(max_depth=5)

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
