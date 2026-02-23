# Chapter 4 Gap Analysis: Thesis Claims vs. Implementation

> **Date:** 2026-02-23 (updated after implementation session)
> **Scope:** Chapter 4 — "Data Model for Humans"
> **Repos:** `compas_ifc` (branch: `brep`), `compas_model` (`D:\Github\compas_model`)
> **Prior art:** `update/compas_model` branch — early draft of integration (reviewed)

---

## Decisions Made

| Question | Decision |
|---|---|
| **Architecture** | Big refactor: extend `compas_model.Model` → `BuildingModel` (or `BuildingInformationModel`), extend `compas_model.Element` → `GenericElement`, wrap current `Base` as internal `_ifc_entity` |
| **compas_model** | Integrate as real dependency; inherit Tree + InteractionGraph, modify as needed |
| **IfcProject** | Merge IfcProject capabilities into the BuildingModel class itself (not a separate element), since the model may span multiple buildings |
| **Evaluation scripts** | Produce real results, adjust thesis numbers to match; aim for minimal user-facing API |
| **Validation** | Replace jsonschema with Pydantic |
| **Geometry import** | ifcopenshell handles all import (converts everything → Brep via OCC); may need special treatment for primitives later — defer |
| **Backwards compat** | Not needed; all existing scripts can be rewritten with new clean API |
| **Class/method names** | Thesis names are tentative; implementation should aim for clean minimal API, thesis adapts |

---

## Implementation Progress (2026-02-23)

Today's session completed the core implementation in 3 commits:

1. **Bi-directional BIM model** (`2578076`) — Full creation pipeline with IFCFile compatibility layer, `add_element`/`remove_element` overrides that sync to IFC, `template()` classmethod for scaffolding, typed convenience methods (`create_wall`, `create_slab`, etc.), and placement rectification during import.

2. **Element extraction** (`1cb7f5a`) — `extract_elements()` method that creates self-contained sub-models from selected elements, with options to preserve geometry, properties, materials, styles, and type definitions.

3. **Non-hierarchical spatial relationship graph** (`4f3e3a5`, refined in follow-up) — `_load_relationships_into_graph()` imports non-hierarchical spatial relationships as typed edges in the interaction graph, organized into three groups:
   - **Topology** — voids, fills, connections, space boundaries, coverings, interference, projections
   - **Structural** — structural member/activity relationships
   - **MEP** — port connections, port-element links, flow control, services, spatial references

   Non-spatial relationships (type definitions, materials, group assignments, external references, decomposition) are excluded — they are accessible via `_ifc_entity`.

   Edge storage preserves **every IFC relationship instance**: each edge carries a `relationships` list of dicts (one record per IFC relationship), so multiple relationships between the same element pair (e.g. multiple space boundary levels, wall connections at both ends) are not collapsed. Two-level query API: `get_interactions_by_group("topology")` and `get_interactions_by_category("connection")`. Schema-safe across IFC2X3/IFC4/IFC4X3.

4. **Pydantic validation** — `validation.py` module with Pydantic BaseModel schemas for 8 standard IFC property sets (Pset_WallCommon, Pset_SlabCommon, Pset_DoorCommon, Pset_WindowCommon, Pset_BeamCommon, Pset_ColumnCommon, Pset_SpaceCommon, Pset_RoofCommon). `Specification` dataclass mirrors IDS structure (applicability + requirements). Advisory `model.validate(specs)` for bulk reporting + optional enforcement via `model.specifications` list checked in `add_element()`. On the Duplex model: 146 checks, 145 pass, 1 fail. Pydantic schema is 79% more concise than equivalent IDS XML (14 vs 68 lines). JSON Schema export comes free via `model_json_schema()`.

5. **Relationship export** — `_export_mutual_relationships()` expanded from 4 to all 14 relationship types (topology + structural + MEP). Schema-safe across IFC2X3/IFC4. Both `extract()` and `file.export()` benefit automatically. Tested with storey extraction: 169 relationship records exported across 135 unique edges.

### What remains

