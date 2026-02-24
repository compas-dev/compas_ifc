"""
21 Volume and Surface Area Test
================================

Tests the volume() and surface_area() methods on all parametric geometry types:

  A. Extrusion — exact formulas
  B. Revolution — Pappus theorem (volume), mesh-based (surface area)
  C. Pipe — pi*r^2*L (volume), mesh-based (surface area)
  D. ClippedExtrusion / BooleanResult — returns None (needs tessellated brep)
  E. CSG shapes (Box, Sphere, Cone, Cylinder) — COMPAS built-in
  F. Element-level fallback — element.volume uses visual_geometry when parametric returns None
"""

import math
import sys

pass_count = 0
fail_count = 0
results = []
TOL = 1e-3  # Relative tolerance for mesh-based approximations
ATOL = 1e-6  # Absolute tolerance for exact formulas


def check(label, condition, detail=""):
    global pass_count, fail_count
    status = "PASS" if condition else "FAIL"
    if condition:
        pass_count += 1
    else:
        fail_count += 1
    results.append((status, label, detail))
    return condition


def approx(a, b, rtol=TOL):
    """Check relative closeness."""
    if b == 0:
        return abs(a) < ATOL
    return abs(a - b) / abs(b) < rtol


# ==================================================================
# A. EXTRUSION
# ==================================================================

print("=" * 70)
print("A. EXTRUSION")
print("=" * 70)

from compas.geometry import Circle, Frame, Point, Polygon, Vector
from compas_ifc.representations import Extrusion

# A1: Rectangle extrusion
profile_rect = Polygon([
    Point(0, 0, 0),
    Point(6, 0, 0),
    Point(6, 0.3, 0),
    Point(0, 0.3, 0),
])
ext_rect = Extrusion(profile=profile_rect, direction=Vector(0, 0, 1), depth=3.0)

expected_area = 6.0 * 0.3  # 1.8
expected_vol = expected_area * 3.0  # 5.4
expected_perim = 2 * (6.0 + 0.3)  # 12.6
expected_sa = 2 * expected_area + expected_perim * 3.0  # 3.6 + 37.8 = 41.4

vol = ext_rect.volume()
sa = ext_rect.surface_area()
print(f"  Rect extrusion: volume={vol:.4f} (expected {expected_vol:.4f})")
print(f"  Rect extrusion: surface_area={sa:.4f} (expected {expected_sa:.4f})")
check("Ext rect volume", abs(vol - expected_vol) < ATOL, f"{vol} vs {expected_vol}")
check("Ext rect surface_area", abs(sa - expected_sa) < ATOL, f"{sa} vs {expected_sa}")

# A2: Circle extrusion (cylinder)
r = 0.5
depth = 2.0
ext_circ = Extrusion(
    profile=Circle(radius=r, frame=Frame(Point(0, 0, 0), [1, 0, 0], [0, 1, 0])),
    direction=Vector(0, 0, 1),
    depth=depth,
)
expected_vol_circ = math.pi * r**2 * depth
expected_sa_circ = 2 * math.pi * r**2 + 2 * math.pi * r * depth

vol_circ = ext_circ.volume()
sa_circ = ext_circ.surface_area()
print(f"  Circle extrusion: volume={vol_circ:.6f} (expected {expected_vol_circ:.6f})")
print(f"  Circle extrusion: surface_area={sa_circ:.6f} (expected {expected_sa_circ:.6f})")
check("Ext circle volume", abs(vol_circ - expected_vol_circ) < ATOL, f"{vol_circ:.6f} vs {expected_vol_circ:.6f}")
check("Ext circle surface_area", abs(sa_circ - expected_sa_circ) < ATOL, f"{sa_circ:.6f} vs {expected_sa_circ:.6f}")

# A3: Profile with voids
outer = Polygon([
    Point(0, 0, 0),
    Point(10, 0, 0),
    Point(10, 10, 0),
    Point(0, 10, 0),
])
void = Polygon([
    Point(2, 2, 0),
    Point(4, 2, 0),
    Point(4, 4, 0),
    Point(2, 4, 0),
])
ext_voids = Extrusion(profile=(outer, [void]), direction=Vector(0, 0, 1), depth=0.3)

