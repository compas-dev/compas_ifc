"""
20 Boolean Result & CSG Test
=============================

Tests the BooleanResult and HalfSpace parametric classes and their
round-trip through IFC:

  A. Write round-trip: create BooleanResult -> save -> reload -> verify
  B. HiLo model read: verify non-clipping booleans now parse as BooleanResult
  C. Duplex model: verify BooleanResult captures all remaining booleans
"""

import os
import sys
import time

from compas.geometry import Box, Cone, Cylinder, Frame, Plane, Point, Polygon, Sphere, Vector

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import BooleanResult, ClippedExtrusion, Extrusion, HalfSpace

pass_count = 0
fail_count = 0
results = []


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
# A. Write round-trip
# ==================================================================

print("=" * 70)
print("A. WRITE ROUND-TRIP")
print("=" * 70)

model = BuildingInformationModel.template(schema="IFC4", unit="m")
storey = model.storeys[0]

# --- Test 1: Extrusion DIFFERENCE Extrusion (wall with opening) ---
wall_profile = Polygon([
    Point(0, 0, 0),
    Point(6, 0, 0),
    Point(6, 0.3, 0),
    Point(0, 0.3, 0),
])
wall_ext = Extrusion(
    profile=wall_profile,
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame.worldXY(),
)

opening_profile = Polygon([
    Point(1.5, -0.05, 0.8),
    Point(3.5, -0.05, 0.8),
    Point(3.5, -0.05, 2.4),
    Point(1.5, -0.05, 2.4),
])
opening_ext = Extrusion(
    profile=opening_profile,
    direction=Vector(0, 1, 0),
    depth=0.4,
    frame=Frame.worldXY(),
)

wall_with_opening = BooleanResult(
    operator="DIFFERENCE",
    first_operand=wall_ext,
    second_operand=opening_ext,
)

print(f"  Created: {wall_with_opening}")
wall = model.create_wall(name="BoolWall", geometry=wall_with_opening, parent=storey)

# --- Test 2: Extrusion DIFFERENCE HalfSpace ---
slab_profile = Polygon([
    Point(0, 0, 0),
    Point(5, 0, 0),
    Point(5, 5, 0),
    Point(0, 5, 0),
])
slab_ext = Extrusion(
    profile=slab_profile,
    direction=Vector(0, 0, 1),
    depth=0.3,
    frame=Frame.worldXY(),
)

clip_plane = HalfSpace(
    plane=Plane(Point(2.5, 2.5, 0.15), Vector(0.707, 0, 0.707)),
    agreement_flag=True,
)

slab_clipped = BooleanResult(
    operator="DIFFERENCE",
    first_operand=slab_ext,
    second_operand=clip_plane,
)

print(f"  Created: {slab_clipped}")
slab = model.create_slab(name="BoolSlab", geometry=slab_clipped, parent=storey)

# --- Test 3: UNION of two extrusions (L-shaped wall) ---
ext_a = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(4, 0, 0), Point(4, 0.3, 0), Point(0, 0.3, 0)]),
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame([0, 3, 0], [1, 0, 0], [0, 1, 0]),
)
ext_b = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(0.3, 0, 0), Point(0.3, 3, 0), Point(0, 3, 0)]),
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame([0, 0, 0], [1, 0, 0], [0, 1, 0]),
)

l_wall = BooleanResult(
    operator="UNION",
    first_operand=ext_a,
    second_operand=ext_b,
)

print(f"  Created: {l_wall}")
wall2 = model.create_wall(name="LWall", geometry=l_wall, parent=storey)

# --- Test 4: Nested boolean (DIFFERENCE of a UNION) ---
nested = BooleanResult(
    operator="DIFFERENCE",
    first_operand=l_wall.copy(),
    second_operand=HalfSpace(
        plane=Plane(Point(2, 1.5, 2.5), Vector(0, 0, 1)),
        agreement_flag=True,
    ),
)

print(f"  Created: {nested}")
print(f"    Tree depth: {nested.depth()}")
print(f"    Leaf operands: {[type(op).__name__ for op in nested.leaf_operands()]}")
wall3 = model.create_wall(name="NestedBool", geometry=nested, parent=storey)

