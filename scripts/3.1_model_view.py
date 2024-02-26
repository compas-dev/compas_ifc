from compas_viewer import Viewer
from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")

viewer = Viewer()

for entity in model.building_elements:
    viewer.add(entity.body_with_opening, name=entity.Name, **entity.style)

viewer.show()
