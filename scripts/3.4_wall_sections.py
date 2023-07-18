import os

from compas_view2.app import App
from compas_view2.collections import Collection

from compas.geometry import Plane
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

sectionPlane = Plane([0, 0, 1], [0, 0, 1])

for wall in model.get_entities_by_type("IfcWall"):
    print("Converting brep:", wall)
    viewer.add(Collection(wall.body_with_opening), name="{}.Body".format(wall.name), opacity=0.5)

    print("creating section...")
    sections = []
    for shape in wall.body_with_opening:
        sections.append(shape.slice(sectionPlane))

    print(sections)

    viewer.add(Collection(sections), name="{}.Sections".format(wall.name), linecolor=(1, 0, 0), linewidth=5)

print("Finished")

viewer.view.camera.zoom_extents()
viewer.run()
