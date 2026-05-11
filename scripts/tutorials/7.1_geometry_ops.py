from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel(filepath="data/wall-with-opening-and-window.ifc")
model.print_hierarchy()

unit = model.unit

element = model.get_elements_by_type("IfcWindow")[0]
print("Volume:", element.volume, unit + "³")
print("Surface Area:", element.surface_area, unit + "²")
