from pprint import pprint
from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")

assert len(model.projects) > 0

project = model.projects[0]
assert len(project.sites) > 0

site = project.sites[0]
assert len(site.buildings) > 0

building = site.buildings[0]
assert len(building.building_storeys) > 0

storey = building.building_storeys[0]
assert len(storey.windows) > 0

window = storey.windows[0]

# =============================================================================
# Info
# =============================================================================

print("\n" + "*" * 53)
print("Window")
print("*" * 53 + "\n")

window.print_inheritance()

print("\nAttributes")
print("=" * 53 + "\n")

pprint(window.attributes)

print("\nProperties")
print("=" * 53 + "\n")

pprint(window.properties)

print()