- **~~Automatic connection creation~~** — **DONE** — see § Automatic Connection Detection below
- **Geometry pre-loading** — Migrate multiprocessing-based geometry loading
- **Convenience queries** — by name, by storey, by material (by type already works)
- **Evaluation scripts** — One per thesis section (4.6.1–4.6.5)

### Automatic Connection Detection (2026-02-23)

**Implementation:** `GenericElement.compute_contacts()` (element.py) + `BuildingInformationModel.compute_connections()` (bim.py). Test script: `scripts/9.10_auto_connections_test.py`.

**How it works:**
1. `GenericElement.compute_contacts()` overrides `compas_model.Element.compute_contacts()` to handle `TessellatedBrep` geometry (the default IFC geometry type that is neither `Mesh` nor `Brep`) by converting it to `compas.Mesh` before calling `mesh_mesh_contacts`. Also dispatches to `brep_brep_contacts` when `use_occ=True`.
2. `compute_connections()` runs a two-stage broadphase pipeline:
   - **Stage 1:** BVH spatial search (inflated 1.2× AABBs, from `compas_model`)
   - **Stage 2:** Tight world-space AABB overlap test — reduces candidates dramatically (1596 → 150 for Duplex walls)
   - **Narrowphase:** `mesh_mesh_contacts` on surviving pairs
3. Discovered contacts are stored as `"connection"` edges (with `"source": "computed"`) in the interaction graph, alongside any existing IFC-imported relationships.
4. Accepts `element_types` filter (e.g. `["IfcWall", "IfcWallStandardCase"]`) to scope the search.

**Duplex model results (57 walls):**

| Metric | Count |
|---|---|
| Original IFC connections (`IfcRelConnectsPathElements`) | 78 |
| Auto-discovered connections | 99 |
| Recovered (overlap) | 64 (82%) |
| Missed (in IFC, not auto-found) | 14 |
| Newly found (not in IFC) | 35 |

**Analysis:**
- **82% recovery rate** — the geometric method rediscovers most IFC-defined connections.
- **14 missed:** Mostly thin furring walls (38mm stud) that connect end-to-end. Their contact areas fall below the `minimum_area` threshold on tessellated geometry, or the triangulated normals don't align as precisely opposing. IFC defines these as path connections (topological), not face contacts (geometric).
- **35 new:** Real geometric contacts that `IfcRelConnectsPathElements` does not capture: wall-to-foundation contacts, stacked exterior walls between floors, etc. These are valid adjacencies that the IFC authoring tool's "wall join" logic never created.

**Limitations to address in future work:**

1. **Performance — O(n×m) face-pair loop (17–18s for 57 walls).** The bottleneck is `mesh_mesh_contacts` in `compas_model`, which iterates all face pairs between two meshes in pure Python. For walls with 76–112 triangular faces each, this means ~8k comparisons per pair × 150 pairs. Potential improvements:
   - *Face-normal pre-grouping:* Bucket faces by quantised normal direction; only pair buckets with opposing normals. Would reduce per-pair work by ~6× for typical wall meshes.
   - *Per-face AABB tree:* Spatial index on individual faces to skip distant face pairs entirely.
   - *C-level implementation:* Move the hot loop to compiled code (upstream `compas_model` improvement).

2. **Tessellated geometry mismatch.** `mesh_mesh_contacts` checks for *exactly* opposing face normals. Tessellated IFC geometry produces triangulated faces that may not be perfectly coplanar even on nominally flat surfaces, causing near-miss false negatives. A tolerance on the normal opposition check (currently strict `is_opposite_normal_normal`) would improve recall.

3. **Path connections vs face contacts.** IFC's `IfcRelConnectsPathElements` represents *topological* wall-join relationships (L-joins, T-joins, etc.) which do not require shared face area — just edge adjacency. The geometric contact method inherently requires a shared face polygon with area ≥ `minimum_area`. Thin walls that join end-on have zero (or sub-threshold) shared face area. Recovering these would require an *edge-adjacency* detection mode in addition to face-contact detection.

4. **No IFC relationship generation yet.** Currently `compute_connections()` only creates graph edges with `"source": "computed"`. It does not yet generate `IfcRelConnectsElements` entities in the IFC file. This would require a write-back step: for each new computed connection edge, create the corresponding IFC relationship entity via `model.create()`.

