import os

from compas_view2.app import App
from compas_view2.collections import Collection

from compas_ifc.model import Model

HERE = os.path.dirname(__file__)
FILE = os.path.join(
    HERE,
    "..",
    "data",
    "wall-with-opening-and-window.ifc",
)
model = Model(FILE)
viewer = App(enable_sceneform=True)

for entity in model.get_entities_by_type("IfcBuildingElement"):
    print("Converting to brep:", entity)
    obj = viewer.add(Collection(entity.body_with_opening), name=entity.name)

viewer.run()
