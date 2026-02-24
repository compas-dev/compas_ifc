# Bidirectional Geometry Mapping: COMPAS ↔ IFC

> **Date:** 2026-02-24 (updated after Phase 5+6 implementation)
> **COMPAS version:** 2.15.0
> **IFC schema:** IFC4
> **Purpose:** Define every mapping between COMPAS geometry types and IFC entities, for both reading and writing.
> **New types:** `compas_ifc.representations.Extrusion`, `Revolution`, `Pipe` — parametric solids preserving swept solid parameters from IFC.

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
| `Transformation` | `IfcCartesianTransformationOperator3D` | ❌ | ✅ | `reading.py`: `_cartesian_transform_operator_to_transformation` |

---

## 3. Curves

### 3.1 Writing: COMPAS Curve → IFC Curve

| COMPAS Curve | IFC Entity | Status | Where | Notes |
|---|---|---|---|---|
| `Line` | `IfcLine` | 🔧 | `brep.py` | Only as B-Rep edge curves, not standalone |
| `Polyline` | `IfcPolyline` | ✅ | `representation.py` | `polyline_to_IfcPolyline` — standalone open curve |
| `Polygon` | `IfcPolyline` (closed) | ✅ | `representation.py` | `polygon_to_IfcPolyline` — standalone closed curve |
| `Circle` | `IfcCircle` | 🔧 | `brep.py` | Only as B-Rep edge curves |
| `Arc` | `IfcTrimmedCurve(IfcCircle)` | ❌ | — | Arc = trimmed circle in IFC |
| `Ellipse` | `IfcEllipse` | 🔧 | `brep.py` | Only as B-Rep edge curves |
| `NurbsCurve` | `IfcRationalBSplineCurveWithKnots` | 🔧 | `brep.py` | Only as B-Rep edge curves |
| `Bezier` | `IfcRationalBSplineCurveWithKnots` | ❌ | — | Convert to NURBS first |
| `Parabola` | ➖ | ➖ | — | No direct IFC entity |
| `Hyperbola` | ➖ | ➖ | — | No direct IFC entity |

**Note:** `Polyline` and `Polygon` can now be written as standalone curves (e.g., for axis representations). Other curve types are still only written inside B-Rep topology.

### 3.2 Reading: IFC Curve → COMPAS Curve

| IFC Entity | COMPAS Type | Status | Notes |
|---|---|---|---|
| `IfcLine` | `Line` | ❌ | Not parsed standalone. Handled inside composite curves |
| `IfcPolyline` | `Polygon` / `Polyline` | ✅ | `reading.py`: `Polygon` for profiles, `Polyline` for axis reps |
| `IfcCircle` | `Circle` | 🔧 | Parsed inside `IfcTrimmedCurve` (arc sampling), not standalone |
| `IfcEllipse` | `Ellipse` | ❌ | Not parsed directly |
| `IfcTrimmedCurve` | `Polygon` (sampled) | ✅ | `reading.py`: arc segments sampled to polygon points |
| `IfcCompositeCurve` | `Polygon` | ✅ | `reading.py`: segments concatenated into polygon |
| `IfcBSplineCurveWithKnots` | `NurbsCurve` | ❌ | Not parsed |
| `IfcRationalBSplineCurveWithKnots` | `NurbsCurve` | ❌ | Not parsed |
| `IfcIndexedPolyCurve` | `Polygon` | ✅ | `reading.py`: parsed as profile curve with arc linearisation |

**Note:** Curves are read as `Polygon` for extrusion profiles and as `Polyline` for axis/path representations. All four curve types support both outputs via parallel `read_curve_to_polygon` / `read_curve_to_polyline` dispatchers.

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
| `Torus` | `IfcAdvancedBrep` | ✅ | `representation.py` | Via `Brep.from_torus()` → `brep_to_IfcAdvancedBrep` |
| `Capsule` | `IfcPolygonalFaceSet` | ✅ | `representation.py` | Via tessellation (`.to_brep()` not available); falls back to B-Rep if OCC supports it |
| `Polyhedron` | ❌ | ❌ | — | Use `IfcFacetedBrep` or Mesh export |

### 5.2 Reading: IFC CSG Primitive → COMPAS Shape

