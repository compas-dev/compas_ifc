"""
Generated Round-Trip Test
=========================

Creates one IFC model with all supported geometry types, saves to disk,
reloads, and verifies that parametric data is preserved through the
write-read cycle.

Covers 12 geometry type categories across 22 named elements:
  - Extrusion (polygon, circle, profile-with-voids)
  - Revolution (full 360, partial 180)
  - Pipe (solid, hollow)
  - CSG primitives (Box, Sphere, Cone, Cylinder)
  - ClippedExtrusion (1 clip, 2 clips)
  - BooleanResult (DIFFERENCE, UNION, INTERSECTION, nested, half-space)
  - Mesh (IfcPolygonalFaceSet)
  - Instancing (IfcRepresentationMap / IfcMappedItem)
"""

import os
import sys

from compas.datastructures import Mesh
from compas.geometry import Box, Circle, Cone, Cylinder, Frame, Plane, Point, Polygon, Polyline, Sphere, Vector

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import BooleanResult, ClippedExtrusion, Extrusion, HalfSpace, Pipe, Revolution

pass_count = 0
fail_count = 0
results = []
TOL = 1e-4


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
# CREATE MODEL
# ==================================================================

print("=" * 70)
print("CREATING TEST MODEL")
print("=" * 70)

model = BuildingInformationModel.template(schema="IFC4", unit="m")
storey = model.storeys[0]

# ------------------------------------------------------------------
# A1: Extrusion with polygon profile
# ------------------------------------------------------------------
ext_polygon = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(6, 0, 0), Point(6, 0.3, 0), Point(0, 0.3, 0)]),
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame.worldXY(),
)
model.create_wall(name="Ext_Polygon", geometry=ext_polygon, parent=storey)
print("  A1  Ext_Polygon       Extrusion (polygon, depth=3.0)")

