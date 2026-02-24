# Geometry Conversion Review: compas_ifc

> **Date:** 2026-02-24
> **Scope:** Complete audit of reading and writing for all 3D geometry types
> **Branch:** `brep`

---

## Executive Summary

compas_ifc currently handles **3 geometry export paths** (CSG primitives, Mesh, B-Rep) and relies on **ifcopenshell.geom** for all import. The Duplex test model reveals that **the most common IFC geometry types in practice are exactly the ones we do NOT export**: `IfcExtrudedAreaSolid` (48% of all items), `IfcMappedItem` (29%), and `IfcBooleanClippingResult` (1%). Our B-Rep exporter — the most sophisticated piece — produces `IfcAdvancedBrep`, which is actually rare in real BIM files.

This means compas_ifc can **read** virtually anything (via ifcopenshell), but **writes** geometry in a form that doesn't match how BIM authoring tools typically produce it.

---

## 1. What the Duplex Model Actually Contains

Auditing `Duplex_A_20110907.ifc` (our primary test model) shows:

### Body representations by type

| RepresentationType | Count | What it means |
|---|---|---|
| `SweptSolid` | 180 | `IfcExtrudedAreaSolid` — profile + extrusion direction |
| `MappedRepresentation` | 99 | `IfcMappedItem` — instanced geometry (reuse) |
| `SurfaceModel` | 40 | `IfcFaceBasedSurfaceModel` — explicit face meshes |
| `Clipping` | 4 | `IfcBooleanClippingResult` — boolean subtraction |

### Underlying geometry items

| IFC Type | Count | % |
|---|---|---|
| `IfcExtrudedAreaSolid` | 278 | 48% |
| `IfcMappedItem` | 167 | 29% |
| `IfcPolyline` | 67 | 12% |
| `IfcFaceBasedSurfaceModel` | 40 | 7% |
| `IfcGeometricSet` | 25 | 4% |
| `IfcBooleanClippingResult` | 4 | 1% |

### Non-body representations

| Identifier | Type | Count | Purpose |
|---|---|---|---|
| `Axis` | `Curve2D` | 65 | Wall/beam centerlines (IfcPolyline) |
| `Plan` | `GeometricSet` / `MappedRepresentation` | 91 | Floor plan projections |
| `Boundary` | `GeometricSet` | 2 | Space boundary curves |
| `WalkingLine` | `Curve2D` | 2 | Stair walking lines |

### `wall-with-opening-and-window.ifc`

All 3 body items are `IfcExtrudedAreaSolid`, plus 1 `IfcPolyline` axis.

**Key insight:** Real BIM files are dominated by extrusions and mapped items. The Duplex model has **zero** `IfcAdvancedBrep` entities.

---

## 2. Current Architecture

### Reading (IFC → COMPAS)

```
IFC File
  ↓
ifcopenshell.geom.iterator()     ← handles ALL IFC geometry types
  ↓                                 (extrusions, booleans, CSG, B-Rep, tessellation, ...)
  ├→ TessellatedBrep              ← default: triangulated vertices/faces (numpy)
  └→ OCCBrep                      ← optional: full OCC B-Rep topology (requires compas_occ)
```

**ifcopenshell does all the heavy lifting.** It evaluates any parametric representation (extrusions, booleans, sweeps) into either tessellated triangles or OCC shapes. compas_ifc just stores the result.

**Consequence:** All parametric information is lost on import. An `IfcExtrudedAreaSolid` (profile + direction + depth) becomes a tessellated mesh or OCC solid — you cannot recover the original profile curve or extrusion depth.

### Writing (COMPAS → IFC)

```
COMPAS Geometry
  ↓
representation.py dispatch
  ├→ Box/Sphere/Cone/Cylinder  →  shapes.py   →  IfcCsgSolid (CSG primitive)
  ├→ Mesh                     →  mesh.py     →  IfcFaceBasedSurfaceModel / IfcPolygonalFaceSet
  └→ Brep (OCC available)     →  brep.py     →  IfcAdvancedBrep
      Brep (no OCC)           →  mesh.py     →  IfcFaceBasedSurfaceModel (tessellated fallback)
```

---

## 3. Detailed Inventory: What Works

### 3.1 Reading (Import)

