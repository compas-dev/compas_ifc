import os

import compas
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Sphere
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
print("Create Geometry Examples")
print("*" * 53 + "\n")


print("\nInsert geometry into existing model")
print("=" * 53 + "\n")
building_storey = model.get_entities_by_type("IfcBuildingStorey")[0]
size = 1 / model.project.length_scale
box = Box.from_width_height_depth(size, size, size)

inserted_element = model.insert(box, parent=building_storey, name="Box", description="This is a box")
print("Inserted element: ", inserted_element)

model.save("temp/insert_geometry.ifc")


print("\nCreate IFC from scrach")
print("=" * 53 + "\n")

model = Model()

box = Box.from_width_height_depth(5, 5, 5)
sphere = Sphere([10, 0, 0], 5)
mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

# A minimal hierarchy will be created if parent is not specified
element1 = model.insert(box, name="Box")
element2 = model.insert(sphere, name="Sphere")
element3 = model.insert(mesh, name="Mesh")

print("Inserted elements: ", element1, element2, element3)

model.save("temp/create_geometry.ifc")