| IFC Entity | COMPAS Type | Status | Notes |
|---|---|---|---|
| `IfcBlock` | `Box` | ✅ | `reading.py`: `read_IfcBlock` — corner→center offset applied |
| `IfcSphere` | `Sphere` | ✅ | `reading.py`: `read_IfcSphere` |
| `IfcRightCircularCone` | `Cone` | ✅ | `reading.py`: `read_IfcRightCircularCone` |
| `IfcRightCircularCylinder` | `Cylinder` | ✅ | `reading.py`: `read_IfcRightCircularCylinder` |
| `IfcRectangularPyramid` | `Polyhedron` | ❌ | Would need custom construction |

---

## 6. Solids (the main geometry representations)

### 6.1 Writing: COMPAS → IFC Solid

| COMPAS Type | IFC Entity | RepresentationType | Status | Where |
|---|---|---|---|---|
| `Box/Sphere/Cone/Cylinder` | `IfcCsgSolid` | "CSG" | ✅ | `shapes.py` + `representation.py` |
| `Mesh` | `IfcPolygonalFaceSet` | "Tessellation" | ✅ | `mesh.py` — **default dispatch** since Phase 5 |
| `Mesh` | `IfcFaceBasedSurfaceModel` | "SurfaceModel" | ✅ | `mesh.py` — available, no longer default |
| `Mesh` | `IfcTriangulatedFaceSet` | "Tessellation" | ✅ | `mesh.py`: `mesh_to_IfcTriangulatedFaceSet` — fan triangulation |
| `Mesh` | `IfcFacetedBrep` | "Brep" | ❌ | Would give solid semantics (closed=True meshes) |
| `Brep` (with OCC) | `IfcAdvancedBrep` | "SolidModel" | ✅ | `brep.py` |
| `Brep` (no OCC) | `IfcPolygonalFaceSet` | "Tessellation" | 🔄 | Tessellated fallback via `mesh.py` |
| `Extrusion(profile, direction, depth)` | `IfcExtrudedAreaSolid` | "SweptSolid" | ✅ | `representation.py`: `extrusion_to_IfcExtrudedAreaSolid` |
| `Brep.from_sweep(profile, path)` | `IfcSurfaceCurveSweptAreaSolid` | "AdvancedSweptSolid" | ❌ | Rare |
| `Pipe(directrix, radius)` | `IfcSweptDiskSolid` | "SweptSolid" | ✅ | `representation.py`: `pipe_to_IfcSweptDiskSolid` |
| `Brep.from_loft(curves)` | `IfcAdvancedBrep` | "SolidModel" | 🔄 | No parametric loft in IFC; falls back to B-Rep |
| `Brep` (boolean result) | `IfcBooleanResult` | "CSG" | ❌ | Boolean tree not preserved |
| `Torus` | `IfcAdvancedBrep` | "SolidModel" | ✅ | Via `Brep.from_torus()` → `brep_to_IfcAdvancedBrep` |
| `Capsule` | `IfcPolygonalFaceSet` | "Tessellation" | ✅ | Via tessellation; B-Rep if OCC supports it |

### 6.2 Reading: IFC Solid → COMPAS

| IFC Entity | COMPAS Type | Status | Notes |
|---|---|---|---|
| `IfcExtrudedAreaSolid` | `Extrusion(profile, direction, depth)` | ✅ | `reading.py`: preserves profile, direction, depth, frame |
| `IfcRevolvedAreaSolid` | `Revolution(profile, axis, angle)` | ✅ | `reading.py`: `read_IfcRevolvedAreaSolid` — preserves profile, axis, angle, frame |
| `IfcSweptDiskSolid` | `Pipe(directrix, radius)` | ✅ | `reading.py`: `read_IfcSweptDiskSolid` — preserves directrix, radius, inner_radius |
| `IfcCsgSolid` | `Box` / `Sphere` / `Cone` / `Cylinder` | ✅ | `reading.py`: `read_IfcCsgSolid` dispatches to primitive readers |
| `IfcAdvancedBrep` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. Topology preserved in OCC mode. |
| `IfcFacetedBrep` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. |
| `IfcBooleanResult` | `TessellatedBrep` / `OCCBrep` | 🔄 | Evaluated. Boolean tree lost. |
| `IfcBooleanClippingResult` | `TessellatedBrep` / `OCCBrep` | 🔄 | Falls back to `visual_geometry`. |
| `IfcFaceBasedSurfaceModel` | `Mesh` | ✅ | `reading.py`: `read_IfcFaceBasedSurfaceModel` |
| `IfcTriangulatedFaceSet` | `Mesh` | ✅ | `reading.py`: `read_IfcTriangulatedFaceSet` |
| `IfcPolygonalFaceSet` | `Mesh` | ✅ | `reading.py`: `read_IfcPolygonalFaceSet` |
| `IfcMappedItem` | (unwrapped inner geometry) | ✅ | `reading.py`: `read_IfcMappedItem` — resolves origin+target transform |

