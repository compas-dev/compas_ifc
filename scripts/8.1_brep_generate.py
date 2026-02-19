"""
Generate STEP files for comprehensive B-Rep to IFC conversion testing.

Surface types (IfcAdvancedFace valid surfaces):
  - Plane             (box faces)
  - CylindricalSurface (cylinder lateral)
  - SphericalSurface   (full sphere, hemisphere)
  - ToroidalSurface    (full torus, partial torus)
  - Cone              (no IfcConicalSurface in IFC4/4X3 -> NURBS fallback)
  - SurfaceOfRevolution (revolved profile -> NURBS fallback)
  - SurfaceOfLinearExtrusion (extruded profile -> NURBS fallback)
  - BSplineSurface     (free-form NURBS solid)

Edge curve types:
  - Line              (box edges, cylinder seams)
  - Circle            (cylinder caps, sphere meridians, torus)
  - Ellipse           (ellipsoid boundary)
  - BSplineCurve      (NURBS solid edges, swept edges)

Topology:
  - Single solid         -> IfcAdvancedBrep
  - Solid with voids     -> IfcAdvancedBrepWithVoids
  - Multi-solid compound -> multiple IfcAdvancedBrep

Edge cases:
  - Degenerate edges (sphere poles, cone apex)
  - Seam edges (cylinder, torus wrapping)
  - Periodic surfaces (sphere, torus, cylinder)
  - Mixed surface types in one solid (fillet on box)
  - Compound of two separate solids
  - Non-planar face on a box with chamfered edge
  - Very small geometry (tolerance test)
  - Very large geometry (scale test)

Output directory: temp/brep_conversion_tests/

Run with:
    python scripts/8.1_brep_generate.py
"""

import os
import sys
import math

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet, BRepFilletAPI_MakeChamfer
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe, BRepOffsetAPI_MakeThickSolid
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeHalfSpace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeTorus
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeWedge
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.Geom import Geom_BSplineSurface
from OCC.Core.GeomFill import GeomFill_BSplineCurves, GeomFill_StretchStyle
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCC.Core.TColgp import TColgp_Array2OfPnt
from OCC.Core.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal, TColStd_Array2OfReal
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.gp import (
    gp_Ax1, gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec, gp_OX, gp_OZ,
)


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(REPO_ROOT, "temp", "brep_conversion_tests")
os.makedirs(OUT_DIR, exist_ok=True)


def save_step(shape, name):
    path = os.path.join(OUT_DIR, f"{name}.stp")
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    status = writer.Write(path)
    tag = "[OK]" if status == IFSelect_RetDone else "[FAIL]"
    print(f"  {tag} {name}.stp")
    return path


# ===================================================================
# Helper: NURBS pillow surface (free-form)
# ===================================================================

def make_nurbs_pillow():
    """Create a solid from a NURBS pillow surface lofted between two B-Spline curves."""
    from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeSolid
    from OCC.Core.TColgp import TColgp_Array1OfPnt

    pts1 = TColgp_Array1OfPnt(1, 5)
    pts1.SetValue(1, gp_Pnt(0, 0, 0))
    pts1.SetValue(2, gp_Pnt(1, 0, 0.5))
    pts1.SetValue(3, gp_Pnt(2, 0, 0.3))
    pts1.SetValue(4, gp_Pnt(3, 0, 0.7))
    pts1.SetValue(5, gp_Pnt(4, 0, 0))

    pts2 = TColgp_Array1OfPnt(1, 5)
    pts2.SetValue(1, gp_Pnt(0, 4, 0))
    pts2.SetValue(2, gp_Pnt(1, 4, 0.8))
    pts2.SetValue(3, gp_Pnt(2, 4, 0.2))
    pts2.SetValue(4, gp_Pnt(3, 4, 0.9))
    pts2.SetValue(5, gp_Pnt(4, 4, 0))

    curve1 = GeomAPI_PointsToBSpline(pts1).Curve()
    curve2 = GeomAPI_PointsToBSpline(pts2).Curve()

    fill = GeomFill_BSplineCurves(curve1, curve2, GeomFill_StretchStyle)
    surface = fill.Surface()

    face = BRepBuilderAPI_MakeFace(surface, 1e-6).Face()

    # Extrude the surface downward to make a solid
    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
    solid = BRepPrimAPI_MakePrism(face, gp_Vec(0, 0, -1)).Shape()
    return solid


# ===================================================================
# Generate test geometries
# ===================================================================

