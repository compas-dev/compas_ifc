# Chapter 4 Gap Analysis: Thesis Claims vs. Implementation

> **Date:** 2026-02-20 (updated after discussion)
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
| IFC file I/O (`IFCFile` wrapper) | current Model | **MIGRATE** |
| Schema detection (IFC2X3/IFC4/IFC4X3) | current Model via IFCFile | **MIGRATE** |
| Entity queries by IFC type (e.g. "IfcWall") | current Model | **REBUILD** — adapt `find_all_elements_of_type` to work with string-based IFC types, not Python class types |
| Entity creation with fuzzy type matching | current Model.create() | **MIGRATE** |
| Geometry pre-loading (multiprocessing) | current Model via IFCFile | **MIGRATE** |
| Export with hierarchy scaffolding | current Model.export() | **MIGRATE** |
| `project`, `sites`, `buildings`, `storeys` properties | current Model | **REBUILD** — IfcProject merges into BuildingModel; sites/buildings/storeys become tree queries |
| IFC import pipeline (file → elements → tree → graph) | update/compas_model draft | **REBUILD** — needs rectified transformations, graph edges, proper geometry |
| IFC export pipeline (tree → IFC entities → file) | not implemented | **BUILD** |
| Convenience queries: by name, by type, by storey, by material | some exist | **BUILD** |

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
| `aabb` / `obb` | compas_model.Element (needs `compute_aabb`) | **BUILD** — implement abstract method, delegate to geometry |
| `point` (centroid) | compas_model.Element (needs `compute_point`) | **BUILD** — implement, delegate to geometry centroid |
| `collision_mesh` / `surface_mesh` | compas_model.Element (needs implementations) | **BUILD** — delegate to geometry.to_mesh() or similar |
| `elementgeometry` | compas_model.Element (needs `compute_elementgeometry`) | **BUILD** — return stored geometry (identity for IFC imports) |
| `_ifc_entity` reference | update/compas_model draft | **BUILD** — raw IFC entity as optional escape hatch |
| `type` attribute (string → IFC class mapping) | thesis concept | **BUILD** |
| `properties` (unified dict, lazy-loaded from _ifc_entity) | current Base.property_sets | **BUILD** — lazy load from `_ifc_entity.property_sets`, store locally for programmatic elements |
| Pydantic validation | not implemented | **BUILD** |
| Lazy loading of all properties from `_ifc_entity` | not implemented | **BUILD** — core design: first access triggers extraction, then cached |

### 3. Spatial Hierarchy (Tree)

| Capability | Source | Status |
|---|---|---|
| Parent-child structure | compas_model.ElementTree | **FREE** |
| Add/remove elements | compas_model | **FREE** |
| Hierarchy traversal | compas_model | **FREE** |
| IfcProject as root | Need to map IfcProject → BuildingModel (not a tree element) | **BUILD** — IfcSite becomes first-level tree element |
| Placement chain rectification during import | not implemented | **BUILD** — critical algorithm |
| Granular export (subset → valid IFC) | current Model.export() | **REBUILD** |
| Auto-generate IFC scaffolding for export | current Model.export(as_snippet=True) | **MIGRATE** |

### 4. Interaction Graph

| Capability | Source | Status |
|---|---|---|
| Graph structure | compas_model.InteractionGraph | **FREE** |
| Edge storage (modifiers, contacts) | compas_model.InteractionGraph | **FREE** |
| Contact detection | compas_model.Model.compute_contacts() | **FREE** (once `compute_aabb` etc. are implemented) |
| **Category/semantic filtering** | NOT in compas_model | **BUILD** — need to add edge `category` attribute and filtered queries |
| IFC relationship import → graph edges | not implemented | **BUILD** |
| IFC relationship export ← graph edges | not implemented | **BUILD** |
| Semantic groupings: structural, system, material, geometric | not implemented | **BUILD** |

### 5. Pydantic Validation

| Capability | Status |
|---|---|
| Replace jsonschema with Pydantic | **BUILD** |
| Schema definition as BaseModel subclasses | **BUILD** |
| Validate element properties | **BUILD** |
| JSON Schema export | **FREE** via `model_json_schema()` |
| Add `pydantic` dependency | **BUILD** |

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

### Q3: InteractionGraph — **Subclass in compas_ifc**

Subclass InteractionGraph and modify as needed to support IFC relationship categories. If the changes are small enough, just use edge attributes instead. Can also push useful generalizations upstream to compas_model.

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

1. **Foundation:** Add compas_model dep, create BuildingModel + GenericElement skeletons
2. **Import pipeline:** IFC file → GenericElements → tree (with rectified transforms)
3. **Abstract methods:** Implement `compute_elementgeometry`, `compute_aabb`, `compute_point`, etc.
4. **Basic export:** Tree → IFC file (using existing converters)
5. **Interaction graph:** Import non-hierarchical IFC relationships as edges with categories
6. **Pydantic validation:** Replace jsonschema
7. **Evaluation scripts:** One per thesis section
8. **Polish:** Convenience API, edge cases, docs
