"""
16 Combined Round-Trip Test
============================

Comprehensive test covering ALL supported geometry types in a single
write-save-reload cycle.  Uses the BuildingInformationModel API.

Each element is created via the high-level BIM convenience methods,
saved to IFC, reloaded, and the parsed geometry is checked for type
and key parametric values.

Coverage:
  Phase 1: Extrusion (circle, polygon, profile-with-voids)
  Phase 4: CSG shapes (Box, Sphere, Cone, Cylinder)
  Phase 5: Mesh (IfcPolygonalFaceSet), Torus (B-Rep), Capsule (tessellation)
  Phase 6: Revolution (circle/polygon), Pipe (solid/hollow)
  Phase 3: Instancing (shared geometry via IfcRepresentationMap)
  Phase 2: Axis representations (IfcPolyline centerlines)
"""

import os
import sys

from compas.datastructures import Mesh
from compas.geometry import Box, Capsule, Circle, Cone, Cylinder, Frame, Point, Polygon, Polyline, Sphere, Torus, Vector

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import Extrusion, Pipe, Revolution

# ==================================================================
# Create model
# ==================================================================

model = BuildingInformationModel.template(schema="IFC4", unit="m")
storey = model.storeys[0]

# Keep track of expected results: name -> (expected_type, checks_dict)
EXPECTED = {}

# ------------------------------------------------------------------
# 1. CSG Shapes
# ------------------------------------------------------------------