5. **Element type scoping.** Without `element_types` filter, including all 215 elements (railings, furniture, stairs with 700–1100 faces) would make the BVH produce thousands of false-positive pairs and push runtime to minutes. The `element_types` parameter is essential for practical use but requires the user to know which types to include.

---

## What `update/compas_model` Branch Already Did

The branch (4 commits, diverged pre-brep-work) established the basic pattern:

```python
class BuildingModel(compas_model.Model):
    def __init__(self, filepath=None):
        super().__init__()
        self.file = IFCFile(None, filepath=filepath)
        self.load_hierarchy()  # walks IFC spatial structure → tree

class BuildingElement(compas_model.Element):
    def __init__(self, ifc_entity=None, model=None):
        super().__init__()
        self.ifc_entity = ifc_entity  # read-only reference

    # Properties delegate to ifc_entity
    geometry → ifc_entity.geometry
    transformation → ifc_entity.frame.to_transformation()
    ifc_attributes → ifc_entity.attributes
    ifc_psets → ifc_entity.property_sets
```

**What worked:** Hierarchy loading, viewer visualization, basic property delegation.

**What was incomplete/broken:**
- 8 abstract methods from Element not implemented (`compute_elementgeometry`, `compute_aabb`, etc.)
- `transformation` returns global (from IFC placement chain) but compas_model expects **relative to parent** — mismatch
- No interaction graph usage
- No validation
- Older brep.py (pre-26-test improvements)
- No export pipeline

---

## What `compas_model` Provides (for free upon inheritance)

### From `Model`:
- `self.tree` (ElementTree) — spatial hierarchy with parent-child
- `self.graph` (InteractionGraph) — edge-based relationships
- `self._elements` (dict) — GUID-keyed element storage
- `add_element(element, parent)` / `remove_element(element)` — manages tree + graph + dict
- `find_element_with_name(name)` / `find_all_elements_of_type(type)`
- `self.bvh` / `self.kdtree` — spatial acceleration (lazy, need `compute_aabb`/`compute_point`)
- `compute_contacts()` — collision detection between elements
- `add_interaction(a, b)` — create graph edge
- `add_modifier(source, target, modifier)` — inter-element modifications
- Serialization via `__data__` / `__from_data__`

### From `Element`:
- `geometry` (Brep | Mesh) — stored, settable, resets cached computations
- `transformation` — **relative to parent** (composes up via `modeltransformation`)
- `modeltransformation` — auto-composed from ancestor chain (scene-graph!)
- `frame` — from modeltransformation
- `parent` / `children` — from tree
- `material` — via GUID lookup
- `features` — parametric modifications
- Lazy computed: `elementgeometry`, `modelgeometry`, `aabb`, `obb`, `collision_mesh`, `point`, `surface_mesh`, `volumetric_mesh`

### From `InteractionGraph`:
- Extends `compas.datastructures.Graph`
- Nodes = elements, Edges = interactions
- Edge attributes: `modifiers`, `contacts`
- **No category/semantic filtering built-in** — we'll need to add this for IFC

### From `ElementTree`:
- Extends `compas.datastructures.Tree`
- Root is synthetic (not an element)
- `add_element(element, parent)` → creates `ElementNode`

---

## Detailed Gap Analysis (What Still Needs Building)

### 1. BuildingModel — The Main Class

**Inherits from:** `compas_model.Model`
**Absorbs:** current `compas_ifc.Model` + IfcProject capabilities

