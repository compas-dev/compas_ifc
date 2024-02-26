from compas_viewer import Viewer
from compas_ifc.model import Model
from compas.geometry import Translation

model = Model("data/wall-with-opening-and-window.ifc")
viewer = Viewer()

for entity in model.get_entities_by_type("IfcWall"):

    viewer.add(entity.body, name="body", opacity=0.5)

    obj = viewer.add(entity.opening, name="opening")
    obj.transformation = Translation.from_vector([0, 1, 0])

    obj = viewer.add(entity.body_with_opening, name="combined")
    obj.transformation = Translation.from_vector([0, 2, 0])


viewer.show()
