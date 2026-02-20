"""Visualization test for BuildingInformationModel.

Opens the Duplex model and displays it in compas_viewer using
the new BuildingInformationModel.show() method.
"""

from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

print(f"Schema: {model.schema_name}")
print(f"Unit: {model.unit}")
print(f"Elements: {len(list(model.elements()))}")

elements_with_geom = [e for e in model.elements() if e.geometry is not None]
print(f"Elements with geometry: {len(elements_with_geom)}")

model.print_hierarchy(max_depth=2)
model.show()