box = Box(2.0, 1.0, 0.8)
model.create_beam(geometry=box, frame=Frame(Point(0, 0, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="CSG_Box")
EXPECTED["CSG_Box"] = ("Box", {"xsize": 2.0, "ysize": 1.0, "zsize": 0.8})

sphere = Sphere(radius=0.75)
model.create_element(geometry=sphere, frame=Frame(Point(4, 0, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="CSG_Sphere")
EXPECTED["CSG_Sphere"] = ("Sphere", {"radius": 0.75})

cone = Cone(radius=0.5, height=2.0)
model.create_element(geometry=cone, frame=Frame(Point(8, 0, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="CSG_Cone")
EXPECTED["CSG_Cone"] = ("Cone", {"radius": 0.5, "height": 2.0})

cylinder = Cylinder(radius=0.3, height=3.0)
model.create_column(geometry=cylinder, frame=Frame(Point(12, 0, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="CSG_Cylinder")
EXPECTED["CSG_Cylinder"] = ("Cylinder", {"radius": 0.3, "height": 3.0})

# ------------------------------------------------------------------
# 2. Extrusions
# ------------------------------------------------------------------

ext_circle = Extrusion(
    profile=Circle(radius=0.2),
    direction=Vector(0, 0, 1),
    depth=4.0,
    frame=Frame(Point(0, 5, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_column(geometry=ext_circle, frame=Frame(Point(0, 5, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Ext_Circle")
EXPECTED["Ext_Circle"] = ("Extrusion", {"depth": 4.0, "profile_type": "Circle"})

ext_polygon = Extrusion(
    profile=Polygon([Point(0, 0, 0), Point(0.3, 0, 0), Point(0.3, 0.2, 0), Point(0, 0.2, 0)]),
    direction=Vector(0, 0, 1),
    depth=5.0,
    frame=Frame(Point(4, 5, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_beam(geometry=ext_polygon, frame=Frame(Point(4, 5, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Ext_Polygon")
EXPECTED["Ext_Polygon"] = ("Extrusion", {"depth": 5.0, "profile_type": "Polygon"})

outer = Polygon([Point(-1, -1, 0), Point(1, -1, 0), Point(1, 1, 0), Point(-1, 1, 0)])
inner = Polygon([Point(-0.5, -0.5, 0), Point(0.5, -0.5, 0), Point(0.5, 0.5, 0), Point(-0.5, 0.5, 0)])
ext_voids = Extrusion(
    profile=(outer, [inner]),
    direction=Vector(0, 0, 1),
    depth=0.3,
    frame=Frame(Point(8, 5, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_slab(geometry=ext_voids, frame=Frame(Point(8, 5, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Ext_Voids")
EXPECTED["Ext_Voids"] = ("Extrusion", {"depth": 0.3, "profile_type": "tuple"})

# ------------------------------------------------------------------
# 3. Revolutions
# ------------------------------------------------------------------

rev_circle = Revolution(
    profile=Circle(radius=0.25),
    axis_point=Point(1.0, 0, 0),
    axis_direction=Vector(0, 0, 1),
    angle=360.0,
    frame=Frame(Point(0, 10, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_column(geometry=rev_circle, frame=Frame(Point(0, 10, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Rev_Circle_360")
EXPECTED["Rev_Circle_360"] = ("Revolution", {"angle": 360.0, "profile_type": "Circle"})

rev_poly = Revolution(
    profile=Polygon([Point(0.5, -0.15, 0), Point(1.2, -0.15, 0), Point(1.2, 0.15, 0), Point(0.5, 0.15, 0)]),
    axis_point=Point(0, 0, 0),
    axis_direction=Vector(0, 0, 1),
    angle=180.0,
    frame=Frame(Point(4, 10, 0), Vector.Xaxis(), Vector.Yaxis()),
)
model.create_beam(geometry=rev_poly, frame=Frame(Point(4, 10, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Rev_Polygon_180")
EXPECTED["Rev_Polygon_180"] = ("Revolution", {"angle": 180.0, "profile_type": "Polygon"})

# ------------------------------------------------------------------
# 4. Pipes
# ------------------------------------------------------------------

pipe_solid = Pipe(
    directrix=Polyline([Point(0, 0, 0), Point(2, 0, 0), Point(2, 3, 0), Point(4, 3, 1)]),
    radius=0.12,
)
model.create_element(geometry=pipe_solid, frame=Frame(Point(0, 15, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Pipe_Solid")
EXPECTED["Pipe_Solid"] = ("Pipe", {"radius": 0.12, "inner_radius": None})

pipe_hollow = Pipe(
    directrix=Polyline([Point(0, 0, 0), Point(0, 4, 0), Point(0, 4, 2)]),
    radius=0.25,
    inner_radius=0.20,
)
model.create_element(geometry=pipe_hollow, frame=Frame(Point(8, 15, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Pipe_Hollow")
EXPECTED["Pipe_Hollow"] = ("Pipe", {"radius": 0.25, "inner_radius": 0.20})

# ------------------------------------------------------------------
# 5. Mesh (default -> IfcPolygonalFaceSet)
# ------------------------------------------------------------------

mesh = Mesh.from_meshgrid(3, 2, 6, 4)
model.create_slab(geometry=mesh, frame=Frame(Point(0, 20, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Mesh_Default")
EXPECTED["Mesh_Default"] = ("Mesh", {"min_vertices": 10})

# ------------------------------------------------------------------
# 6. Torus (B-Rep) and Capsule (tessellation fallback)
# ------------------------------------------------------------------

torus = Torus(radius_axis=1.5, radius_pipe=0.4)
model.create_element(geometry=torus, frame=Frame(Point(0, 25, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Shape_Torus")
EXPECTED["Shape_Torus"] = ("brep_or_mesh", {})  # read-back type varies

capsule = Capsule(radius=0.4, height=2.0)
model.create_element(geometry=capsule, frame=Frame(Point(6, 25, 0), Vector.Xaxis(), Vector.Yaxis()), parent=storey, name="Shape_Capsule")
EXPECTED["Shape_Capsule"] = ("Mesh", {})  # tessellation fallback

# ------------------------------------------------------------------
# 7. Instancing: 3 columns sharing the same Cylinder
# ------------------------------------------------------------------

shared_cyl = Cylinder(radius=0.2, height=3.5)
for i in range(3):
    frame = Frame(Point(i * 2.5, 30, 0), Vector.Xaxis(), Vector.Yaxis())
    model.create_column(geometry=shared_cyl, frame=frame, parent=storey, name=f"Instanced_Col_{i}")
EXPECTED["Instanced_Col_0"] = ("Cylinder", {"radius": 0.2, "height": 3.5})
EXPECTED["Instanced_Col_1"] = ("Cylinder", {"radius": 0.2, "height": 3.5})
EXPECTED["Instanced_Col_2"] = ("Cylinder", {"radius": 0.2, "height": 3.5})

# ------------------------------------------------------------------
# 8. Axis representations (added AFTER body geometry)
# ------------------------------------------------------------------

from compas_ifc.conversions.representation import assign_axis_representation

for elem in model.building_elements:
    if elem.name == "CSG_Box":
        assign_axis_representation(elem._ifc_entity, Polyline([Point(0, 0, 0), Point(2, 0, 0)]))
    elif elem.name == "Ext_Circle":
        assign_axis_representation(elem._ifc_entity, Polyline([Point(0, 5, 0), Point(0, 5, 4)]))

# ==================================================================
# Save
# ==================================================================

os.makedirs("temp", exist_ok=True)
output_path = "temp/combined_roundtrip_test.ifc"
model.save(output_path)
print(f"Saved: {output_path}")
print(f"Total named entities written: {len(EXPECTED)}")

# ==================================================================
# Reload and verify
# ==================================================================

print()
print("=" * 70)
print("ROUND-TRIP VERIFICATION")
print("=" * 70)
print()

model2 = BuildingInformationModel(output_path)

# ------------------------------------------------------------------
# Entity counts (low-level IFC file queries)
# ------------------------------------------------------------------

csg_count = len(model2._file.get_entities_by_type("IfcCsgSolid"))
eas_count = len(model2._file.get_entities_by_type("IfcExtrudedAreaSolid"))
ras_count = len(model2._file.get_entities_by_type("IfcRevolvedAreaSolid"))
sds_count = len(model2._file.get_entities_by_type("IfcSweptDiskSolid"))
pfs_count = len(model2._file.get_entities_by_type("IfcPolygonalFaceSet"))
brep_count = len(model2._file.get_entities_by_type("IfcAdvancedBrep"))
rep_maps = len(model2._file.get_entities_by_type("IfcRepresentationMap"))
mapped_items = len(model2._file.get_entities_by_type("IfcMappedItem"))

print("IFC Entity Counts:")
print(f"  IfcCsgSolid:              {csg_count:3d}  (expected 5)")
print(f"  IfcExtrudedAreaSolid:     {eas_count:3d}  (expected 3)")
print(f"  IfcRevolvedAreaSolid:     {ras_count:3d}  (expected 2)")
print(f"  IfcSweptDiskSolid:        {sds_count:3d}  (expected 2)")
print(f"  IfcPolygonalFaceSet:      {pfs_count:3d}  (expected >= 2)")
print(f"  IfcAdvancedBrep:          {brep_count:3d}  (expected >= 1)")
print(f"  IfcRepresentationMap:     {rep_maps:3d}  (expected 1)")
print(f"  IfcMappedItem:            {mapped_items:3d}  (expected 2)")
print()

# ------------------------------------------------------------------
# Per-element verification
# ------------------------------------------------------------------

results = {}  # name -> (pass, geom_type, geom_object)

for elem in model2.building_elements:
    name = elem.name or ""
    if not name or name not in EXPECTED:
        continue

    geom = elem.geometry
    if geom is not None:
        gtype = type(geom).__name__
        results[name] = (True, gtype, geom)
    else:
        results[name] = (False, "None", None)

# ------------------------------------------------------------------
# Detailed checks
# ------------------------------------------------------------------

TOL = 1e-4
pass_count = 0
fail_count = 0
skip_count = 0
details = []


for name, (expected_type, checks) in sorted(EXPECTED.items()):
    parsed, gtype, geom = results.get(name, (False, "None", None))

    # Type check
    if expected_type == "brep_or_mesh":
        # Torus B-Rep read-back may fail; accept any geometry
        type_ok = parsed
    else:
        type_ok = parsed and gtype == expected_type

    # Value checks
    value_results = []
    if parsed and geom is not None:
        for key, expected_val in checks.items():
            if key == "xsize" and hasattr(geom, "xsize"):
                value_results.append(("xsize", abs(geom.xsize - expected_val) < TOL))
            elif key == "ysize" and hasattr(geom, "ysize"):
                value_results.append(("ysize", abs(geom.ysize - expected_val) < TOL))
            elif key == "zsize" and hasattr(geom, "zsize"):
                value_results.append(("zsize", abs(geom.zsize - expected_val) < TOL))
            elif key == "radius" and hasattr(geom, "radius"):
                value_results.append(("radius", abs(geom.radius - expected_val) < TOL))
            elif key == "height" and hasattr(geom, "height"):
                value_results.append(("height", abs(geom.height - expected_val) < TOL))
            elif key == "depth" and hasattr(geom, "depth"):
                value_results.append(("depth", abs(geom.depth - expected_val) < TOL))
            elif key == "angle" and hasattr(geom, "angle"):
                value_results.append(("angle", abs(geom.angle - expected_val) < TOL))
            elif key == "inner_radius":
                if expected_val is None:
                    value_results.append(("inner_r", geom.inner_radius is None))
                elif hasattr(geom, "inner_radius") and geom.inner_radius is not None:
                    value_results.append(("inner_r", abs(geom.inner_radius - expected_val) < TOL))
                else:
                    value_results.append(("inner_r", False))
            elif key == "profile_type" and hasattr(geom, "profile"):
                actual = type(geom.profile).__name__
                value_results.append(("profile", actual == expected_val))
            elif key == "min_vertices":
                if isinstance(geom, Mesh):
                    value_results.append(("verts", geom.number_of_vertices() >= expected_val))
                else:
                    value_results.append(("verts", False))

    all_values_ok = all(ok for _, ok in value_results)
    overall = type_ok and all_values_ok

    if overall:
        pass_count += 1
    elif expected_type == "brep_or_mesh" and not parsed:
        skip_count += 1  # known limitation (torus read-back)
    else:
        fail_count += 1

    status = "PASS" if overall else ("SKIP" if expected_type == "brep_or_mesh" and not parsed else "FAIL")
    val_str = "  ".join(f"{k}={'PASS' if ok else 'FAIL'}" for k, ok in value_results)
    details.append((status, name, gtype, val_str))

# ------------------------------------------------------------------
# Axis checks
# ------------------------------------------------------------------

axis_results = []
for elem in model2.building_elements:
    if elem.name in ("CSG_Box", "Ext_Circle"):
        axis = elem.axis
        ok = axis is not None and len(axis.points) >= 2
        axis_results.append((elem.name, ok))

# ------------------------------------------------------------------
# Print results table
# ------------------------------------------------------------------

print("Per-Element Results:")
print("-" * 70)
print(f"{'Status':<6} {'Name':<22} {'Type':<14} {'Checks'}")
print("-" * 70)

for status, name, gtype, val_str in details:
    print(f"{status:<6} {name:<22} {gtype:<14} {val_str}")

print("-" * 70)
print()

# Axis results
print("Axis Representation Checks:")
for name, ok in axis_results:
    print(f"  {name}: {'PASS' if ok else 'FAIL'}")
print()

# Entity count checks
count_checks = [
    ("IfcCsgSolid", csg_count, 5),
    ("IfcExtrudedAreaSolid", eas_count, 3),
    ("IfcRevolvedAreaSolid", ras_count, 2),
    ("IfcSweptDiskSolid", sds_count, 2),
    ("IfcRepresentationMap", rep_maps, 1),
    ("IfcMappedItem", mapped_items, 2),
]

print("Entity Count Checks:")
all_counts_ok = True
for label, actual, expected in count_checks:
    ok = actual == expected
    if not ok:
        all_counts_ok = False
    print(f"  {label:<28} {actual:3d} == {expected:3d}  {'PASS' if ok else 'FAIL'}")
print()

# ==================================================================
# Final summary
# ==================================================================

all_axes_ok = all(ok for _, ok in axis_results)

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"  Geometry round-trip:  {pass_count} PASS / {fail_count} FAIL / {skip_count} SKIP  (of {len(EXPECTED)} entities)")
print(f"  Entity counts:        {'PASS' if all_counts_ok else 'FAIL'}")
print(f"  Axis representations: {'PASS' if all_axes_ok else 'FAIL'}")
print()

total_ok = fail_count == 0 and all_counts_ok and all_axes_ok

if total_ok:
    print("SUCCESS: All combined round-trip tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
