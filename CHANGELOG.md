# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

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