| IFC Geometry Type | Supported? | How | What you get |
|---|---|---|---|
| **IfcExtrudedAreaSolid** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcRevolvedAreaSolid** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcSweptDiskSolid** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcBooleanResult** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcBooleanClippingResult** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcCsgSolid** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcBlock/Sphere/Cone/Cylinder** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcAdvancedBrep** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcFacetedBrep** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcFaceBasedSurfaceModel** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcTriangulatedFaceSet** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcPolygonalFaceSet** | YES | ifcopenshell evaluates | TessellatedBrep or OCCBrep |
| **IfcMappedItem** | YES* | ifcopenshell evaluates | Geometry duplicated per instance |
| **IfcPolyline** (Axis) | NO | Not extracted | Only Body representations are loaded |
| **IfcGeometricSet** (Plan) | NO | Not extracted | Only Body representations are loaded |

*`IfcMappedItem` instancing relationships are lost — each instance gets its own separate geometry copy.

### 3.2 Writing (Export)

| COMPAS Type | IFC Output | RepresentationType | Quality |
|---|---|---|---|
| `Box` | `IfcBlock` in `IfcCsgSolid` | "CSG" | Good — parametric |
| `Sphere` | `IfcSphere` in `IfcCsgSolid` | "CSG" | Good — parametric |
| `Cone` | `IfcRightCircularCone` in `IfcCsgSolid` | "CSG" | Good — parametric |
| `Cylinder` | `IfcRightCircularCylinder` in `IfcCsgSolid` | "CSG" | Good — parametric |
| `Mesh` | `IfcFaceBasedSurfaceModel` | "SurfaceModel" | OK — no solid semantics |
| `Mesh` | `IfcPolygonalFaceSet` | (available but not used by dispatch) | Better — IFC4 indexed format |
| `Brep` (with OCC) | `IfcAdvancedBrep` | "SolidModel" | Excellent — full NURBS topology |
| `Brep` (no OCC) | `IfcFaceBasedSurfaceModel` | "SurfaceModel" | Degraded — tessellation fallback |

---

## 4. What's Missing

### 4.1 Writing: Major Gaps

#### A. `IfcExtrudedAreaSolid` — Extrusions (**HIGH PRIORITY**)

This is the #1 most common geometry type in real IFC files (48% of items in Duplex). Currently, if a user creates an element with geometry, it can only be exported as a CSG primitive, mesh, or B-Rep — never as the compact parametric extrusion that BIM tools produce.

**What's needed:**
1. Profile conversion: COMPAS 2D curve → `IfcProfileDef` subtypes
   - `IfcRectangleProfileDef` (most walls, slabs, beams)
   - `IfcCircleProfileDef` (columns, pipes)
   - `IfcArbitraryClosedProfileDef` (arbitrary 2D profiles via `IfcPolyline` or `IfcCompositeCurve`)
   - `IfcArbitraryProfileDefWithVoids` (profiles with holes)
   - I/L/T/U/Z standard structural profiles
2. Extrusion assembly: profile + direction vector + depth → `IfcExtrudedAreaSolid`
3. Dispatch logic: detect when a `Brep` is actually an extrusion and decompose it

**COMPAS limitation:** There is no `Extrusion` geometry type in COMPAS. An extrusion created via `OCCBrep.from_extrusion()` becomes a `Brep` — the profile/direction/depth are lost. We'd need either:
- A new input type (e.g., dict with `profile`, `direction`, `depth` keys)
- A Brep analysis function that detects extrusion topology and extracts the profile
- Direct construction from IFC parameters

**Practical value:** Very high. Most BIM elements (walls, slabs, beams, columns) are extrusions. Being able to write them as `IfcExtrudedAreaSolid` produces much smaller files and preserves editability in other BIM tools.

#### B. `IfcMappedItem` — Geometry Instancing (**MEDIUM PRIORITY**)

29% of geometry items in the Duplex model. Mapped items let multiple elements share the same geometry definition, just with different placements. This saves enormous file space for repeated elements (doors, windows, furniture, fittings).

**What's needed:**
1. `IfcRepresentationMap` creation (origin + base representation)
2. `IfcMappedItem` creation (map source + transform)
3. Detection of shared geometry objects in the element tree
4. Caching to reuse representation maps

