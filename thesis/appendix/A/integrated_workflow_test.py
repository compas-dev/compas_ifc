"""Integrated Workflow Test
===========================

Runs the pure workflow from ``workflow.py`` and verifies every step.
Reports workflow-only line count separately from test infrastructure.
"""

import sys

from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation

from integrated_workflow_code import COLUMN_HEIGHT
from integrated_workflow_code import COLUMN_SECTION
from integrated_workflow_code import GRID_SIZE
from integrated_workflow_code import FunicularSlabSchema
from integrated_workflow_code import FunicularSlabUnit
from integrated_workflow_code import run

# ===========================================================================
# Test infrastructure
# ===========================================================================

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


# ===========================================================================
# Run workflow
# ===========================================================================

print("=" * 70)
print("INTEGRATED WORKFLOW TEST")
print("=" * 70)

w = run()

brep = w["brep"]
model = w["model"]
model2 = w["model2"]
sub = w["sub"]
spec = w["spec"]
units = w["units"]
columns = w["columns"]
beams = w["beams"]
SPACING_X = w["SPACING_X"]
SPACING_Y = w["SPACING_Y"]

expected_slabs = GRID_SIZE**2
expected_cols = (GRID_SIZE + 1) ** 2
expected_beams = (GRID_SIZE + 1) * GRID_SIZE
expected_slab_edges = GRID_SIZE * (GRID_SIZE - 1)  # 6: slabs touch along one axis only
expected_beam_beam = (GRID_SIZE + 1) * (GRID_SIZE - 1)  # 8: beams meet end-to-end within each column
expected_slab_beam = 2 * GRID_SIZE**2  # 18: each slab rests on the two beams along its long edges
expected_total_edges = expected_slab_edges + expected_slab_beam + expected_beam_beam  # 32

# ===========================================================================
# PART 1: Custom Element Class
# ===========================================================================
print("\n" + "=" * 70)
print("PART 1: CUSTOM ELEMENT CLASS")
print("=" * 70)

# Combined schema validation
valid_data = {
    "Pset_SlabCommon": FunicularSlabUnit.DEFAULTS_SLAB_COMMON,
    "Pset_EnvironmentalImpactIndicators": FunicularSlabUnit.DEFAULTS_ENVIRONMENTAL,
    "ConcreteRecipeProperties": FunicularSlabUnit.DEFAULTS_RECIPE,
}
try:
    FunicularSlabSchema(**valid_data)
    check("Schema: all psets valid (combined)", True)
except Exception as e:
    check("Schema: all psets valid (combined)", False, str(e))

invalid_data = {
    "Pset_SlabCommon": {**FunicularSlabUnit.DEFAULTS_SLAB_COMMON, "Status": "INVALID"},
    "Pset_EnvironmentalImpactIndicators": {**FunicularSlabUnit.DEFAULTS_ENVIRONMENTAL, "ClimateChangePerUnit": -1.0},
    "ConcreteRecipeProperties": {**FunicularSlabUnit.DEFAULTS_RECIPE, "CompressiveStrength_MPa": 0.0},
}
try:
    FunicularSlabSchema(**invalid_data)
    check("Schema: rejects invalid across psets", False)
except Exception as e:
    error_count = e.error_count() if hasattr(e, "error_count") else 0
    check("Schema: rejects invalid across psets", True, f"{error_count} errors")

unit0 = FunicularSlabUnit(name="test_unit")
check("Class: correct ifc_type", unit0.ifc_type == "IfcSlab")
check("Class: has embedded geometry", unit0.geometry is not None)
check("Class: has 3 property sets", len(unit0._properties) == 3, list(unit0._properties.keys()))
check("Class: geometry volume > 0", brep.volume > 0, f"{brep.volume:.4f}")
check("Class: geometry area > 0", brep.area > 0, f"{brep.area:.4f}")

print(f"\n  Geometry: {FunicularSlabUnit.STEP_PATH}")
print(f"  Volume:  {brep.volume:.4f} m3")
print(f"  Area:    {brep.area:.4f} m2")
print(f"  Footprint: {SPACING_X:.2f} x {SPACING_Y:.2f} m")
print(f"  Property sets: {list(FunicularSlabUnit.Schema.model_fields.keys())}")

# ===========================================================================
# PART 2: Enforcement
# ===========================================================================
print("\n" + "=" * 70)
print("PART 2: MODEL CREATION WITH SPECIFICATION ENFORCEMENT")
print("=" * 70)

