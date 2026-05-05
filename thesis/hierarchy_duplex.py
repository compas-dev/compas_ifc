"""
Duplex Model Hierarchy Rectification Test
==========================================

Loads the Duplex_A_20110907.ifc model (IFC2X3, ~295 elements) and verifies
that the spatial hierarchy correctly nests void/fill relationships and that
IFC placement rectification produces consistent transforms.

  Part 1: Tree Structure — void/fill chains are nested under their hosts
  Part 2: Transform Accuracy — all element world positions match IFC data
  Part 3: Save / Reload Stability — hierarchy survives a round-trip to disk

This model contains walls with openings hosting doors/windows, furnishing
elements with cabinet openings, roof slabs with skylight openings, and
stair assemblies with sub-components whose placements need rectification.
"""

import os
import sys

from compas.geometry import Point, Transformation

from compas_ifc.bim import BuildingInformationModel

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


# ==================================================================
# PART 1: TREE STRUCTURE
# ==================================================================

print("=" * 70)
print("PART 1: TREE STRUCTURE — data/Duplex_A_20110907.ifc")
print("=" * 70)

model = BuildingInformationModel(
    "data/Duplex_A_20110907.ifc",
    rectify_placements=True,
    rectify_verbose=False,
)

rect_stats = model.rectification_stats

total_elements = len(list(model.elements()))
building_elements = len(model.building_elements)
storey_count = len(model.storeys)

print(f"\n  Total elements: {total_elements}")
print(f"  Building elements: {building_elements}")
print(f"  Storeys: {storey_count}")

# ------------------------------------------------------------------
# IFC type distribution
# ------------------------------------------------------------------

type_counts = {}
for e in model.elements():
    type_counts[e.ifc_type] = type_counts.get(e.ifc_type, 0) + 1

print(f"\n  {'IFC Type':<30s} {'Count':>5s}  {'%':>6s}")
print("  " + "-" * 45)
for ifc_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    pct = count / total_elements * 100
    print(f"  {ifc_type:<30s} {count:5d}  {pct:5.1f}%")
print()

# ------------------------------------------------------------------
# Void/fill chain analysis
# ------------------------------------------------------------------

openings = [e for e in model.elements() if e.ifc_type == "IfcOpeningElement"]
opening_count = len(openings)

# Full chains: host -> opening -> filler(s)
chains_with_fillers = []
chains_void_only = []
for opening in openings:
    host = opening.parent
    fillers = [c for c in opening.children if c.ifc_type in ("IfcWindow", "IfcDoor")]
    if fillers:
        for filler in fillers:
            chains_with_fillers.append((host, opening, filler))
    else:
        chains_void_only.append((host, opening))

# Fillers that are correctly nested under openings
fillers_under_openings = sum(
    1 for e in model.elements()
    if e.ifc_type in ("IfcWindow", "IfcDoor")
    and e.parent is not None
    and e.parent.ifc_type == "IfcOpeningElement"
)

# Fillers that are NOT under openings (should be 0 for elements with void/fill chains)
fillers_flat = sum(
    1 for e in model.elements()
    if e.ifc_type in ("IfcWindow", "IfcDoor")
    and (e.parent is None or e.parent.ifc_type != "IfcOpeningElement")
)

print(f"  Void/Fill Chain Summary:")
print(f"    Openings in tree:                {opening_count}")
print(f"    Chains with fillers (host->opening->filler): {len(chains_with_fillers)}")
print(f"    Void-only chains (host->opening):            {len(chains_void_only)}")
print(f"    Fillers nested under openings:               {fillers_under_openings}")
print(f"    Fillers flat (not under opening):            {fillers_flat}")
print()

# Print sample chains (first 5 with fillers, first 3 void-only)
print("  Sample chains with fillers:")
for host, opening, filler in chains_with_fillers[:5]:
    host_label = f"{host.ifc_type} '{host.name}'" if host else "<root>"
    print(f"    {host_label}")
    print(f"      -> {opening.ifc_type} '{opening.name}'")
    print(f"        -> {filler.ifc_type} '{filler.name}'")
print()

if chains_void_only:
    print("  Sample void-only chains:")
    for host, opening in chains_void_only[:3]:
        host_label = f"{host.ifc_type} '{host.name}'" if host else "<root>"
        print(f"    {host_label} -> {opening.ifc_type} '{opening.name}'")
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

