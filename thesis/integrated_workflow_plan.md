# Implementation Plan: Integrated Workflow Test (`integrated_workflow.py`)

## Purpose

This test demonstrates that all front-end model capabilities compose in a single
workflow. The other evaluation scripts test features in isolation; this one
exercises them together. It should be concise (the thesis section referencing it
is short) and produce a clear console output like the other test scripts.

## Simplification from the original thesis draft

The original draft loaded an existing building model as coordination context,
which duplicated what the granular export and hierarchy tests already cover.
The simplified version creates everything from scratch, keeping the focus on
feature composition rather than re-testing individual capabilities.

---

## Workflow Overview

```
Template model → Custom class definition → STEP geometry import →
Array creation on storey → Graph edge creation → Extract + export → Verify
```

## Part-by-Part Plan

### Part 0: Setup

- Use the same `check()` / pass/fail infrastructure as the other test scripts.
- Create output in `temp/` directory.

### Part 1: Custom Element Class with Validation

**Goal:** Define a Pydantic schema and a Specification, then demonstrate that
validation accepts conforming elements and rejects non-conforming ones.

**API pattern** (from `validation_evaluation.py`):
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from compas_ifc.bim import BuildingInformationModel
from compas_ifc.element import GenericElement
from compas_ifc.validation import Specification

class FunicularSlabProperties(BaseModel):
    span_capacity_m: float = Field(gt=0, le=15)
    load_capacity_kn_m2: float = Field(gt=0)
    gwp_kg_co2_eq: float = Field(gt=0)
    shell_thickness_mm: float = Field(gt=20, lt=200)

# Create model with specification enforcement
model = BuildingInformationModel.template(schema="IFC4", unit="m")
spec = Specification(
    name="Funicular slab properties",
    ifc_types=["IfcSlab"],
    required_psets={"FunicularSlabProperties": FunicularSlabProperties},
)
model.specifications = [spec]
storey = model.storeys[0]
```

**Checks:**
- Pydantic schema instantiation with valid properties succeeds
- Pydantic schema instantiation with invalid properties (e.g. negative span) raises ValidationError
- `model.add_element` with conforming slab accepted
- `model.add_element` with non-conforming slab rejected

### Part 2: STEP Geometry Import

**Goal:** Load a BRep geometry from a STEP file and attach it to an element.

**Which STEP file to use:** Pick one of the existing shapes from the BRep test
corpus that has interesting curved geometry. Good candidates:
- `box_filleted` (simple, non-trivial)
- `revolved_l_profile` (architectural relevance)
- `torus_partial` (curved)

If the funicular unit STEP file (`FunicularSlabUnit.stp` or similar) exists in
the data directory, use that instead. If not, use one of the above as a stand-in
and note this in the script docstring.

**API pattern** (from `roundtrip_brep.py`):
```python
from compas_occ.brep import OCCBrep

brep = OCCBrep.from_step("path/to/shape.stp")
original_volume = brep.volume
original_area = brep.area
```

**Checks:**
- STEP file loads successfully
- Volume > 0
- Surface area > 0

### Part 3: Array Creation with Placement

**Goal:** Create a grid of elements (e.g. 3×3 or 4×4) on the storey, each with
local transformation offsets. This tests spatial hierarchy + placement
integration.

**API pattern** (from `roundtrip_generated.py`):
```python
from compas.geometry import Frame, Point, Vector, Translation

units = []
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        element = GenericElement(
            ifc_type="IfcSlab",
            name=f"FSU_{i}_{j}",
        )
        element.geometry = brep  # same BRep for all (tests instancing potential)
        element.properties = {
            "FunicularSlabProperties": {
                "span_capacity_m": 8.0,
                "load_capacity_kn_m2": 5.0,
                "gwp_kg_co2_eq": 42.5,
                "shell_thickness_mm": 60.0,
            }
        }
        # Set local placement relative to storey
        element.frame = Frame(
            Point(i * SPACING_X, j * SPACING_Y, 0),
            Vector.Xaxis(),
            Vector.Yaxis(),
        )
        model.add_element(element, parent=storey)
        units.append(element)
