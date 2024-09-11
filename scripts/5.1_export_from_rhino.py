#! python3

### This is a draft script to export a model from Rhino to IFC.
### The example should be run in Rhino8 with COMPAS IFC installed, using template file the "data/layer_template.3dm"

from compas_rhino.objects import get_objects
from compas_rhino.objects import get_object_layers
from compas_rhino.conversions import brepobject_to_compas
from compas_ifc.model import Model
from compas.datastructures import Mesh
import re


def parse_string(input_string):
    pattern = r"^(.*)\[(.*)\]$"
    match = re.match(pattern, input_string)
    if match:
        name = match.group(1)
        type_ = match.group(2)
    else:
        name = None
        type_ = input_string

    return name, type_


objs = get_objects()
layer_info = get_object_layers(objs)


entities = {}

model = Model()
model.create_default_project()
model.unit = "m"

for obj, layers in zip(objs, layer_info):
    compas_brep = brepobject_to_compas(obj)

    # TODO: add support to convert Rhino brep to IFC brep.
    meshes = compas_brep.to_meshes()
    mesh = Mesh()
    for m in meshes:
        mesh.join(m)

    layers = layers.split("::")

    parent_layer = None
    for layer in layers:
        if layer not in entities:
            name, ifc_type = parse_string(layer)

            if ifc_type == "IfcProject":
                model.project.Name = name
                entities[layer] = model.project
            elif name is None:
                model.create(ifc_type, name=name, geometry=mesh, parent=entities[parent_layer])
            else:
                entities[layer] = model.create(ifc_type, name=name, parent=entities[parent_layer])

        parent_layer = layer


model.print_spatial_hierarchy(max_depth=10)

# Change the path to the desired output location
model.save("D:/Github/compas_ifc/temp/Rhino/rhino.ifc")
