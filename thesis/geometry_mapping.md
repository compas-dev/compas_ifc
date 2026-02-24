# Bidirectional Geometry Mapping: COMPAS ↔ IFC

> **Date:** 2026-02-24
> **COMPAS version:** 2.15.0
> **IFC schema:** IFC4
> **Purpose:** Define every mapping between COMPAS geometry types and IFC entities, for both reading and writing.

---

## 1. Mapping Legend

| Symbol | Meaning |
|---|---|
| ✅ | Implemented and working |
| 🔧 | Partially implemented or needs fix |
| ❌ | Not implemented |
| ➖ | No direct equivalent / not applicable |
| 🔄 | Via intermediate conversion (lossy) |

---

## 2. Points, Vectors, Frames (Foundational)

These are building blocks used inside other representations, not standalone geometry.

| COMPAS Type | IFC Entity | Write | Read | Notes |
|---|---|---|---|---|
| `Point` | `IfcCartesianPoint` | ✅ | ✅ | Used everywhere internally |
| `Vector` | `IfcDirection` | ✅ | ✅ | Direction only (unit vector) |
| `Vector` | `IfcVector` | ✅ | ✅ | Direction + magnitude |
| `Frame` | `IfcAxis2Placement3D` | ✅ | ✅ | `frame.py`: `create_IfcAxis2Placement3D` |
| `Frame` | `IfcLocalPlacement` | ✅ | ✅ | `frame.py`: `assign_entity_frame` / `IfcLocalPlacement_to_transformation` |
| `Plane` | `IfcPlane` | ✅ | ✅ | Used in brep.py for planar faces |
| `Transformation` | `IfcCartesianTransformationOperator3D` | ❌ | 🔧 | Old code had `IfcCartesianTransformationOperator3D_to_frame` |

---

## 3. Curves

### 3.1 Writing: COMPAS Curve → IFC Curve

| COMPAS Curve | IFC Entity | Status | Where | Notes |
|---|---|---|---|---|
| `Line` | `IfcLine` | 🔧 | `brep.py` | Only as B-Rep edge curves, not standalone |
| `Polyline` | `IfcPolyline` | ❌ | — | Not written. Needed for axis reps, profiles |
| `Polygon` | `IfcPolyline` (closed) | ❌ | — | Polygon = closed polyline in IFC |
| `Circle` | `IfcCircle` | 🔧 | `brep.py` | Only as B-Rep edge curves |
| `Arc` | `IfcTrimmedCurve(IfcCircle)` | ❌ | — | Arc = trimmed circle in IFC |
| `Ellipse` | `IfcEllipse` | 🔧 | `brep.py` | Only as B-Rep edge curves |
| `NurbsCurve` | `IfcRationalBSplineCurveWithKnots` | 🔧 | `brep.py` | Only as B-Rep edge curves |
| `Bezier` | `IfcRationalBSplineCurveWithKnots` | ❌ | — | Convert to NURBS first |
| `Parabola` | ➖ | ➖ | — | No direct IFC entity |
| `Hyperbola` | ➖ | ➖ | — | No direct IFC entity |

**Gap:** All curve types are only written inside B-Rep topology. None can be written as standalone curve geometry (e.g., for axis representations or profile definitions).

### 3.2 Reading: IFC Curve → COMPAS Curve

| IFC Entity | COMPAS Type | Status | Notes |
|---|---|---|---|
| `IfcLine` | `Line` | ❌ | Not parsed. ifcopenshell evaluates away |
| `IfcPolyline` | `Polyline` | ❌ | Not parsed. Would be needed for axis import |
| `IfcCircle` | `Circle` | ❌ | Not parsed directly |
| `IfcEllipse` | `Ellipse` | ❌ | Not parsed directly |
| `IfcTrimmedCurve` | `Arc` / `NurbsCurve` | ❌ | Not parsed |
| `IfcCompositeCurve` | `Polyline` or list of curves | ❌ | Not parsed |
| `IfcBSplineCurveWithKnots` | `NurbsCurve` | ❌ | Not parsed |
| `IfcRationalBSplineCurveWithKnots` | `NurbsCurve` | ❌ | Not parsed |
| `IfcIndexedPolyCurve` | `Polyline` | 🔧 | Old code had `IfcIndexedPolyCurve_to_lines` |

**Gap:** No curve types are read directly from IFC. All are consumed by ifcopenshell's geometry evaluator.

---

## 4. Surfaces

