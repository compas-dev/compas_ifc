"""Clash detection on structural + envelope elements."""

from compas_ifc.bim import BuildingInformationModel

print("Loading Duplex model...")
model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

STRUCTURE_AND_ENVELOPE = [
    # Structural
    "IfcBeam",
    "IfcColumn",
    "IfcMember",
    "IfcFooting",
    "IfcPile",
    "IfcPlate",
    # Envelope / shared
    "IfcWall",
    "IfcWallStandardCase",
    "IfcSlab",
    "IfcRoof",
    "IfcCurtainWall",
]

counts = {}
for e in model.elements():
    if e.ifc_type in STRUCTURE_AND_ENVELOPE:
        counts[e.ifc_type] = counts.get(e.ifc_type, 0) + 1
print("Candidate elements:")
for t, n in sorted(counts.items()):
    print(f"  {t}: {n}")

model.show_collision_pairs(
    tolerance=1e-6,
    min_depth=1e-4,
    element_types=STRUCTURE_AND_ENVELOPE,
)
