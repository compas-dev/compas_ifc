import compas
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Frame
from compas_ifc.model import Model


model = Model.template(storey_count=1)

box = Box.from_width_height_depth(5, 5, 0.5)
sphere = Sphere(2, Frame([10, 0, 0]))
mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

storey = model.building_storeys[0]

element1 = model.create("IfcWall", geometry=box, frame=Frame([0, 0, 0]), Name="Wall", parent=storey)
element3 = model.create("IfcRoof", geometry=mesh, frame=Frame([0, 0, 0]), Name="Roof", parent=storey)
element2 = model.create(geometry=sphere, frame=Frame([5, 0, 0]), Name="Sphere", parent=storey)

model.save("temp/create_geometry.ifc")