**Phase 1 reading** directly parses the IFC entity graph, preserving parametric data for extrusions (98.6% of Duplex). Remaining types (IfcBooleanClippingResult, IfcRevolvedAreaSolid, etc.) fall back to `visual_geometry`.

---

## 7. Profiles (2D cross-sections for extrusions/sweeps)

Profiles are the 2D shapes used by `IfcExtrudedAreaSolid`, `IfcRevolvedAreaSolid`, etc.

### 7.1 Writing: COMPAS 2D Geometry → IFC Profile

| COMPAS Type | IFC Profile | Status | Notes |
|---|---|---|---|
| `(width, height)` tuple | `IfcRectangleProfileDef` | ❌ | Most common profile (70% of Duplex) |
| `(width, height, wall_thickness)` | `IfcRectangleHollowProfileDef` | ❌ | Hollow rectangular sections |
| `Circle` | `IfcCircleProfileDef` | ✅ | `representation.py`: `_circle_to_IfcCircleProfileDef` |
| `Circle` (inner+outer) | `IfcCircleHollowProfileDef` | ❌ | Hollow circular sections |
| `Ellipse` | `IfcEllipseProfileDef` | ❌ | Rare |
| `Polygon` / `Polyline` | `IfcArbitraryClosedProfileDef` | ✅ | `representation.py`: `_polygon_to_IfcArbitraryClosedProfileDef` |
| `Polygon` + list[`Polygon`] | `IfcArbitraryProfileDefWithVoids` | ✅ | `representation.py`: `_profile_with_voids_to_ifc` |
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
| `IfcRectangleProfileDef` | `Polygon` (4 corners) | ✅ | `reading.py`: `read_IfcRectangleProfileDef` — handles 2D Position offset |
| `IfcCircleProfileDef` | `Circle` | ✅ | `reading.py`: `read_IfcCircleProfileDef` |
| `IfcEllipseProfileDef` | `Polygon` (sampled) | ✅ | `reading.py`: `read_IfcEllipseProfileDef` — 32-point polygon approximation |
| `IfcArbitraryClosedProfileDef` | `Polygon` | ✅ | `reading.py`: `read_IfcArbitraryClosedProfileDef` — parses `.OuterCurve` |
| `IfcArbitraryProfileDefWithVoids` | `(Polygon, [Polygon])` | ✅ | `reading.py`: `read_IfcArbitraryProfileDefWithVoids` |
| `IfcIShapeProfileDef` | params dict or `Polygon` | ❌ | Convert to polygon outline |
| `IfcCompositeProfileDef` | list of profiles | ❌ | Recursive |

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
| `IfcRepresentationMap` | Defines reusable geometry template | ✅ | ✅ | `representation.py`: `_create_representation_map` — auto-created on shared geometry |
| `IfcMappedItem` | Instance of mapped representation | ✅ | ✅ | Write: `_assign_mapped_body`. Read: `read_IfcMappedItem` with template caching |
| `IfcCartesianTransformationOperator3D` | Transform for mapped items | ✅ | ✅ | Write: `transformation_to_IfcCartesianTransformationOperator3D`. Read: `_cartesian_transform_operator_to_transformation` |

---

## 10. Non-Body Representations

| RepresentationIdentifier | IFC Geometry Used | COMPAS Target | Write | Read |
|---|---|---|---|---|
| `"Body"` | Solids, B-Rep, CSG, etc. | `Brep` / `Mesh` / shapes | ✅ | ✅ |
| `"Axis"` | `IfcPolyline` | `Polyline` | ✅ | ✅ |
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
| `IfcAxis2Placement2D` | `Frame` (2D) | ❌ | ✅ | `frame.py`: `IfcAxis2Placement2D_to_frame` — used for profile Position offsets |
| `IfcLocalPlacement` | `Frame` / `Transformation` | ✅ | ✅ | `frame.py` |
| `IfcAxis1Placement` | `(Point, Vector)` | ✅ | ❌ | `frame.py`: `create_IfcAxis1Placement` — used for revolution axes |
| `IfcCartesianTransformationOperator3D` | `Transformation` | ✅ | ✅ | Write: `representation.py`. Read: `reading.py` |

---

## 12. Summary: Implementation Status by Category

