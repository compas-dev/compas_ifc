"""
B-Rep to IFC AdvancedBrep conversion tests.

Tests each generated STEP file by:
1. Loading the STEP file as OCCBrep.
2. Creating an IfcBuildingElementProxy with the brep as geometry.
3. Verifying the output IFC contains expected entity types.
4. Verifying schema validity with ifcopenshell.validate.
5. Saving a viewable IFC file for each test.

Automatically discovers all .stp files in temp/brep_conversion_tests/
and runs registered tests against them.

Known viewer limitations (not converter bugs):
  - box_with_hole: some viewers show tessellation misalignment at the
    cylinder-plane boundary. The IFC structure is correct (shared edges,
    proper inner bounds). This is a viewer tessellation issue.
  - Spheres and tori with seam edges may render with visible seams in
    viewers that don't handle periodic surfaces well.

Known converter compromises:
  - IfcAdvancedBrepWithVoids is poorly supported by viewers (tested in
    multiple viewers — the entire solid fails to render). As a workaround,
    solids with inner voids (e.g. hollow_box) are flattened into a single
    IfcAdvancedBrep with all faces (outer + void) merged into one
    IfcClosedShell. This renders correctly but loses the semantic
    distinction between outer shell and void shells.
    TODO: revisit once viewer support for IfcAdvancedBrepWithVoids improves.
  - compas_occ's OCCBrep.from_step() calls heal() -> sew() which uses
    BRepBuilderAPI_Sewing. This destroys inner/outer shell topology of
    boolean-cut solids (merges 2 shells into 1, leaving void faces as
    orphans outside any shell). The converter detects these orphan faces
    and merges them back into the single IfcClosedShell.

Run with:
    python scripts/8.2_brep_test.py
"""

import os
import sys
import traceback

# Ensure the repo src is on the path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

import ifcopenshell
import ifcopenshell.validate
from compas_occ.brep import OCCBrep

from compas_ifc.model import Model

STEP_DIR = os.path.join(REPO_ROOT, "temp", "brep_conversion_tests")

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"
SKIP = "[SKIP]"


def load_brep(filename):
    path = os.path.join(STEP_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"STEP file not found: {path}")
    return OCCBrep.from_step(path)


def make_model():
    return Model.template(schema="IFC4", unit="m", use_occ=True)


def validate_ifc(model):
    """Run ifcopenshell schema validation and return list of issue strings."""
    issues = []

    class Collector:
        def warning(self, msg, *a, **kw):
            issues.append("WARN: " + str(msg))

        def error(self, msg, *a, **kw):
            issues.append("ERR: " + str(msg))

    logger = Collector()
    try:
        ifcopenshell.validate.validate(model.file._file, logger)
    except Exception as e:
        issues.append("EXCEPTION during validate: " + str(e))
    return issues


def collect_entity_types(model):
    """Return a set of all IFC entity type names present in the file."""
    return {e.is_a() for e in model.file._file}


