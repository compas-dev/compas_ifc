from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")
model.print_summary()

unit = model.unit

element = model.get_entities_by_type("IfcWindow")[0]
print("Volume:", element.geometry.volume, unit + "³")
print("Surface Area:", element.geometry.surface_area, unit + "²")