### 4.1 Writing: COMPAS Surface → IFC Surface

| COMPAS Surface | IFC Entity | Status | Where | Notes |
|---|---|---|---|---|
| `PlanarSurface` | `IfcPlane` | 🔧 | `brep.py` | Only as B-Rep face surfaces |
| `CylindricalSurface` | `IfcCylindricalSurface` | 🔧 | `shapes.py` | Only as B-Rep face surfaces |
| `SphericalSurface` | `IfcSphericalSurface` | 🔧 | `shapes.py` | Only as B-Rep face surfaces |
| `ConicalSurface` | ➖ | ➖ | — | `IfcConicalSurface` does NOT exist in IFC4 |
| `ToroidalSurface` | `IfcToroidalSurface` | 🔧 | `shapes.py` | Only as B-Rep face surfaces |
| `NurbsSurface` | `IfcRationalBSplineSurfaceWithKnots` | 🔧 | `brep.py` | Only as B-Rep face surfaces (NURBS fallback) |

**Note:** All surface types are written exclusively within `IfcAdvancedFace` topology (B-Rep). There is no standalone surface export.

### 4.2 Reading: IFC Surface → COMPAS Surface

| IFC Entity | COMPAS Type | Status | Notes |
|---|---|---|---|
| `IfcPlane` | `PlanarSurface` / `Plane` | ❌ | Not parsed; evaluated by ifcopenshell |
| `IfcCylindricalSurface` | `CylindricalSurface` | ❌ | Not parsed |
| `IfcSphericalSurface` | `SphericalSurface` | ❌ | Not parsed |
| `IfcToroidalSurface` | `ToroidalSurface` | ❌ | Not parsed |
| `IfcBSplineSurfaceWithKnots` | `NurbsSurface` | ❌ | Not parsed |
| `IfcSurfaceOfRevolution` | ➖ | ❌ | No COMPAS equivalent |
| `IfcSurfaceOfLinearExtrusion` | ➖ | ❌ | No COMPAS equivalent |

---

## 5. Shapes (CSG Primitives)

### 5.1 Writing: COMPAS Shape → IFC CSG Primitive

| COMPAS Shape | IFC Entity | Status | Where | Notes |
|---|---|---|---|---|
| `Box` | `IfcBlock` → `IfcCsgSolid` | ✅ | `shapes.py` | Wrapped in `IfcCsgSolid` |
| `Sphere` | `IfcSphere` → `IfcCsgSolid` | ✅ | `shapes.py` | |
| `Cone` | `IfcRightCircularCone` → `IfcCsgSolid` | ✅ | `shapes.py` | |
| `Cylinder` | `IfcRightCircularCylinder` → `IfcCsgSolid` | ✅ | `shapes.py` | |
| `Torus` | ❌ | ❌ | — | No `IfcTorus` CSG primitive. Use `IfcAdvancedBrep` via Brep.from_torus |
| `Capsule` | ❌ | ❌ | — | No IFC equivalent. Use `IfcAdvancedBrep` via Brep |
| `Polyhedron` | ❌ | ❌ | — | Use `IfcFacetedBrep` or Mesh export |

### 5.2 Reading: IFC CSG Primitive → COMPAS Shape

| IFC Entity | COMPAS Type | Status | Notes |
|---|---|---|---|
| `IfcBlock` | `Box` | ❌ | Could map directly: XLength/YLength/ZLength + Position |
| `IfcSphere` | `Sphere` | ❌ | Could map directly: Radius + Position |
| `IfcRightCircularCone` | `Cone` | ❌ | Could map directly: Height/BottomRadius + Position |
| `IfcRightCircularCylinder` | `Cylinder` | ❌ | Could map directly: Height/Radius + Position |
| `IfcRectangularPyramid` | `Polyhedron` | ❌ | Would need custom construction |

**Gap:** None of the CSG primitives are read back into COMPAS shapes. All go through ifcopenshell → tessellation/OCC.

---

## 6. Solids (the main geometry representations)

### 6.1 Writing: COMPAS → IFC Solid