# ------------------------------------------------------------------
# A2: Extrusion with circle profile
# ------------------------------------------------------------------
ext_circle = Extrusion(
    profile=Circle(radius=0.5),
    direction=Vector(0, 0, 1),
    depth=2.0,
    frame=Frame(Point(10, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_column(name="Ext_Circle", geometry=ext_circle, parent=storey)
print("  A2  Ext_Circle        Extrusion (circle r=0.5, depth=2.0)")

# ------------------------------------------------------------------
# A3: Extrusion with profile-with-voids
# ------------------------------------------------------------------
outer = Polygon([Point(-1, -1, 0), Point(1, -1, 0), Point(1, 1, 0), Point(-1, 1, 0)])
inner = Polygon([Point(-0.4, -0.4, 0), Point(0.4, -0.4, 0), Point(0.4, 0.4, 0), Point(-0.4, 0.4, 0)])
ext_voids = Extrusion(
    profile=(outer, [inner]),
    direction=Vector(0, 0, 1),
    depth=0.3,
    frame=Frame(Point(20, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_slab(name="Ext_Voids", geometry=ext_voids, parent=storey)
print("  A3  Ext_Voids         Extrusion (polygon+void, depth=0.3)")

# ------------------------------------------------------------------
# A4: Revolution with circle profile (360)
# ------------------------------------------------------------------
rev_circle = Revolution(
    profile=Circle(radius=0.1),
    axis_point=Point(1.0, 0, 0),
    axis_direction=Vector(0, 0, 1),
    angle=360.0,
    frame=Frame(Point(0, 10, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_column(name="Rev_Circle", geometry=rev_circle, parent=storey)
print("  A4  Rev_Circle        Revolution (circle r=0.1, 360 deg)")

# ------------------------------------------------------------------
# A5: Revolution with polygon profile (180)
# ------------------------------------------------------------------
rev_polygon = Revolution(
    profile=Polygon([Point(0.5, -0.15, 0), Point(1.2, -0.15, 0), Point(1.2, 0.15, 0), Point(0.5, 0.15, 0)]),
    axis_point=Point(0, 0, 0),
    axis_direction=Vector(0, 0, 1),
    angle=180.0,
    frame=Frame(Point(10, 10, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_beam(name="Rev_Polygon", geometry=rev_polygon, parent=storey)
print("  A5  Rev_Polygon       Revolution (polygon, 180 deg)")

# ------------------------------------------------------------------
# A6: Pipe (solid)
# ------------------------------------------------------------------
pipe_solid = Pipe(
    directrix=Polyline([Point(0, 0, 0), Point(2, 0, 0), Point(2, 3, 1)]),
    radius=0.15,
)
model.create_element(name="Pipe_Solid", geometry=pipe_solid, frame=Frame(Point(0, 20, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey)
print("  A6  Pipe_Solid        Pipe (r=0.15, 3-pt directrix)")

# ------------------------------------------------------------------
# A7: Pipe (hollow)
# ------------------------------------------------------------------
pipe_hollow = Pipe(
    directrix=Polyline([Point(0, 0, 0), Point(0, 4, 0), Point(0, 4, 2)]),
    radius=0.25,
    inner_radius=0.10,
)
model.create_element(name="Pipe_Hollow", geometry=pipe_hollow, frame=Frame(Point(10, 20, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey)
print("  A7  Pipe_Hollow       Pipe (r=0.25, inner=0.10)")

# ------------------------------------------------------------------
# A8-A11: CSG primitives
# ------------------------------------------------------------------
box = Box(1.0, 2.0, 3.0)
model.create_beam(name="CSG_Box", geometry=box, frame=Frame(Point(0, 30, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey)
print("  A8  CSG_Box           Box (1, 2, 3)")

sphere = Sphere(radius=1.5)
model.create_element(name="CSG_Sphere", geometry=sphere, frame=Frame(Point(10, 30, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey)
print("  A9  CSG_Sphere        Sphere (r=1.5)")

cone = Cone(radius=1.0, height=2.5)
model.create_element(name="CSG_Cone", geometry=cone, frame=Frame(Point(20, 30, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey)
print("  A10 CSG_Cone          Cone (r=1.0, h=2.5)")

cyl = Cylinder(radius=0.4, height=3.0)
model.create_column(name="CSG_Cylinder", geometry=cyl, frame=Frame(Point(30, 30, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey)
print("  A11 CSG_Cylinder      Cylinder (r=0.4, h=3.0)")

# ------------------------------------------------------------------
# A12: ClippedExtrusion (1 clip)
# ------------------------------------------------------------------
clip1_ext = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(4, 0, 0), Point(4, 0.2, 0), Point(0, 0.2, 0)]),
    direction=Vector(0, 0, 1),
    depth=2.8,
    frame=Frame(Point(0, 40, 0), Vector.Xaxis(), Vector.Yaxis()),
)
clip1_plane = Plane(Point(2, 0.1, 2.0), Vector(0, 0, 1))
clip_single = ClippedExtrusion(extrusion=clip1_ext, clipping_planes=[(clip1_plane, True)])
model.create_slab(name="Clip_Single", geometry=clip_single, parent=storey)
print("  A12 Clip_Single       ClippedExtrusion (1 clip)")

# ------------------------------------------------------------------
# A13: ClippedExtrusion (2 clips)
# ------------------------------------------------------------------
clip2_ext = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(6, 0, 0), Point(6, 0.3, 0), Point(0, 0.3, 0)]),
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame(Point(10, 40, 0), Vector.Xaxis(), Vector.Yaxis()),
)
clip2_p1 = Plane(Point(1.0, 0.15, 2.5), Vector(0, 0, 1))
clip2_p2 = Plane(Point(5.0, 0.15, 0.5), Vector(0, 0, -1))
clip_double = ClippedExtrusion(extrusion=clip2_ext, clipping_planes=[(clip2_p1, True), (clip2_p2, False)])
model.create_wall(name="Clip_Double", geometry=clip_double, parent=storey)
print("  A13 Clip_Double       ClippedExtrusion (2 clips)")

# ------------------------------------------------------------------
# A14: BooleanResult DIFFERENCE (ext - ext)
# ------------------------------------------------------------------
bool_diff_first = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(6, 0, 0), Point(6, 0.3, 0), Point(0, 0.3, 0)]),
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame.worldXY(),
)
bool_diff_second = Extrusion(
    profile=Polygon([Point(1.5, -0.05, 0.8), Point(3.5, -0.05, 0.8), Point(3.5, -0.05, 2.4), Point(1.5, -0.05, 2.4)]),
    direction=Vector(0, 1, 0),
    depth=0.4,
    frame=Frame.worldXY(),
)
bool_diff = BooleanResult(operator="DIFFERENCE", first_operand=bool_diff_first, second_operand=bool_diff_second)
model.create_wall(name="Bool_Diff", geometry=bool_diff, parent=storey)
print("  A14 Bool_Diff         BooleanResult DIFFERENCE (ext-ext)")

# ------------------------------------------------------------------
# A15: BooleanResult UNION (ext + ext)
# ------------------------------------------------------------------
bool_union_a = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(4, 0, 0), Point(4, 0.3, 0), Point(0, 0.3, 0)]),
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame([0, 50, 0], [1, 0, 0], [0, 1, 0]),
)
bool_union_b = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(0.3, 0, 0), Point(0.3, 3, 0), Point(0, 3, 0)]),
    direction=Vector(0, 0, 1),
    depth=3.0,
    frame=Frame([0, 47, 0], [1, 0, 0], [0, 1, 0]),
)
bool_union = BooleanResult(operator="UNION", first_operand=bool_union_a, second_operand=bool_union_b)
model.create_wall(name="Bool_Union", geometry=bool_union, parent=storey)
print("  A15 Bool_Union        BooleanResult UNION (ext+ext)")

# ------------------------------------------------------------------
# A16: BooleanResult INTERSECTION (ext & ext)
# ------------------------------------------------------------------
bool_inter_a = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(4, 0, 0), Point(4, 4, 0), Point(0, 4, 0)]),
    direction=Vector(0, 0, 1),
    depth=2.0,
    frame=Frame([0, 60, 0], [1, 0, 0], [0, 1, 0]),
)
bool_inter_b = Extrusion(
    profile=Polygon([Point(1, 1, 0), Point(5, 1, 0), Point(5, 5, 0), Point(1, 5, 0)]),
    direction=Vector(0, 0, 1),
    depth=2.0,
    frame=Frame([0, 60, 0], [1, 0, 0], [0, 1, 0]),
)
bool_inter = BooleanResult(operator="INTERSECTION", first_operand=bool_inter_a, second_operand=bool_inter_b)
model.create_slab(name="Bool_Inter", geometry=bool_inter, parent=storey)
print("  A16 Bool_Inter        BooleanResult INTERSECTION (ext&ext)")

# ------------------------------------------------------------------
# A17: BooleanResult nested (DIFFERENCE of UNION + halfspace)
# ------------------------------------------------------------------
nested_union = BooleanResult(
    operator="UNION",
    first_operand=Extrusion(
        profile=Polygon([Point(0, 0, 0), Point(4, 0, 0), Point(4, 0.3, 0), Point(0, 0.3, 0)]),
        direction=Vector(0, 0, 1),
        depth=3.0,
        frame=Frame([0, 70, 0], [1, 0, 0], [0, 1, 0]),
    ),
    second_operand=Extrusion(
        profile=Polygon([Point(0, 0, 0), Point(0.3, 0, 0), Point(0.3, 3, 0), Point(0, 3, 0)]),
        direction=Vector(0, 0, 1),
        depth=3.0,
        frame=Frame([0, 67, 0], [1, 0, 0], [0, 1, 0]),
    ),
)
nested_bool = BooleanResult(
    operator="DIFFERENCE",
    first_operand=nested_union,
    second_operand=HalfSpace(plane=Plane(Point(2, 68.5, 2.5), Vector(0, 0, 1)), agreement_flag=True),
)
model.create_wall(name="Bool_Nested", geometry=nested_bool, parent=storey)
print("  A17 Bool_Nested       BooleanResult nested DIFF(UNION, halfspace)")

# ------------------------------------------------------------------
# A18: BooleanResult DIFFERENCE (ext - halfspace)
# ------------------------------------------------------------------
bool_hs_ext = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(5, 0, 0), Point(5, 5, 0), Point(0, 5, 0)]),
    direction=Vector(0, 0, 1),
    depth=0.3,
    frame=Frame(Point(20, 40, 0), Vector.Xaxis(), Vector.Yaxis()),
)
bool_hs_half = HalfSpace(plane=Plane(Point(2.5, 2.5, 0.15), Vector(0.707, 0, 0.707)), agreement_flag=True)
bool_halfspace = BooleanResult(operator="DIFFERENCE", first_operand=bool_hs_ext, second_operand=bool_hs_half)
model.create_slab(name="Bool_HalfSpace", geometry=bool_halfspace, parent=storey)
print("  A18 Bool_HalfSpace    BooleanResult DIFF (ext-halfspace)")

# ------------------------------------------------------------------
# A19: Mesh (IfcPolygonalFaceSet)
# ------------------------------------------------------------------
mesh = Mesh.from_polyhedron(6)
model.create_slab(name="Mesh_Quad", geometry=mesh, frame=Frame(Point(0, 80, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey)
print("  A19 Mesh_Quad         Mesh (polyhedron)")

# ------------------------------------------------------------------
# A20-A22: Instancing (3 columns sharing same Cylinder)
# ------------------------------------------------------------------
shared_cyl = Cylinder(radius=0.2, height=3.5)
for i in range(3):
    frame = Frame(Point(i * 3, 90, 0), Vector.Xaxis(), Vector.Yaxis())
    model.create_column(name=f"Instance_{i+1}", geometry=shared_cyl, frame=frame, parent=storey)
print("  A20-22 Instance_1..3  Cylinder (shared, instanced)")

# ==================================================================
# SAVE
# ==================================================================

os.makedirs("temp", exist_ok=True)
out_path = "temp/thesis_roundtrip_generated.ifc"
model.save(out_path)
print(f"\n  Saved to {out_path}")

# ==================================================================
# RELOAD AND VERIFY
# ==================================================================

print()
print("=" * 70)
print("ROUND-TRIP VERIFICATION")
print("=" * 70)

model2 = BuildingInformationModel(out_path)

# ------------------------------------------------------------------
# IFC entity counts
# ------------------------------------------------------------------

entity_counts = {}
for etype in [
    "IfcExtrudedAreaSolid", "IfcRevolvedAreaSolid", "IfcSweptDiskSolid",
    "IfcCsgSolid", "IfcBooleanClippingResult", "IfcBooleanResult",
    "IfcPolygonalFaceSet", "IfcRepresentationMap", "IfcMappedItem",
]:
    entity_counts[etype] = len(model2.file.get_entities_by_type(etype))

print("\n  IFC Entity Counts:")
for etype, count in entity_counts.items():
    print(f"    {etype:30s} {count:3d}")
print()

# ------------------------------------------------------------------
# Per-element geometry parsing
# ------------------------------------------------------------------

parsed_geoms = {}  # name -> geom
parsed_elems = {}  # name -> elem (for element-level volume/SA checks)
for elem in model2.building_elements:
    name = elem.name or ""
    if not name:
        continue
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        geom = None
    parsed_geoms[name] = geom
    parsed_elems[name] = elem

# ------------------------------------------------------------------
# Verification checks
# ------------------------------------------------------------------

print("  ROUND-TRIP RESULTS:")
print("  " + "-" * 66)
print(f"  {'ID':<5} {'Name':<20} {'Expected':<20} {'Actual':<20} {'Status'}")
print("  " + "-" * 66)


def verify_type(name, expected_type_name):
    """Check that parsed geometry matches expected type."""
    geom = parsed_geoms.get(name)
    actual = type(geom).__name__ if geom is not None else "None"
    ok = actual == expected_type_name
    status = "PASS" if ok else "FAIL"
    return ok, actual, status


# A1: Ext_Polygon
ok, actual, status = verify_type("Ext_Polygon", "Extrusion")
print(f"  {'A1':<5} {'Ext_Polygon':<20} {'Extrusion':<20} {actual:<20} {status}")
check("Ext_Polygon type", ok, actual)
if ok:
    g = parsed_geoms["Ext_Polygon"]
    check("Ext_Polygon depth=3.0", abs(g.depth - 3.0) < TOL, f"{g.depth}")
    check("Ext_Polygon profile=Polygon(4)", isinstance(g.profile, Polygon) and len(g.profile.points) == 4)
    check("Ext_Polygon direction Z", abs(g.direction[2] - 1.0) < TOL, f"{g.direction}")

# A2: Ext_Circle
ok, actual, status = verify_type("Ext_Circle", "Extrusion")
print(f"  {'A2':<5} {'Ext_Circle':<20} {'Extrusion':<20} {actual:<20} {status}")
check("Ext_Circle type", ok, actual)
if ok:
    g = parsed_geoms["Ext_Circle"]
    check("Ext_Circle depth=2.0", abs(g.depth - 2.0) < TOL, f"{g.depth}")
    check("Ext_Circle profile=Circle", isinstance(g.profile, Circle))
    if isinstance(g.profile, Circle):
        check("Ext_Circle radius=0.5", abs(g.profile.radius - 0.5) < TOL, f"{g.profile.radius}")

# A3: Ext_Voids
ok, actual, status = verify_type("Ext_Voids", "Extrusion")
print(f"  {'A3':<5} {'Ext_Voids':<20} {'Extrusion':<20} {actual:<20} {status}")
check("Ext_Voids type", ok, actual)
if ok:
    g = parsed_geoms["Ext_Voids"]
    check("Ext_Voids depth=0.3", abs(g.depth - 0.3) < TOL, f"{g.depth}")
    check("Ext_Voids profile is tuple", isinstance(g.profile, tuple), type(g.profile).__name__)
    if isinstance(g.profile, tuple):
        check("Ext_Voids has 1 void", len(g.profile[1]) == 1, f"{len(g.profile[1])}")

# A4: Rev_Circle
ok, actual, status = verify_type("Rev_Circle", "Revolution")
print(f"  {'A4':<5} {'Rev_Circle':<20} {'Revolution':<20} {actual:<20} {status}")
check("Rev_Circle type", ok, actual)
if ok:
    g = parsed_geoms["Rev_Circle"]
    check("Rev_Circle angle=360", abs(g.angle - 360.0) < TOL, f"{g.angle}")
    check("Rev_Circle profile=Circle", isinstance(g.profile, Circle))
    if isinstance(g.profile, Circle):
        check("Rev_Circle radius=0.1", abs(g.profile.radius - 0.1) < TOL, f"{g.profile.radius}")

# A5: Rev_Polygon
ok, actual, status = verify_type("Rev_Polygon", "Revolution")
print(f"  {'A5':<5} {'Rev_Polygon':<20} {'Revolution':<20} {actual:<20} {status}")
check("Rev_Polygon type", ok, actual)
if ok:
    g = parsed_geoms["Rev_Polygon"]
    check("Rev_Polygon angle=180", abs(g.angle - 180.0) < TOL, f"{g.angle}")
    check("Rev_Polygon profile=Polygon", isinstance(g.profile, Polygon))
    if isinstance(g.profile, Polygon):
        check("Rev_Polygon profile 4 pts", len(g.profile.points) == 4, f"{len(g.profile.points)}")

# A6: Pipe_Solid
ok, actual, status = verify_type("Pipe_Solid", "Pipe")
print(f"  {'A6':<5} {'Pipe_Solid':<20} {'Pipe':<20} {actual:<20} {status}")
check("Pipe_Solid type", ok, actual)
if ok:
    g = parsed_geoms["Pipe_Solid"]
    check("Pipe_Solid radius=0.15", abs(g.radius - 0.15) < TOL, f"{g.radius}")
    check("Pipe_Solid inner=None", g.inner_radius is None, f"{g.inner_radius}")
    check("Pipe_Solid directrix 3 pts", len(g.directrix.points) == 3, f"{len(g.directrix.points)}")

# A7: Pipe_Hollow
ok, actual, status = verify_type("Pipe_Hollow", "Pipe")
print(f"  {'A7':<5} {'Pipe_Hollow':<20} {'Pipe':<20} {actual:<20} {status}")
check("Pipe_Hollow type", ok, actual)
if ok:
    g = parsed_geoms["Pipe_Hollow"]
    check("Pipe_Hollow radius=0.25", abs(g.radius - 0.25) < TOL, f"{g.radius}")
    check("Pipe_Hollow inner=0.10", g.inner_radius is not None and abs(g.inner_radius - 0.10) < TOL, f"{g.inner_radius}")

# A8: CSG_Box
ok, actual, status = verify_type("CSG_Box", "Box")
print(f"  {'A8':<5} {'CSG_Box':<20} {'Box':<20} {actual:<20} {status}")
check("CSG_Box type", ok, actual)
if ok:
    g = parsed_geoms["CSG_Box"]
    check("CSG_Box xsize=1.0", abs(g.xsize - 1.0) < TOL, f"{g.xsize}")
    check("CSG_Box ysize=2.0", abs(g.ysize - 2.0) < TOL, f"{g.ysize}")
    check("CSG_Box zsize=3.0", abs(g.zsize - 3.0) < TOL, f"{g.zsize}")

# A9: CSG_Sphere
ok, actual, status = verify_type("CSG_Sphere", "Sphere")
print(f"  {'A9':<5} {'CSG_Sphere':<20} {'Sphere':<20} {actual:<20} {status}")
check("CSG_Sphere type", ok, actual)
if ok:
    g = parsed_geoms["CSG_Sphere"]
    check("CSG_Sphere radius=1.5", abs(g.radius - 1.5) < TOL, f"{g.radius}")

# A10: CSG_Cone
ok, actual, status = verify_type("CSG_Cone", "Cone")
print(f"  {'A10':<5} {'CSG_Cone':<20} {'Cone':<20} {actual:<20} {status}")
check("CSG_Cone type", ok, actual)
if ok:
    g = parsed_geoms["CSG_Cone"]
    check("CSG_Cone radius=1.0", abs(g.radius - 1.0) < TOL, f"{g.radius}")
    check("CSG_Cone height=2.5", abs(g.height - 2.5) < TOL, f"{g.height}")

# A11: CSG_Cylinder
ok, actual, status = verify_type("CSG_Cylinder", "Cylinder")
print(f"  {'A11':<5} {'CSG_Cylinder':<20} {'Cylinder':<20} {actual:<20} {status}")
check("CSG_Cylinder type", ok, actual)
if ok:
    g = parsed_geoms["CSG_Cylinder"]
    check("CSG_Cylinder radius=0.4", abs(g.radius - 0.4) < TOL, f"{g.radius}")
    check("CSG_Cylinder height=3.0", abs(g.height - 3.0) < TOL, f"{g.height}")

# A12: Clip_Single
ok, actual, status = verify_type("Clip_Single", "ClippedExtrusion")
print(f"  {'A12':<5} {'Clip_Single':<20} {'ClippedExtrusion':<20} {actual:<20} {status}")
check("Clip_Single type", ok, actual)
if ok:
    g = parsed_geoms["Clip_Single"]
    check("Clip_Single depth=2.8", abs(g.extrusion.depth - 2.8) < TOL, f"{g.extrusion.depth}")
    check("Clip_Single 1 clip", len(g.clipping_planes) == 1, f"{len(g.clipping_planes)}")
    check("Clip_Single agree=True", g.clipping_planes[0][1] is True)

# A13: Clip_Double
ok, actual, status = verify_type("Clip_Double", "ClippedExtrusion")
print(f"  {'A13':<5} {'Clip_Double':<20} {'ClippedExtrusion':<20} {actual:<20} {status}")
check("Clip_Double type", ok, actual)
if ok:
    g = parsed_geoms["Clip_Double"]
    check("Clip_Double depth=3.0", abs(g.extrusion.depth - 3.0) < TOL, f"{g.extrusion.depth}")
    check("Clip_Double 2 clips", len(g.clipping_planes) == 2, f"{len(g.clipping_planes)}")
    check("Clip_Double clip1 agree=True", g.clipping_planes[0][1] is True)
    check("Clip_Double clip2 agree=False", g.clipping_planes[1][1] is False)

# A14: Bool_Diff
ok, actual, status = verify_type("Bool_Diff", "BooleanResult")
print(f"  {'A14':<5} {'Bool_Diff':<20} {'BooleanResult':<20} {actual:<20} {status}")
check("Bool_Diff type", ok, actual)
if ok:
    g = parsed_geoms["Bool_Diff"]
    check("Bool_Diff op=DIFFERENCE", g.operator == "DIFFERENCE", g.operator)
    check("Bool_Diff first=Extrusion", isinstance(g.first_operand, Extrusion))
    check("Bool_Diff second=Extrusion", isinstance(g.second_operand, Extrusion))

# A15: Bool_Union
ok, actual, status = verify_type("Bool_Union", "BooleanResult")
print(f"  {'A15':<5} {'Bool_Union':<20} {'BooleanResult':<20} {actual:<20} {status}")
check("Bool_Union type", ok, actual)
if ok:
    g = parsed_geoms["Bool_Union"]
    check("Bool_Union op=UNION", g.operator == "UNION", g.operator)
    check("Bool_Union first=Extrusion", isinstance(g.first_operand, Extrusion))
    check("Bool_Union second=Extrusion", isinstance(g.second_operand, Extrusion))

# A16: Bool_Inter
ok, actual, status = verify_type("Bool_Inter", "BooleanResult")
print(f"  {'A16':<5} {'Bool_Inter':<20} {'BooleanResult':<20} {actual:<20} {status}")
check("Bool_Inter type", ok, actual)
if ok:
    g = parsed_geoms["Bool_Inter"]
    check("Bool_Inter op=INTERSECTION", g.operator == "INTERSECTION", g.operator)
    check("Bool_Inter first=Extrusion", isinstance(g.first_operand, Extrusion))
    check("Bool_Inter second=Extrusion", isinstance(g.second_operand, Extrusion))

# A17: Bool_Nested
ok, actual, status = verify_type("Bool_Nested", "BooleanResult")
print(f"  {'A17':<5} {'Bool_Nested':<20} {'BooleanResult':<20} {actual:<20} {status}")
check("Bool_Nested type", ok, actual)
if ok:
    g = parsed_geoms["Bool_Nested"]
    check("Bool_Nested op=DIFFERENCE", g.operator == "DIFFERENCE", g.operator)
    check("Bool_Nested first=BooleanResult", isinstance(g.first_operand, BooleanResult))
    check("Bool_Nested second=HalfSpace", isinstance(g.second_operand, HalfSpace))
    check("Bool_Nested depth>=2", g.depth() >= 2, f"{g.depth()}")
    leaves = list(g.leaf_operands())
    check("Bool_Nested 3 leaves", len(leaves) == 3, f"{len(leaves)}")

# A18: Bool_HalfSpace
# Note: ext-halfspace DIFFERENCE may parse as ClippedExtrusion (fast path)
g = parsed_geoms.get("Bool_HalfSpace")
actual_type = type(g).__name__ if g is not None else "None"
# Accept either ClippedExtrusion (fast-path) or BooleanResult (generic)
is_clipped = isinstance(g, ClippedExtrusion)
is_bool = isinstance(g, BooleanResult)
ok = is_clipped or is_bool
status = "PASS" if ok else "FAIL"
print(f"  {'A18':<5} {'Bool_HalfSpace':<20} {'Bool/Clip':<20} {actual_type:<20} {status}")
check("Bool_HalfSpace type (BooleanResult or ClippedExtrusion)", ok, actual_type)
if is_bool:
    check("Bool_HalfSpace op=DIFFERENCE", g.operator == "DIFFERENCE", g.operator)
    check("Bool_HalfSpace second=HalfSpace", isinstance(g.second_operand, HalfSpace))
elif is_clipped:
    check("Bool_HalfSpace (as ClippedExtrusion) depth=0.3", abs(g.extrusion.depth - 0.3) < TOL, f"{g.extrusion.depth}")
    check("Bool_HalfSpace (as ClippedExtrusion) 1 clip", len(g.clipping_planes) == 1, f"{len(g.clipping_planes)}")

# A19: Mesh_Quad
ok, actual, status = verify_type("Mesh_Quad", "Mesh")
print(f"  {'A19':<5} {'Mesh_Quad':<20} {'Mesh':<20} {actual:<20} {status}")
check("Mesh_Quad type", ok, actual)
if ok:
    g = parsed_geoms["Mesh_Quad"]
    check("Mesh_Quad vertices>=8", g.number_of_vertices() >= 8, f"{g.number_of_vertices()}")
    check("Mesh_Quad faces>=6", g.number_of_faces() >= 6, f"{g.number_of_faces()}")

# A20-22: Instancing
for i in range(1, 4):
    name = f"Instance_{i}"
    ok, actual, status = verify_type(name, "Cylinder")
    print(f"  {'A'+str(19+i):<5} {name:<20} {'Cylinder':<20} {actual:<20} {status}")
    check(f"{name} type", ok, actual)
    if ok:
        g = parsed_geoms[name]
        check(f"{name} radius=0.2", abs(g.radius - 0.2) < TOL, f"{g.radius}")
        check(f"{name} height=3.5", abs(g.height - 3.5) < TOL, f"{g.height}")

print("  " + "-" * 66)
print()

# ------------------------------------------------------------------
# Entity count checks
# ------------------------------------------------------------------

print("  IFC ENTITY COUNT CHECKS:")
count_checks = [
    ("IfcExtrudedAreaSolid", entity_counts["IfcExtrudedAreaSolid"], 3, ">="),
    ("IfcRevolvedAreaSolid", entity_counts["IfcRevolvedAreaSolid"], 2, "=="),
    ("IfcSweptDiskSolid", entity_counts["IfcSweptDiskSolid"], 2, "=="),
    ("IfcCsgSolid", entity_counts["IfcCsgSolid"], 5, ">="),
    ("IfcBooleanClippingResult", entity_counts["IfcBooleanClippingResult"], 3, ">="),
    ("IfcBooleanResult", entity_counts["IfcBooleanResult"], 3, ">="),
    ("IfcPolygonalFaceSet", entity_counts["IfcPolygonalFaceSet"], 1, ">="),
    ("IfcRepresentationMap", entity_counts["IfcRepresentationMap"], 1, ">="),
    ("IfcMappedItem", entity_counts["IfcMappedItem"], 2, ">="),
]

for label, actual, expected, op in count_checks:
    if op == "==":
        ok = actual == expected
    else:
        ok = actual >= expected
    check(f"Count {label} {op} {expected}", ok, f"{actual}")
    print(f"    {label:30s} {actual:3d} {op} {expected:3d}  {'PASS' if ok else 'FAIL'}")

print()

# ------------------------------------------------------------------
# Volume and surface area verification
# ------------------------------------------------------------------

import math

print("  VOLUME & SURFACE AREA:")
print("  " + "-" * 66)
print(f"  {'ID':<5} {'Name':<20} {'Volume':<30} {'Status'}")
print("  " + "-" * 66)

# Expected volumes for each element (computed from creation parameters)
expected_volumes = {
    "Ext_Polygon": 6.0 * 0.3 * 3.0,  # 5.4
    "Ext_Circle": math.pi * 0.5**2 * 2.0,  # ~1.5708
    "Ext_Voids": (4.0 - 0.8 * 0.8) * 0.3,  # (4.0 - 0.64) * 0.3 = 1.008
    "Pipe_Solid": math.pi * 0.15**2 * Pipe(directrix=Polyline([Point(0, 0, 0), Point(2, 0, 0), Point(2, 3, 1)]), radius=0.15).directrix.length,
    "Pipe_Hollow": math.pi * (0.25**2 - 0.10**2) * Pipe(directrix=Polyline([Point(0, 0, 0), Point(0, 4, 0), Point(0, 4, 2)]), radius=0.25).directrix.length,
    "CSG_Box": 1.0 * 2.0 * 3.0,  # 6.0
    "CSG_Sphere": 4.0 / 3.0 * math.pi * 1.5**3,  # ~14.137
    "CSG_Cone": math.pi * 1.0**2 * 2.5 / 3,  # ~2.618
    "CSG_Cylinder": math.pi * 0.4**2 * 3.0,  # ~1.508
    "Mesh_Quad": None,  # polyhedron — just check > 0
}

# Elements where volume is checked via element-level fallback (visual_geometry)
FALLBACK_NAMES = ["Clip_Single", "Clip_Double", "Bool_Diff", "Bool_Union", "Bool_Inter", "Bool_Nested", "Bool_HalfSpace"]
# Instanced elements
INSTANCE_NAMES = ["Instance_1", "Instance_2", "Instance_3"]
INSTANCE_VOL = math.pi * 0.2**2 * 3.5

vol_id = 0
for name, expected in expected_volumes.items():
    vol_id += 1
    elem = parsed_elems.get(name)
    if elem is None:
        check(f"{name} volume", False, "element missing")
        print(f"  {'V'+str(vol_id):<5} {name:<20} {'MISSING':<30} FAIL")
        continue
    v = elem.volume
    if expected is not None:
        ok = v is not None and v > 0 and abs(v - expected) / expected < 0.01
        check(f"{name} volume", ok, f"{v:.4f} vs {expected:.4f}" if v else "None")
        status = "PASS" if ok else "FAIL"
        print(f"  {'V'+str(vol_id):<5} {name:<20} {f'{v:.4f} (exp {expected:.4f})':<30} {status}")
    else:
        ok = v is not None and v > 0
        check(f"{name} volume > 0", ok, f"{v}")
        status = "PASS" if ok else "FAIL"
        print(f"  {'V'+str(vol_id):<5} {name:<20} {f'{v:.4f}':<30} {status}" if v else f"  {'V'+str(vol_id):<5} {name:<20} {'None':<30} {status}")

# ClippedExtrusion and BooleanResult: check element-level volume > 0 (via visual_geometry)
for name in FALLBACK_NAMES:
    vol_id += 1
    elem = parsed_elems.get(name)
    if elem is None:
        check(f"{name} volume", False, "element missing")
        print(f"  {'V'+str(vol_id):<5} {name:<20} {'MISSING':<30} FAIL")
        continue
    v = elem.volume
    ok = v is not None and v > 0
    check(f"{name} elem.volume > 0", ok, f"{v:.4f}" if v else "None")
    status = "PASS" if ok else "FAIL"
    src = "parametric" if (parsed_geoms.get(name) is not None and hasattr(parsed_geoms[name], 'volume') and callable(getattr(parsed_geoms[name], 'volume', None)) and parsed_geoms[name].volume() is not None) else "visual_geom"
    print(f"  {'V'+str(vol_id):<5} {name:<20} {f'{v:.4f} ({src})':<30} {status}" if v else f"  {'V'+str(vol_id):<5} {name:<20} {'None':<30} {status}")

# Instanced elements
for name in INSTANCE_NAMES:
    vol_id += 1
    elem = parsed_elems.get(name)
    if elem is None:
        check(f"{name} volume", False, "element missing")
        print(f"  {'V'+str(vol_id):<5} {name:<20} {'MISSING':<30} FAIL")
        continue
    v = elem.volume
    ok = v is not None and v > 0 and abs(v - INSTANCE_VOL) / INSTANCE_VOL < 0.01
    check(f"{name} volume", ok, f"{v:.4f} vs {INSTANCE_VOL:.4f}" if v else "None")
    status = "PASS" if ok else "FAIL"
    print(f"  {'V'+str(vol_id):<5} {name:<20} {f'{v:.4f} (exp {INSTANCE_VOL:.4f})':<30} {status}")

# Surface area spot-checks
print()
print("  SURFACE AREA SPOT-CHECKS:")
sa_checks = {
    "Ext_Polygon": 2 * (6.0 * 0.3) + 2 * (6.0 + 0.3) * 3.0,  # 41.4
    "CSG_Box": 2 * (1.0 * 2.0 + 2.0 * 3.0 + 1.0 * 3.0),  # 22.0
    "CSG_Sphere": 4 * math.pi * 1.5**2,  # ~28.274
}
for name, expected_sa in sa_checks.items():
    elem = parsed_elems.get(name)
    if elem is None:
        check(f"{name} surface_area", False, "element missing")
        continue
    sa = elem.surface_area
    ok = sa is not None and sa > 0 and abs(sa - expected_sa) / expected_sa < 0.01
    check(f"{name} surface_area", ok, f"{sa:.4f} vs {expected_sa:.4f}" if sa else "None")
    status = "PASS" if ok else "FAIL"
    print(f"    {name:<20} SA={sa:.4f} (exp {expected_sa:.4f})  {status}" if sa else f"    {name:<20} SA=None  {status}")

# All elements should have positive surface area via element-level API
all_sa_ok = True
sa_fail_names = []
for name, elem in parsed_elems.items():
    sa = elem.surface_area
    if sa is None or sa <= 0:
        all_sa_ok = False
        sa_fail_names.append(name)
check("All elements: surface_area > 0", all_sa_ok, ", ".join(sa_fail_names) if sa_fail_names else "")

print("  " + "-" * 66)
print()

# ==================================================================
# SUMMARY
# ==================================================================

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
    print("SUCCESS: All generated round-trip tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