check("Enforce: non-conforming detected", any(r.status == "fail" for r in w["bad_results"]), "negative GWP")
check("Enforce: conforming accepted", all(r.status == "pass" for r in w["good_results"]))

print(f"\n  Specification: {spec.name}")
print(f"  Applies to: {spec.ifc_types}")

# ===========================================================================
# PART 3: Array Creation
# ===========================================================================
print("\n" + "=" * 70)
print(f"PART 3: ARRAY CREATION ({GRID_SIZE}x{GRID_SIZE} slabs + columns + beams)")
print("=" * 70)

storey = model.storeys[0]
slab_children = [e for e in storey.children if e.ifc_type == "IfcSlab"]

check("Array: slab count", len(units) == expected_slabs, f"{len(units)}")
check("Array: slabs under storey", len(slab_children) == expected_slabs, f"{len(slab_children)}")
check("Array: all slabs pass validation", all(r.status == "pass" for r in w["model_results"]), f"{sum(r.status == 'pass' for r in w['model_results'])}/{len(w['model_results'])}")
check("Array: column count", len(columns) == expected_cols, f"{len(columns)}")
check("Array: beam count", len(beams) == expected_beams, f"{len(beams)}")

print(f"\n  Slabs:   {GRID_SIZE}x{GRID_SIZE} = {expected_slabs}, spacing {SPACING_X:.2f} x {SPACING_Y:.2f} m")
print(f"  Columns: {GRID_SIZE+1}x{GRID_SIZE+1} = {expected_cols}, section {COLUMN_SECTION} m, height {COLUMN_HEIGHT} m")
print(f"  Beams:   {expected_beams} along Y axis")
print(f"  Total building elements: {expected_slabs + expected_cols + expected_beams}")

# ===========================================================================
# PART 4: Graph Edges
# ===========================================================================
print("\n" + "=" * 70)
print("PART 4: GRAPH EDGES (compute_connections)")
print("=" * 70)

# Break the detected connections down by element-type pair. The 3x3 slab grid
# on a 4x4 column grid with Y-spanning beams is arranged to produce a known set
# of geometric contacts: 6 slab-slab, 18 slab-beam, 8 beam-beam (32 total).
_bd = {}
for _edge in model.connections:
    _na, _nb = _edge
    _key = tuple(sorted((model.graph.node_element(_na).ifc_type, model.graph.node_element(_nb).ifc_type)))
    _bd[_key] = _bd.get(_key, 0) + 1
n_slab_slab = _bd.get(("IfcSlab", "IfcSlab"), 0)
n_slab_beam = _bd.get(("IfcBeam", "IfcSlab"), 0)
n_beam_beam = _bd.get(("IfcBeam", "IfcBeam"), 0)

check("Graph: total connections", w["edge_count"] == expected_total_edges, f"{w['edge_count']} == {expected_total_edges}")
check("Graph: slab-slab connections", n_slab_slab == expected_slab_edges, f"{n_slab_slab} == {expected_slab_edges}")
check("Graph: slab-beam connections", n_slab_beam == expected_slab_beam, f"{n_slab_beam} == {expected_slab_beam}")
check("Graph: beam-beam connections", n_beam_beam == expected_beam_beam, f"{n_beam_beam} == {expected_beam_beam}")
check("Graph: stored in model", model.graph.number_of_edges() == w["edge_count"], f"{model.graph.number_of_edges()}")

print(f"\n  Computed connections: {w['edge_count']}  (slab-slab {n_slab_slab}, slab-beam {n_slab_beam}, beam-beam {n_beam_beam})")
print(f"  Graph edges: {model.graph.number_of_edges()}")

# ===========================================================================
# PART 5: Save / Reload / Verify
# ===========================================================================
print("\n" + "=" * 70)
print("PART 5: SAVE / RELOAD / VERIFY")
print("=" * 70)

slabs2 = [e for e in model2.building_elements if e.ifc_type == "IfcSlab"]
cols2 = [e for e in model2.building_elements if e.ifc_type == "IfcColumn"]
beams2 = [e for e in model2.building_elements if e.ifc_type == "IfcBeam"]
check("Reload: slab count", len(slabs2) == expected_slabs, f"{len(slabs2)} vs {expected_slabs}")
check("Reload: column count", len(cols2) == expected_cols, f"{len(cols2)} vs {expected_cols}")
check("Reload: beam count", len(beams2) == expected_beams, f"{len(beams2)} vs {expected_beams}")