| Category | Total Mappings | ✅ Done | 🔧 Partial | ❌ Missing |
|---|---|---|---|---|
| **Points/Vectors/Frames** | 7 | 6 | 0 | 1 |
| **Curves (write)** | 10 | 2 | 4 | 4 |
| **Curves (read)** | 9 | 4 | 1 | 4 |
| **Surfaces (write)** | 6 | 0 | 5 | 1 |
| **Surfaces (read)** | 7 | 0 | 0 | 7 |
| **Shapes/CSG (write)** | 7 | 6 | 0 | 1 |
| **Shapes/CSG (read)** | 5 | 4 | 0 | 1 |
| **Solids (write)** | 14 | 9 | 2 | 3 |
| **Solids (read)** | 12 | 8 | 0 | 4 |
| **Profiles (write)** | 14 | 3 | 0 | 11 |
| **Profiles (read)** | 7 | 5 | 0 | 2 |
| **Topology (B-Rep)** | 11 | 8 | 0 | 3 |
| **Containers/Instancing** | 5 | 5 | 0 | 0 |
| **Non-Body Reps** | 8 | 3 | 1 | 4 |
| **Placements** | 5 | 4 | 1 | 0 |
| **TOTAL** | **127** | **67** | **14** | **46** |

Phase 1 added 27 new read implementations (40% coverage). Phase 2 added 4 more (Polyline/Polygon write + Axis read/write). Phase 3 completed instancing (IfcRepresentationMap + IfcMappedItem + IfcCartesianTransformationOperator3D write). Phase 4 confirmed CSG round-trip. Phase 5 added Torus/Capsule write, IfcTriangulatedFaceSet write, and switched default mesh to IfcPolygonalFaceSet. Phase 6 added IfcRevolvedAreaSolid and IfcSweptDiskSolid full round-trip with new `Revolution` and `Pipe` parametric classes. Total coverage: 53% (up from 44% after Phase 3). Remaining 🔄 entries (IfcBooleanClippingResult, IfcAdvancedBrep, etc.) fall back to `visual_geometry`.

---

## 13. Priority Implementation Order

Based on frequency in real IFC files (Duplex model) and practical value:

### Phase 1: Extrusion Pipeline ✅ COMPLETE (covers ~98.6% of Duplex)

```
Write:  Extrusion(profile, direction, depth) → IfcExtrudedAreaSolid     ✅
Read:   IfcExtrudedAreaSolid → Extrusion                                ✅
        IfcFaceBasedSurfaceModel / IfcPolygonalFaceSet → Mesh           ✅
        IfcTriangulatedFaceSet → Mesh                                   ✅
        IfcMappedItem → unwrap + transform inner geometry               ✅
        IfcCsgSolid → Box/Sphere/Cone/Cylinder                          ✅

Profiles implemented (read + write):
  1. IfcRectangleProfileDef       → Polygon (4 corners)                 ✅
  2. IfcArbitraryClosedProfileDef → Polygon (via curve parsing)         ✅
  3. IfcArbitraryProfileDefWithVoids → (Polygon, [Polygon])             ✅
  4. IfcCircleProfileDef          → Circle                              ✅
  5. IfcEllipseProfileDef         → Polygon (32-point approx)           ✅

Curve parsing (for profiles):
  - IfcPolyline, IfcIndexedPolyCurve, IfcCompositeCurve, IfcTrimmedCurve ✅

Duplex results: 282/286 (98.6%) directly parsed.
Only 4 IfcBooleanClippingResult entities fall back to visual_geometry.
```

### Phase 2: Curves & Non-Body Representations ✅ COMPLETE

```
Write:  Polyline → IfcPolyline (standalone)                              ✅
        Polygon → IfcPolyline (closed)                                   ✅
Read:   IfcPolyline → Polyline (for axis representations)                ✅

Implemented:
  1. Standalone curve writers (polyline_to_IfcPolyline, polygon_to_IfcPolyline)  ✅
  2. Axis representation reader (read_axis_representation)                       ✅
  3. Axis representation writer (assign_axis_representation)                     ✅
  4. IfcProduct.axis property (getter + setter)                                  ✅
  5. default_axis_context on IFCFile                                             ✅

Duplex results: 65/295 products have axis representations
  - 56 IfcWallStandardCase, 8 IfcBeam, 1 IfcWall
  - All are 2-point IfcPolyline centerlines
Round-trip verified: write axis → save IFC → reload → read axis back
```

### Phase 3: Instancing ✅ COMPLETE

