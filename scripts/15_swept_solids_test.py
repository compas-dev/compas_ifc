"""
15 Swept Solids Round-Trip Test
================================

Phase 6 test: creates IfcRevolvedAreaSolid and IfcSweptDiskSolid entities,
saves to IFC, reloads, and verifies that they parse back into Revolution
and Pipe parametric classes.

Tests:
- Revolution with circular profile (full 360 deg) → round-trip
- Revolution with polygon profile (180 deg arc) → round-trip
- Pipe with polyline directrix → round-trip
"""

import os

from compas.geometry import Circle, Frame, Point, Polygon, Polyline, Vector

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import Pipe, Revolution

# ------------------------------------------------------------------
# Create model
# ------------------------------------------------------------------

model = BuildingInformationModel.template(schema="IFC4", unit="m")
storey = model.storeys[0]

# ------------------------------------------------------------------
# 1. Revolution: circle profile, 360 degrees (full torus-like solid)
# ------------------------------------------------------------------

rev1 = Revolution(
    profile=Circle(radius=0.3),
    axis_point=Point(1.0, 0, 0),
    axis_direction=Vector(0, 0, 1),
    angle=360.0,
    frame=Frame(Point(0, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
)

model.create_element(
    ifc_type="IfcColumn",
    geometry=rev1,
    frame=Frame(Point(0, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
    parent=storey,
    name="Revolution_Circle_360",
)

# ------------------------------------------------------------------
# 2. Revolution: polygon profile, 180 degrees (half-revolution)
# ------------------------------------------------------------------

profile_poly = Polygon([
    Point(0.5, -0.2, 0),
    Point(1.5, -0.2, 0),
    Point(1.5, 0.2, 0),
    Point(0.5, 0.2, 0),
])

rev2 = Revolution(
    profile=profile_poly,
    axis_point=Point(0, 0, 0),
    axis_direction=Vector(0, 0, 1),
    angle=180.0,
    frame=Frame(Point(5, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
)

model.create_element(
    ifc_type="IfcBeam",
    geometry=rev2,
    frame=Frame(Point(5, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
    parent=storey,
    name="Revolution_Polygon_180",
)

# ------------------------------------------------------------------
# 3. Pipe: polyline directrix
# ------------------------------------------------------------------

pipe1 = Pipe(
    directrix=Polyline([
        Point(0, 0, 0),
        Point(2, 0, 0),
        Point(2, 3, 0),
        Point(4, 3, 1),
    ]),
    radius=0.15,
)

model.create_element(
    ifc_type="IfcBuildingElementProxy",
    geometry=pipe1,
    frame=Frame(Point(10, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
    parent=storey,
    name="Pipe_Basic",
)

# ------------------------------------------------------------------
# 4. Pipe: hollow (with inner radius)
# ------------------------------------------------------------------

pipe2 = Pipe(
    directrix=Polyline([
        Point(0, 0, 0),
        Point(0, 5, 0),
        Point(0, 5, 3),
    ]),
    radius=0.3,
    inner_radius=0.25,
)

model.create_element(
    ifc_type="IfcBuildingElementProxy",
    geometry=pipe2,
    frame=Frame(Point(15, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
    parent=storey,
    name="Pipe_Hollow",
)

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------

os.makedirs("temp", exist_ok=True)
output_path = "temp/swept_solids_test.ifc"
model.save(output_path)
print(f"Saved: {output_path}")

# ------------------------------------------------------------------
# Reload and verify
# ------------------------------------------------------------------

print()
print("=" * 60)
print("Verification: Reload and check parametric round-trip")
print("=" * 60)

model2 = BuildingInformationModel(output_path)

# Count swept solid entities
revolved = model2._file.get_entities_by_type("IfcRevolvedAreaSolid")
swept_disk = model2._file.get_entities_by_type("IfcSweptDiskSolid")

print(f"IfcRevolvedAreaSolid entities: {len(revolved)}")
print(f"IfcSweptDiskSolid entities:    {len(swept_disk)}")
print()

# Verify each element
results = {}

for element in model2.building_elements:
    if not element.name:
        continue

    geom = element.geometry

    if geom is not None:
        gtype = type(geom).__name__
        results[element.name] = ("OK", gtype, geom)
        print(f"  [{element.ifc_type}] {element.name}: geometry={gtype}")

        # Print parametric details
        if isinstance(geom, Revolution):
            print(f"    profile: {type(geom.profile).__name__}")
            print(f"    axis_point: ({geom.axis_point.x:.2f}, {geom.axis_point.y:.2f}, {geom.axis_point.z:.2f})")
            print(f"    axis_direction: ({geom.axis_direction.x:.2f}, {geom.axis_direction.y:.2f}, {geom.axis_direction.z:.2f})")
            print(f"    angle: {geom.angle:.1f} deg")
        elif isinstance(geom, Pipe):
            print(f"    directrix: {len(geom.directrix.points)} points")
            print(f"    radius: {geom.radius:.3f}")
            if geom.inner_radius is not None:
                print(f"    inner_radius: {geom.inner_radius:.3f}")
        print()
    else:
        results[element.name] = ("MISSING", "None", None)
        print(f"  [{element.ifc_type}] {element.name}: geometry=MISSING")
        print()

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

print("=" * 60)
print("Results")
print("=" * 60)

# Check Revolution round-trips
rev1_ok = results.get("Revolution_Circle_360", ("FAIL",))[0] == "OK"
rev1_type = results.get("Revolution_Circle_360", ("", ""))[1] == "Revolution"

rev2_ok = results.get("Revolution_Polygon_180", ("FAIL",))[0] == "OK"
rev2_type = results.get("Revolution_Polygon_180", ("", ""))[1] == "Revolution"

# Check Pipe round-trips
pipe1_ok = results.get("Pipe_Basic", ("FAIL",))[0] == "OK"
pipe1_type = results.get("Pipe_Basic", ("", ""))[1] == "Pipe"

pipe2_ok = results.get("Pipe_Hollow", ("FAIL",))[0] == "OK"
pipe2_type = results.get("Pipe_Hollow", ("", ""))[1] == "Pipe"

# Check parametric details
rev1_geom = results.get("Revolution_Circle_360", ("", "", None))[2]
rev1_angle_ok = isinstance(rev1_geom, Revolution) and abs(rev1_geom.angle - 360.0) < 1e-6

rev2_geom = results.get("Revolution_Polygon_180", ("", "", None))[2]
rev2_angle_ok = isinstance(rev2_geom, Revolution) and abs(rev2_geom.angle - 180.0) < 1e-6

pipe1_geom = results.get("Pipe_Basic", ("", "", None))[2]
pipe1_radius_ok = isinstance(pipe1_geom, Pipe) and abs(pipe1_geom.radius - 0.15) < 1e-6

pipe2_geom = results.get("Pipe_Hollow", ("", "", None))[2]
pipe2_inner_ok = isinstance(pipe2_geom, Pipe) and pipe2_geom.inner_radius is not None and abs(pipe2_geom.inner_radius - 0.25) < 1e-6

expected_revolved = 2
expected_swept = 2

ok_rev_count = len(revolved) == expected_revolved
ok_swept_count = len(swept_disk) == expected_swept

print(f"IfcRevolvedAreaSolid:    {len(revolved)} (expected {expected_revolved}) {'PASS' if ok_rev_count else 'FAIL'}")
print(f"IfcSweptDiskSolid:       {len(swept_disk)} (expected {expected_swept}) {'PASS' if ok_swept_count else 'FAIL'}")
print()
print(f"Rev circle 360:  parsed={'PASS' if rev1_ok else 'FAIL'}  type={'PASS' if rev1_type else 'FAIL'}  angle={'PASS' if rev1_angle_ok else 'FAIL'}")
print(f"Rev polygon 180: parsed={'PASS' if rev2_ok else 'FAIL'}  type={'PASS' if rev2_type else 'FAIL'}  angle={'PASS' if rev2_angle_ok else 'FAIL'}")
print(f"Pipe basic:      parsed={'PASS' if pipe1_ok else 'FAIL'}  type={'PASS' if pipe1_type else 'FAIL'}  radius={'PASS' if pipe1_radius_ok else 'FAIL'}")
print(f"Pipe hollow:     parsed={'PASS' if pipe2_ok else 'FAIL'}  type={'PASS' if pipe2_type else 'FAIL'}  inner_r={'PASS' if pipe2_inner_ok else 'FAIL'}")

all_ok = all([
    ok_rev_count, ok_swept_count,
    rev1_ok, rev1_type, rev1_angle_ok,
    rev2_ok, rev2_type, rev2_angle_ok,
    pipe1_ok, pipe1_type, pipe1_radius_ok,
    pipe2_ok, pipe2_type, pipe2_inner_ok,
])

if all_ok:
    print("\nSUCCESS: All Phase 6 swept solid round-trip tests passed.")
else:
    print("\nWARNING: Some tests failed.")