**Current state:** `representation.py` already caches by `id(representation)` to avoid re-exporting identical geometry objects. But it creates full `IfcShapeRepresentation` copies, not `IfcMappedItem` instances. The infrastructure is partially there.

**Practical value:** File size reduction. A model with 50 identical windows would store the geometry once instead of 50 times.

#### C. `IfcBooleanClippingResult` — Boolean Operations (**LOW-MEDIUM**)

Only 4 instances in Duplex, but critical for walls with openings. When a wall is "clipped" (e.g., sloped at the top), the authoring tool stores `IfcBooleanClippingResult` = wall extrusion MINUS half-space.

**What's needed:**
1. `IfcBooleanResult` export with recursive operand handling
2. `IfcHalfSpaceSolid` / `IfcPolygonalBoundedHalfSpace` export
3. Tree structure preservation (first operand, second operand, operator)

**Current state:** Old code in `__old/geometricmodel.py` has `IfcBooleanResult_to_brep()` for **reading** booleans (evaluating them via OCC), but no **writing** counterpart.

**COMPAS limitation:** `Brep` boolean operations (`A - B`) produce a flattened solid — the operation tree is lost.

#### D. `IfcRevolvedAreaSolid` — Revolutions (**LOW PRIORITY**)

Rare in typical building models but used for columns, handrails, and MEP fittings.

**What's needed:**
1. Profile + axis + angle → `IfcRevolvedAreaSolid`
2. Same profile conversion infrastructure as extrusions

#### E. `IfcSweptDiskSolid` — Pipe Sweeps (**LOW PRIORITY**)

Used for MEP routing — a circle swept along a 3D curve.

**What's needed:**
1. Directrix curve export (`IfcCompositeCurve` or `IfcPolyline`)
2. Inner/outer radius
3. Start/end parameters

#### F. `IfcTriangulatedFaceSet` — Indexed Triangulation (**LOW PRIORITY**)

IFC4 alternative to `IfcPolygonalFaceSet` with optional per-vertex normals. Better for rendering-oriented export.

**What's needed:**
1. Triangle-specific export (vs. n-gon polygonal)
2. Normal vector computation and export
3. Optional `PnIndex` for point reuse compression

### 4.2 Reading: Major Gaps

#### A. Non-Body Representations (**MEDIUM PRIORITY**)

Currently only "Body" representations are loaded. The Duplex model has 160 non-body representations:

| Identifier | Content | Potential use |
|---|---|---|
| `Axis` (65) | Wall/beam centerlines as `IfcPolyline` | Structural analysis, connection detection |
| `Plan` (91) | Floor plan projections | 2D drawing generation |
| `Boundary` (2) | Space boundary curves | Energy analysis |
| `WalkingLine` (2) | Stair walking lines | Accessibility analysis |

**What's needed:**
1. Extract axis curves → `compas.geometry.Polyline`
2. Store on element as `.axis` property (or similar)
3. Old code in `__old/representation.py` had `entity_axis_geometry()` and `entity_box_geometry()` — these could be revived

#### B. Parametric Decomposition (**NICE-TO-HAVE, HARD**)

Recovering the original parametric representation from an imported element:

| Want to recover | From | Difficulty |
|---|---|---|
| Profile curve + extrusion depth | `IfcExtrudedAreaSolid` → OCCBrep | Hard — need to identify which faces are the profile caps |
| Boolean tree | `IfcBooleanClippingResult` → OCCBrep | Very hard — boolean evaluation is one-way |
| Instance grouping | `IfcMappedItem` → separate OCCBreps | Medium — compare geometry hashes |

This is a research problem, not an engineering task. **Not recommended for thesis scope.**

#### C. Opening Geometry (**MEDIUM PRIORITY**)

Openings (`IfcOpeningElement`) and their relationship to walls (`IfcRelVoidsElement`) are partially handled:
- `__old/representation.py` has `entity_opening_geometry()` and `entity_body_with_opening_geometry()` that perform boolean subtraction
- Current pipeline: ifcopenshell's iterator already applies openings when tessellating
- But: the opening volumes themselves are not accessible as separate geometry objects

### 4.3 Writing: Minor Issues