```
Write:  Shared geometry detection -> IfcRepresentationMap + IfcMappedItem  ✅
Read:   IfcMappedItem -> geometry + transform (with template caching)      ✅

Implemented:
  1. IfcRepresentationMap creation (_create_representation_map)              ✅
  2. IfcMappedItem creation (_assign_mapped_body)                           ✅
  3. IfcCartesianTransformationOperator3D writer                            ✅
  4. Shared geometry detection in assign_body_representation                ✅
  5. Read-side template caching (_MAPPED_GEOMETRY_CACHE)                    ✅

Write behaviour:
  - 1st use of geometry object: direct IfcShapeRepresentation
  - 2nd use: creates IfcRepresentationMap from 1st entity's inner rep,
    assigns IfcMappedItem to this entity
  - 3rd+ use: reuses map, creates new IfcMappedItem

Duplex model: 60 IfcRepresentationMap, 167 IfcMappedItem
  - 47 maps have >1 instance (shared geometry)
  - All 99 products with mapped reps parse correctly
Round-trip verified: write 5 shared columns -> save -> reload -> 1 map + 4 items
```

### Phase 4: CSG Round-Trip ✅ COMPLETE

```
Write:  COMPAS Shape → direct IfcCsgPrimitive (shapes.py)              ✅
Read:   IfcBlock → Box                                                 ✅
        IfcSphere → Sphere                                             ✅
        IfcRightCircularCone → Cone                                    ✅
        IfcRightCircularCylinder → Cylinder                            ✅

All implemented in reading.py as part of Phase 1.
```

### Phase 5: Missing Shapes & Mesh Improvements ✅ COMPLETE

```
Write:  Torus → IfcAdvancedBrep (via Brep.from_torus())                     ✅
        Capsule → IfcPolygonalFaceSet (tessellation fallback)               ✅
        Mesh → IfcPolygonalFaceSet (new default dispatch)                   ✅
        Mesh → IfcTriangulatedFaceSet (fan triangulation)                   ✅
Read:   IfcPolygonalFaceSet / IfcTriangulatedFaceSet → Mesh                ✅ (Phase 1)

Implemented:
  1. mesh_to_IfcTriangulatedFaceSet (mesh.py)                                ✅
  2. Torus dispatch: to_brep() → brep_to_IfcAdvancedBrep                     ✅
  3. Capsule dispatch: to_vertices_and_faces() → mesh → IfcPolygonalFaceSet  ✅
     (Capsule.to_brep() not available; graceful try/except fallback)
  4. Default mesh write switched from IfcFaceBasedSurfaceModel
     to IfcPolygonalFaceSet                                                  ✅

Notes:
  - Torus B-Rep write succeeds but read-back via ifcopenshell geometry
    evaluator may fail (pre-existing brep.py toroidal surface limitation)
  - Capsule uses tessellation because COMPAS Capsule.to_brep() raises
    NotImplementedError; will auto-upgrade to B-Rep when OCC adds support
```

### Phase 6: Remaining Swept Solids ✅ COMPLETE

```
Write:  Revolution(profile, axis, angle) → IfcRevolvedAreaSolid             ✅
        Pipe(directrix, radius) → IfcSweptDiskSolid                         ✅
Read:   IfcRevolvedAreaSolid → Revolution                                   ✅
        IfcSweptDiskSolid → Pipe                                            ✅

New parametric classes (compas_ifc.representations):
  1. Revolution — IfcRevolvedAreaSolid round-trip                             ✅
     - profile: Polygon | Circle | (Polygon, [Polygon])
     - axis_point + axis_direction: revolution axis (IfcAxis1Placement)
     - angle: degrees (IFC convention), 360 = full revolution
     - frame: local placement (IfcAxis2Placement3D)
     - to_vertices_and_faces(): Rodrigues' rotation mesh generation
  2. Pipe — IfcSweptDiskSolid round-trip                                      ✅
     - directrix: Polyline (3D sweep path)
     - radius: outer radius
     - inner_radius: optional (hollow pipes)
     - to_vertices_and_faces(): ring-based tube mesh generation

New helpers:
  - create_IfcAxis1Placement (frame.py): point + direction axis placement    ✅
  - _profile_to_ifc (representation.py): shared profile writer               ✅
  - revolution_to_IfcRevolvedAreaSolid (representation.py)                    ✅
  - pipe_to_IfcSweptDiskSolid (representation.py)                            ✅
  - read_IfcRevolvedAreaSolid (reading.py)                                    ✅
  - read_IfcSweptDiskSolid (reading.py)                                       ✅

Round-trip verified: create → save → reload → parametric class returned
  with correct parameters (4/4 test cases pass)
```