| COMPAS Type | IFC Entity | RepresentationType | Status | Where |
|---|---|---|---|---|
| `Box/Sphere/Cone/Cylinder` | `IfcCsgSolid` | "CSG" | ✅ | `shapes.py` + `representation.py` |
| `Mesh` | `IfcFaceBasedSurfaceModel` | "SurfaceModel" | ✅ | `mesh.py` |
| `Mesh` | `IfcPolygonalFaceSet` | "Tessellation" | 🔧 | `mesh.py` — implemented but not wired into dispatch |
| `Mesh` | `IfcFacetedBrep` | "Brep" | ❌ | Would give solid semantics (closed=True meshes) |
| `Mesh` | `IfcTriangulatedFaceSet` | "Tessellation" | ❌ | IFC4 indexed triangles with optional normals |
| `Brep` (with OCC) | `IfcAdvancedBrep` | "SolidModel" | ✅ | `brep.py` |
| `Brep` (no OCC) | `IfcFaceBasedSurfaceModel` | "SurfaceModel" | 🔄 | Tessellated fallback via `mesh.py` |
| `Brep.from_extrusion(profile, vector)` | `IfcExtrudedAreaSolid` | "SweptSolid" | ❌ | **Most common type in real files!** |
| `Brep.from_sweep(profile, path)` | `IfcSurfaceCurveSweptAreaSolid` | "AdvancedSweptSolid" | ❌ | Rare |
| `Brep.from_pipe(path, radius)` | `IfcSweptDiskSolid` | "SweptSolid" | ❌ | Circle swept along directrix |
| `Brep.from_loft(curves)` | `IfcAdvancedBrep` | "SolidModel" | 🔄 | No parametric loft in IFC; falls back to B-Rep |
| `Brep` (boolean result) | `IfcBooleanResult` | "CSG" | ❌ | Boolean tree not preserved |
| `Torus` | `IfcAdvancedBrep` | "SolidModel" | ❌ | Via `Brep.from_torus()` → brep.py |
| `Capsule` | `IfcAdvancedBrep` | "SolidModel" | ❌ | Via `Brep` → brep.py |

### 6.2 Reading: IFC Solid → COMPAS

| IFC Entity | COMPAS Type | Status | Notes |
|---|---|---|---|
| `IfcExtrudedAreaSolid` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated by ifcopenshell. Parameters lost. |
| `IfcExtrudedAreaSolid` | `Extrusion(profile, direction, depth)` | ❌ | **Proposed**: Direct parsing of IFC entity graph |
| `IfcRevolvedAreaSolid` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. Parameters lost. |
| `IfcSweptDiskSolid` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. Parameters lost. |
| `IfcCsgSolid` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. CSG tree lost. |
| `IfcAdvancedBrep` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. Topology preserved in OCC mode. |
| `IfcFacetedBrep` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. |
| `IfcBooleanResult` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. Boolean tree lost. |
| `IfcBooleanClippingResult` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. |
| `IfcFaceBasedSurfaceModel` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. |
| `IfcTriangulatedFaceSet` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. |
| `IfcPolygonalFaceSet` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. |
| `IfcMappedItem` | `TessellatedBrep` / `OCCBrep` (per instance) | 🔄 | Instancing relationship lost. |

**All reading goes through ifcopenshell.geom → evaluated shape. No parametric data is preserved.**

---

## 7. Profiles (2D cross-sections for extrusions/sweeps)

Profiles are the 2D shapes used by `IfcExtrudedAreaSolid`, `IfcRevolvedAreaSolid`, etc.

### 7.1 Writing: COMPAS 2D Geometry → IFC Profile

| COMPAS Type | IFC Profile | Status | Notes |
|---|---|---|---|
| `(width, height)` tuple | `IfcRectangleProfileDef` | ❌ | Most common profile (70% of Duplex) |
| `(width, height, wall_thickness)` | `IfcRectangleHollowProfileDef` | ❌ | Hollow rectangular sections |
| `Circle` | `IfcCircleProfileDef` | ❌ | Columns, pipes (2% of Duplex) |
| `Circle` (inner+outer) | `IfcCircleHollowProfileDef` | ❌ | Hollow circular sections |
| `Ellipse` | `IfcEllipseProfileDef` | ❌ | Rare |
| `Polygon` / `Polyline` | `IfcArbitraryClosedProfileDef` | ❌ | Arbitrary shapes (24% of Duplex) |
| `Polygon` + list[`Polygon`] | `IfcArbitraryProfileDefWithVoids` | ❌ | With holes (4% of Duplex) |
| ➖ | `IfcIShapeProfileDef` | ❌ | I-beam (could map from params dict) |
| ➖ | `IfcCShapeProfileDef` | ❌ | C-channel |
| ➖ | `IfcLShapeProfileDef` | ❌ | L-angle |
| ➖ | `IfcTShapeProfileDef` | ❌ | T-section |
| ➖ | `IfcUShapeProfileDef` | ❌ | U-channel |
| ➖ | `IfcZShapeProfileDef` | ❌ | Z-section |
| ➖ | `IfcTrapeziumProfileDef` | ❌ | Trapezoid |

