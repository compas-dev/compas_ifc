# Formal Round-Trip Tests for Thesis

## Context

The thesis needs a definitive demonstration that `compas_ifc`'s parametric geometry pipeline preserves data through IFC write-read cycles. We have ~10 geometry types with full round-trip support, plus 2 real-world models (Duplex, HiLo). The tests must systematically cover every type with clear pass/fail results suitable for thesis presentation.

---

## Geometry Type Inventory

### Fully Supported (read + write round-trip)

| # | COMPAS Type | IFC Entity | Variants |
|---|---|---|---|
| 1 | `Extrusion` | `IfcExtrudedAreaSolid` | Polygon, Circle, ProfileWithVoids |
| 2 | `Revolution` | `IfcRevolvedAreaSolid` | Polygon (partial angle), Circle (full 360) |
| 3 | `Pipe` | `IfcSweptDiskSolid` | Solid, Hollow (inner radius) |
| 4 | `ClippedExtrusion` | `IfcBooleanClippingResult` chain | 1 clip, 2+ clips |
| 5 | `BooleanResult` | `IfcBooleanResult` | UNION, DIFFERENCE, INTERSECTION, nested |
| 6 | `HalfSpace` | `IfcHalfSpaceSolid` | As boolean operand |
| 7 | `Box` | `IfcBlock` (in `IfcCsgSolid`) | — |
| 8 | `Sphere` | `IfcSphere` (in `IfcCsgSolid`) | — |
| 9 | `Cone` | `IfcRightCircularCone` (in `IfcCsgSolid`) | — |
| 10 | `Cylinder` | `IfcRightCircularCylinder` (in `IfcCsgSolid`) | — |
| 11 | `Mesh` | `IfcPolygonalFaceSet` | Polygon faces |
| 12 | Instancing | `IfcMappedItem` / `IfcRepresentationMap` | Shared geometry |

### Separate Test (later)

| Type | Notes |
|---|---|
| `Brep` | `IfcAdvancedBrep` write (via `compas_occ`) + read-back as full Brep. Separate script, dealt with later. |

### Not Supported

| IFC Type | Reason |
|---|---|
| `IfcSurfaceOfRevolution` | Sweep surface, not solid |
| `IfcSurfaceOfLinearExtrusion` | Sweep surface, not solid |
| `IfcConicalSurface` | Doesn't exist in IFC4/IFC4X3 |
| B-Spline / NURBS profiles | Only line-segment and circle profiles parsed |
| `IfcEllipseProfileDef` | Read samples to polygon; no Ellipse class to write back |
| `IfcPolygonalBoundedHalfSpace` | Read ignores boundary polygon (plane only) |

---

## Script Structure

Three scripts in `thesis/` (repo root):

### 1. `thesis/roundtrip_generated.py`

Creates one IFC model with all supported geometry types, saves, reloads, and verifies parametric data preservation.

**Test cases:**

| ID | Name | Geometry | Key Checks |
|---|---|---|---|
| A1 | `Ext_Polygon` | Extrusion, 4-pt polygon, depth=3.0 | type, depth, profile point count, direction |
| A2 | `Ext_Circle` | Extrusion, circle (r=0.5), depth=2.0 | type, depth, profile radius |
| A3 | `Ext_Voids` | Extrusion, polygon + 1 void, depth=0.3 | type, depth, outer pts, void count |
| A4 | `Rev_Circle` | Revolution 360, circle (r=0.1) | type, angle, profile radius |
| A5 | `Rev_Polygon` | Revolution 180, polygon profile | type, angle, profile point count |
| A6 | `Pipe_Solid` | Pipe, 3-pt directrix, r=0.15 | type, radius, inner_radius is None, directrix pts |
| A7 | `Pipe_Hollow` | Pipe, inner_r=0.10 | type, radius, inner_radius |
| A8 | `CSG_Box` | Box(1, 2, 3) | type, xsize, ysize, zsize |
| A9 | `CSG_Sphere` | Sphere(r=1.5) | type, radius |
| A10 | `CSG_Cone` | Cone(r=1.0, h=2.5) | type, radius, height |
| A11 | `CSG_Cylinder` | Cylinder(r=0.4, h=3.0) | type, radius, height |
| A12 | `Clip_Single` | ClippedExtrusion, 1 clip | type, extrusion.depth, len(clips)==1, plane normal, agreement |
| A13 | `Clip_Double` | ClippedExtrusion, 2 clips | type, extrusion.depth, len(clips)==2 |
| A14 | `Bool_Diff` | BooleanResult DIFFERENCE (ext-ext) | type, operator, operand types |
| A15 | `Bool_Union` | BooleanResult UNION (ext+ext) | type, operator, operand types |
| A16 | `Bool_Inter` | BooleanResult INTERSECTION (ext&ext) | type, operator, operand types |
| A17 | `Bool_Nested` | BooleanResult DIFF(UNION(ext,ext), halfspace) | type, operator, depth>=2, leaf count |
| A18 | `Bool_HalfSpace` | BooleanResult DIFF (ext-halfspace) | type, second is HalfSpace, plane data |
| A19 | `Mesh_Quad` | Mesh (box-like polygon faces) | type, n_vertices>=8, n_faces>=6 |
| A20-22 | `Instance_1..3` | 3 columns sharing Cylinder geometry | type match, RepMap=1, MappedItem=2 |

