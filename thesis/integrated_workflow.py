"""Integrated Workflow Test
===========================

Demonstrates that all front-end model capabilities compose in a single workflow:

    custom element class → template model → validation enforcement →
    array creation → graph edges → save/reload → granular extract

Uses ``temp/devday/rfs.stp`` as the funicular slab unit geometry.
"""

import sys

import ifcopenshell.guid
from pydantic import BaseModel
from pydantic import Field

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import Vector
from compas_occ.brep import OCCBrep

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation
from compas_ifc.element import GenericElement
from compas_ifc.validation import Specification
from compas_ifc.validation import validate_model

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


GRID_SIZE = 3
SPACING = 6.5  # metres (slab footprint is ~6.36 x 6.21 m)


# ===========================================================================
# Custom element class with embedded geometry and properties
# ===========================================================================


class FunicularSlabUnit(GenericElement):
    """Prefabricated funicular slab unit.

    The geometry source (STEP file) and default structural properties are
    defined as part of the class, making each instance self-describing.
    A nested Pydantic schema validates property ranges.
    """

    STEP_PATH = "temp/devday/rfs.stp"
    STEP_SCALE = 0.001  # STEP file is in mm, IFC model is in m
    PSET_NAME = "FunicularSlabProperties"
    _cached_brep = None

    class Schema(BaseModel):
        """Pydantic validation schema for slab properties."""

        span_capacity_m: float = Field(gt=0, le=15)
        load_capacity_kn_m2: float = Field(gt=0)
        gwp_kg_co2_eq: float = Field(gt=0)
        shell_thickness_mm: float = Field(gt=20, lt=200)

    @classmethod
    def _load_geometry(cls):
        """Load, scale (mm → m), and cache the BRep geometry."""
        if cls._cached_brep is None:
            cls._cached_brep = OCCBrep.from_step(cls.STEP_PATH).scaled(cls.STEP_SCALE)
        return cls._cached_brep

    @classmethod
    def specification(cls):
        """Return a Specification that enforces this class's schema."""
        return Specification(
            name=cls.PSET_NAME,
            ifc_types=["IfcSlab"],
            required_psets={cls.PSET_NAME: cls.Schema},
        )

    def __init__(self, name=None, frame=None, span_capacity_m=8.0, load_capacity_kn_m2=5.0, gwp_kg_co2_eq=42.5, shell_thickness_mm=60.0, **kwargs):
        transformation = Transformation.from_frame(frame) if frame else None
        super().__init__(
            ifc_type="IfcSlab",
            geometry=self._load_geometry(),
            transformation=transformation,
            name=name,
            **kwargs,
        )
        self._properties = {
            self.PSET_NAME: {
                "span_capacity_m": span_capacity_m,
                "load_capacity_kn_m2": load_capacity_kn_m2,
                "gwp_kg_co2_eq": gwp_kg_co2_eq,
                "shell_thickness_mm": shell_thickness_mm,
            }
        }


# ===========================================================================
# Main workflow
# ===========================================================================

print("=" * 70)
print("INTEGRATED WORKFLOW TEST")
print("=" * 70)

# -----------------------------------------------------------------------
# PART 1: Custom Element Class
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 1: CUSTOM ELEMENT CLASS")
print("=" * 70)

# Pydantic schema validation
try:
    FunicularSlabUnit.Schema(span_capacity_m=8.0, load_capacity_kn_m2=5.0, gwp_kg_co2_eq=42.5, shell_thickness_mm=60.0)
    check("Schema: valid properties accepted", True)
except Exception:
    check("Schema: valid properties accepted", False)

try:
    FunicularSlabUnit.Schema(span_capacity_m=-1.0, load_capacity_kn_m2=5.0, gwp_kg_co2_eq=42.5, shell_thickness_mm=60.0)
    check("Schema: invalid properties rejected", False)
except Exception:
    check("Schema: invalid properties rejected", True, "negative span")

# Custom class instance
unit0 = FunicularSlabUnit(name="test_unit")
check("Class: correct ifc_type", unit0.ifc_type == "IfcSlab")
check("Class: has embedded geometry", unit0.geometry is not None)
check("Class: has embedded properties", unit0.PSET_NAME in (unit0._properties or {}))

brep = FunicularSlabUnit._load_geometry()
check("Class: geometry volume > 0", brep.volume > 0, f"{brep.volume:.4f}")
check("Class: geometry area > 0", brep.area > 0, f"{brep.area:.4f}")

print(f"\n  Geometry: {FunicularSlabUnit.STEP_PATH}")
print(f"  Volume:  {brep.volume:.4f} m3")
print(f"  Area:    {brep.area:.4f} m2")
print(f"  Schema:  {list(FunicularSlabUnit.Schema.model_fields.keys())}")

# -----------------------------------------------------------------------
# PART 2: Model + Enforcement
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 2: MODEL CREATION WITH SPECIFICATION ENFORCEMENT")
print("=" * 70)

model = BuildingInformationModel.template(schema="IFC4", unit="m", use_occ=True)
spec = FunicularSlabUnit.specification()
model.specifications = [spec]
storey = model.storeys[0]

# Enforcement: validate_element detects non-conforming properties
from compas_ifc.validation import validate_element

bad = FunicularSlabUnit(name="bad_unit", span_capacity_m=-5.0)
bad_results = validate_element(bad, [spec])
check("Enforce: non-conforming detected", any(r.status == "fail" for r in bad_results), "negative span")

good = FunicularSlabUnit(name="good_unit")
good_results = validate_element(good, [spec])
check("Enforce: conforming accepted", all(r.status == "pass" for r in good_results))

print(f"\n  Specification: {spec.name}")
print(f"  Applies to: {spec.ifc_types}")