| Issue | Location | Impact |
|---|---|---|
| ~~`print(pt)` debug statement in production code~~ | ~~`shapes.py:31`~~ | ~~Fixed~~ |
| `mesh_to_IfcPolygonalFaceSet` exists but never called by dispatch | `mesh.py` vs `representation.py` | Dispatch always uses `IfcFaceBasedSurfaceModel` (IFC2X3 compat) |
| `IfcAdvancedBrepWithVoids` avoided due to viewer bugs | `brep.py` | Void shells merged into single IfcClosedShell — semantic loss |
| `read_representation()` is a stub (`pass`) | `representation.py:103` | No round-trip capability |
| Representation caching uses `id(representation)` | `representation.py:34` | Cache invalid after garbage collection; breaks if same geometry assigned to multiple elements across sessions |

---

## 5. The Old Code (`__old/`) — Salvageable Assets

The `__old/` directory contains previous implementations that were never integrated into the current pipeline:

### Geometry converters (`__old/geometricmodel.py`)

| Function | Status | Salvageable? |
|---|---|---|
| `IfcExtrudedAreaSolid_to_brep()` | Implemented, working | YES — converts profile → OCC extrusion → Brep |
| `IfcBooleanResult_to_brep()` | Implemented, working | YES — recursive boolean evaluation via OCC |
| `IfcBooleanClippingResult_to_brep()` | Delegates to above | YES |
| `IfcPolygonalFaceSet_to_brep()` | Implemented, working | YES — polygons → OCC Brep |
| `IfcTriangulatedFaceSet_to_brep()` | Implemented, working | YES — triangles → OCC Brep |
| `IfcAdvancedBrep_to_brep()` | Stub (pass) | NO |
| `IfcFacetedBrep_to_brep()` | Stub (pass) | NO |
| `IfcShape_to_brep()` | Implemented | YES — generic: ifcopenshell.geom → OCC shape |
| `IfcMappedItem_to_transformation()` | Implemented | YES — extract instance transform |

### Representation handling (`__old/representation.py`)

| Function | Status | Salvageable? |
|---|---|---|
| `entity_body_geometry()` | Implemented | YES — per-item geometry extraction (not bulk iterator) |
| `entity_opening_geometry()` | Implemented | YES — opening volume extraction |
| `entity_body_with_opening_geometry()` | Implemented | YES — boolean subtract openings |
| `entity_axis_geometry()` | Implemented | YES — axis curve extraction |
| `entity_box_geometry()` | Implemented | YES — bounding box extraction |
| `entity_profile_geometry()` | Stub (pass) | NO |
| `IfcMappedItem_to_transformation()` | Implemented | YES — mapped item transform |

### Profile conversion (was in `resources/geometry.py` — deleted)

`IfcProfileDef_to_curve` was imported by the old code but the module no longer exists. This would need to be rewritten.

---

## 6. Priority Recommendations

### Tier 1: Essential for Thesis (do now)

| Task | Effort | Impact |
|---|---|---|
| **Fix `print(pt)` in `shapes.py:31`** | 1 min | Removes debug noise |
| **Use `IfcPolygonalFaceSet` for IFC4 mesh export** | 30 min | Better mesh export for IFC4 files (already implemented, just wire into dispatch) |
| **Document the gap** in thesis | — | Acknowledge that extrusion/mapped-item export is future work |

### Tier 2: High Value, Feasible for Thesis

| Task | Effort | Impact |
|---|---|---|
| **IfcExtrudedAreaSolid export** (rectangular profiles) | 2-3h | Cover the most common case: `IfcRectangleProfileDef` + direction + depth |
| **Axis representation import** | 1-2h | Revive `entity_axis_geometry()` from `__old/` — useful for connection detection thesis claims |
| **IfcMappedItem export** | 2-3h | Detect shared geometry and export as instances — significant file size benefit |

### Tier 3: Valuable but Can Be Deferred

| Task | Effort | Impact |
|---|---|---|
| **IfcExtrudedAreaSolid export** (arbitrary profiles) | 4-6h | Handle `IfcArbitraryClosedProfileDef` — polyline/composite curve profiles |
| **IfcBooleanClippingResult export** | 3-4h | Boolean tree export — rare but important for walls with clipped tops |
| **IfcTriangulatedFaceSet export** | 1-2h | With normals — better rendering quality |
| **Opening geometry access** | 2-3h | Expose opening volumes as separate geometry on elements |

