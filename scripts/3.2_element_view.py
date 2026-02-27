from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")
model.get_elements_by_type("IfcWindow")[0].show()