| Capability | Source | Status |
|---|---|---|
| Tree + Graph (structure) | compas_model.Model | **FREE** |
| Element storage + lookup | compas_model.Model | **FREE** |
| `add_element` / `remove_element` | compas_model.Model | **FREE** |
| IFC file I/O (`IFCFile` wrapper) | current Model | **DONE** — compatibility layer in `bim.py` delegates to `IFCFile` |
| Schema detection (IFC2X3/IFC4/IFC4X3) | current Model via IFCFile | **DONE** — inherited from `IFCFile` |
| Entity queries by IFC type (e.g. "IfcWall") | current Model | **DONE** — `elements_of_type()` queries by IFC class string |
| Entity creation with fuzzy type matching | current Model.create() | **DONE** — `create_element()` and typed helpers (`create_wall`, `create_slab`, etc.) |
| Geometry pre-loading (multiprocessing) | current Model via IFCFile | **MIGRATE** |
| Export with hierarchy scaffolding | current Model.export() | **MIGRATE** |
| `project`, `sites`, `buildings`, `storeys` properties | current Model | **DONE** — IfcProject merged into BuildingModel; `sites`/`buildings`/`storeys` are tree queries |
| IFC import pipeline (file → elements → tree → graph) | update/compas_model draft | **DONE** — full pipeline with rectified transforms + relationship graph loading |
| IFC export pipeline (tree → IFC entities → file) | not implemented | **DONE** — bi-directional sync: mutations on GenericElement immediately update the IFC file |
| Convenience queries: by name, by type, by storey, by material | some exist | **PARTIAL** — by type works; by name/storey/material still needed |
| Element extraction (subset → new model) | not implemented | **DONE** — `extract_elements()` with options for geometry, properties, materials, styles, types |

### 2. GenericElement — The Unified Element

**Inherits from:** `compas_model.Element`
**Wraps:** current `Base` (as `._ifc_entity`)

| Capability | Source | Status |
|---|---|---|
| `geometry` (Brep \| Mesh) | compas_model.Element | **FREE** — set during import |
| `transformation` (relative to parent) | compas_model.Element | **FREE** — compute during import via rectification |
| `modeltransformation` (composed global) | compas_model.Element | **FREE** — auto-computed from ancestors |
| Scene-graph propagation (move parent → moves children) | compas_model.Element | **FREE** |
| `parent` / `children` | compas_model.Element | **FREE** |
| `aabb` / `obb` | compas_model.Element (needs `compute_aabb`) | **DONE** — delegates to geometry.aabb / geometry.obb, with Mesh fallback |
| `point` (centroid) | compas_model.Element (needs `compute_point`) | **DONE** — delegates to geometry.centroid |
| `collision_mesh` / `surface_mesh` | compas_model.Element (needs implementations) | **DONE** — delegates to geometry.to_tesselation() / to_mesh() |
| `elementgeometry` | compas_model.Element (needs `compute_elementgeometry`) | **DONE** — returns stored geometry |
| `_ifc_entity` reference | update/compas_model draft | **DONE** — stored on GenericElement, accessible as escape hatch |
| `type` attribute (string → IFC class mapping) | thesis concept | **DONE** — `ifc_type` property on GenericElement |
| `properties` (unified dict, lazy-loaded from _ifc_entity) | current Base.property_sets | **DONE** — bi-directional setter syncs to IFC file |
| Pydantic validation | not implemented | **DONE** — `validation.py` module with Specification + enforcement on `add_element()` |
| Lazy loading of all properties from `_ifc_entity` | not implemented | **PARTIAL** — properties load from IFC entity; full lazy-loading pattern still evolving |

### 3. Spatial Hierarchy (Tree)

| Capability | Source | Status |
|---|---|---|
| Parent-child structure | compas_model.ElementTree | **FREE** |
| Add/remove elements | compas_model | **FREE** |
| Hierarchy traversal | compas_model | **FREE** |
| IfcProject as root | Need to map IfcProject → BuildingModel (not a tree element) | **DONE** — IfcProject merged into BuildingModel; IfcSite is first tree element |
| Placement chain rectification during import | not implemented | **DONE** — `rectify_placements=True` rewrites `PlacementRelTo` to match spatial hierarchy, with verbose reporting |
| Granular export (subset → valid IFC) | current Model.export() | **DONE** — `extract_elements()` creates self-contained sub-models |
| Auto-generate IFC scaffolding for export | current Model.export(as_snippet=True) | **DONE** — `template()` classmethod creates Project→Site→Building→Storey scaffold |

### 4. Interaction Graph

