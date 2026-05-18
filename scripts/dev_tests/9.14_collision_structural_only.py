"""Clash detection restricted to structural elements (beams, columns, slabs, ...)."""

from compas_ifc.bim import BuildingInformationModel

print("Loading Duplex model...")
model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

STRUCTURAL = [
    "IfcBeam",
    "IfcColumn",
    "IfcMember",
    "IfcSlab",
    "IfcFooting",
    "IfcPile",
    "IfcPlate",
]

# Quick inventory
counts = {}
for e in model.elements():
    if e.ifc_type in STRUCTURAL:
        counts[e.ifc_type] = counts.get(e.ifc_type, 0) + 1
print("Structural elements present:")
for t, n in sorted(counts.items()):
    print(f"  {t}: {n}")

model.show_collision_pairs(
    tolerance=1e-6,
    min_depth=1e-4,
    element_types=STRUCTURAL,
)
