"""
Duplex Model Round-Trip Test
=============================

Loads the real-world Duplex_A_20110907.ifc model (IFC2X3, ~265 building
elements) and verifies that geometry parsing produces correct parametric
types with valid data.

This model is dominated by Extrusion (IfcExtrudedAreaSolid) geometry
with some Mesh fallback for complex elements.
"""

import sys

from compas.geometry import Circle, Polygon

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import Extrusion

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

print("=" * 70)
print("DUPLEX MODEL: data/Duplex_A_20110907.ifc")
print("=" * 70)

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

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
# Basic checks
# ------------------------------------------------------------------

check("Total geometries >= 260", geom_count >= 260, f"{geom_count}")
check("Parse errors == 0", parse_errors == 0, f"{parse_errors}")
check("Extrusion count >= 190", type_counts.get("Extrusion", 0) >= 190, f"{type_counts.get('Extrusion', 0)}")
check("Mesh count >= 50", type_counts.get("Mesh", 0) >= 50, f"{type_counts.get('Mesh', 0)}")

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
check("Polygon(4) dominant (>= 140)", profile_types.get("Polygon(4)", 0) >= 140, f"{profile_types.get('Polygon(4)', 0)}")

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
    print("SUCCESS: All Duplex round-trip tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
