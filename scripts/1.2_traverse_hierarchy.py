from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/wall-with-opening-and-window.ifc")

print("\n" + "*" * 53)
print("Hierarchy")
print("*" * 53 + "\n")


print("\nModel spatial hierarchy")
print("=" * 53 + "\n")

model.print_hierarchy()


print("\nShortcut APIs")
print("=" * 53 + "\n")

print("Sites:", model.sites)
print("Buildings:", model.buildings)
print("Building elements:", model.building_elements)

print("\nSite contains:")
site = model.sites[0]
print("Site:", site)

print("\nBuilding contains:")
building = model.buildings[0]
print("Building:", building)


print("\nTraverse spatial hierarchy (GenericElement tree)")
print("=" * 53 + "\n")

building_element = model.buildings[0]
print(building_element)
print("Parent: ", building_element.parent)
print("Children: ", building_element.children)