| Capability | Source | Status |
|---|---|---|
| Graph structure | compas_model.InteractionGraph | **FREE** |
| Edge storage (modifiers, contacts) | compas_model.InteractionGraph | **FREE** |
| Contact detection | compas_model.Model.compute_contacts() | **FREE** (once `compute_aabb` etc. are implemented) |
| **Two-level semantic query API** | NOT in compas_model | **DONE** — `RELATIONSHIP_GROUPS` constant defines three groups (topology, structural, MEP); `get_interactions_by_group()` and `get_interactions_by_category()` provide two-level filtering |
| **Multi-record edge storage** | NOT in compas_model | **DONE** — each edge stores a `relationships` list of dicts preserving every IFC relationship instance (e.g. multiple space boundary levels between same pair); `edge_relationships(edge)` accessor |
| IFC spatial relationship import → graph edges | not implemented | **DONE** — `_load_relationships_into_graph()` imports topology (voids, fills, connections, space boundaries, coverings, interference, projections), structural (member/activity), and MEP (ports, flow control, services, spatial references). Schema-safe across IFC2X3/IFC4/IFC4X3 |
| IFC relationship export ← graph edges | not implemented | **DONE** — `_export_mutual_relationships()` exports all 14 relationship types; used by both `extract()` and `file.export()` |
| Automatic connection creation via contact detection | compas_model.Model.compute_contacts() | **DONE** — `compute_connections()` with two-stage broadphase (BVH + tight AABB); 82% recovery on Duplex walls; see § Automatic Connection Detection for limitations |

### 5. Pydantic Validation

| Capability | Status |
|---|---|
| Replace jsonschema with Pydantic | **DONE** — `validation.py` module |
| Schema definition as BaseModel subclasses | **DONE** — 8 standard IFC Pset schemas (Wall, Slab, Door, Window, Beam, Column, Space, Roof) |
| Validate element properties | **DONE** — `validate_model()` / `model.validate()` with structured `ValidationResult` |
| JSON Schema export | **DONE** — `Pset_WallCommon.model_json_schema()` etc. |
| Add `pydantic` dependency | **DONE** — already in `requirements.txt` |
| Specification class (IDS-like) | **DONE** — `Specification` dataclass with applicability + required Psets |
| Enforcement on add_element | **DONE** — `model.specifications` list, checked in `add_element()`, raises `ValueError` |

### 6. Geometry

| Capability | Status |
|---|---|
| Import: ifcopenshell → Brep/Mesh | **PARTIAL** — ifcopenshell does it; we store result |
| Export: Brep → IfcAdvancedBrep | **DONE** (brep.py, 26/26 tests) |
| Export: primitives → IFC shapes | **DONE** (shapes.py) |
| Export: Mesh → IFC | **DONE** (mesh.py) |
| Primitive detection on import (is this Brep actually a box?) | **DEFER** |
| CSG / Boolean | **DEFER** |
| Unified geometry properties (volume, area, centroid) | **CHECK** — may already be on COMPAS Brep/Mesh classes |

---

## Evaluation Scripts Needed

### 4.6.1 — Complexity Reduction
- Count public classes + methods on the new API
- Target: < 100 elements

### 4.6.2 — Geometric Fidelity
- **Round-trip:** Import IFC → export → reimport → compare geometry properties
- **Cross-format:** STEP → IFC4 → verify Brep preserved (leverages existing 8.x scripts)

### 4.6.3 — Spatial Hierarchy
- **Rectification:** Import model with misaligned placements → verify global positions preserved
- **Granular export:** Extract subset → verify self-contained + correct positions
- Need suitable test file (Duplex_A or similar)

### 4.6.4 — Validation
- Define Pydantic schema → apply to test model → count/categorize failures
- Compare with IDS equivalent (line count)

### 4.6.5 — Integrated Workflow
- Custom element + STEP geometry + array + contacts + scoped export
- Depends on all other phases being complete

---

## Resolved Design Questions

### Q1: GenericElement and `_ifc_entity` access — **Option B with lazy loading**

GenericElement is self-contained with unified API (`geometry`, `properties`, `type`, etc.). The `_ifc_entity` is kept as an optional read-only escape hatch. **But**: properties are **lazy-loaded** from `_ifc_entity` on first access, not eagerly extracted. Big IFC files would be too slow otherwise. Elements created programmatically (no `_ifc_entity`) work identically — they just populate attributes directly. This lazy unified API is a core claim of the paper.

### Q2: Spatial containers — **Everything is GenericElement**