**IFC entity count checks** (on saved file):
- IfcExtrudedAreaSolid, IfcRevolvedAreaSolid, IfcSweptDiskSolid, IfcCsgSolid
- IfcBooleanClippingResult, IfcBooleanResult
- IfcPolygonalFaceSet, IfcRepresentationMap, IfcMappedItem

**Output:** `temp/thesis_roundtrip_generated.ifc`

### 2. `thesis/roundtrip_duplex.py`

Loads `data/Duplex_A_20110907.ifc` (IFC2X3, ~265 elements), verifies parsing and parametric data.

**Checks:**
| Check | Expected |
|---|---|
| Total elements with geometry | >= 260 |
| Parse errors | 0 |
| Extrusion count | >= 190 |
| Mesh count | >= 50 |
| All extrusion depths > 0 | True |
| All extrusion profiles valid | True |

**Prints:** Geometry type distribution table (type, count, %).

### 3. `thesis/roundtrip_hilo.py`

Loads `temp/1072_HiLo_Model-Architecture.ifc` (IFC2X3, ~1920 elements), verifies parsing including boolean clipping.

**Checks:**
| Check | Expected |
|---|---|
| Total elements with geometry | >= 1400 |
| Parse errors | 0 |
| Extrusion count | >= 1000 |
| ClippedExtrusion count | >= 120 |
| BooleanResult count | >= 0 |
| TessellatedBrep count | >= 200 |
| All ClippedExtrusion clips valid | True |
| All BooleanResult operands valid | True |

**Prints:** Geometry type distribution table (type, count, %).

### (Later) `thesis/roundtrip_brep.py`

B-Rep round-trip via `compas_occ`. Separate implementation. Not part of this task.

---

## Shared Test Infrastructure

All three scripts share the same `check()` pattern and summary format:

```python
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
```

Summary output at end:
```
======================================================================
SUMMARY
======================================================================

  PASS  Ext_Polygon type=Extrusion              (Extrusion)
  PASS  Ext_Polygon depth=3.0                    (3.0)
  ...

  42 PASS / 0 FAIL (of 42 checks)

SUCCESS: All round-trip tests passed.
```

Exit code 1 if any failures.

---

## Key Files

- **New:** `thesis/roundtrip_generated.py`, `thesis/roundtrip_duplex.py`, `thesis/roundtrip_hilo.py`
- **Refs:** `src/compas_ifc/representations/*.py`, `src/compas_ifc/conversions/reading.py`, `src/compas_ifc/conversions/representation.py`
- **Test data:** `data/Duplex_A_20110907.ifc`, `temp/1072_HiLo_Model-Architecture.ifc`
- **Output:** `temp/thesis_roundtrip_generated.ifc`

## Verification

1. `cmd.exe /c "conda run -n compas-ifc python thesis/roundtrip_generated.py"` — all PASS
2. `cmd.exe /c "conda run -n compas-ifc python thesis/roundtrip_duplex.py"` — all PASS
3. `cmd.exe /c "conda run -n compas-ifc python thesis/roundtrip_hilo.py"` — all PASS (requires HiLo file in temp/)
4. `invoke test` — existing pytest still passes
5. Existing scripts 16-20 unchanged