### Tier 4: Future Work (Post-Thesis)

| Task | Effort | Impact |
|---|---|---|
| **IfcRevolvedAreaSolid export** | 3-4h | Rare in building models |
| **IfcSweptDiskSolid export** | 3-4h | MEP-specific |
| **CSG tree export** | 6-8h | Full boolean operation tree preservation |
| **Parametric decomposition on import** | Research | Recovering profiles from evaluated geometry |
| **Non-body representations** (Plan, Boundary, etc.) | 4-6h | Specialized uses |

---

## 7. Round-Trip Analysis

The fundamental asymmetry:

```
Import:  IfcExtrudedAreaSolid → ifcopenshell → TessellatedBrep/OCCBrep
Export:  OCCBrep → IfcAdvancedBrep  (NOT IfcExtrudedAreaSolid!)
```

A wall created in Revit as an `IfcExtrudedAreaSolid` (3 parameters: profile, direction, depth = ~50 bytes) gets imported, then re-exported as an `IfcAdvancedBrep` (NURBS surfaces, edge curves, knot vectors = ~50,000 bytes). The geometry is **mathematically equivalent** but the representation is 1000× larger and no longer parametrically editable.

This round-trip inflation is the biggest practical limitation of the current geometry pipeline and should be acknowledged in the thesis as a known trade-off: compas_ifc prioritizes **geometric fidelity** (exact shape preservation via B-Rep) over **parametric fidelity** (preserving the authoring intent).

---

## 8. Comparison with IFC Geometry Taxonomy

The IFC schema organizes geometry in a hierarchy. Here's the full picture:

```
IfcRepresentationItem
├── IfcGeometricRepresentationItem
│   ├── IfcSolidModel                        ← 3D solids
│   │   ├── IfcCsgSolid                      ✓ write (primitives only)
│   │   ├── IfcManifoldSolidBrep
│   │   │   ├── IfcAdvancedBrep              ✓ write (brep.py)
│   │   │   ├── IfcAdvancedBrepWithVoids     ⚠ write (merged into AdvancedBrep)
│   │   │   ├── IfcFacetedBrep               ✗ not written
│   │   │   └── IfcFacetedBrepWithVoids      ✗ not written
│   │   ├── IfcSweptAreaSolid
│   │   │   ├── IfcExtrudedAreaSolid         ✗ NOT WRITTEN (most common type!)
│   │   │   ├── IfcExtrudedAreaSolidTapered  ✗ not written
│   │   │   ├── IfcRevolvedAreaSolid         ✗ not written
│   │   │   └── IfcRevolvedAreaSolidTapered  ✗ not written
│   │   └── IfcSweptDiskSolid               ✗ not written
│   │
│   ├── IfcBooleanResult                     ✗ not written
│   │   └── IfcBooleanClippingResult         ✗ not written
│   │
│   ├── IfcTessellatedItem                   ← IFC4 tessellation
│   │   ├── IfcTriangulatedFaceSet           ✗ not written
│   │   └── IfcPolygonalFaceSet              ✓ write (mesh.py, not in dispatch)
│   │
│   ├── IfcSurfaceModel                      ← surface collections
│   │   ├── IfcFaceBasedSurfaceModel         ✓ write (mesh.py)
│   │   └── IfcShellBasedSurfaceModel        ✗ not written
│   │
│   ├── IfcCurve                             ← curves
│   │   ├── IfcLine                          ✓ write (in brep.py only)
│   │   ├── IfcCircle                        ✓ write (in brep.py only)
│   │   ├── IfcEllipse                       ✓ write (in brep.py only)
│   │   ├── IfcBSplineCurve                  ✓ write (in brep.py only)
│   │   ├── IfcPolyline                      ✗ not written standalone
│   │   ├── IfcCompositeCurve                ✗ not written
│   │   └── IfcTrimmedCurve                  ✗ not written
│   │
│   ├── IfcSurface                           ← surfaces
│   │   ├── IfcPlane                         ✓ write (in brep.py)
│   │   ├── IfcCylindricalSurface            ✓ write (in brep.py)
│   │   ├── IfcSphericalSurface              ✓ write (in brep.py)
│   │   ├── IfcToroidalSurface              ✓ write (in brep.py)
│   │   ├── IfcBSplineSurface               ✓ write (in brep.py, NURBS fallback)
│   │   └── IfcConicalSurface               ✗ does not exist in IFC4/4X3
│   │
│   ├── IfcCsgPrimitive3D                    ← CSG leaves
│   │   ├── IfcBlock                         ✓ write (shapes.py)
│   │   ├── IfcSphere                        ✓ write (shapes.py)
│   │   ├── IfcRightCircularCone             ✓ write (shapes.py)
│   │   └── IfcRightCircularCylinder         ✓ write (shapes.py)
│   │
│   ├── IfcMappedItem                        ✗ not written (instancing)
│   │
│   └── IfcProfileDef                        ← 2D profiles for sweeps
│       ├── IfcRectangleProfileDef           ✗ not written
│       ├── IfcCircleProfileDef              ✗ not written
│       ├── IfcArbitraryClosedProfileDef     ✗ not written
│       ├── IfcIShapeProfileDef              ✗ not written
│       └── ... (25+ profile subtypes)       ✗ none written

ALL types: ✓ read via ifcopenshell.geom.iterator() → tessellated/OCC
```

