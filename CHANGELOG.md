# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