check("Tree: total elements >= 290", total_elements >= 290, f"{total_elements}")
check("Tree: storeys == 4", storey_count == 4, f"{storey_count}")
check("Tree: openings in tree >= 48", opening_count >= 48, f"{opening_count}")
check("Tree: fillers nested >= 36", fillers_under_openings >= 36, f"{fillers_under_openings}")
check("Tree: no fillers flat under storey", fillers_flat == 0, f"{fillers_flat}")
check("Tree: void/fill chains >= 48", len(chains_with_fillers) + len(chains_void_only) >= 48,
      f"{len(chains_with_fillers) + len(chains_void_only)}")

# Verify that openings are children of building elements (not storeys)
openings_under_spatial = sum(
    1 for o in openings if o.parent is not None and o.parent._is_spatial
)
check("Tree: no openings directly under spatial elements", openings_under_spatial == 0,
      f"{openings_under_spatial}")


# ==================================================================
# PART 2: TRANSFORM ACCURACY
# ==================================================================

print()
print("=" * 70)
print("PART 2: TRANSFORM ACCURACY")
print("=" * 70)

# For each element with an IFC entity, compare the composed model transform
# (product of all parent local transforms) with the IFC global placement.

from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation

misaligned = []
checked_count = 0

for elem in model.elements():
    if elem._ifc_entity is None:
        continue
    if not hasattr(elem._ifc_entity, "ObjectPlacement") or not elem._ifc_entity.ObjectPlacement:
        continue
    # Skip graph-only elements (no treenode)
    if getattr(elem, "treenode", None) is None:
        continue

    # IFC global transform (from placement chain)
    ifc_global = IfcLocalPlacement_to_transformation(elem._ifc_entity.ObjectPlacement)
    ifc_pos = Point(ifc_global.matrix[0][3], ifc_global.matrix[1][3], ifc_global.matrix[2][3])

    # Model global transform (composed from tree)
    model_global = elem.modeltransformation
    model_pos = Point(model_global.matrix[0][3], model_global.matrix[1][3], model_global.matrix[2][3])

    dist = ifc_pos.distance_to_point(model_pos)
    checked_count += 1

    if dist > POSITION_TOL:
        misaligned.append((elem, dist, ifc_pos, model_pos))

print(f"\n  Elements checked: {checked_count}")
print(f"  Misaligned (>{POSITION_TOL}m): {len(misaligned)}")

if misaligned:
    print("\n  Misaligned elements:")
    for elem, dist, ifc_pos, model_pos in misaligned[:10]:
        print(f"    {elem.ifc_type} '{elem.name}': error={dist:.6f}m")
        print(f"      IFC:   ({ifc_pos.x:.4f}, {ifc_pos.y:.4f}, {ifc_pos.z:.4f})")
        print(f"      Model: ({model_pos.x:.4f}, {model_pos.y:.4f}, {model_pos.z:.4f})")
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
rt_path = "temp/thesis_hierarchy_duplex.ifc"
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

print(f"  Reloaded elements: {total2} (original: {total_elements})")
print(f"  Reloaded openings: {openings2} (original: {opening_count})")
print(f"  Reloaded fillers under openings: {fillers2} (original: {fillers_under_openings})")
print(f"  Reloaded graph edges: {edges2}")

# Check transform alignment after reload
misaligned2 = 0
checked2 = 0
for elem in model2.elements():
    if elem._ifc_entity is None:
        continue
    if not hasattr(elem._ifc_entity, "ObjectPlacement") or not elem._ifc_entity.ObjectPlacement:
        continue
    if getattr(elem, "treenode", None) is None:
        continue
    ifc_global = IfcLocalPlacement_to_transformation(elem._ifc_entity.ObjectPlacement)
    ifc_pos = Point(ifc_global.matrix[0][3], ifc_global.matrix[1][3], ifc_global.matrix[2][3])
    model_global = elem.modeltransformation
    model_pos = Point(model_global.matrix[0][3], model_global.matrix[1][3], model_global.matrix[2][3])
    dist = ifc_pos.distance_to_point(model_pos)
    checked2 += 1
    if dist > POSITION_TOL:
        misaligned2 += 1

print(f"  Reloaded transform check: {misaligned2} misaligned of {checked2}")
print()

check("Reload: element count preserved", total2 == total_elements,
      f"{total2} vs {total_elements}")
check("Reload: openings preserved", openings2 == opening_count,
      f"{openings2} vs {opening_count}")
check("Reload: fillers nested preserved", fillers2 == fillers_under_openings,
      f"{fillers2} vs {fillers_under_openings}")
check("Reload: transforms aligned", misaligned2 == 0,
      f"{misaligned2} misaligned of {checked2}")


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
    print("SUCCESS: All Duplex hierarchy rectification tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
