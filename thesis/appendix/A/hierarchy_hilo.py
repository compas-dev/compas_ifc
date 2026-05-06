"""
HiLo Model Hierarchy Rectification Test
=========================================

Loads the HiLo_Model-Architecture.ifc model (IFC2X3, ~1920 building
elements) and verifies that the spatial hierarchy correctly nests void/fill
relationships and that IFC placement rectification produces consistent
transforms.

  Part 1: Tree Structure — void/fill chains nested, type distribution
  Part 2: Transform Accuracy — all element world positions match IFC data
  Part 3: Save / Reload Stability — hierarchy survives a round-trip

The HiLo model is significantly larger than Duplex and features a rich
mix of structural members, MEP distribution ports, walls with openings,
and multi-storey spatial decomposition.  Output is condensed to summary
tables rather than per-element detail.
"""

import os
import sys

from compas.geometry import Point, Transformation

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation

pass_count = 0
fail_count = 0
results = []

POSITION_TOL = 1e-3  # mm-level tolerance for position comparison


def check(label, condition, detail=""):
    global pass_count, fail_count
    status = "PASS" if condition else "FAIL"
    if condition:
        pass_count += 1
    else:
        fail_count += 1
    results.append((status, label, detail))
    return condition


def check_transforms(model, label_prefix=""):
    """Check that all element transforms match IFC global placements.

    Skips graph-only elements (no treenode, e.g. IfcDistributionPort) since
    they have no model transform to compare.

    Returns (checked_count, misaligned_list).
    """
    misaligned = []
    checked = 0
    for elem in model.elements():
        if elem._ifc_entity is None:
            continue
        if not hasattr(elem._ifc_entity, "ObjectPlacement") or not elem._ifc_entity.ObjectPlacement:
            continue
        # Skip graph-only elements (no treenode)
        if getattr(elem, "treenode", None) is None:
            continue
        ifc_global = IfcLocalPlacement_to_transformation(elem._ifc_entity.ObjectPlacement)
        ifc_pos = Point(ifc_global.matrix[0][3], ifc_global.matrix[1][3], ifc_global.matrix[2][3])
        model_global = elem.modeltransformation
        model_pos = Point(model_global.matrix[0][3], model_global.matrix[1][3], model_global.matrix[2][3])
        dist = ifc_pos.distance_to_point(model_pos)
        checked += 1
        if dist > POSITION_TOL:
            misaligned.append((elem, dist))
    return checked, misaligned


# ==================================================================
# PART 1: TREE STRUCTURE
# ==================================================================

print("=" * 70)
print("PART 1: TREE STRUCTURE — HiLo_Model-Architecture.ifc")
print("=" * 70)

model = BuildingInformationModel(
    "temp/HiLo_Model-Architecture.ifc",
    rectify_placements=True,
    rectify_verbose=False,
)

rect_stats = model.rectification_stats

total_elements = len(list(model.elements()))
building_elements = len(model.building_elements)
storey_count = len(model.storeys)

print(f"\n  Total elements:    {total_elements}")
print(f"  Building elements: {building_elements}")
print(f"  Storeys:           {storey_count}")

# ------------------------------------------------------------------
# IFC type distribution (condensed: top 15)
# ------------------------------------------------------------------

type_counts = {}
for e in model.elements():
    type_counts[e.ifc_type] = type_counts.get(e.ifc_type, 0) + 1

sorted_types = sorted(type_counts.items(), key=lambda x: -x[1])

print(f"\n  {'IFC Type':<30s} {'Count':>5s}  {'%':>6s}")
print("  " + "-" * 45)
for ifc_type, count in sorted_types[:15]:
    pct = count / total_elements * 100
    print(f"  {ifc_type:<30s} {count:5d}  {pct:5.1f}%")
if len(sorted_types) > 15:
    rest = sum(c for _, c in sorted_types[15:])
    print(f"  {'(other types)':<30s} {rest:5d}  {rest/total_elements*100:5.1f}%")
print("  " + "-" * 45)
print(f"  {'Total':<30s} {total_elements:5d}")
print()

# ------------------------------------------------------------------
# Void/fill chain analysis (condensed)
# ------------------------------------------------------------------

openings = [e for e in model.elements() if e.ifc_type == "IfcOpeningElement"]
opening_count = len(openings)

# Classify chains by host type
chains_by_host_type = {}  # host_ifc_type -> (with_filler_count, void_only_count)
filler_total = 0
void_only_total = 0
for opening in openings:
    host = opening.parent
    host_type = host.ifc_type if host else "<root>"
    fillers = [c for c in opening.children if c.ifc_type in ("IfcWindow", "IfcDoor")]
    entry = chains_by_host_type.setdefault(host_type, [0, 0])
    if fillers:
        entry[0] += len(fillers)
        filler_total += len(fillers)
    else:
        entry[1] += 1
        void_only_total += 1

# Fillers correctly nested
fillers_under_openings = sum(
    1 for e in model.elements()
    if e.ifc_type in ("IfcWindow", "IfcDoor")
    and e.parent is not None
    and e.parent.ifc_type == "IfcOpeningElement"
)

fillers_flat = sum(
    1 for e in model.elements()
    if e.ifc_type in ("IfcWindow", "IfcDoor")
    and (e.parent is None or e.parent.ifc_type != "IfcOpeningElement")
)

print(f"  Void/Fill Chain Summary:")
print(f"    Total openings in tree:  {opening_count}")
print(f"    Chains with fillers:     {filler_total}")
print(f"    Void-only chains:        {void_only_total}")
print(f"    Fillers nested:          {fillers_under_openings}")
print(f"    Fillers flat:            {fillers_flat}")
print()

