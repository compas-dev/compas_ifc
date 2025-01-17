from pprint import pprint
from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")

site = model.project.sites[0]

# =============================================================================
# Info
# =============================================================================

print("\n" + "*" * 53)
print("Site")
print("*" * 53 + "\n")

print("\nSpatial Structure")
print("=" * 53 + "\n")

site.print_spatial_hierarchy()

print("\nAttributes")
print("=" * 53 + "\n")

pprint(site.to_dict())

print("\nProperties")
print("=" * 53 + "\n")

pprint(site.property_sets)

print("\nBuildings")
print("=" * 53 + "\n")

print(site.buildings)
