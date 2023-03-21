import os

from compas_ifc.model import Model

HERE = os.path.dirname(__file__)
FILE = os.path.join(
    HERE,
    "..",
    "data",
    "wall-with-opening-and-window.ifc",
)

model = Model(FILE)

print("\n" + "*" * 53)
print("Query Examples")
print("*" * 53 + "\n")

print("\nEntities by type")
print("=" * 53 + "\n")

all_entities = model.get_all_entities()
spatial_elements = model.get_entities_by_type("IfcSpatialElement")
building_elements = model.get_entities_by_type("IfcBuildingElement")

print("Total number of entities: ", len(all_entities))
for entity in all_entities[-5:]:
    print(entity)
print("...\n")

print("Total number of spatial elements: ", len(spatial_elements))
for entity in spatial_elements[-5:]:
    print(entity)
print("...\n")

print("Total number of building elements: ", len(building_elements))
for entity in building_elements[-5:]:
    print(entity)
print("...\n")


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
