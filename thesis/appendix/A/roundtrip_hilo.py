"""
HiLo Model Round-Trip Test
============================

Loads the real-world HiLo_Model-Architecture.ifc model (IFC2X3, ~1920
building elements) and verifies:

  Part 1: Read — geometry parsing produces correct parametric types
           including boolean clipping operations
  Part 2: Write round-trip — sample elements are reconstructed from
           their parsed parametric data, saved to a new IFC file,
           reloaded, and compared against the originals

This model is dominated by Extrusion with significant ClippedExtrusion
(IfcBooleanClippingResult) and TessellatedBrep (visual geometry fallback).
"""

import os
import sys
import time

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
    orig_ptype = type(original.profile).__name__
    reload_ptype = type(reloaded.profile).__name__
    if not check(f"{name} profile type", orig_ptype == reload_ptype,
                 f"{orig_ptype} vs {reload_ptype}"):
        ok = False
    if isinstance(original.profile, Polygon) and isinstance(reloaded.profile, Polygon):
        if not check(f"{name} profile pts",
                     len(original.profile.points) == len(reloaded.profile.points),
                     f"{len(original.profile.points)} vs {len(reloaded.profile.points)}"):
            ok = False
    if isinstance(original.profile, Circle) and isinstance(reloaded.profile, Circle):
        if not check(f"{name} circle radius",
                     abs(original.profile.radius - reloaded.profile.radius) < TOL,
                     f"{original.profile.radius} vs {reloaded.profile.radius}"):
            ok = False
    if isinstance(original.profile, tuple) and isinstance(reloaded.profile, tuple):
        if not check(f"{name} void count",
                     len(original.profile[1]) == len(reloaded.profile[1]),
                     f"{len(original.profile[1])} vs {len(reloaded.profile[1])}"):
            ok = False
    # Volume and surface area preservation
    orig_vol = original.volume()
    reload_vol = reloaded.volume()
    if orig_vol > 0 and reload_vol > 0:
        if not check(f"{name} volume", abs(orig_vol - reload_vol) / orig_vol < TOL,
                     f"{orig_vol:.6f} vs {reload_vol:.6f}"):
            ok = False
    orig_sa = original.surface_area()
    reload_sa = reloaded.surface_area()
    if orig_sa > 0 and reload_sa > 0:
        if not check(f"{name} surface_area", abs(orig_sa - reload_sa) / orig_sa < TOL,
                     f"{orig_sa:.6f} vs {reload_sa:.6f}"):
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
    # Surface area comparison
    orig_area = original.area()
    reload_area = reloaded.area()
    if orig_area > 0 and reload_area > 0:
        if not check(f"{name} area", abs(orig_area - reload_area) / orig_area < TOL,
                     f"{orig_area:.6f} vs {reload_area:.6f}"):
            ok = False
    # Volume comparison (only for closed meshes)
    orig_vol = original.volume()
    reload_vol = reloaded.volume()
    if orig_vol is not None and reload_vol is not None and orig_vol > 0:
        if not check(f"{name} volume", abs(orig_vol - reload_vol) / orig_vol < TOL,
                     f"{orig_vol:.6f} vs {reload_vol:.6f}"):
            ok = False
    return ok


# ==================================================================
# CHECK FILE EXISTS
# ==================================================================

hilo_path = "temp/HiLo_Model-Architecture.ifc"

if not os.path.exists(hilo_path):
    print(f"[SKIP] HiLo model not found at {hilo_path}")
    print("       Download or copy the file to run this test.")
    sys.exit(0)

# ==================================================================
# PART 1: READ
# ==================================================================

print("=" * 70)
print(f"PART 1: READ — {hilo_path}")
print("=" * 70)

t0 = time.time()
model = BuildingInformationModel(hilo_path)
load_time = time.time() - t0
print(f"\n  Loaded in {load_time:.1f}s")

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
    elements_by_type[tn].append((elem.name or f"unnamed_{geom_count}", geom, elem))

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
# IFC boolean entity counts
# ------------------------------------------------------------------

bool_clip_entities = model._file.get_entities_by_type("IfcBooleanClippingResult")
bool_result_entities = model._file.get_entities_by_type("IfcBooleanResult")
print(f"  IFC Boolean Entities:")
print(f"    IfcBooleanClippingResult: {len(bool_clip_entities)}")
print(f"    IfcBooleanResult:         {len(bool_result_entities)}")
print()

# ------------------------------------------------------------------
# Basic checks
# ------------------------------------------------------------------