print("=" * 60)
print("Generating STEP files for B-Rep conversion tests")
print(f"Output: {OUT_DIR}")
print("=" * 60)

# ------------------------------------------------------------------
# 1. SURFACE TYPES
# ------------------------------------------------------------------

print("\n--- Surface types ---")

# 1a. Plane (box)
box = BRepPrimAPI_MakeBox(2.0, 3.0, 1.0).Shape()
save_step(box, "plane_box")

# 1b. Cube (unit cube, simplest plane case)
cube = BRepPrimAPI_MakeBox(1.0, 1.0, 1.0).Shape()
save_step(cube, "cube")

# 1c. Cylindrical surface (cylinder with plane caps)
cyl = BRepPrimAPI_MakeCylinder(1.0, 3.0).Shape()
save_step(cyl, "cylinder")

# 1d. Spherical surface (full sphere — degenerate edges at poles)
sphere = BRepPrimAPI_MakeSphere(1.5).Shape()
save_step(sphere, "sphere")

# 1e. Hemisphere (partial sphere — plane cap + spherical surface)
hemisphere = BRepPrimAPI_MakeSphere(1.5, math.pi / 2).Shape()
save_step(hemisphere, "hemisphere")

# 1f. Toroidal surface (full torus — periodic in both U and V)
torus = BRepPrimAPI_MakeTorus(2.0, 0.6).Shape()
save_step(torus, "torus")

# 1g. Partial torus (quarter torus — toroidal + plane caps)
partial_torus = BRepPrimAPI_MakeTorus(2.0, 0.6, 0, math.pi / 2).Shape()
save_step(partial_torus, "torus_partial")

# 1h. Cone (conical surface -> NURBS fallback, degenerate edge at apex)
cone = BRepPrimAPI_MakeCone(1.0, 0.0, 2.0).Shape()
save_step(cone, "cone")

# 1i. Truncated cone / frustum (conical -> NURBS, no degenerate apex)
frustum = BRepPrimAPI_MakeCone(1.5, 0.5, 2.0).Shape()
save_step(frustum, "cone_truncated")

# 1j. Wedge (tapered box — has angled planar faces)
wedge = BRepPrimAPI_MakeWedge(2.0, 1.5, 3.0, 0.5).Shape()
save_step(wedge, "wedge")

# ------------------------------------------------------------------
# 2. EDGE TYPES
# ------------------------------------------------------------------

print("\n--- Edge types ---")

# 2a. Ellipse edges (ellipsoid — sphere stretched in Z)
# OCC doesn't have MakeEllipsoid directly; scale a sphere non-uniformly
sphere_for_ellipsoid = BRepPrimAPI_MakeSphere(1.0).Shape()
trsf = gp_Trsf()
trsf.SetValues(
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.7, 0.0, 0.0,
    0.0, 0.0, 1.5, 0.0,
)
ellipsoid = BRepBuilderAPI_Transform(sphere_for_ellipsoid, trsf, True).Shape()
save_step(ellipsoid, "ellipsoid")

# 2b. BSpline curve edges (NURBS pillow solid)
try:
    pillow = make_nurbs_pillow()
    save_step(pillow, "nurbs_pillow")
except Exception as e:
    print(f"  [SKIP] nurbs_pillow: {e}")

# ------------------------------------------------------------------
# 3. MIXED SURFACE TYPES (single solid with multiple surface types)
# ------------------------------------------------------------------

print("\n--- Mixed surfaces ---")

# 3a. Box with filleted edges (plane + cylindrical faces + circle/line edges)
box_for_fillet = BRepPrimAPI_MakeBox(3.0, 2.0, 1.5).Shape()
fillet = BRepFilletAPI_MakeFillet(box_for_fillet)
explorer = TopExp_Explorer(box_for_fillet, TopAbs_EDGE)
edge_count = 0
while explorer.More():
    fillet.Add(0.3, explorer.Current())
    edge_count += 1
    explorer.Next()
    if edge_count >= 4:
        break
try:
    fillet.Build()
    filleted_box = fillet.Shape()
    save_step(filleted_box, "box_filleted")
except Exception as e:
    print(f"  [SKIP] box_filleted: {e}")

# 3b. Cylinder with spherical end caps (cylinder + sphere boolean fuse)
cyl2 = BRepPrimAPI_MakeCylinder(1.0, 2.0).Shape()
cap1 = BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, 0), 1.0).Shape()
cap2 = BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, 2), 1.0).Shape()
try:
    fuse1 = BRepAlgoAPI_Fuse(cyl2, cap1)
    fuse1.Build()
    fuse2 = BRepAlgoAPI_Fuse(fuse1.Shape(), cap2)
    fuse2.Build()
    capsule = fuse2.Shape()
    save_step(capsule, "capsule")