```

Use a small grid (3×3 = 9 elements or 4×4 = 16) to keep test runtime short.
SPACING should be something reasonable relative to the shape size.

**Checks:**
- Expected number of elements created (GRID_SIZE²)
- All elements are children of the storey
- All elements pass validation (since we set conforming properties)

### Part 4: Graph Edge Creation

**Goal:** Add interaction graph edges between adjacent units and demonstrate
that the graph stores these relationships.

**Approach:** Rather than relying on a geometric contact detector (which may not
be available), create edges based on grid adjacency. This is honest about what
we're testing: the graph storage and export mechanism, not a collision algorithm.

If `compas_model.interactions.ContactDetector` or similar exists and is
importable, use it. Otherwise, fall back to adjacency-based edges.

**API pattern** (from `hierarchy_duplex.py` which reads `model.graph`):
```python
# Add edges for adjacent units in the grid
edge_count = 0
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        idx = i * GRID_SIZE + j
        # Right neighbor
        if j + 1 < GRID_SIZE:
            right_idx = i * GRID_SIZE + (j + 1)
            model.graph.add_edge(
                units[idx],
                units[right_idx],
                attr_dict={"category": "structural_connection"}
            )
            edge_count += 1
        # Top neighbor
        if i + 1 < GRID_SIZE:
            top_idx = (i + 1) * GRID_SIZE + j
            model.graph.add_edge(
                units[idx],
                units[top_idx],
                attr_dict={"category": "structural_connection"}
            )
            edge_count += 1
```

NOTE: You will need to check the actual `model.graph` API. It is a COMPAS
`Graph` object. The `add_edge` call might use positional args, keyword args, or
a different method name. Check the graph API used in the hierarchy test outputs
where `model.graph.number_of_edges()` is called. Inspect what methods are
available on `model.graph`.

**Checks:**
- Edge count matches expected (for NxN grid: 2*N*(N-1) edges)
- `model.graph.number_of_edges()` returns expected count

### Part 5: Save, Reload, and Verify

**Goal:** Save the model to IFC, reload it, and verify that everything survives.

```python
out_path = "temp/thesis_integrated_workflow.ifc"
model.save(out_path)

model2 = BuildingInformationModel(
    out_path,
    rectify_placements=True,
    load_geometries=False,  # faster; we check counts not geometry
)
```

**Checks:**
- Element count preserved
- All elements have expected IFC type (IfcSlab or IfcBuildingElementProxy)
- Graph edges preserved (count matches)
- Properties survive round-trip (spot-check one element's custom pset values)

### Part 6: Granular Extract

**Goal:** Extract the storey (with all units) into a standalone IFC file and
verify it is self-contained.

```python
extract_path = "temp/thesis_integrated_extract.ifc"
storey2 = model2.storeys[0]
sub = model2.extract(storey2, path=extract_path, load_geometries=False)
```

**Checks:**
- Extracted model has IfcProject, IfcSite, IfcBuilding, IfcBuildingStorey
- Element count matches (all units present)
- Graph edges preserved in extracted model

### Summary Section

Print the standard summary table like other test scripts:
```
SUMMARY
=======
  PASS  Custom: valid schema accepted
  PASS  Custom: invalid schema rejected
  ...
  X PASS / Y FAIL (of Z checks)
```

---

## Implementation Notes

1. **Follow the exact same structure** as the other test scripts:
   `check()` function, global pass/fail counters, `results` list, formatted
   summary at the end, `sys.exit(1)` on failure.

2. **Keep it short.** Target ~200-250 lines. This is one of 8 test scripts;
   it doesn't need to be exhaustive. The other scripts already cover depth.

3. **Use `use_occ=True`** on the model template if attaching BRep geometry
   (see `roundtrip_brep.py` pattern).

4. **Grid size:** 3×3 is fine (9 elements, 12 adjacency edges). Enough to
   demonstrate the pattern without slow runtime.

5. **If the graph edge API doesn't work as sketched:** The `model.graph` is
   used for reading in the existing tests but edges are loaded from IFC
   relationships (IfcRelConnectsElements, etc.), not created manually. If
   manual edge creation isn't supported, skip Part 4 and note it. The thesis
   text can mention that connections are stored as IFC relationships and
   preserved through extract, which is already tested in granular_export.py.

6. **If `compas_occ` is not available in the environment:** Fall back to
   creating elements with simple `Extrusion` geometry instead of BRep.
   The key point is feature composition, not BRep specifically.

7. **Expected output structure:**
   ```
   ======================================================================
   INTEGRATED WORKFLOW TEST
   ======================================================================

   PART 1: CUSTOM ELEMENT CLASS WITH VALIDATION
   ...

   PART 2: STEP GEOMETRY IMPORT
   ...

   PART 3: ARRAY CREATION (3x3 grid)
   ...

   PART 4: GRAPH EDGES (structural adjacency)
   ...

   PART 5: SAVE / RELOAD / VERIFY
   ...

   PART 6: GRANULAR EXTRACT
   ...

   SUMMARY
   ======================================================================
     PASS  ...
     ...
     N PASS / 0 FAIL (of N checks)

   SUCCESS: All integrated workflow tests passed.
   ```

---

## Files to produce

- `integrated_workflow.py` — the test script
- Run it and capture output to `integrated_workflow.txt`
