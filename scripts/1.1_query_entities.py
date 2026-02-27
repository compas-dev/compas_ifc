from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/wall-with-opening-and-window.ifc")

print("\n" + "*" * 53)
print("Query Examples")
print("*" * 53 + "\n")

print("\nAll elements in the model")
print("=" * 53 + "\n")

elements = list(model.elements())
print("Total number of elements: ", len(elements))
for i, element in enumerate(elements):
    print(element)
    if i > 5:
        print("...\n")
        break

print("\nSpatial elements")
print("=" * 53 + "\n")

spatial_elements = [e for e in model.elements() if e._is_spatial]
print("Total number of spatial elements: ", len(spatial_elements))
for element in spatial_elements:
    print(element)
print()

print("\nBuilding elements")
print("=" * 53 + "\n")

building_elements = model.building_elements
print("Total number of building elements: ", len(building_elements))
for element in building_elements:
    print(element)
print()


print("\nElements by name")
print("=" * 53 + "\n")

name = "Window for Test Example"
elements = model.get_elements_by_name(name)
print("Found elements with the name: {}".format(name))
print(elements)


print("\nElements by id")
print("=" * 53 + "\n")

global_id = "3ZYW59sxj8lei475l7EhLU"
element = model.get_element_by_global_id(global_id)
print("Found element with the global id: {}".format(global_id))
print(element, "\n")
