# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

Archival release accompanying the DOI citation for chapter 4 of the PhD
thesis. Restores correct geometric connection detection (regressed by the
`2.0.0` clash-detection refactor), makes the evaluation suite deterministically
reproducible, and completes packaging/citation metadata.

### Added

* `BuildingInformationModel.trace_connections(start, category, max_depth)` —
  breadth-first traversal of the interaction graph from a starting element,
  filtered by relationship category or group, returning the reachable
  elements. Useful for tracing connectivity networks such as MEP flow
  systems or chains of structurally connected members.
* `BuildingInformationModel.save` now accepts `schema` and
  `tessellation_tolerance` arguments for future cross-schema export. Passing
  a `schema` different from the model's current schema currently raises
  `NotImplementedError`; saving in the current schema is unchanged.
* `CITATION.cff` — citation metadata for the archival (DOI) release.
* `requirements-freeze.txt` — exact dependency versions pinning the
  reference environment used to produce the chapter 4 evaluation results.
* `COMPAS_IFC_GEOM_WORKERS` environment variable to control the number of
  workers used by the geometry iterator in `IFCFile.load_geometries`. Set it
  to `1` for deterministic, reproducible geometry evaluation. The chapter 4
  evaluation suite (`thesis/appendix/A/run_all.py`) now pins this to `1`.

### Fixed

* Geometric connection detection (`compute_connections`) now reproduces the
  designed contact counts again. The `2.0.0` refactor that routed clash
  detection through cached world-coord meshes for speed had regressed it;
  several independent defects are addressed:
  * `GenericElement.compute_contacts` now uses exact B-Rep face-to-face
    contact detection (`brep_brep_contacts`) when both elements expose B-Rep
    geometry, falling back to the mesh approximation otherwise. The
    mesh-only path could not resolve coplanar "just-touching" faces (e.g.
    beams meeting end-to-end).
  * `GenericElement.compute_aabb` / `compute_obb` now honour the `inflate`
    scaling factor. It was previously ignored, so the `compas_model` BVH
    broadphase (which inflates AABBs to catch touching neighbours) missed
    element pairs that only touch.
  * `IFCFile.load_geometries` now fills in the definition-holder products of
    instanced geometry (`IfcRepresentationMap` / `IfcMappedItem`), which the
    ifcopenshell geometry iterator does not yield. Previously the shared
    definition holder of every instanced group received no `visual_geometry`.
  * `compute_connections` / `compute_collisions` load tessellated geometry
    for freshly created (not-yet-saved) elements before contact detection,
    so a model built in-memory yields correct contacts without a save/reload.
* `GenericElement._world_triangles` now falls back to the parametric
  `geometry` when the tessellated `visual_geometry` is unavailable, so `aabb`
  no longer returns `None` for such elements (which crashed the BVH).
* `thesis/appendix/A/run_all.py` now reports a crashed evaluation stage as
  an explicit error in the summary instead of silently recording it as
  `0 PASS / 0 FAIL`.
* `thesis/appendix/A/integrated_workflow_test.py` now asserts the exact
  designed connection breakdown (6 slab-slab, 18 slab-beam, 8 beam-beam = 32)
  and its preservation through reload and granular export, rather than a loose
  lower-bound check that had masked the connection-detection regression.

### Changed

* `requirements.txt` now declares the previously-undeclared runtime
  dependencies `shapely` (used by contact/collision detection) and `numpy`.
* README: corrected the geometry-kernel description — contact/collision
  detection uses a NumPy + Shapely pipeline; CGAL is not currently a
  dependency.


## [2.0.0] 2026-05-18

This release aligns the package with the front-end data model described in
chapter 4 of the underlying PhD thesis. The user-facing API now consists of
two classes (`BuildingInformationModel`, `GenericElement`) plus an
explicit spatial tree, an interaction graph, a Pydantic-based validation
engine, and a parametric geometry layer. Internal helpers have been
reorganised accordingly and the legacy `compas_ifc.model` entry point is
gone.

### Added

* `compas_ifc.bim.BuildingInformationModel` — the front-end model class,
  combining `ElementFactoryMixin`, `InteractionMixin`, and `TreeMixin`.
* `compas_ifc.element.GenericElement` — unified element abstraction with
  bidirectional sync to the underlying IFC entity. Replaces per-product
  subclasses for everyday usage.
* `compas_ifc.factory.ElementFactoryMixin` — typed creators
  (`create_wall`, `create_slab`, …) plus a `template()` classmethod that
  scaffolds default IfcProject / IfcSite / IfcBuilding / IfcBuildingStorey.
* `create_element` now normalises arbitrary type strings (`"IfcWall"`,
  `"Wall"`, `"wall"` → `IfcWall`) and falls back to
  `IfcBuildingElementProxy` (with `ObjectType` preserved) for unknown
  custom strings.
