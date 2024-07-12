from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")

project = model.project

print("\n" + "*" * 53)
print("Hierarchy")
print("*" * 53 + "\n")


print("\nModel spatial hierarchy")
print("=" * 53 + "\n")

model.print_spatial_hierarchy()


print("\nClass inheritance hierarchy")
print("=" * 53 + "\n")

project = model.project

print("\nShortcut APIs")
print("=" * 53 + "\n")

print("Project contains:")
print("Sites:", project.sites)
print("Buildings:", project.buildings)
print("Building elements:", project.building_elements)
print("Geographic elements:", project.geographic_elements)

print("\nSite contains:")
site = model.sites[0]
print("Building elements:", site.building_elements)
print("Geographic elements:", site.geographic_elements)

print("\nBuilding contains:")
building = model.buildings[0]
print("Building elements:", building.building_elements)
print("Geographic elements:", building.geographic_elements)


print("\nTraverse spatial hierarchy")
print("=" * 53 + "\n")

print(building)

print("Parent: ", building.parent)
print("Children: ", building.children)

building.print_spatial_hierarchy()
