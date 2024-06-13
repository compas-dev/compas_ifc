from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")
model.get_entities_by_type("IfcWall")[0].show()