All spatial containers are GenericElement instances. IfcProject merges into BuildingModel itself (since the model may span multiple buildings → "BuildingInformationModel"). The tree looks like:

```
BuildingModel (= IfcProject-level)
  └─ tree root
       ├─ GenericElement type="IfcSite"
       │    └─ GenericElement type="IfcBuilding"
       │         └─ GenericElement type="IfcBuildingStorey"
       │              ├─ GenericElement type="IfcWall"
       │              ├─ GenericElement type="IfcSlab"
       │              └─ ...
       └─ ...
```

Spatial containers simply have no geometry. Uniform interface, no special classes.

### Q3: InteractionGraph — **Multi-record edges, three relationship groups, two-level query API**

The interaction graph stores non-hierarchical spatial relationships in three groups:
- **Topology** — voids, fills, connections, space boundaries, coverings, interference, projections
- **Structural** — structural member/activity relationships
- **MEP** — port connections, port-element links, flow control, services, spatial references

Non-spatial relationships (type definitions, materials, group assignments, external references, decomposition) are excluded — they are accessible via `_ifc_entity`.

Each edge stores a `relationships` list of dicts (one record per IFC relationship instance), preserving multiplicity. For example, the Duplex model has 407 IFC relationship instances mapped to 358 unique graph edges, with 39 edges carrying multiple records (e.g. multiple space boundary levels between the same space and wall, or walls connecting at both ends). Two-level query API: `get_interactions_by_group("topology")` filters by group; `get_interactions_by_category("connection")` filters by individual category. `RELATIONSHIP_GROUPS` class constant maps group names to category sets.

### Q4: Transformations — **Compute relative transforms during import**

The `update/compas_model` branch bug is resolved: during import, compute proper local (relative-to-parent) transforms. This naturally achieves "placement chain rectification" — it's just correct import logic, not a special algorithm. Scene-graph behavior (move parent → moves children) comes free from compas_model.

### Q5: compas_model modifications — **Modify upstream as needed**

We can change compas_model. Likely changes:
- InteractionGraph: add `category` support (upstream PR or subclass)
- Element: provide default implementations for abstract methods where sensible
- ElementTree: modifications if needed for IFC mapping

Same for ElementTree — subclass if needed, attribute if change is trivial.

---

## Existing Assets to Preserve

These work well and should survive the refactor:

- **B-Rep export** (`brep.py`) — 26/26 tests, battle-tested
- **Shape export** (`shapes.py`) — primitives to IFC
- **Mesh export** (`mesh.py`) — mesh to IFC
- **Frame/placement conversions** (`frame.py`) — placement chain resolution
- **Property set I/O** (`pset.py`) — dict-based read/write
- **Type fuzzy matching** (`search_ifc_classes()`) — IFC class lookup
- **Multi-schema support** — IFC2X3/IFC4/IFC4X3 detection and dispatch
- **Geometry pre-loading** — multiprocessing iterator
- **Entity extensions** — IfcProject, IfcBuilding, IfcSite properties
- **Export with hierarchy scaffolding** (`export(as_snippet=True)`)

---

## Suggested Implementation Order

1. ~~**Foundation:** Add compas_model dep, create BuildingModel + GenericElement skeletons~~ **DONE**
2. ~~**Import pipeline:** IFC file → GenericElements → tree (with rectified transforms)~~ **DONE**
3. ~~**Abstract methods:** Implement `compute_elementgeometry`, `compute_aabb`, `compute_point`, etc.~~ **DONE**
4. ~~**Basic export:** Tree → IFC file (using existing converters)~~ **DONE** (bi-directional sync)
5. ~~**Interaction graph:** Import non-hierarchical IFC relationships as edges with categories~~ **DONE**
6. ~~**Automatic connections:** Use contact detection to auto-create `IfcRelConnectsElements` between touching elements~~ **DONE** (82% recovery on Duplex walls; limitations documented)
7. ~~**Pydantic validation:** Replace jsonschema~~ **DONE** (8 Pset schemas, Specification, advisory + enforcement)
8. **Evaluation scripts:** One per thesis section
9. **Polish:** Convenience API, edge cases, docs
