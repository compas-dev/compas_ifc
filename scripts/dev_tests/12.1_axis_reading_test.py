"""
12.1 Axis Representation Reading Test
======================================

Test script for Phase 2: reads axis representations from the Duplex model
and prints statistics about which elements have axis data.

Expected result: ~65 elements with axis representations (all IfcPolyline,
typically 2-point centerlines for walls, beams, columns).
"""

from compas_ifc.bim import BuildingInformationModel

# ------------------------------------------------------------------
# Load model
# ------------------------------------------------------------------

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")
products = model.get_elements_by_type("IfcProduct")

# ------------------------------------------------------------------
# Read axis representations
# ------------------------------------------------------------------

axis_count = 0
type_counts = {}
total_products = 0

print("=" * 70)
print("Axis Representation Reading Test")
print("=" * 70)
print()

for element in products:
    total_products += 1
    axis = element.axis
    if axis is None:
        continue

    axis_count += 1
    type_counts[element.ifc_type] = type_counts.get(element.ifc_type, 0) + 1

    n_pts = len(axis.points)

    if axis_count <= 10:
        pts_str = " ->".join(f"({p.x:.1f}, {p.y:.1f}, {p.z:.1f})" for p in axis.points)
        print(f"  [{element.ifc_type}] {element.name}")
        print(f"    Axis: {n_pts} points -- {pts_str}")
        print()

if axis_count > 10:
    print(f"  ... and {axis_count - 10} more")
    print()

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

print("=" * 70)
print("Summary")
print("=" * 70)
print(f"Total products:          {total_products}")
print(f"Products with axis:      {axis_count}")
print()
print("By IFC type:")
for ifc_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {ifc_type:30s}  {count:4d}")
print()

if axis_count > 0:
    print("SUCCESS: Axis representations parsed correctly.")
else:
    print("WARNING: No axis representations found.")