**Legend:** ✓ = actively written | ⚠ = partially written | ✗ = not written

---

## 9. OCC Mode Does Not Preserve Parametric Data

A critical finding from empirical testing: **enabling `use_occ=True` does NOT preserve any parametric information** from the original IFC representation.

### Experiment

We tested what ifcopenshell's OCC mode returns for each geometry type in the Duplex model:

| Original IFC type | OCC result | Surface types |
|---|---|---|
| `IfcExtrudedAreaSolid` (rectangle profile, depth=2.795) | `TopoDS_Compound` → 1 solid, 6 faces | **All `Plane`** |
| `IfcBooleanClippingResult` (wall - half-space) | `TopoDS_Compound` → 1 solid, 6 faces | **All `Plane`** |
| `IfcMappedItem` (door with 3 extrusions) | `TopoDS_Compound` → 3 solids, 26 faces | **All `Plane`** |
| `IfcFaceBasedSurfaceModel` (ceiling) | `TopoDS_Compound` → 16 faces (no solids) | **All `Plane`** |

**Key observations:**

1. **No `GeomAbs_SurfaceOfExtrusion` faces.** ifcopenshell's OCC kernel fully evaluates extrusions into primitive surfaces (planes, cylinders). The extrusion construction is not preserved in the OCC topology.

2. **No boolean tree.** A `BooleanClippingResult` becomes a single solid — the operand tree (first operand, operator, second operand) is completely consumed during evaluation.

3. **No instancing.** A `MappedItem` produces a standalone compound — the `IfcRepresentationMap` reference and `IfcCartesianTransformationOperator3D` transform are lost.

4. **Calling `create_shape()` on raw items also evaluates.** Even `ifcopenshell.geom.create_shape(settings, IfcExtrudedAreaSolid)` returns a fully-evaluated `TopoDS_Compound`, not a construction-aware OCC shape.

### Concrete example

```
Original IFC:
  IfcExtrudedAreaSolid #350
    SweptArea: IfcRectangleProfileDef (XDim=3.583, YDim=0.124)
    ExtrudedDirection: (0, 0, 1)
    Depth: 2.587

After ifcopenshell.geom → OCC:
  TopoDS_Compound
    └─ TopoDS_Solid
       └─ TopoDS_Shell
          ├─ Face 0: GeomAbs_Plane  (area=10.01)
          ├─ Face 1: GeomAbs_Plane  (area=0.35)
          ├─ Face 2: GeomAbs_Plane  (area=10.01)
          ├─ Face 3: GeomAbs_Plane  (area=0.35)
          ├─ Face 4: GeomAbs_Plane  (area=0.44)
          └─ Face 5: GeomAbs_Plane  (area=0.44)

  → The profile (rectangle 3.583×0.124) and depth (2.587) are GONE.
  → You can measure face areas, but cannot recover the original parameters.
```

