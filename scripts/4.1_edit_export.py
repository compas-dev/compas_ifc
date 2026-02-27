from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/wall-with-opening-and-window.ifc")


print("\n" + "*" * 53)
print("Export Examples")
print("*" * 53 + "\n")


print("\nChange Project Name and Description")
print("=" * 53 + "\n")

model.name = "New Project Name"
model.description = "New Project Description"
model.save("temp/change_project_name.ifc")

print("\nExport selected entities")
print("=" * 53 + "\n")

window = model.get_elements_by_type("IfcWindow")[0]
model.export("temp/selected_entities.ifc", [window])