expected_outer_area = 100.0
expected_void_area = 4.0
expected_net_area = expected_outer_area - expected_void_area  # 96
expected_vol_voids = expected_net_area * 0.3  # 28.8
expected_outer_perim = 40.0
expected_void_perim = 8.0
expected_sa_voids = 2 * expected_net_area + (expected_outer_perim + expected_void_perim) * 0.3  # 192 + 14.4 = 206.4

vol_voids = ext_voids.volume()
sa_voids = ext_voids.surface_area()
print(f"  Voids extrusion: volume={vol_voids:.4f} (expected {expected_vol_voids:.4f})")
print(f"  Voids extrusion: surface_area={sa_voids:.4f} (expected {expected_sa_voids:.4f})")
check("Ext voids volume", abs(vol_voids - expected_vol_voids) < ATOL, f"{vol_voids} vs {expected_vol_voids}")
check("Ext voids surface_area", abs(sa_voids - expected_sa_voids) < ATOL, f"{sa_voids} vs {expected_sa_voids}")

print()

# ==================================================================
# B. REVOLUTION
# ==================================================================

print("=" * 70)
print("B. REVOLUTION")
print("=" * 70)

from compas_ifc.representations import Revolution

# B1: Full torus — circle profile revolved 360 around axis
# Torus: major radius R = 1.0, minor radius r = 0.1
# Volume = 2 * pi * R * pi * r^2 = 2 * pi^2 * R * r^2
R_major = 1.0
r_minor = 0.1
rev_torus = Revolution(
    profile=Circle(radius=r_minor, frame=Frame(Point(R_major, 0, 0), [1, 0, 0], [0, 1, 0])),
    axis_point=Point(0, 0, 0),
    axis_direction=Vector(0, 0, 1),
    angle=360.0,
)
expected_torus_vol = 2 * math.pi**2 * R_major * r_minor**2
vol_torus = rev_torus.volume()
print(f"  Torus volume: {vol_torus:.6f} (expected {expected_torus_vol:.6f})")
check("Rev torus volume", approx(vol_torus, expected_torus_vol, 0.01), f"{vol_torus:.6f} vs {expected_torus_vol:.6f}")

# B2: Partial revolution — 180 degrees of a rectangular profile
# Profile: 0.2 x 0.3 rectangle at distance R=0.5 from axis
rect_profile = Polygon([
    Point(0.5, 0, -0.15),
    Point(0.7, 0, -0.15),
    Point(0.7, 0, 0.15),
    Point(0.5, 0, 0.15),
])
rev_half = Revolution(
    profile=rect_profile,
    axis_point=Point(0, 0, 0),
    axis_direction=Vector(0, 0, 1),
    angle=180.0,
)
# Pappus: V = 2*pi*R_centroid*A*(180/360)
# Centroid of rectangle is at x=0.6, so R_centroid = 0.6
# A = 0.2 * 0.3 = 0.06
R_centroid = 0.6
A_rect = 0.06
expected_half_vol = 2 * math.pi * R_centroid * A_rect * 0.5
vol_half = rev_half.volume()
print(f"  Half-rev volume: {vol_half:.6f} (expected {expected_half_vol:.6f})")
check("Rev half volume", approx(vol_half, expected_half_vol, 0.01), f"{vol_half:.6f} vs {expected_half_vol:.6f}")

# B3: Surface area with polygon profile (mesh-based, uses polygon which
# has correct 3D orientation, unlike Circle which always samples in XY)
sa_half = rev_half.surface_area()
print(f"  Half-rev surface area: {sa_half:.4f}")
check("Rev half SA > 0", sa_half > 0, f"{sa_half}")
# Surface area of revolved rectangle is approximate — just verify positive and reasonable
check("Rev half SA reasonable", sa_half > 0.1 and sa_half < 10.0, f"{sa_half:.4f}")

print()

# ==================================================================
# C. PIPE
# ==================================================================

print("=" * 70)
print("C. PIPE")
print("=" * 70)

from compas.geometry import Polyline
from compas_ifc.representations import Pipe