except Exception as e:
    print(f"  [SKIP] capsule: {e}")

# ------------------------------------------------------------------
# 4. TOPOLOGY CASES
# ------------------------------------------------------------------

print("\n--- Topology cases ---")

# 4a. Box with spherical void (IfcAdvancedBrepWithVoids)
big_box = BRepPrimAPI_MakeBox(4.0, 4.0, 4.0).Shape()
inner_sphere = BRepPrimAPI_MakeSphere(1.2).Shape()
trsf2 = gp_Trsf()
trsf2.SetTranslation(gp_Vec(2.0, 2.0, 2.0))
inner_moved = BRepBuilderAPI_Transform(inner_sphere, trsf2).Shape()
cut = BRepAlgoAPI_Cut(big_box, inner_moved)
cut.Build()
hollow_box = cut.Shape()
save_step(hollow_box, "hollow_box")

# 4b. Box with cylindrical hole (void with cylindrical surface)
box_for_hole = BRepPrimAPI_MakeBox(3.0, 3.0, 2.0).Shape()
hole_cyl = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(1.5, 1.5, -0.1), gp_Dir(0, 0, 1)), 0.5, 2.2).Shape()
cut2 = BRepAlgoAPI_Cut(box_for_hole, hole_cyl)
cut2.Build()
box_with_hole = cut2.Shape()
save_step(box_with_hole, "box_with_hole")

# 4c. Compound of two separate solids (multi-solid)
compound = TopoDS_Compound()
builder = BRep_Builder()
builder.MakeCompound(compound)
box_a = BRepPrimAPI_MakeBox(1.0, 1.0, 1.0).Shape()
trsf3 = gp_Trsf()
trsf3.SetTranslation(gp_Vec(3.0, 0.0, 0.0))
box_b = BRepBuilderAPI_Transform(BRepPrimAPI_MakeBox(1.0, 1.0, 1.0).Shape(), trsf3).Shape()
builder.Add(compound, box_a)
builder.Add(compound, box_b)
save_step(compound, "compound_two_boxes")

# 4d. Compound of different shapes (box + cylinder)
compound2 = TopoDS_Compound()
builder.MakeCompound(compound2)
builder.Add(compound2, BRepPrimAPI_MakeBox(1.5, 1.5, 1.5).Shape())
trsf4 = gp_Trsf()
trsf4.SetTranslation(gp_Vec(4.0, 0.0, 0.0))
cyl_moved = BRepBuilderAPI_Transform(BRepPrimAPI_MakeCylinder(0.5, 2.0).Shape(), trsf4).Shape()
builder.Add(compound2, cyl_moved)
save_step(compound2, "compound_box_cylinder")

# ------------------------------------------------------------------
# 5. EDGE CASES
# ------------------------------------------------------------------

print("\n--- Edge cases ---")

# 5a. Very small geometry (tolerance test)
tiny_box = BRepPrimAPI_MakeBox(0.001, 0.001, 0.001).Shape()
save_step(tiny_box, "tiny_box")

# 5b. Very large geometry (scale test)
big = BRepPrimAPI_MakeBox(1000.0, 1000.0, 1000.0).Shape()
save_step(big, "large_box")

# 5c. Thin plate (high aspect ratio)
thin = BRepPrimAPI_MakeBox(10.0, 10.0, 0.01).Shape()
save_step(thin, "thin_plate")

# 5d. Box with chamfered edge (non-planar geometry from chamfer)
box_for_chamfer = BRepPrimAPI_MakeBox(2.0, 2.0, 2.0).Shape()
chamfer = BRepFilletAPI_MakeChamfer(box_for_chamfer)
explorer2 = TopExp_Explorer(box_for_chamfer, TopAbs_EDGE)
if explorer2.More():
    chamfer.Add(0.3, explorer2.Current())
try:
    chamfer.Build()
    chamfered_box = chamfer.Shape()
    save_step(chamfered_box, "box_chamfered")
except Exception as e:
    print(f"  [SKIP] box_chamfered: {e}")