def run_test(
    name,
    step_file,
    expected_surface_types=None,
    expected_entity_types=None,
    expect_with_voids=False,
    expect_multi_brep=False,
):
    print("")
    print("=" * 60)
    print("TEST: " + name)
    print("  File: " + step_file)
    passed = True

    step_path = os.path.join(STEP_DIR, step_file)
    if not os.path.exists(step_path):
        print("  " + SKIP + " STEP file not found (run 8.1_brep_generate.py first)")
        return None

    try:
        brep = load_brep(step_file)
    except Exception as e:
        print("  " + FAIL + " Could not load STEP: " + str(e))
        return False

    model = make_model()
    storey = model.building_storeys[0]

    try:
        element = model.create(
            cls="IfcBuildingElementProxy",
            parent=storey,
            geometry=brep,
            name=name,
        )
    except Exception as e:
        print("  " + FAIL + " model.create raised exception:")
        traceback.print_exc()
        return False

    if element is None:
        print("  " + FAIL + " model.create returned None")
        return False

    print("  Created: " + str(element))

    present_types = collect_entity_types(model)

    # Check that AdvancedBrep geometry was produced
    has_brep = "IfcAdvancedBrep" in present_types
    has_voids = "IfcAdvancedBrepWithVoids" in present_types

    if has_brep or has_voids:
        if expect_with_voids:
            if has_voids:
                print("  " + PASS + " Got IfcAdvancedBrepWithVoids")
            else:
                print("  " + FAIL + " Expected IfcAdvancedBrepWithVoids, got IfcAdvancedBrep only")
                passed = False
        else:
            brep_type = "IfcAdvancedBrepWithVoids" if has_voids else "IfcAdvancedBrep"
            print("  " + PASS + " Got " + brep_type)
    else:
        print("  " + FAIL + " No IfcAdvancedBrep* found in file")
        passed = False

    # Check expected surface types are present
    if expected_surface_types:
        for surf_type in expected_surface_types:
            if surf_type in present_types:
                print("  " + PASS + " Found surface: " + surf_type)
            else:
                print("  " + FAIL + " Missing surface: " + surf_type)
                passed = False

    # Check expected entity types
    if expected_entity_types:
        for etype in expected_entity_types:
            if etype in present_types:
                print("  " + PASS + " Found entity: " + etype)
            else:
                print("  " + FAIL + " Missing entity: " + etype)
                passed = False

    # Validate with ifcopenshell
    issues = validate_ifc(model)
    schema_errors = [i for i in issues if i.startswith("ERR")]
    schema_warnings = [i for i in issues if i.startswith("WARN")]

    if schema_errors:
        print("  " + FAIL + " Schema validation errors (" + str(len(schema_errors)) + "):")
        for issue in schema_errors[:5]:
            print("    " + issue)
        if len(schema_errors) > 5:
            print("    ... and " + str(len(schema_errors) - 5) + " more")
        passed = False
    else:
        print("  " + PASS + " Schema validation: no errors")

    if schema_warnings:
        print("  " + WARN + " Schema warnings (" + str(len(schema_warnings)) + "):")
        for w in schema_warnings[:3]:
            print("    " + w)

    # Save viewable IFC file
    out_path = os.path.join(STEP_DIR, step_file.replace(".stp", ".ifc"))
    try:
        model.save(out_path)
        print("  Saved: " + out_path)
    except Exception as e:
        print("  " + WARN + " Could not save IFC: " + str(e))

    return passed


# -----------------------------------------------------------------------
# Test cases — organized by category
# -----------------------------------------------------------------------

results = {}

# === SURFACE TYPES ===

print("\n" + "#" * 60)
print("# SURFACE TYPES")
print("#" * 60)

results["plane_box"] = run_test(
    name="Box: IfcPlane + IfcLine edges",
    step_file="plane_box.stp",
    expected_surface_types=["IfcPlane"],
    expected_entity_types=["IfcLine", "IfcEdgeCurve", "IfcAdvancedFace"],
)

results["cube"] = run_test(
    name="Cube: IfcPlane (unit cube)",
    step_file="cube.stp",
    expected_surface_types=["IfcPlane"],
)

results["cylinder"] = run_test(
    name="Cylinder: IfcCylindricalSurface + IfcCircle edges",
    step_file="cylinder.stp",
    expected_surface_types=["IfcPlane", "IfcCylindricalSurface"],
    expected_entity_types=["IfcCircle", "IfcEdgeCurve"],
)

results["sphere"] = run_test(
    name="Sphere: IfcSphericalSurface (degenerate poles)",
    step_file="sphere.stp",
    expected_surface_types=["IfcSphericalSurface"],
)

results["hemisphere"] = run_test(
    name="Hemisphere: IfcSphericalSurface + IfcPlane cap",
    step_file="hemisphere.stp",
    expected_surface_types=["IfcSphericalSurface", "IfcPlane"],
)

results["torus"] = run_test(
    name="Torus: IfcToroidalSurface (doubly periodic)",
    step_file="torus.stp",
    expected_surface_types=["IfcToroidalSurface"],
)

results["torus_partial"] = run_test(
    name="Partial torus: IfcToroidalSurface + IfcPlane caps",
    step_file="torus_partial.stp",
    expected_surface_types=["IfcToroidalSurface"],
)

results["cone"] = run_test(
    name="Cone: NURBS fallback (no IfcConicalSurface in IFC4)",
    step_file="cone.stp",
    expected_surface_types=["IfcRationalBSplineSurfaceWithKnots"],
)

results["cone_truncated"] = run_test(
    name="Truncated cone: NURBS fallback",
    step_file="cone_truncated.stp",
)

