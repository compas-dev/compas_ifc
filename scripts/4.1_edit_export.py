import os

from compas_ifc.model import Model

HERE = os.path.dirname(__file__)
FILE = os.path.join(
    HERE,
    "..",
    "data",
    "wall-with-opening-and-window.ifc",
)


model = Model(FILE)

print("\n" + "*" * 53)
print("Export Examples")
print("*" * 53 + "\n")


print("\nChange Project Name and Description")
print("=" * 53 + "\n")

model.project["Name"] = "New Project Name"
model.project["Description"] = "New Project Description"
model.save("temp/change_project_name.ifc")

print("\nExport selected entities")
print("=" * 53 + "\n")

window = model.get_entities_by_type("IfcWindow")[0]
model.export([window], "temp/selected_entities.ifc")