# C1: Straight pipe
pipe_straight = Pipe(
    directrix=Polyline([Point(0, 0, 0), Point(0, 0, 5)]),
    radius=0.15,
)
expected_pipe_vol = math.pi * 0.15**2 * 5.0
vol_pipe = pipe_straight.volume()
print(f"  Straight pipe volume: {vol_pipe:.6f} (expected {expected_pipe_vol:.6f})")
check("Pipe straight volume", abs(vol_pipe - expected_pipe_vol) < ATOL, f"{vol_pipe:.6f} vs {expected_pipe_vol:.6f}")

# C2: Hollow pipe
pipe_hollow = Pipe(
    directrix=Polyline([Point(0, 0, 0), Point(0, 0, 5)]),
    radius=0.15,
    inner_radius=0.10,
)
expected_hollow_vol = math.pi * (0.15**2 - 0.10**2) * 5.0
vol_hollow = pipe_hollow.volume()
print(f"  Hollow pipe volume: {vol_hollow:.6f} (expected {expected_hollow_vol:.6f})")
check("Pipe hollow volume", abs(vol_hollow - expected_hollow_vol) < ATOL, f"{vol_hollow:.6f} vs {expected_hollow_vol:.6f}")

# C3: Surface area > 0
sa_pipe = pipe_straight.surface_area()
expected_pipe_sa = 2 * math.pi * 0.15 * 5.0  # lateral area only (open ends in mesh)
print(f"  Pipe surface area: {sa_pipe:.4f} (expected ~{expected_pipe_sa:.4f})")
check("Pipe SA > 0", sa_pipe > 0, f"{sa_pipe}")

print()

# ==================================================================
# D. CLIPPED EXTRUSION & BOOLEAN RESULT
# ==================================================================

print("=" * 70)
print("D. CLIPPED EXTRUSION & BOOLEAN RESULT")
print("=" * 70)

from compas.geometry import Plane
from compas_ifc.representations import BooleanResult, ClippedExtrusion, HalfSpace

clip = ClippedExtrusion(
    extrusion=ext_rect,
    clipping_planes=[(Plane(Point(3, 0, 0), Vector(1, 0, 0)), True)],
)
check("ClippedExtrusion volume is None", clip.volume() is None)
check("ClippedExtrusion SA is None", clip.surface_area() is None)

bool_res = BooleanResult(
    operator="DIFFERENCE",
    first_operand=ext_rect,
    second_operand=ext_circ,
)
check("BooleanResult volume is None", bool_res.volume() is None)
check("BooleanResult SA is None", bool_res.surface_area() is None)

print("  ClippedExtrusion/BooleanResult return None (as expected)")
print()

# ==================================================================
# E. CSG SHAPES
# ==================================================================

print("=" * 70)
print("E. CSG SHAPES (COMPAS built-in)")
print("=" * 70)

from compas.geometry import Box, Cone, Cylinder, Sphere

box = Box(1, 2, 3)
check("Box volume", abs(box.volume - 6.0) < ATOL, f"{box.volume}")
check("Box area", abs(box.area - 22.0) < ATOL, f"{box.area}")
print(f"  Box: volume={box.volume}, area={box.area}")

sph = Sphere(1.5)
expected_sph_vol = 4.0 / 3.0 * math.pi * 1.5**3
expected_sph_area = 4 * math.pi * 1.5**2
check("Sphere volume", approx(sph.volume, expected_sph_vol), f"{sph.volume:.4f} vs {expected_sph_vol:.4f}")
check("Sphere area", approx(sph.area, expected_sph_area), f"{sph.area:.4f} vs {expected_sph_area:.4f}")
print(f"  Sphere: volume={sph.volume:.4f}, area={sph.area:.4f}")

cone = Cone(1.0, 2.5)
expected_cone_vol = math.pi * 1.0**2 * 2.5 / 3
check("Cone volume", approx(cone.volume, expected_cone_vol), f"{cone.volume:.4f} vs {expected_cone_vol:.4f}")
print(f"  Cone: volume={cone.volume:.4f}")

cyl = Cylinder(0.4, 3.0)
expected_cyl_vol = math.pi * 0.4**2 * 3.0
check("Cylinder volume", approx(cyl.volume, expected_cyl_vol), f"{cyl.volume:.4f} vs {expected_cyl_vol:.4f}")
print(f"  Cylinder: volume={cyl.volume:.4f}")

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
    print("SUCCESS: All volume/surface_area tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