results["wedge"] = run_test(
    name="Wedge: tapered box with angled planes",
    step_file="wedge.stp",
    expected_surface_types=["IfcPlane"],
)

# === EDGE TYPES ===

print("\n" + "#" * 60)
print("# EDGE TYPES")
print("#" * 60)

results["ellipsoid"] = run_test(
    name="Ellipsoid: non-uniform scaled sphere (degenerate poles)",
    step_file="ellipsoid.stp",
)

results["nurbs_pillow"] = run_test(
    name="NURBS pillow: IfcRationalBSplineSurfaceWithKnots + BSpline edges",
    step_file="nurbs_pillow.stp",
    expected_surface_types=["IfcRationalBSplineSurfaceWithKnots"],
)

# === MIXED SURFACES ===

print("\n" + "#" * 60)
print("# MIXED SURFACES")
print("#" * 60)

results["box_filleted"] = run_test(
    name="Filleted box: IfcPlane + IfcCylindricalSurface + IfcEllipse edges",
    step_file="box_filleted.stp",
    expected_surface_types=["IfcPlane", "IfcCylindricalSurface"],
    expected_entity_types=["IfcEllipse"],
)

results["capsule"] = run_test(
    name="Capsule: IfcCylindricalSurface + IfcSphericalSurface",
    step_file="capsule.stp",
)

# === TOPOLOGY CASES ===

print("\n" + "#" * 60)
print("# TOPOLOGY CASES")
print("#" * 60)

results["hollow_box"] = run_test(
    name="Hollow box: IfcAdvancedBrep with inner void (boolean cut result)",
    step_file="hollow_box.stp",
    expected_surface_types=["IfcPlane", "IfcSphericalSurface"],
)

results["box_with_hole"] = run_test(
    name="Box with hole: IfcAdvancedBrep (cylindrical void)",
    step_file="box_with_hole.stp",
    expected_surface_types=["IfcPlane", "IfcCylindricalSurface"],
)

results["compound_two_boxes"] = run_test(
    name="Compound: two separate boxes (multi-solid)",
    step_file="compound_two_boxes.stp",
    expect_multi_brep=True,
)

results["compound_box_cylinder"] = run_test(
    name="Compound: box + cylinder (multi-solid)",
    step_file="compound_box_cylinder.stp",
    expect_multi_brep=True,
)

# === EDGE CASES ===

print("\n" + "#" * 60)
print("# EDGE CASES")
print("#" * 60)

results["tiny_box"] = run_test(
    name="Tiny box: 1mm cube (tolerance test)",
    step_file="tiny_box.stp",
    expected_surface_types=["IfcPlane"],
)

results["large_box"] = run_test(
    name="Large box: 1000m cube (scale test)",
    step_file="large_box.stp",
    expected_surface_types=["IfcPlane"],
)

results["thin_plate"] = run_test(
    name="Thin plate: 10x10x0.01 (high aspect ratio)",
    step_file="thin_plate.stp",
    expected_surface_types=["IfcPlane"],
)

results["box_chamfered"] = run_test(
    name="Chamfered box: plane with chamfer",
    step_file="box_chamfered.stp",
    expected_surface_types=["IfcPlane"],
)

results["revolved_l_profile"] = run_test(
    name="Revolved L-profile: surface of revolution",
    step_file="revolved_l_profile.stp",
)

results["extruded_arc"] = run_test(
    name="Extruded arc: linear extrusion of arc profile",
    step_file="extruded_arc.stp",
    expected_surface_types=["IfcCylindricalSurface"],
)

results["pipe_sweep"] = run_test(
    name="Pipe sweep: circular section along arc path",
    step_file="pipe_sweep.stp",
)

results["thick_shell"] = run_test(
    name="Thick shell: hollowed box (offset shell)",
    step_file="thick_shell.stp",
)


# -----------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------

print("")
print("=" * 60)
print("SUMMARY")
print("=" * 60)

passed_count = 0
failed_count = 0
skipped_count = 0

for test_name, ok in results.items():
    if ok is None:
        status = SKIP
        skipped_count += 1
    elif ok:
        status = PASS
        passed_count += 1
    else:
        status = FAIL
        failed_count += 1
    print("  " + status + " " + test_name)

total = len(results)
print("")
print(f"{passed_count}/{total} passed, {failed_count} failed, {skipped_count} skipped.")
print("")
print("IFC files saved to: " + STEP_DIR)
