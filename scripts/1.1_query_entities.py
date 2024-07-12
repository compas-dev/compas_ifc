from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")

print("\n" + "*" * 53)
print("Query Examples")
print("*" * 53 + "\n")

print("\nEntities by type")
print("=" * 53 + "\n")


print("Total number of entities: ", len(list(model.entities)))
for i, entity in enumerate(model.entities):
    print(entity)
    if i > 5:
        print("...\n")
        break

spatial_elements = model.get_entities_by_type("IfcSpatialElement")
print("Total number of spatial elements: ", len(spatial_elements))
for entity in spatial_elements:
    print(entity)
print()

building_elements = model.get_entities_by_type("IfcBuildingElement")
print("Total number of building elements: ", len(building_elements))
for entity in building_elements:
    print(entity)
print()


print("\nEntities by name")
print("=" * 53 + "\n")

name = "Window for Test Example"
entities = model.get_entities_by_name(name)
print("Found entities with the name: {}".format(name))
print(entities)


print("\nEntities by id")
print("=" * 53 + "\n")

global_id = "3ZYW59sxj8lei475l7EhLU"
entity = model.get_entity_by_global_id(global_id)
print("Found entity with the global id: {}".format(global_id))
print(entity, "\n")

id = 1
entity = model.get_entity_by_id(id)
print("Found entity with the id: {}".format(id))
print(entity)