### 7.2 Reading: IFC Profile → COMPAS 2D Geometry

| IFC Profile | COMPAS Type | Status | Notes |
|---|---|---|---|
| `IfcRectangleProfileDef` | `(XDim, YDim)` or `Polygon` | ❌ | Trivial to implement |
| `IfcCircleProfileDef` | `Circle` | ❌ | Trivial |
| `IfcEllipseProfileDef` | `Ellipse` | ❌ | Trivial |
| `IfcArbitraryClosedProfileDef` | `Polygon` / `Polyline` | ❌ | Parse `.OuterCurve` |
| `IfcArbitraryProfileDefWithVoids` | `Polygon` + list[`Polygon`] | ❌ | Parse `.OuterCurve` + `.InnerCurves` |
| `IfcIShapeProfileDef` | params dict or `Polygon` | ❌ | Convert to polygon outline |
| `IfcCompositeProfileDef` | list of profiles | ❌ | Recursive |

**Old code:** `IfcProfileDef_to_curve` existed in `resources/geometry.py` (now deleted).

---

## 8. Topology (B-Rep building blocks)

These are used inside `IfcAdvancedBrep` and are fully handled by `brep.py`.

| IFC Entity | COMPAS B-Rep Type | Write | Read | Notes |
|---|---|---|---|---|
| `IfcClosedShell` | Brep shell | ✅ | 🔄 | Written in brep.py |
| `IfcAdvancedFace` | `BrepFace` | ✅ | 🔄 | Written in brep.py |
| `IfcFaceOuterBound` | `BrepLoop` (outer) | ✅ | 🔄 | |
| `IfcFaceBound` | `BrepLoop` (inner) | ✅ | 🔄 | |
| `IfcEdgeLoop` | `BrepLoop` | ✅ | 🔄 | |
| `IfcOrientedEdge` | `BrepEdge` | ✅ | 🔄 | |
| `IfcEdgeCurve` | `BrepEdge` | ✅ | 🔄 | |
| `IfcVertexPoint` | `BrepVertex` | ✅ | 🔄 | |
| `IfcPolyLoop` | — | ✅ | 🔄 | Used in mesh.py for FaceBasedSurfaceModel |
| `IfcFace` | — | ✅ | 🔄 | Used in mesh.py |
| `IfcConnectedFaceSet` | — | ✅ | 🔄 | Used in mesh.py |

---

## 9. Representation Containers & Instancing

| IFC Entity | Purpose | Write | Read | Notes |
|---|---|---|---|---|
| `IfcShapeRepresentation` | Groups geometry items with context | ✅ | ✅ | `representation.py` |
| `IfcProductDefinitionShape` | Assigns representations to products | ✅ | ✅ | |
| `IfcRepresentationMap` | Defines reusable geometry template | ❌ | ❌ | Needed for instancing |
| `IfcMappedItem` | Instance of mapped representation | ❌ | 🔄 | Read as separate geometry copy (instancing lost) |
| `IfcCartesianTransformationOperator3D` | Transform for mapped items | ❌ | 🔧 | Old code had converter |

---

## 10. Non-Body Representations

| RepresentationIdentifier | IFC Geometry Used | COMPAS Target | Write | Read |
|---|---|---|---|---|
| `"Body"` | Solids, B-Rep, CSG, etc. | `Brep` / `Mesh` / shapes | ✅ | ✅ |
| `"Axis"` | `IfcPolyline` | `Polyline` | ❌ | ❌ |
| `"Plan"` | `IfcGeometricSet` | list of curves | ❌ | ❌ |
| `"Box"` | `IfcBoundingBox` | `Box` | ❌ | 🔧 |
| `"Boundary"` | `IfcGeometricSet` | list of curves | ❌ | ❌ |
| `"WalkingLine"` | `IfcPolyline` | `Polyline` | ❌ | ❌ |
| `"Profile"` | profile curves | curves | ❌ | ❌ |
| `"Surface"` | surface geometry | surfaces | ❌ | ❌ |

---

## 11. Placement & Transformations

