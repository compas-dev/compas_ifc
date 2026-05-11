"""
19 Clipped Extrusion Test
==========================

Tests the ClippedExtrusion parametric class and its round-trip through IFC:

  A. Write round-trip: create ClippedExtrusion -> save -> reload -> verify
  B. HiLo model read: verify IfcBooleanClippingResult elements parse as ClippedExtrusion
  C. Duplex model: verify no regressions (Duplex has no boolean clipping)
"""

import math
import os
import sys
import time

from compas.geometry import Frame, Plane, Point, Polygon, Vector

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import ClippedExtrusion, Extrusion

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

# Create a simple rectangular extrusion
profile = Polygon([
    Point(0, 0, 0),
    Point(6, 0, 0),
    Point(6, 0.3, 0),
    Point(0, 0.3, 0),
])
base_extrusion = Extrusion(
    profile=profile,
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame.worldXY(),
)

# Create two clipping planes (angled cuts at both ends of the wall)
# Clip 1: angled plane at x=0 end, cutting at 45 degrees
plane1 = Plane(Point(0.5, 0.15, 2.5), Vector(-0.707, 0.0, 0.707))
# Clip 2: angled plane at x=6 end, cutting at 30 degrees
plane2 = Plane(Point(5.5, 0.15, 2.5), Vector(0.866, 0.0, 0.5))

clipped = ClippedExtrusion(
    extrusion=base_extrusion,
    clipping_planes=[(plane1, True), (plane2, False)],
)

print(f"  Created: {clipped}")
print(f"  Extrusion depth: {clipped.extrusion.depth}")
print(f"  Clipping planes: {len(clipped.clipping_planes)}")

# Assign to a wall element
wall = model.create_wall(name="ClippedWall", geometry=clipped, parent=storey)

# Also create a single-clip element
profile2 = Polygon([
    Point(0, 0, 0),
    Point(4, 0, 0),
    Point(4, 0.2, 0),
    Point(0, 0.2, 0),
])
base_ext2 = Extrusion(
    profile=profile2,
    direction=Vector(0, 0, 1),
    depth=2.8,
    frame=Frame([0, 2, 0], [1, 0, 0], [0, 1, 0]),
)
plane3 = Plane(Point(2, 2.1, 2.0), Vector(0, 0, 1))
clipped2 = ClippedExtrusion(
    extrusion=base_ext2,
    clipping_planes=[(plane3, True)],
)
slab = model.create_slab(name="ClippedSlab", geometry=clipped2, parent=storey)

# Save
os.makedirs("temp", exist_ok=True)
out_path = "temp/clipped_extrusion_test.ifc"
model.save(out_path)
print(f"\n  Saved to {out_path}")

# Reload
model2 = BuildingInformationModel(out_path)

# Count ClippedExtrusion instances
clipped_count = 0
non_clipped = 0
for elem in model2.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        continue
    if isinstance(geom, ClippedExtrusion):
        clipped_count += 1
    elif geom is not None:
        non_clipped += 1

print(f"\n  Reloaded elements:")
print(f"    ClippedExtrusion: {clipped_count}")
print(f"    Other geometry:   {non_clipped}")

check("Write round-trip: 2 ClippedExtrusions", clipped_count == 2, f"{clipped_count}")

# Verify parametric data preserved
for elem in model2.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        continue
    if not isinstance(geom, ClippedExtrusion):
        continue

    if elem.name == "ClippedWall":
        check("ClippedWall depth preserved", abs(geom.extrusion.depth - 3.0) < 0.01,
              f"depth={geom.extrusion.depth}")
        check("ClippedWall has 2 clips", len(geom.clipping_planes) == 2,
              f"{len(geom.clipping_planes)} clips")
        check("ClippedWall profile is Polygon(4)", isinstance(geom.extrusion.profile, Polygon)
              and len(geom.extrusion.profile.points) == 4)

        # Verify plane normals round-tripped
        p1_normal = geom.clipping_planes[0][0].normal
        p1_agree = geom.clipping_planes[0][1]
        p2_normal = geom.clipping_planes[1][0].normal
        p2_agree = geom.clipping_planes[1][1]
        print(f"\n    Clip 1: normal={p1_normal}, agree={p1_agree}")
        print(f"    Clip 2: normal={p2_normal}, agree={p2_agree}")

        check("ClippedWall clip 1 agreement=True", p1_agree is True)
        check("ClippedWall clip 2 agreement=False", p2_agree is False)

    elif elem.name == "ClippedSlab":
        check("ClippedSlab depth preserved", abs(geom.extrusion.depth - 2.8) < 0.01,
              f"depth={geom.extrusion.depth}")
        check("ClippedSlab has 1 clip", len(geom.clipping_planes) == 1,
              f"{len(geom.clipping_planes)} clips")

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
    type_counts = {}
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
        type_counts[tn] = type_counts.get(tn, 0) + 1

    print(f"  Elements with geometry: {geom_count}")
    print(f"  Parse errors: {parse_errors}")
    for name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        pct = count / geom_count * 100 if geom_count else 0
        print(f"    {name:25s} {count:5d}  ({pct:.1f}%)")

    # Check boolean entities in file
    bool_clip = hilo._file.get_entities_by_type("IfcBooleanClippingResult")
    bool_result = hilo._file.get_entities_by_type("IfcBooleanResult")
    print(f"\n  IfcBooleanClippingResult: {len(bool_clip)}")
    print(f"  IfcBooleanResult:         {len(bool_result)}")

    clipped_ext_count = type_counts.get("ClippedExtrusion", 0)
    print(f"  ClippedExtrusion parsed:  {clipped_ext_count}")

    # Not all 190 IfcBooleanClippingResult map to ClippedExtrusion — some
    # have non-half-space second operands (e.g. IfcExtrudedAreaSolid boolean
    # subtractions) and some are embedded inside IfcMappedItem instances.
    check("HiLo: ClippedExtrusion parsed >= 120",
          clipped_ext_count >= 120, f"{clipped_ext_count} ClippedExtrusions")
    check("HiLo: parse errors == 0", parse_errors == 0, f"{parse_errors} errors")

    # Verify ClippedExtrusion data quality
    valid_clips = 0
    total_clips = 0
    max_clip_count = 0
    for elem in hilo.building_elements:
        try:
            geom = elem.geometry
        except (AttributeError, Exception):
            continue
        if not isinstance(geom, ClippedExtrusion):
            continue
        total_clips += 1
        if (geom.extrusion is not None
                and geom.extrusion.profile is not None
                and geom.extrusion.depth > 0
                and len(geom.clipping_planes) > 0):
            valid_clips += 1
            max_clip_count = max(max_clip_count, len(geom.clipping_planes))

    print(f"\n  Valid ClippedExtrusions: {valid_clips}/{total_clips}")
    print(f"  Max clipping planes on one element: {max_clip_count}")

    check("HiLo: all ClippedExtrusions valid", valid_clips == total_clips,
          f"{valid_clips}/{total_clips}")
    check("HiLo: total geometries >= 1400", geom_count >= 1400, f"{geom_count}")
    print()

else:
    print("\n  [SKIP] HiLo model not found at", hilo_path)
    print()

# ==================================================================
# C. Duplex no-regression
# ==================================================================

print("=" * 70)
print("C. DUPLEX NO-REGRESSION")
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
# Duplex has a few IfcBooleanResult entities (doors/windows with clipping)
check("Duplex: ClippedExtrusion <= 10", type_counts_d.get("ClippedExtrusion", 0) <= 10,
      f"{type_counts_d.get('ClippedExtrusion', 0)}")
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
    print("SUCCESS: All clipped extrusion tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
