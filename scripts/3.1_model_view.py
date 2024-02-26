from compas_viewer import Viewer
from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")

viewer = Viewer()

for entity in model.get_entities_by_type("IfcBuildingElement"):
    viewer.add(entity.body_with_opening, name=entity.name, **entity.style)

viewer.show()