| IFC Entity | COMPAS Type | Write | Read | Notes |
|---|---|---|---|---|
| `IfcAxis2Placement3D` | `Frame` | ✅ | ✅ | `frame.py` |
| `IfcAxis2Placement2D` | `Frame` (2D) | ❌ | ❌ | Needed for profiles |
| `IfcLocalPlacement` | `Frame` / `Transformation` | ✅ | ✅ | `frame.py` |
| `IfcAxis1Placement` | `(Point, Vector)` | ❌ | ❌ | Needed for revolved solids |
| `IfcCartesianTransformationOperator3D` | `Transformation` | ❌ | 🔧 | Needed for mapped items |

---

## 12. Summary: Implementation Status by Category

| Category | Total Mappings | ✅ Done | 🔧 Partial | ❌ Missing |
|---|---|---|---|---|
| **Points/Vectors/Frames** | 7 | 5 | 1 | 1 |
| **Curves (write)** | 10 | 0 | 4 | 6 |
| **Curves (read)** | 9 | 0 | 1 | 8 |
| **Surfaces (write)** | 6 | 0 | 5 | 1 |
| **Surfaces (read)** | 7 | 0 | 0 | 7 |
| **Shapes/CSG (write)** | 7 | 4 | 0 | 3 |
| **Shapes/CSG (read)** | 5 | 0 | 0 | 5 |
| **Solids (write)** | 13 | 2 | 2 | 9 |
| **Solids (read)** | 12 | 0 | 0 | 12* |
| **Profiles (write)** | 14 | 0 | 0 | 14 |
| **Profiles (read)** | 7 | 0 | 0 | 7 |
| **Topology (B-Rep)** | 11 | 8 | 0 | 3 |
| **Containers/Instancing** | 5 | 2 | 1 | 2 |
| **Non-Body Reps** | 8 | 1 | 1 | 6 |
| **Placements** | 5 | 2 | 1 | 2 |
| **TOTAL** | **126** | **24** | **16** | **86** |

*All 12 solid reads work via ifcopenshell (🔄), but none preserve parametric data.

---

## 13. Priority Implementation Order

Based on frequency in real IFC files (Duplex model) and practical value:

### Phase 1: Extrusion Pipeline (covers ~70% of real geometry)

```
Write:  COMPAS geometry + profile params → IfcExtrudedAreaSolid
Read:   IfcExtrudedAreaSolid → typed Extrusion object

Requires implementing:
  1. IfcRectangleProfileDef       ← covers 70% of profiles
  2. IfcArbitraryClosedProfileDef ← covers 94% total
  3. IfcCircleProfileDef          ← covers 96%
  4. IfcExtrudedAreaSolid assembly
  5. Extrusion reader (parse entity graph)
```

### Phase 2: Curves & Non-Body Representations

```
Write:  Polyline → IfcPolyline (standalone)
        Polygon → IfcPolyline (closed)
Read:   IfcPolyline → Polyline (for axis representations)

Requires implementing:
  1. Standalone curve writers
  2. Axis representation reader
  3. Wire into IfcProduct.axis property
```

### Phase 3: Instancing

```
Write:  Shared geometry detection → IfcRepresentationMap + IfcMappedItem
Read:   IfcMappedItem → geometry + transform (preserve instancing)

Requires implementing:
  1. IfcRepresentationMap creation
  2. IfcMappedItem creation
  3. IfcCartesianTransformationOperator3D writer
  4. Shared geometry detection in export pipeline
```

### Phase 4: CSG Round-Trip

```
Write:  COMPAS Shape → direct IfcCsgPrimitive (already done)
Read:   IfcBlock → Box, IfcSphere → Sphere, etc. (parse entity graph)

Requires implementing:
  1. IfcBlock → Box reader
  2. IfcSphere → Sphere reader
  3. IfcRightCircularCone → Cone reader
  4. IfcRightCircularCylinder → Cylinder reader
```

### Phase 5: Missing Shapes & Mesh Improvements

```
Write:  Torus → IfcAdvancedBrep (via Brep.from_torus)
        Capsule → IfcAdvancedBrep (via Brep)
        Mesh → IfcPolygonalFaceSet (IFC4 dispatch)
        Mesh → IfcTriangulatedFaceSet
Read:   (covered by ifcopenshell)
```

### Phase 6: Remaining Swept Solids

```
Write:  Brep.from_pipe() → IfcSweptDiskSolid
        Profile + axis + angle → IfcRevolvedAreaSolid
Read:   Parse from entity graph
```
