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

for entity in model.get_entities_by_type("IfcWall"):
    print("Converting brep:", entity)
    viewer.add(Collection(entity.body), name="body", opacity=0.5, facecolor=(0, 1, 0))
    viewer.add(Collection(entity.opening), name="opening", facecolor=(1, 0, 0))
    obj = viewer.add(Collection(entity.body_with_opening), name="combined", show_faces=True)
    obj.translation = [0, 2, 0]

viewer.view.camera.zoom_extents()
viewer.run()