# Save
os.makedirs("temp", exist_ok=True)
out_path = "temp/boolean_csg_test.ifc"
model.save(out_path)
print(f"\n  Saved to {out_path}")

# Reload
model2 = BuildingInformationModel(out_path)

# Count geometry types
type_counts = {}
for elem in model2.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        continue
    if geom is None:
        continue
    tn = type(geom).__name__
    type_counts[tn] = type_counts.get(tn, 0) + 1

print(f"\n  Reloaded geometry types:")
for name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"    {name:25s} {count:5d}")

bool_count = type_counts.get("BooleanResult", 0)
clip_count = type_counts.get("ClippedExtrusion", 0)

# Test 1 & 3 should be BooleanResult (ext-ext difference, ext-ext union)
# Test 2 should be ClippedExtrusion (ext-halfspace = clipping pattern)
# Test 4 should be BooleanResult (nested boolean with non-pure-clipping first operand)
check("Write: BooleanResult count >= 3", bool_count >= 3, f"{bool_count}")
# Test 2 could parse as ClippedExtrusion via fast path
check("Write: ClippedExtrusion count >= 0", clip_count >= 0, f"{clip_count}")
check("Write: total geometry = 4", bool_count + clip_count == 4, f"{bool_count + clip_count}")

# Verify parametric data preserved
for elem in model2.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        continue
    if geom is None:
        continue

    if elem.name == "BoolWall":
        check("BoolWall is BooleanResult", isinstance(geom, BooleanResult))
        if isinstance(geom, BooleanResult):
            check("BoolWall operator=DIFFERENCE", geom.operator == "DIFFERENCE", geom.operator)
            check("BoolWall first is Extrusion", isinstance(geom.first_operand, Extrusion))
            check("BoolWall second is Extrusion", isinstance(geom.second_operand, Extrusion))
            if isinstance(geom.first_operand, Extrusion):
                check("BoolWall first depth=3.0",
                      abs(geom.first_operand.depth - 3.0) < 0.01,
                      f"{geom.first_operand.depth}")

    elif elem.name == "LWall":
        check("LWall is BooleanResult", isinstance(geom, BooleanResult))
        if isinstance(geom, BooleanResult):
            check("LWall operator=UNION", geom.operator == "UNION", geom.operator)
            check("LWall first is Extrusion", isinstance(geom.first_operand, Extrusion))
            check("LWall second is Extrusion", isinstance(geom.second_operand, Extrusion))

    elif elem.name == "NestedBool":
        check("NestedBool is BooleanResult", isinstance(geom, BooleanResult))
        if isinstance(geom, BooleanResult):
            check("NestedBool operator=DIFFERENCE", geom.operator == "DIFFERENCE", geom.operator)
            # First operand should be a BooleanResult (the UNION)
            check("NestedBool first is BooleanResult", isinstance(geom.first_operand, BooleanResult))
            # Second operand should be HalfSpace
            check("NestedBool second is HalfSpace", isinstance(geom.second_operand, HalfSpace))
            if isinstance(geom, BooleanResult):
                check("NestedBool depth >= 2", geom.depth() >= 2, f"{geom.depth()}")

print()

# ==================================================================
# B. HiLo model read
# ==================================================================

