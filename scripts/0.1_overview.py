from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/wall-with-opening-and-window.ifc")
model.print_hierarchy()
