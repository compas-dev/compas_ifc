from compas_ifc.model import Model

model = Model("data/Duplex_A_20110907.ifc")
model.get_entities_by_type("IfcWindow")[0].show()