### Architectural implication

Since ifcopenshell's geometry kernel is a **one-way evaluator** regardless of OCC mode, preserving parametric data requires a fundamentally different approach:

```
┌─────────────────────────────────────────────────┐
│                  IFC File                        │
│                                                  │
│  IfcExtrudedAreaSolid                           │
│    SweptArea: IfcRectangleProfileDef(3.58, 0.12) │
│    Direction: (0, 0, 1)                          │
│    Depth: 2.587                                  │
└───────────┬──────────────────┬───────────────────┘
            │                  │
    Path A: ifcopenshell.geom  │  Path B: Direct IFC entity parsing
    (evaluate → OCC/tess)      │  (read → typed Python objects)
            │                  │
            ▼                  ▼
    ┌──────────────┐    ┌─────────────────────┐
    │ .geometry    │    │ .representation      │
    │ OCCBrep /    │    │ Extrusion(           │
    │ TessellatedBr│    │   profile=Rectangle, │
    │ (for viz)    │    │   depth=2.587,       │
    │              │    │   direction=(0,0,1)) │
    └──────────────┘    └─────────────────────┘
```

- **Path A** (current): fast, handles everything, but destructive
- **Path B** (proposed): reads the raw IFC entity graph via `Base.__getattr__` delegation, wraps in typed Python objects that preserve all parameters

Both paths can coexist. Path A is already working well for visualization. Path B would enable round-trip fidelity and parametric queries.

---

## 10. COMPAS Geometry Types vs IFC Export

| COMPAS Type | Available? | Current IFC Export | Ideal IFC Export |
|---|---|---|---|
| `Box` | YES | `IfcBlock` (CSG) | `IfcBlock` ✓ |
| `Sphere` | YES | `IfcSphere` (CSG) | `IfcSphere` ✓ |
| `Cone` | YES | `IfcRightCircularCone` (CSG) | `IfcRightCircularCone` ✓ |
| `Cylinder` | YES | `IfcRightCircularCylinder` (CSG) | `IfcRightCircularCylinder` ✓ |
| `Torus` | YES | Not handled (raises error) | `IfcCsgSolid` or `IfcAdvancedBrep` |
| `Capsule` | YES | Not handled (raises error) | `IfcAdvancedBrep` |
| `Polyhedron` | YES | Not handled (raises error) | `IfcFacetedBrep` |
| `Mesh` | YES | `IfcFaceBasedSurfaceModel` | `IfcPolygonalFaceSet` (IFC4) or `IfcFacetedBrep` |
| `Brep` | YES | `IfcAdvancedBrep` | `IfcAdvancedBrep` ✓ |
| `NurbsSurface` | YES | Not handled directly | Via `Brep` → `IfcAdvancedBrep` |
| `NurbsCurve` | YES | Not handled directly | Via `Brep` edge curves |
| `Polygon` | YES | Not handled | `IfcPolyline` (2D) |
| `Polyline` | YES | Not handled | `IfcPolyline` |
| `Circle` | YES | Not handled standalone | `IfcCircle` |
| `Ellipse` | YES | Not handled standalone | `IfcEllipse` |
| `Line` | YES | Not handled standalone | `IfcLine` |
| `Pointcloud` | YES | Not handled | No direct IFC equivalent |
| `Extrusion` | NO (doesn't exist in COMPAS) | — | Would need `IfcExtrudedAreaSolid` |

---

## 11. Profile Types in Practice

From the Duplex model, the 421 `IfcExtrudedAreaSolid` + `IfcMappedItem` instances use these profile types:

| Profile Type | Count | % | COMPAS equivalent |
|---|---|---|---|
| `IfcRectangleProfileDef` | 293 | 70% | `(width, height)` tuple |
| `IfcArbitraryClosedProfileDef` | 102 | 24% | `Polygon` or `Polyline` |
| `IfcArbitraryProfileDefWithVoids` | 18 | 4% | `Polygon` + list of `Polygon` (holes) |
| `IfcCircleProfileDef` | 8 | 2% | `Circle` |

This tells us that implementing just `IfcRectangleProfileDef` would cover 70% of cases. Adding `IfcArbitraryClosedProfileDef` (polyline profiles) would cover 94%.
