"""
12.1 Axis Representation Reading Test
======================================

Test script for Phase 2: reads axis representations from the Duplex model
and prints statistics about which elements have axis data.

Expected result: ~65 elements with axis representations (all IfcPolyline,
typically 2-point centerlines for walls, beams, columns).
"""

from compas_ifc.model import Model

# ------------------------------------------------------------------
# Load model
# ------------------------------------------------------------------

model = Model("data/Duplex_A_20110907.ifc")
products = model.get_entities_by_type("IfcProduct")

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

for entity in products:
    total_products += 1
    axis = entity.axis
    if axis is None:
        continue

    axis_count += 1
    ifc_type = entity.is_a()
    type_counts[ifc_type] = type_counts.get(ifc_type, 0) + 1

    name = getattr(entity, "Name", "") or ""
    n_pts = len(axis.points)

    if axis_count <= 10:
        pts_str = " ->".join(f"({p.x:.1f}, {p.y:.1f}, {p.z:.1f})" for p in axis.points)
        print(f"  [{ifc_type}] {name}")
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