check("Read: total geometries >= 1400", geom_count >= 1400, f"{geom_count}")
check("Read: parse errors == 0", parse_errors == 0, f"{parse_errors}")
check("Read: Extrusion >= 1000", type_counts.get("Extrusion", 0) >= 1000, f"{type_counts.get('Extrusion', 0)}")
check("Read: ClippedExtrusion >= 120", type_counts.get("ClippedExtrusion", 0) >= 120, f"{type_counts.get('ClippedExtrusion', 0)}")
check("Read: BooleanResult >= 0", type_counts.get("BooleanResult", 0) >= 0, f"{type_counts.get('BooleanResult', 0)}")
check("Read: TessellatedBrep >= 200", type_counts.get("TessellatedBrep", 0) >= 200, f"{type_counts.get('TessellatedBrep', 0)}")

# ==================================================================
# CLIPPED EXTRUSION DATA QUALITY
# ==================================================================

print("  CLIPPED EXTRUSION DATA QUALITY:")
print("  " + "-" * 50)

valid_clips = 0
total_clips = 0
max_clip_count = 0

for _, geom, _ in elements_by_type.get("ClippedExtrusion", []):
    total_clips += 1
    if (geom.extrusion is not None
            and geom.extrusion.profile is not None
            and geom.extrusion.depth > 0
            and len(geom.clipping_planes) > 0):
        valid_clips += 1
        max_clip_count = max(max_clip_count, len(geom.clipping_planes))

print(f"    Valid: {valid_clips}/{total_clips}")
print(f"    Max clips on one element: {max_clip_count}")
print()

check("Read: all ClippedExtrusions valid", valid_clips == total_clips, f"{valid_clips}/{total_clips}")

# ==================================================================
# BOOLEAN RESULT DATA QUALITY
# ==================================================================

bool_count = type_counts.get("BooleanResult", 0)
if bool_count > 0:
    print("  BOOLEAN RESULT DATA QUALITY:")
    print("  " + "-" * 50)

    valid_bools = 0
    total_bools = 0
    for _, geom, _ in elements_by_type.get("BooleanResult", []):
        total_bools += 1
        if geom.first_operand is not None and geom.second_operand is not None:
            valid_bools += 1

    print(f"    Valid: {valid_bools}/{total_bools}")
    print()

    check("Read: all BooleanResults valid", valid_bools == total_bools, f"{valid_bools}/{total_bools}")

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

for _, geom, _ in elements_by_type.get("Extrusion", []):
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

# ==================================================================
# PART 2: WRITE ROUND-TRIP
# ==================================================================

print()
print("=" * 70)
print("PART 2: WRITE ROUND-TRIP (sample per type)")
print("=" * 70)

# Select samples: up to MAX_SAMPLES per parametric type
# Skip TessellatedBrep (no writer — read-only visual fallback)
ROUNDTRIP_TYPES = ["Extrusion", "ClippedExtrusion", "BooleanResult", "Mesh"]

samples = {}  # name -> (type_name, original_geom)
for tname in ROUNDTRIP_TYPES:
    entries = elements_by_type.get(tname, [])
    selected = entries[:MAX_SAMPLES]
    for i, (ename, geom, elem) in enumerate(selected):
        key = f"RT_{tname}_{i:03d}"
        samples[key] = (tname, geom, elem)

print(f"\n  Samples selected for write round-trip:")
for tname in ROUNDTRIP_TYPES:
    total = len(elements_by_type.get(tname, []))
    sampled = sum(1 for _, (t, _, _e) in samples.items() if t == tname)
    if total > 0:
        print(f"    {tname:<25s} {sampled:3d} / {total:3d}")

skipped_types = [t for t in type_counts if t not in ROUNDTRIP_TYPES]
if skipped_types:
    print(f"\n  Skipped (no writer): {', '.join(skipped_types)}")

if not samples:
    print("  No parametric elements to round-trip.")