# -----------------------------------------------------------------------
# PART 3: Array Creation
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print(f"PART 3: ARRAY CREATION ({GRID_SIZE}x{GRID_SIZE} grid)")
print("=" * 70)

units = []
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        u = FunicularSlabUnit(
            name=f"FSU_{i}_{j}",
            frame=Frame(Point(i * SPACING, j * SPACING, 0), Vector.Xaxis(), Vector.Yaxis()),
        )
        model.add_element(u, parent=storey)
        units.append(u)

expected = GRID_SIZE**2
check("Array: element count", len(units) == expected, f"{len(units)}")

children = [e for e in storey.children if e.ifc_type == "IfcSlab"]
check("Array: all under storey", len(children) == expected, f"{len(children)}")

vresults = validate_model(model, [spec])
check("Array: all pass validation", all(r.status == "pass" for r in vresults), f"{sum(r.status == 'pass' for r in vresults)}/{len(vresults)}")

print(f"\n  Grid: {GRID_SIZE}x{GRID_SIZE} = {expected} elements")
print(f"  Spacing: {SPACING} m")

# -----------------------------------------------------------------------
# PART 4: Graph Edges (structural adjacency)
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 4: GRAPH EDGES (structural adjacency)")
print("=" * 70)

edge_count = 0
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        idx = i * GRID_SIZE + j
        for di, dj in [(0, 1), (1, 0)]:
            ni, nj = i + di, j + dj
            if ni < GRID_SIZE and nj < GRID_SIZE:
                nidx = ni * GRID_SIZE + nj
                edge = model.add_interaction(units[idx], units[nidx])
                model.graph.edge_attribute(edge, "relationships", [{"category": "connection", "source": "adjacency"}])
                # Create IFC relationship for round-trip persistence
                model._file._file.create_entity(
                    "IfcRelConnectsElements",
                    GlobalId=ifcopenshell.guid.new(),
                    RelatingElement=units[idx]._ifc_entity.entity,
                    RelatedElement=units[nidx]._ifc_entity.entity,
                )
                edge_count += 1

expected_edges = 2 * GRID_SIZE * (GRID_SIZE - 1)
check("Graph: edge count", edge_count == expected_edges, f"{edge_count} == {expected_edges}")
check("Graph: stored in model", model.graph.number_of_edges() >= expected_edges, f"{model.graph.number_of_edges()}")

print(f"\n  Adjacency edges: {edge_count}")
print(f"  Graph edges: {model.graph.number_of_edges()}")

# -----------------------------------------------------------------------
# PART 5: Save / Reload / Verify
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 5: SAVE / RELOAD / VERIFY")
print("=" * 70)

out_path = "temp/thesis_integrated_workflow.ifc"
model.save(out_path)

model2 = BuildingInformationModel(out_path, rectify_placements=True, load_geometries=False)

slabs2 = [e for e in model2.building_elements if e.ifc_type == "IfcSlab"]
check("Reload: slab count", len(slabs2) == expected, f"{len(slabs2)} vs {expected}")

# Properties round-trip
sample = slabs2[0]
sample_props = sample.properties.get("FunicularSlabProperties", {})
check("Reload: properties survive", "span_capacity_m" in sample_props, str(list(sample_props.keys())[:4]))

# Graph edges
check("Reload: graph edges", model2.graph.number_of_edges() >= expected_edges, f"{model2.graph.number_of_edges()}")

# Transform alignment
misaligned = 0
for elem in slabs2:
    if elem._ifc_entity and elem._ifc_entity.ObjectPlacement:
        ifc_t = IfcLocalPlacement_to_transformation(elem._ifc_entity.ObjectPlacement)
        model_t = elem.modeltransformation
        ifc_pos = ifc_t.translation_vector
        model_pos = model_t.translation_vector
        dist = sum((a - b) ** 2 for a, b in zip(ifc_pos, model_pos)) ** 0.5
        if dist > 0.001:
            misaligned += 1
check("Reload: transforms aligned", misaligned == 0, f"{misaligned} of {len(slabs2)}")

print(f"\n  Saved to: {out_path}")
print(f"  Reloaded slabs: {len(slabs2)}")
print(f"  Graph edges: {model2.graph.number_of_edges()}")
print(f"  Misaligned: {misaligned}")

# -----------------------------------------------------------------------
# PART 6: Granular Extract
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 6: GRANULAR EXTRACT")
print("=" * 70)

extract_path = "temp/thesis_integrated_extract.ifc"
storey2 = model2.storeys[0]
sub = model2.extract(storey2, path=extract_path, load_geometries=False)

has_project = len(sub._file._file.by_type("IfcProject")) > 0
has_storey = len(sub.storeys) >= 1
check("Extract: spatial scaffolding", has_project and has_storey)

extract_slabs = [e for e in sub.building_elements if e.ifc_type == "IfcSlab"]
check("Extract: slab count", len(extract_slabs) == expected, f"{len(extract_slabs)} vs {expected}")

check("Extract: graph edges", sub.graph.number_of_edges() >= expected_edges, f"{sub.graph.number_of_edges()}")

print(f"\n  Extracted to: {extract_path}")
print(f"  Slabs: {len(extract_slabs)}")
print(f"  Graph edges: {sub.graph.number_of_edges()}")

# -----------------------------------------------------------------------
# SUMMARY
# -----------------------------------------------------------------------
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

for status, label, detail in results:
    line = f"  {status:4s}  {label}"
    if detail:
        line += f"  ({detail})"
    print(line)

print(f"\n  {pass_count} PASS / {fail_count} FAIL  (of {pass_count + fail_count} checks)\n")

if fail_count == 0:
    print("SUCCESS: All integrated workflow tests passed.\n")
else:
    print("FAILURE: Some tests failed.\n")
    sys.exit(1)
