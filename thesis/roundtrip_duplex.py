"""
Duplex Model Round-Trip Test
=============================

Loads the real-world Duplex_A_20110907.ifc model (IFC2X3, ~265 building
elements) and verifies:

  Part 1: Read — geometry parsing produces correct parametric types
  Part 2: Write round-trip — sample elements are reconstructed from
           their parsed parametric data, saved to a new IFC file,
           reloaded, and compared against the originals

This model is dominated by Extrusion (IfcExtrudedAreaSolid) geometry
with some Mesh fallback for complex elements.
"""

import os
import sys

from compas.datastructures import Mesh
from compas.geometry import Circle, Polygon

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import BooleanResult, ClippedExtrusion, Extrusion

pass_count = 0
fail_count = 0
results = []
TOL = 1e-4

# Maximum samples per geometry type for the write round-trip
MAX_SAMPLES = 20


def check(label, condition, detail=""):
    global pass_count, fail_count
    status = "PASS" if condition else "FAIL"
    if condition:
        pass_count += 1
    else:
        fail_count += 1
    results.append((status, label, detail))
    return condition


def compare_extrusion(original, reloaded, name):
    """Compare two Extrusion objects for parametric equivalence."""
    ok = True
    if not check(f"{name} depth", abs(original.depth - reloaded.depth) < TOL,
                 f"{original.depth} vs {reloaded.depth}"):
        ok = False
    # Profile type
    orig_ptype = type(original.profile).__name__
    reload_ptype = type(reloaded.profile).__name__
    if not check(f"{name} profile type", orig_ptype == reload_ptype,
                 f"{orig_ptype} vs {reload_ptype}"):
        ok = False
    # Profile point count (for Polygon)
    if isinstance(original.profile, Polygon) and isinstance(reloaded.profile, Polygon):
        if not check(f"{name} profile pts",
                     len(original.profile.points) == len(reloaded.profile.points),
                     f"{len(original.profile.points)} vs {len(reloaded.profile.points)}"):
            ok = False
    # Circle radius
    if isinstance(original.profile, Circle) and isinstance(reloaded.profile, Circle):
        if not check(f"{name} circle radius",
                     abs(original.profile.radius - reloaded.profile.radius) < TOL,
                     f"{original.profile.radius} vs {reloaded.profile.radius}"):
            ok = False
    # Profile with voids: check void count
    if isinstance(original.profile, tuple) and isinstance(reloaded.profile, tuple):
        if not check(f"{name} void count",
                     len(original.profile[1]) == len(reloaded.profile[1]),
                     f"{len(original.profile[1])} vs {len(reloaded.profile[1])}"):
            ok = False
    return ok


def compare_clipped(original, reloaded, name):
    """Compare two ClippedExtrusion objects."""
    ok = compare_extrusion(original.extrusion, reloaded.extrusion, f"{name}.ext")
    if not check(f"{name} clip count",
                 len(original.clipping_planes) == len(reloaded.clipping_planes),
                 f"{len(original.clipping_planes)} vs {len(reloaded.clipping_planes)}"):
        ok = False
    else:
        for i, ((p1, a1), (p2, a2)) in enumerate(zip(original.clipping_planes, reloaded.clipping_planes)):
            if not check(f"{name} clip[{i}] agree", a1 == a2, f"{a1} vs {a2}"):
                ok = False
    return ok


def compare_boolean(original, reloaded, name):
    """Compare two BooleanResult objects."""
    ok = True
    if not check(f"{name} operator", original.operator == reloaded.operator,
                 f"{original.operator} vs {reloaded.operator}"):
        ok = False
    if not check(f"{name} first type",
                 type(original.first_operand).__name__ == type(reloaded.first_operand).__name__,
                 f"{type(original.first_operand).__name__} vs {type(reloaded.first_operand).__name__}"):
        ok = False
    if not check(f"{name} second type",
                 type(original.second_operand).__name__ == type(reloaded.second_operand).__name__,
                 f"{type(original.second_operand).__name__} vs {type(reloaded.second_operand).__name__}"):
        ok = False
    return ok


def compare_mesh(original, reloaded, name):
    """Compare two Mesh objects."""
    ok = True
    if not check(f"{name} vertices",
                 original.number_of_vertices() == reloaded.number_of_vertices(),
                 f"{original.number_of_vertices()} vs {reloaded.number_of_vertices()}"):
        ok = False
    if not check(f"{name} faces",
                 original.number_of_faces() == reloaded.number_of_faces(),
                 f"{original.number_of_faces()} vs {reloaded.number_of_faces()}"):
        ok = False
    return ok


# ==================================================================
# PART 1: READ
# ==================================================================

print("=" * 70)
print("PART 1: READ — data/Duplex_A_20110907.ifc")
print("=" * 70)

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

print("\n  Parsing all building elements...")

type_counts = {}
geom_count = 0
parse_errors = 0
error_names = []

# Collect all elements with geometry for later sampling
elements_by_type = {}  # type_name -> [(elem_name, geom), ...]

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

    if tn not in elements_by_type:
        elements_by_type[tn] = []
    elements_by_type[tn].append((elem.name or f"unnamed_{geom_count}", geom))

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