# Properties round-trip
sample = slabs2[0]
slab_common_rt = sample.properties.get("Pset_SlabCommon", {})
env_rt = sample.properties.get("Pset_EnvironmentalImpactIndicators", {})
recipe_rt = sample.properties.get("ConcreteRecipeProperties", {})
check("Reload: Pset_SlabCommon survives", "LoadBearing" in slab_common_rt, str(list(slab_common_rt.keys())[:4]))
check("Reload: EnvironmentalImpact survives", "ClimateChangePerUnit" in env_rt, str(list(env_rt.keys())[:4]))
check("Reload: ConcreteRecipe survives", "RecipeName" in recipe_rt, str(list(recipe_rt.keys())[:4]))

# Graph edges
check("Reload: graph edges", model2.graph.number_of_edges() == expected_total_edges, f"{model2.graph.number_of_edges()} == {expected_total_edges}")

# Transform alignment
misaligned = 0
checked = 0
for elem in list(slabs2) + list(cols2) + list(beams2):
    if elem._ifc_entity and elem._ifc_entity.ObjectPlacement:
        ifc_t = IfcLocalPlacement_to_transformation(elem._ifc_entity.ObjectPlacement)
        model_t = elem.modeltransformation
        ifc_pos = ifc_t.translation_vector
        model_pos = model_t.translation_vector
        dist = sum((a - b) ** 2 for a, b in zip(ifc_pos, model_pos)) ** 0.5
        if dist > 0.001:
            misaligned += 1
        checked += 1
check("Reload: transforms aligned", misaligned == 0, f"{misaligned} of {checked}")

print(f"\n  Saved to: {w['out_path']}")
print(f"  Reloaded: {len(slabs2)} slabs, {len(cols2)} columns, {len(beams2)} beams")
print(f"  Graph edges: {model2.graph.number_of_edges()}")
print(f"  Misaligned: {misaligned}")

# ===========================================================================
# PART 6: Granular Extract
# ===========================================================================
print("\n" + "=" * 70)
print("PART 6: GRANULAR EXTRACT")
print("=" * 70)

has_project = len(sub._file._file.by_type("IfcProject")) > 0
has_storey = len(sub.storeys) >= 1
check("Extract: spatial scaffolding", has_project and has_storey)

extract_slabs = [e for e in sub.building_elements if e.ifc_type == "IfcSlab"]
extract_cols = [e for e in sub.building_elements if e.ifc_type == "IfcColumn"]
extract_beams = [e for e in sub.building_elements if e.ifc_type == "IfcBeam"]
check("Extract: slab count", len(extract_slabs) == expected_slabs, f"{len(extract_slabs)} vs {expected_slabs}")
check("Extract: column count", len(extract_cols) == expected_cols, f"{len(extract_cols)} vs {expected_cols}")
check("Extract: beam count", len(extract_beams) == expected_beams, f"{len(extract_beams)} vs {expected_beams}")
check("Extract: graph edges", sub.graph.number_of_edges() == expected_total_edges, f"{sub.graph.number_of_edges()} == {expected_total_edges}")

print(f"\n  Extracted to: {w['extract_path']}")
print(f"  Slabs: {len(extract_slabs)}, Columns: {len(extract_cols)}, Beams: {len(extract_beams)}")
print(f"  Graph edges: {sub.graph.number_of_edges()}")

# ===========================================================================
# SUMMARY
# ===========================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

for status, label, detail in results:
    line = f"  {status:4s}  {label}"
    if detail:
        line += f"  ({detail})"
    print(line)

print(f"\n  {pass_count} PASS / {fail_count} FAIL  (of {pass_count + fail_count} checks)")

# Workflow code metrics
workflow_file = "thesis/appendix/A/integrated_workflow_code.py"
with open(workflow_file) as f:
    lines = f.readlines()
total = len(lines)
non_blank = sum(1 for l in lines if l.strip())
code_only = sum(1 for l in lines if l.strip() and not l.strip().startswith("#") and not l.strip().startswith('"""') and not l.strip().startswith("'''"))
print(f"\n  Workflow code ({workflow_file}): {total} lines total, {non_blank} non-blank, {code_only} code-only")

if fail_count == 0:
    print("\nSUCCESS: All integrated workflow tests passed.\n")
else:
    print("\nFAILURE: Some tests failed.\n")
    sys.exit(1)
