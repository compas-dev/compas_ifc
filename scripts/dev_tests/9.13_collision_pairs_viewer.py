"""Interactive viewer showing every collision pair in a unique colour.

Non-colliding geometry is faded gray; each colliding pair shares one
hue, and penetration points are point markers in the same hue.
"""

from compas_ifc.bim import BuildingInformationModel

print("Loading Duplex model...")
model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

model.show_collision_pairs(tolerance=1e-6, min_depth=1e-4)