# 5e. Revolved solid (surface of revolution -> NURBS fallback)
# Revolve an L-shaped profile around Z axis
try:
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
    e1 = BRepBuilderAPI_MakeEdge(gp_Pnt(1, 0, 0), gp_Pnt(2, 0, 0)).Edge()
    e2 = BRepBuilderAPI_MakeEdge(gp_Pnt(2, 0, 0), gp_Pnt(2, 0, 1)).Edge()
    e3 = BRepBuilderAPI_MakeEdge(gp_Pnt(2, 0, 1), gp_Pnt(1.5, 0, 1)).Edge()
    e4 = BRepBuilderAPI_MakeEdge(gp_Pnt(1.5, 0, 1), gp_Pnt(1.5, 0, 0.5)).Edge()
    e5 = BRepBuilderAPI_MakeEdge(gp_Pnt(1.5, 0, 0.5), gp_Pnt(1, 0, 0.5)).Edge()
    e6 = BRepBuilderAPI_MakeEdge(gp_Pnt(1, 0, 0.5), gp_Pnt(1, 0, 0)).Edge()
    wire = BRepBuilderAPI_MakeWire(e1, e2, e3, e4)
    wire.Add(e5)
    wire.Add(e6)
    face = BRepBuilderAPI_MakeFace(wire.Wire()).Face()
    revolved = BRepPrimAPI_MakeRevol(face, gp_OZ(), 2 * math.pi).Shape()
    save_step(revolved, "revolved_l_profile")
except Exception as e:
    print(f"  [SKIP] revolved_l_profile: {e}")

# 5f. Extruded arc profile (linear extrusion -> NURBS fallback)
try:
    arc = GC_MakeArcOfCircle(gp_Pnt(0, 0, 0), gp_Pnt(1, 1, 0), gp_Pnt(2, 0, 0)).Value()
    seg = GC_MakeSegment(gp_Pnt(2, 0, 0), gp_Pnt(0, 0, 0)).Value()
    e_arc = BRepBuilderAPI_MakeEdge(arc).Edge()
    e_seg = BRepBuilderAPI_MakeEdge(seg).Edge()
    wire = BRepBuilderAPI_MakeWire(e_arc, e_seg).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    extruded = BRepPrimAPI_MakePrism(face, gp_Vec(0, 0, 3)).Shape()
    save_step(extruded, "extruded_arc")
except Exception as e:
    print(f"  [SKIP] extruded_arc: {e}")

# 5g. Pipe sweep (circular section along arc path -> mixed surfaces)
try:
    from OCC.Core.gp import gp_Circ, gp_Ax2
    # Path: arc
    path_arc = GC_MakeArcOfCircle(gp_Pnt(0, 0, 0), gp_Pnt(3, 3, 0), gp_Pnt(6, 0, 0)).Value()
    path_edge = BRepBuilderAPI_MakeEdge(path_arc).Edge()
    path_wire = BRepBuilderAPI_MakeWire(path_edge).Wire()
    # Section: small circle perpendicular to path start
    circ = gp_Circ(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), 0.3)
    section_edge = BRepBuilderAPI_MakeEdge(circ).Edge()
    section_wire = BRepBuilderAPI_MakeWire(section_edge).Wire()
    pipe = BRepOffsetAPI_MakePipe(path_wire, section_wire)
    pipe.Build()
    pipe_shape = pipe.Shape()
    save_step(pipe_shape, "pipe_sweep")
except Exception as e:
    print(f"  [SKIP] pipe_sweep: {e}")

# 5h. Thick shell (hollowed box -> IfcAdvancedBrepWithVoids)
try:
    from OCC.Core.TopTools import TopTools_ListOfShape
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.TopAbs import TopAbs_FACE
    from OCC.Core.TopoDS import topods

    box_for_shell = BRepPrimAPI_MakeBox(3.0, 3.0, 3.0).Shape()
    # Find the top face (highest Z) to open
    explorer3 = TopExp_Explorer(box_for_shell, TopAbs_FACE)
    faces_to_remove = TopTools_ListOfShape()
    # Just remove the first face to create an open shell -> thick solid
    if explorer3.More():
        faces_to_remove.Append(explorer3.Current())
    thick = BRepOffsetAPI_MakeThickSolid()
    thick.MakeThickSolidByJoin(box_for_shell, faces_to_remove, -0.2, 1e-3)
    thick.Build()
    thick_shape = thick.Shape()
    save_step(thick_shape, "thick_shell")
except Exception as e:
    print(f"  [SKIP] thick_shell: {e}")

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

# Count generated files
generated = [f for f in os.listdir(OUT_DIR) if f.endswith(".stp")]
print(f"\n{'=' * 60}")
print(f"Generated {len(generated)} STEP files in: {OUT_DIR}")
for f in sorted(generated):
    print(f"  {f}")
print("=" * 60)