* `compas_ifc.tree.TreeMixin` — IFC import with placement-chain
  rectification, `extract`/`export` for self-contained subsets,
  `print_hierarchy`.
* `compas_ifc.interactions.InteractionMixin` — typed interaction graph
  populated from IFC relationships, plus `compute_connections`,
  `compute_collisions`, and `show_collisions`.
* `compas_ifc.validation` — `Specification` dataclass, `validate_model`,
  `validate_element`, and Pydantic schemas for the standard IFC psets.
  Specifications attached to `model.specifications` enforce validation at
  insertion time; `model.validate(specs)` runs advisory checks.
* `compas_ifc.representations` — parametric geometry types (`Extrusion`,
  `Revolution`, `Pipe`, `ClippedExtrusion`, `BooleanResult`, `HalfSpace`)
  that round-trip losslessly through IFC.
* `compas_ifc.algorithms.contacts` and `algorithms.collisions` — vectorised
  NumPy + Shapely broadphase + narrowphase replacements for the previous
  pure-Python implementations.
* `thesis/appendix/A/` — reproducible evaluation suite for chapter 4 of
  the thesis, with a `run_all.py` runner that writes a consolidated
  `outputs/A-summary.txt`.
* `tests/test_bim.py` and `tests/test_validation.py` — minimal pytest
  coverage of the front-end API.

### Changed

* The package entry point is now
  `from compas_ifc.bim import BuildingInformationModel`. The previous
  `from compas_ifc.model import Model` import path has been removed.
* Spatial hierarchy is materialised as `model.tree` (a COMPAS `Tree`
  instance) with direct `parent` / `children` pointers; non-hierarchical
  IFC relationships go into `model.graph`.
* Documentation has been rewritten end to end (`README.md`, `docs/index`,
  `docs/architecture`, `docs/api/*`, `docs/tutorials/*`,
  `docs/examples`).

### Removed

* `compas_ifc.model.Model` (replaced by
  `compas_ifc.bim.BuildingInformationModel`).
* `src/compas_ifc/__main__.py` (no-op stub).
* `tests/test_placeholder.py` (replaced by real tests).
* Stale documentation: old tutorial and example pages, the
  `compas_ifc.entities.generated` API page, the development planning
  notes under `thesis/`.
* `compas_ifc.entities.generated.{IFC2X3,IFC4,IFC4X3}` — the runtime
  per-class wrappers (~3,000 files, ~20 MB) have been replaced by three
  PEP 561 stub files (`IFC2X3.pyi`, `IFC4.pyi`, `IFC4X3.pyi`) bundled
  with the package. IDE autocomplete on raw IFC attributes is preserved
  through the stubs; runtime code uses dynamic dispatch through
  ``Base.__getattr__``/``__setattr__``. Users who relied on
  ``isinstance(x, IfcWall)`` should switch to ``x.is_a("IfcWall")``;
  runtime imports of ``compas_ifc.entities.generated.IFC4.IfcWall``
  no longer work — type-time imports under ``if TYPE_CHECKING:``
  continue to resolve via the stubs.

### Migration notes

* The hand-written extensions in ``compas_ifc/entities/extensions/``
  now register through the new
  :func:`compas_ifc.entities.base.extends` decorator rather than by
  class name. Each extension class is renamed to ``Ifc<Name>Extras``
  and inherits from ``Base``; the previous ``class IfcElement(IfcElement)``
  shadowing pattern is gone. External code that imported these classes
  by name (e.g. ``from compas_ifc.entities.extensions import IfcProduct``)
  should switch to the new ``IfcProductExtras`` name.


## [1.7.0] 2025-10-24

### Added

* Added `volume` property to `TessellatedBrep` class for calculating volume of closed meshes using COMPAS geometry functions
* Added `surface_area` property to `TessellatedBrep` class for calculating surface area by summing face areas

### Changed

### Removed


## [1.6.1] 2025-07-28

### Added

* Added `linear_deflection` parameter to `Model.show()`, defaulting to 100 for faster BRep tesselation.

### Changed

### Removed

* Removed `Model.update_linear_deflection()`

## [1.6.0] 2025-06-04

### Added

### Changed

### Removed


## [1.5.0] 2025-01-21

### Added

* Added `extensions` keyword argument to `Model` to for inserting custom extensions to IFC classes.

### Changed

### Removed


## [1.4.1] 2024-10-02

### Added

### Changed

### Removed


## [1.4.0] 2024-09-30

### Added