# Chains by host type table
print(f"    {'Host Type':<30s} {'With Filler':>12s} {'Void Only':>10s}")
print("    " + "-" * 55)
for host_type, (wf, vo) in sorted(chains_by_host_type.items(), key=lambda x: -(x[1][0] + x[1][1])):
    print(f"    {host_type:<30s} {wf:12d} {vo:10d}")
print()

# ------------------------------------------------------------------
# Rectification pattern analysis (from model.rectification_stats)
# ------------------------------------------------------------------

patterns = rect_stats["patterns"]

print(f"  Placement Rectification: {rect_stats['rectified_count']} total, {len(patterns)} distinct patterns")
print()

if patterns:
    print(f"    {'Element Type':<25s} {'From Parent':<25s} {'To Parent':<25s} {'Count':>5s}")
    print("    " + "-" * 83)
    for (etype, old, new), info in sorted(patterns.items(), key=lambda x: -x[1]["count"]):
        print(f"    {etype:<25s} {old:<25s} {new:<25s} {info['count']:5d}")
    print()

    # Show one example per pattern
    print(f"  Examples (one per pattern):\n")
    for (etype, old, new), info in sorted(patterns.items(), key=lambda x: -x[1]["count"]):
        print(f"    {info['example']}: {old} -> {new}")
    print()

# ------------------------------------------------------------------
# Checks
# ------------------------------------------------------------------

check("Tree: total elements >= 1900", total_elements >= 1900, f"{total_elements}")
check("Tree: storeys >= 3", storey_count >= 3, f"{storey_count}")
check("Tree: openings in tree >= 380", opening_count >= 380, f"{opening_count}")
check("Tree: fillers nested >= 3", fillers_under_openings >= 3, f"{fillers_under_openings}")
# HiLo has windows/doors without IfcRelFillsElement chains (directly in storey)
check("Tree: fillers flat <= 15", fillers_flat <= 15, f"{fillers_flat}")

# Verify openings are children of building elements (not storeys)
openings_under_spatial = sum(
    1 for o in openings if o.parent is not None and o.parent._is_spatial
)
check("Tree: no openings directly under spatial", openings_under_spatial == 0,
      f"{openings_under_spatial}")


# ==================================================================
# PART 2: TRANSFORM ACCURACY
# ==================================================================

print()
print("=" * 70)
print("PART 2: TRANSFORM ACCURACY")
print("=" * 70)

checked_count, misaligned = check_transforms(model)

print(f"\n  Elements checked: {checked_count}")
print(f"  Misaligned (>{POSITION_TOL}m): {len(misaligned)}")

if misaligned:
    # Show worst 10 by error magnitude
    misaligned.sort(key=lambda x: -x[1])
    print("\n  Top misaligned elements (by error):")
    print(f"    {'IFC Type':<25s} {'Name':<40s} {'Error (m)':>10s}")
    print("    " + "-" * 78)
    for elem, dist in misaligned[:10]:
        name = (elem.name or "")[:38]
        print(f"    {elem.ifc_type:<25s} {name:<40s} {dist:10.6f}")
print()

check("Transform: all placements aligned", len(misaligned) == 0,
      f"{len(misaligned)} misaligned of {checked_count}")


# ==================================================================
# PART 3: SAVE / RELOAD STABILITY
# ==================================================================

print()
print("=" * 70)
print("PART 3: SAVE / RELOAD STABILITY")
print("=" * 70)

os.makedirs("temp", exist_ok=True)
rt_path = "temp/thesis_hierarchy_hilo.ifc"
model.save(rt_path)
print(f"\n  Saved to {rt_path}")

# Reload with rectification
model2 = BuildingInformationModel(rt_path, rectify_placements=True, rectify_verbose=False)

total2 = len(list(model2.elements()))
openings2 = sum(1 for e in model2.elements() if e.ifc_type == "IfcOpeningElement")
fillers2 = sum(
    1 for e in model2.elements()
    if e.ifc_type in ("IfcWindow", "IfcDoor")
    and e.parent is not None
    and e.parent.ifc_type == "IfcOpeningElement"
)
edges2 = model2.graph.number_of_edges()

print(f"\n  {'Metric':<35s} {'Original':>10s} {'Reloaded':>10s} {'Match':>6s}")
print("  " + "-" * 65)

def _row(label, v1, v2):
    match = "OK" if v1 == v2 else "DIFF"
    print(f"  {label:<35s} {v1:10d} {v2:10d} {match:>6s}")

_row("Total elements", total_elements, total2)
_row("Openings in tree", opening_count, openings2)
_row("Fillers under openings", fillers_under_openings, fillers2)
_row("Graph edges", model.graph.number_of_edges(), edges2)

# Transform check after reload
checked2, misaligned2 = check_transforms(model2)
print(f"\n  Reloaded transform check: {len(misaligned2)} misaligned of {checked2}")
print()

check("Reload: element count preserved", total2 == total_elements,
      f"{total2} vs {total_elements}")
check("Reload: openings preserved", openings2 == opening_count,
      f"{openings2} vs {opening_count}")
check("Reload: fillers nested preserved", fillers2 == fillers_under_openings,
      f"{fillers2} vs {fillers_under_openings}")
check("Reload: transforms aligned", len(misaligned2) == 0,
      f"{len(misaligned2)} misaligned of {checked2}")


# ==================================================================
# SUMMARY
# ==================================================================

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print()

for status, label, detail in results:
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status:<6} {label}{suffix}")

print()
print(f"  {pass_count} PASS / {fail_count} FAIL  (of {pass_count + fail_count} checks)")
print()

if fail_count == 0:
    print("SUCCESS: All HiLo hierarchy rectification tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