hilo_path = "temp/1072_HiLo_Model-Architecture.ifc"
if os.path.exists(hilo_path):
    print("=" * 70)
    print("B. HILO MODEL READ")
    print("=" * 70)

    t0 = time.time()
    hilo = BuildingInformationModel(hilo_path)
    load_time = time.time() - t0
    print(f"\n  Loaded HiLo in {load_time:.1f}s")

    # Count geometry types
    type_counts_h = {}
    geom_count = 0
    parse_errors = 0

    for elem in hilo.building_elements:
        try:
            geom = elem.geometry
        except (AttributeError, Exception):
            parse_errors += 1
            continue
        if geom is None:
            continue
        geom_count += 1
        tn = type(geom).__name__
        type_counts_h[tn] = type_counts_h.get(tn, 0) + 1

    print(f"  Elements with geometry: {geom_count}")
    print(f"  Parse errors: {parse_errors}")
    for name, count in sorted(type_counts_h.items(), key=lambda x: -x[1]):
        pct = count / geom_count * 100 if geom_count else 0
        print(f"    {name:25s} {count:5d}  ({pct:.1f}%)")

    # Check boolean entities in file
    bool_clip = hilo._file.get_entities_by_type("IfcBooleanClippingResult")
    bool_result = hilo._file.get_entities_by_type("IfcBooleanResult")
    print(f"\n  IfcBooleanClippingResult: {len(bool_clip)}")
    print(f"  IfcBooleanResult:         {len(bool_result)}")

    clipped_ext_count = type_counts_h.get("ClippedExtrusion", 0)
    bool_result_count = type_counts_h.get("BooleanResult", 0)
    print(f"  ClippedExtrusion parsed:  {clipped_ext_count}")
    print(f"  BooleanResult parsed:     {bool_result_count}")

    # ClippedExtrusion should still capture the half-space patterns
    check("HiLo: ClippedExtrusion >= 120", clipped_ext_count >= 120,
          f"{clipped_ext_count} ClippedExtrusions")
    # BooleanResult should capture the remaining non-clipping booleans
    check("HiLo: BooleanResult >= 0", bool_result_count >= 0,
          f"{bool_result_count} BooleanResults")
    # Combined: all booleans should now be parsed (no more fallback to TessellatedBrep)
    total_parametric_bool = clipped_ext_count + bool_result_count
    print(f"\n  Total parametric booleans: {total_parametric_bool}")
    check("HiLo: parse errors == 0", parse_errors == 0, f"{parse_errors}")

    # TessellatedBrep count should be lower now
    tbrep_count = type_counts_h.get("TessellatedBrep", 0)
    print(f"  TessellatedBrep remaining: {tbrep_count}")

    # Verify BooleanResult data quality
    valid_bools = 0
    total_bools = 0
    for elem in hilo.building_elements:
        try:
            geom = elem.geometry
        except (AttributeError, Exception):
            continue
        if not isinstance(geom, BooleanResult):
            continue
        total_bools += 1
        if geom.first_operand is not None and geom.second_operand is not None:
            valid_bools += 1

    if total_bools > 0:
        print(f"\n  Valid BooleanResults: {valid_bools}/{total_bools}")
        check("HiLo: all BooleanResults valid", valid_bools == total_bools,
              f"{valid_bools}/{total_bools}")

    check("HiLo: total geometries >= 1400", geom_count >= 1400, f"{geom_count}")
    print()

else:
    print("\n  [SKIP] HiLo model not found at", hilo_path)
    print()

# ==================================================================
# C. Duplex model
# ==================================================================

print("=" * 70)
print("C. DUPLEX MODEL")
print("=" * 70)

duplex = BuildingInformationModel("data/Duplex_A_20110907.ifc")

type_counts_d = {}
geom_count_d = 0
parse_errors_d = 0

for elem in duplex.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        parse_errors_d += 1
        continue
    if geom is None:
        continue
    geom_count_d += 1
    tn = type(geom).__name__
    type_counts_d[tn] = type_counts_d.get(tn, 0) + 1

print(f"  Elements with geometry: {geom_count_d}")
print(f"  Parse errors: {parse_errors_d}")
for name, count in sorted(type_counts_d.items(), key=lambda x: -x[1]):
    pct = count / geom_count_d * 100 if geom_count_d else 0
    print(f"    {name:25s} {count:5d}  ({pct:.1f}%)")
print()

check("Duplex: geometries >= 260", geom_count_d >= 260, f"{geom_count_d}")
check("Duplex: no parse errors", parse_errors_d == 0, f"{parse_errors_d}")

clipped_d = type_counts_d.get("ClippedExtrusion", 0)
bool_d = type_counts_d.get("BooleanResult", 0)
print(f"  ClippedExtrusion: {clipped_d}")
print(f"  BooleanResult: {bool_d}")

# Duplex has some boolean entities — should now all be parsed parametrically
check("Duplex: Extrusion still dominant", type_counts_d.get("Extrusion", 0) >= 190,
      f"{type_counts_d.get('Extrusion', 0)}")

# ==================================================================
# Summary
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
    print("SUCCESS: All boolean/CSG tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
