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
project.print_inheritance()

print("\nShortcut APIs")
print("=" * 53 + "\n")

print("Project contains:")
print(model.sites)
print(model.buildings)
print(model.building_storeys)
print(model.elements[:3])


print("\nSite contains:")
site = model.sites[0]
print(site.buildings)
print(site.geographic_elements)

print("\nBuilding contains:")
building = model.buildings[0]
print(building.building_storeys)
print(building.spaces)
print(building.building_elements[:3])


print("\nTraverse spatial hierarchy")
print("=" * 53 + "\n")

print(building)

print("\nParent")
print(building.parent)

print("\nChildren")
print(building.children)

print("\nAncestors")
for ancestor in building.traverse_ancestor():
    print(ancestor)

print("\nDescendants")
for descendant in building.traverse():
    print(descendant)