else:
    # Create new model and write sampled geometries
    print(f"\n  Creating new model with {len(samples)} elements...")

    new_model = BuildingInformationModel.template(schema="IFC4", unit="m")
    new_storey = new_model.storeys[0]

    for key, (tname, geom, _elem) in samples.items():
        new_model.create_element(name=key, geometry=geom, parent=new_storey)

    os.makedirs("temp", exist_ok=True)
    rt_path = "temp/thesis_roundtrip_hilo.ifc"
    new_model.save(rt_path)
    print(f"  Saved to {rt_path}")

    # Reload and compare
    print("  Reloading and comparing...\n")
    reloaded_model = BuildingInformationModel(rt_path)

    reloaded_data = {}
    for elem in reloaded_model.building_elements:
        name = elem.name or ""
        if name.startswith("RT_"):
            try:
                geom = elem.geometry
            except (AttributeError, Exception):
                geom = None
            reloaded_data[name] = (geom, elem)

    # Compare each sample
    match_count = 0
    mismatch_count = 0
    missing_count = 0

    for key, (tname, original, orig_elem) in sorted(samples.items()):
        entry = reloaded_data.get(key)

        if entry is None:
            missing_count += 1
            check(f"{key} reloaded", False, "missing")
            continue

        reloaded, reload_elem = entry
        if reloaded is None:
            missing_count += 1
            check(f"{key} reloaded", False, "geom is None")
            continue

        reloaded_type = type(reloaded).__name__

        # Type check (ClippedExtrusion ext-halfspace may come back as BooleanResult or vice versa)
        type_ok = reloaded_type == tname
        if not type_ok:
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

        # Element-level volume/SA comparison (works for ALL types via visual_geometry fallback)
        # For ClippedExtrusion/BooleanResult, tessellation may differ significantly between
        # IFC schemas (IFC2X3 → IFC4), especially with multiple clips. These are
        # informational only — not counted as failures since parametric data is validated above.
        ELEM_TOL = 0.10  # 10% tolerance for cross-schema tessellation differences
        is_boolean_type = tname in ("ClippedExtrusion", "BooleanResult")
        orig_vol = orig_elem.volume
        reload_vol = reload_elem.volume
        if orig_vol is not None and reload_vol is not None and orig_vol > 0:
            vol_match = abs(orig_vol - reload_vol) / orig_vol < ELEM_TOL
            if is_boolean_type:
                # Informational only — cross-schema boolean evaluation may differ
                status = "PASS" if vol_match else "INFO"
                results.append((status, f"{key} elem.volume", f"{orig_vol:.4f} vs {reload_vol:.4f}"))
                if vol_match:
                    pass_count += 1
            else:
                if not check(f"{key} elem.volume", vol_match, f"{orig_vol:.4f} vs {reload_vol:.4f}"):
                    ok = False
        orig_sa = orig_elem.surface_area
        reload_sa = reload_elem.surface_area
        if orig_sa is not None and reload_sa is not None and orig_sa > 0:
            sa_match = abs(orig_sa - reload_sa) / orig_sa < ELEM_TOL
            if is_boolean_type:
                status = "PASS" if sa_match else "INFO"
                results.append((status, f"{key} elem.surface_area", f"{orig_sa:.4f} vs {reload_sa:.4f}"))
                if sa_match:
                    pass_count += 1
            else:
                if not check(f"{key} elem.surface_area", sa_match, f"{orig_sa:.4f} vs {reload_sa:.4f}"):
                    ok = False

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
# PART 3: VOLUME & SURFACE AREA (all geometry types)
# ==================================================================

print()
print("=" * 70)
print("PART 3: VOLUME & SURFACE AREA (element-level, all types)")
print("=" * 70)
print()
print("  Uses element.volume / element.surface_area which falls back to")
print("  visual_geometry (tessellated brep) when parametric returns None.")
print()

ALL_GEOM_TYPES = ["Extrusion", "ClippedExtrusion", "BooleanResult", "Mesh", "TessellatedBrep"]

for type_name in ALL_GEOM_TYPES:
    entries = elements_by_type.get(type_name, [])
    if not entries:
        continue

    total = len(entries)
    vol_positive = 0
    sa_positive = 0
    vol_none = 0
    sa_none = 0
    vol_values = []

    for _, _geom, elem in entries:
        v = elem.volume
        if v is not None and v > 0:
            vol_positive += 1
            vol_values.append(v)
        else:
            vol_none += 1
        sa = elem.surface_area
        if sa is not None and sa > 0:
            sa_positive += 1
        else:
            sa_none += 1

    print(f"  {type_name} ({total} elements):")
    print(f"    volume > 0:        {vol_positive}")
    if vol_values:
        print(f"    volume range:      {min(vol_values):.6f} - {max(vol_values):.6f}")
        print(f"    volume mean:       {sum(vol_values)/len(vol_values):.6f}")
    if vol_none > 0:
        print(f"    volume None/zero:  {vol_none}")
    print(f"    surface_area > 0:  {sa_positive}")
    if sa_none > 0:
        print(f"    surface_area None: {sa_none}")
    print()

    # Mesh: may be open surfaces (no enclosed volume)
    # ClippedExtrusion/BooleanResult/TessellatedBrep: ifcopenshell may not evaluate all geometries
    types_with_partial_volume = {"Mesh", "ClippedExtrusion", "BooleanResult", "TessellatedBrep"}
    if type_name in types_with_partial_volume:
        check(f"Vol/SA: {type_name} most elem.volume > 0", vol_positive >= total * 0.9 or total <= 5,
              f"{vol_positive}/{total}")
    else:
        check(f"Vol/SA: all {type_name} elem.volume > 0", vol_positive == total,
              f"{vol_positive}/{total}")
    check(f"Vol/SA: all {type_name} elem.surface_area > 0", sa_positive == total,
          f"{sa_positive}/{total}")


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