check("Read: total geometries >= 260", geom_count >= 260, f"{geom_count}")
check("Read: parse errors == 0", parse_errors == 0, f"{parse_errors}")
check("Read: Extrusion count >= 190", type_counts.get("Extrusion", 0) >= 190, f"{type_counts.get('Extrusion', 0)}")
check("Read: Mesh count >= 50", type_counts.get("Mesh", 0) >= 50, f"{type_counts.get('Mesh', 0)}")

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

for _, geom in elements_by_type.get("Extrusion", []):
    ext_count += 1

    if geom.depth <= 0:
        all_depths_positive = False

    depth_range[0] = min(depth_range[0], geom.depth)
    depth_range[1] = max(depth_range[1], geom.depth)

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
if ext_count > 0:
    print(f"    Depth range: {depth_range[0]:.4f} - {depth_range[1]:.4f} m")
print()
print(f"    {'Profile Type':<25s} {'Count':>5s}")
print("    " + "-" * 32)
for ptype, count in sorted(profile_types.items(), key=lambda x: -x[1]):
    print(f"    {ptype:<25s} {count:5d}")
print()

check("Read: all extrusion depths > 0", all_depths_positive)
check("Read: all extrusion profiles valid", all_profiles_valid)
check("Read: Polygon(4) dominant (>= 140)", profile_types.get("Polygon(4)", 0) >= 140, f"{profile_types.get('Polygon(4)', 0)}")

# ==================================================================
# PART 2: WRITE ROUND-TRIP
# ==================================================================

print()
print("=" * 70)
print("PART 2: WRITE ROUND-TRIP (sample per type)")
print("=" * 70)

# Select samples: up to MAX_SAMPLES per parametric type
# Skip TessellatedBrep (no writer)
ROUNDTRIP_TYPES = ["Extrusion", "ClippedExtrusion", "BooleanResult", "Mesh"]

samples = {}  # name -> (type_name, original_geom)
for tname in ROUNDTRIP_TYPES:
    entries = elements_by_type.get(tname, [])
    selected = entries[:MAX_SAMPLES]
    for i, (ename, geom) in enumerate(selected):
        key = f"RT_{tname}_{i:03d}"
        samples[key] = (tname, geom)

print(f"\n  Samples selected for write round-trip:")
for tname in ROUNDTRIP_TYPES:
    total = len(elements_by_type.get(tname, []))
    sampled = sum(1 for _, (t, _) in samples.items() if t == tname)
    if total > 0:
        print(f"    {tname:<25s} {sampled:3d} / {total:3d}")

if not samples:
    print("  No parametric elements to round-trip.")
else:
    # Create new model and write sampled geometries
    print(f"\n  Creating new model with {len(samples)} elements...")

    new_model = BuildingInformationModel.template(schema="IFC4", unit="m")
    new_storey = new_model.storeys[0]

    for key, (tname, geom) in samples.items():
        new_model.create_element(name=key, geometry=geom, parent=new_storey)

    os.makedirs("temp", exist_ok=True)
    rt_path = "temp/thesis_roundtrip_duplex.ifc"
    new_model.save(rt_path)
    print(f"  Saved to {rt_path}")

    # Reload and compare
    print("  Reloading and comparing...\n")
    reloaded_model = BuildingInformationModel(rt_path)

    reloaded_geoms = {}
    for elem in reloaded_model.building_elements:
        name = elem.name or ""
        if name.startswith("RT_"):
            try:
                geom = elem.geometry
            except (AttributeError, Exception):
                geom = None
            reloaded_geoms[name] = geom

    # Compare each sample
    match_count = 0
    mismatch_count = 0
    missing_count = 0

    for key, (tname, original) in sorted(samples.items()):
        reloaded = reloaded_geoms.get(key)

        if reloaded is None:
            missing_count += 1
            check(f"{key} reloaded", False, "missing")
            continue

        reloaded_type = type(reloaded).__name__

        # Type check (ClippedExtrusion ext-halfspace may come back as BooleanResult or vice versa)
        type_ok = reloaded_type == tname
        if not type_ok:
            # Accept ClippedExtrusion ↔ BooleanResult interchange
            if {tname, reloaded_type} <= {"ClippedExtrusion", "BooleanResult"}:
                type_ok = True

        if not type_ok:
            check(f"{key} type", False, f"expected {tname}, got {reloaded_type}")
            mismatch_count += 1
            continue

        # Parametric comparison
        ok = True
        if tname == "Extrusion" and isinstance(reloaded, Extrusion):
            ok = compare_extrusion(original, reloaded, key)
        elif tname == "ClippedExtrusion" and isinstance(reloaded, ClippedExtrusion):
            ok = compare_clipped(original, reloaded, key)
        elif tname == "BooleanResult" and isinstance(reloaded, BooleanResult):
            ok = compare_boolean(original, reloaded, key)
        elif tname == "Mesh" and isinstance(reloaded, Mesh):
            ok = compare_mesh(original, reloaded, key)
        else:
            check(f"{key} type", type_ok, f"{tname} -> {reloaded_type}")

        if ok:
            match_count += 1
        else:
            mismatch_count += 1

    print(f"\n  Write round-trip results:")
    print(f"    Matched:    {match_count}")
    print(f"    Mismatched: {mismatch_count}")
    print(f"    Missing:    {missing_count}")

    check("Write RT: no missing elements", missing_count == 0, f"{missing_count}")
    check("Write RT: no mismatches", mismatch_count == 0, f"{mismatch_count}")

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