* Added `Model.search_ifc_classes()` and `File.search_ifc_classes()` to search for IFC classes.
* Added `Model.create_wall()`.
* Added `Model.create_slab()`.
* Added `Model.create_window()`.
* Added `Model.create_door()`.
* Added `Model.create_stair()`.
* Added `Model.create_railing()`.
* Added `Model.create_column()`.
* Added `Model.create_beam()`.
* Added `aabb` axis-aligned bounding box to `TessellatedBrep`.
* Added `obb` oriented bounding box to `TessellatedBrep`.

### Changed

### Removed


## [1.3.1] 2024-08-25

### Added

### Changed

### Removed


## [1.3.0] 2024-08-23

### Added

* Added `Model.create_default_project()`.
* Added `TesselatedBrep.to_mesh()`.
* Added `location` to `IfcSite` extension.
* Added `compas_ifc.resources.IfcCompoundPlaneAngleMeasure_to_degrees()`.

### Changed

### Removed


## [1.2.4] 2024-08-22

### Added

* Added `max_depth` to `Base.print_properties()`.

### Changed

* Fixed `Model.print_summary()` while the model is empty.

### Removed


## [1.2.3] 2024-08-16

### Added

### 

* Fixed missing `GloabalId` when creating `IfcRoot` based objects.
* Updated `IfcBrepObject` to automatically heal and simplify breps.

### Removed


## [1.2.2] 2024-07-31

### Added

### Changed

* Fixed `Base.to_dict()` to recursively pass down convert_type_defination.

### Removed


## [1.2.1] 2024-07-30

### Added

### Changed

* Fixed `verbose` bug.

### Removed


## [1.2.0] 2024-07-30

### Added

* Added `compas_ifc.entities.extensions.IfcContext` to extend `IfcContext` class.
* Added `verbose` option to `Model` and `IFCFile`.
* Added `compas_ifc.entities.TypeDefinition` class.
* Added `remove()` to `Model` for removing entities.

### Changed

### Removed


## [1.1.0] 2024-07-22

### Added

* Added `export` method to `IFCFile` and `Model` to export selected list of entities.
* Added `update_linear_deflection` to `Model`.
* Added `unit` attribute to `Model`.
* Added `unit` keyword argument to `Model.template()`.
* Added `recursive`, `ignore_fields`, `include_fields` options to `Base.to_dict()`.
* Added `quantities` to `compas_ifc.entities.extensions.IfcObject`.

### Changed

* Automatically convert `Brep` to `Mesh` when assigned in `IFC2X3`.

### Removed


## [1.0.0] 2024-07-12

### Added

* Added full python class mapping for `IFC4` and `IFC2x3` using `compas_ifc.entities.Generator`.
* All `IFC4` and `IFC2x3` classes are now available in `compas_ifc.entities.generated` module.
* All generated classes are strongly typed and have docstrings.
* Added `compas_ifc.entities.extensions` module to extend generated IFC classes.
* Added `show` function to visualize IFC model and individual entities.
* Added `max_depth` in `print_spatial_hierarchy` functions.
* Added `building_storeys` to `compas_ifc.model.Model`.
* Added `compas_ifc.brep.IFCBrepObject`.

### Changed

* Combined `compas_ifc.reader.Reader` and `compas_ifc.writer.Writer` into `compas_ifc.file.IFCFile`.
* Updated `create` in `compas_ifc.model.Model` to accept snake_case keyword arguments.

### Removed

* Removed all `compas_ifc.entities.Entity` based class wrappers, use fully mapped classes in `compas_ifc.entities.generated` instead.
* Removed `representation.py` and `helper.py`.

## [0.6.0] 2024-06-26

### Added

### Changed

### Removed


## [0.5.1] 2024-06-14

### Added

### Changed

* Locked `ifcopenshell` to `0.7.0.240406` to avoid mathutils build failures.

### Removed


## [0.5.0] 2024-06-13

### Added

### Changed

### Removed


## [0.4.1] 2024-05-15

### Added

### Changed

### Removed


## [0.4.0] 2024-05-14

### Added

* Added support to export to `IFC2x3`.
* Added support pre-load geometries using `multi-processing`.

### Changed

* Updated workflow to not use `conda` anymore.
* Updated `Reader` to re-enable lazy loading.
* Update repo to use `pyproject.toml`.

### Removed


## [0.3.0] 2024-02-01

### Added

* Added `entity_opening_geometry`.
* Added `entity_body_with_opening_geometry`.
* Added `opening` attribute to `Product`.
* Added `body_with_opening` attribute to `Product`.
* Added `composite_body` attribute to `BuildingElement`.
* Added `composite_opening` attribute to `BuildingElement`.
* Added `composite_body_with_opening` attribute to `BuildingElement`.
* Added Documentation site.

### Changed

* `entity_body_geometry` no longer includes openings.
* `parent` of `Element` will now also consider `decompose` relation.
* Updated all APIs to COMPAS 2.

### Removed

## [0.2.0] 2023-03-21

### Added

### Changed

### Removed
