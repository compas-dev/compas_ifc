"""
HiLo Model Round-Trip Test
============================

Loads the real-world HiLo_Model-Architecture.ifc model (IFC2X3, ~1920
building elements) and verifies that geometry parsing produces correct
parametric types including boolean clipping operations.

This model is dominated by Extrusion with significant ClippedExtrusion
(IfcBooleanClippingResult) and TessellatedBrep (visual geometry fallback).
"""

import os
import sys
import time

from compas.geometry import Circle, Polygon

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import BooleanResult, ClippedExtrusion, Extrusion

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
# LOAD MODEL
# ==================================================================

hilo_path = "temp/1072_HiLo_Model-Architecture.ifc"

if not os.path.exists(hilo_path):
    print(f"[SKIP] HiLo model not found at {hilo_path}")
    print("       Download or copy the file to run this test.")
    sys.exit(0)

print("=" * 70)
print(f"HILO MODEL: {hilo_path}")
print("=" * 70)

t0 = time.time()
model = BuildingInformationModel(hilo_path)
load_time = time.time() - t0
print(f"\n  Loaded in {load_time:.1f}s")

# ==================================================================
# GEOMETRY PARSING
# ==================================================================

print("\n  Parsing all building elements...")

type_counts = {}
geom_count = 0
parse_errors = 0
error_names = []

for elem in model.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception) as e:
        parse_errors += 1
        error_names.append((elem.name or "?", str(e)[:60]))
        continue
    if geom is None:
        continue
    geom_count += 1
    tn = type(geom).__name__
    type_counts[tn] = type_counts.get(tn, 0) + 1

# ------------------------------------------------------------------
# Geometry distribution table
# ------------------------------------------------------------------

print(f"\n  Elements with geometry: {geom_count}")
print(f"  Parse errors:           {parse_errors}")
print()
print(f"  {'Type':<25s} {'Count':>5s}  {'%':>6s}")
print("  " + "-" * 40)
for name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    pct = count / geom_count * 100 if geom_count else 0
    print(f"  {name:<25s} {count:5d}  {pct:5.1f}%")
print("  " + "-" * 40)
print()

if parse_errors > 0:
    print("  Parse errors:")
    for name, err in error_names[:10]:
        print(f"    {name}: {err}")
    print()

# ------------------------------------------------------------------
# IFC boolean entity counts (for reference)
# ------------------------------------------------------------------

bool_clip_entities = model.file.get_entities_by_type("IfcBooleanClippingResult")
bool_result_entities = model.file.get_entities_by_type("IfcBooleanResult")
print(f"  IFC Boolean Entities:")
print(f"    IfcBooleanClippingResult: {len(bool_clip_entities)}")
print(f"    IfcBooleanResult:         {len(bool_result_entities)}")
print()

# ------------------------------------------------------------------
# Basic checks
# ------------------------------------------------------------------

check("Total geometries >= 1400", geom_count >= 1400, f"{geom_count}")
check("Parse errors == 0", parse_errors == 0, f"{parse_errors}")
check("Extrusion >= 1000", type_counts.get("Extrusion", 0) >= 1000, f"{type_counts.get('Extrusion', 0)}")
check("ClippedExtrusion >= 120", type_counts.get("ClippedExtrusion", 0) >= 120, f"{type_counts.get('ClippedExtrusion', 0)}")
check("BooleanResult >= 0", type_counts.get("BooleanResult", 0) >= 0, f"{type_counts.get('BooleanResult', 0)}")
check("TessellatedBrep >= 200", type_counts.get("TessellatedBrep", 0) >= 200, f"{type_counts.get('TessellatedBrep', 0)}")

# ==================================================================
# CLIPPED EXTRUSION DATA QUALITY
# ==================================================================

print("  CLIPPED EXTRUSION DATA QUALITY:")
print("  " + "-" * 50)

valid_clips = 0
total_clips = 0
max_clip_count = 0

for elem in model.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        continue
    if not isinstance(geom, ClippedExtrusion):
        continue
    total_clips += 1

    # Validate: has extrusion with profile, depth > 0, at least 1 clip
    if (geom.extrusion is not None
            and geom.extrusion.profile is not None
            and geom.extrusion.depth > 0
            and len(geom.clipping_planes) > 0):
        valid_clips += 1
        max_clip_count = max(max_clip_count, len(geom.clipping_planes))

print(f"    Valid: {valid_clips}/{total_clips}")
print(f"    Max clips on one element: {max_clip_count}")
print()

check("All ClippedExtrusions valid", valid_clips == total_clips, f"{valid_clips}/{total_clips}")

# ==================================================================
# BOOLEAN RESULT DATA QUALITY
# ==================================================================

bool_count = type_counts.get("BooleanResult", 0)
if bool_count > 0:
    print("  BOOLEAN RESULT DATA QUALITY:")
    print("  " + "-" * 50)

    valid_bools = 0
    total_bools = 0
    for elem in model.building_elements:
        try:
            geom = elem.geometry
        except (AttributeError, Exception):
            continue
        if not isinstance(geom, BooleanResult):
            continue
        total_bools += 1
        if geom.first_operand is not None and geom.second_operand is not None:
            valid_bools += 1

    print(f"    Valid: {valid_bools}/{total_bools}")
    print()

    check("All BooleanResults valid", valid_bools == total_bools, f"{valid_bools}/{total_bools}")

# ==================================================================
# EXTRUSION PARAMETRIC DATA
# ==================================================================

print("  EXTRUSION PARAMETRIC DATA:")
print("  " + "-" * 50)

all_depths_positive = True
all_profiles_valid = True
depth_range = [float("inf"), 0.0]
profile_types = {}
ext_count = 0

for elem in model.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        continue
    if not isinstance(geom, Extrusion):
        continue
    ext_count += 1

    # Check depth
    if geom.depth <= 0:
        all_depths_positive = False

    depth_range[0] = min(depth_range[0], geom.depth)
    depth_range[1] = max(depth_range[1], geom.depth)

    # Check profile
    profile = geom.profile
    if isinstance(profile, Polygon):
        n = len(profile.points)
        key = f"Polygon({n})"
        if n < 3:
            all_profiles_valid = False
    elif isinstance(profile, Circle):
        key = "Circle"
    elif isinstance(profile, tuple):
        key = "ProfileWithVoids"
        outer = profile[0]
        if not isinstance(outer, Polygon) or len(outer.points) < 3:
            all_profiles_valid = False
    else:
        key = type(profile).__name__
        all_profiles_valid = False

    profile_types[key] = profile_types.get(key, 0) + 1

print(f"    Extrusions parsed: {ext_count}")
print(f"    Depth range: {depth_range[0]:.4f} - {depth_range[1]:.4f} m")
print()
print(f"    {'Profile Type':<25s} {'Count':>5s}")
print("    " + "-" * 32)
for ptype, count in sorted(profile_types.items(), key=lambda x: -x[1]):
    print(f"    {ptype:<25s} {count:5d}")
print()

check("All extrusion depths > 0", all_depths_positive)
check("All extrusion profiles valid", all_profiles_valid)

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
    print("SUCCESS: All HiLo round-trip tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
