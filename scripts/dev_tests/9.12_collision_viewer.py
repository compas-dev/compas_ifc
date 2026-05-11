"""Interactive collision viewer for the Duplex model.

Opens compas_viewer with all building elements and a collision list
sidebar.  Selecting a collision pair highlights the two elements in
red and dims everything else.
"""

from compas_ifc.bim import BuildingInformationModel

print("Loading Duplex model...")
model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

model.show_collisions(tolerance=1e-6, min_depth=1e-4)
