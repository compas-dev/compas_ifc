# compas_ifc cookbook

Short, copy-pasteable recipes for the most common tasks. Every command takes
`--json` if you want to parse the output.

## File summary (use this for "what is this file?")

```
python -m compas_ifc summary building.ifc
```

Bundles project name + description, IfcSite geographic location (when
available), file size, schema, units, and the spatial hierarchy down to
storey level. One call answers the most common opening question.

## Lightweight info

```
python -m compas_ifc info building.ifc
```

Smaller surface than `summary` — schema, units, project name, total
entity count, byte size. No hierarchy, no location.

## Spatial hierarchy

```
python -m compas_ifc tree building.ifc --depth 3
```

## List entities of a class

```
python -m compas_ifc list building.ifc --type IfcWall
python -m compas_ifc list building.ifc --type IfcWindow --limit 5
```

## Filter with a predicate

```
python -m compas_ifc list building.ifc --type IfcWindow --where "OverallHeight>2"
python -m compas_ifc list building.ifc --type IfcWall --where "Name~'partition'"
```

Operators: `=`, `!=`, `>`, `<`, `>=`, `<=`, `~` (case-insensitive substring).

## Elements on a specific storey

Step 1: list storeys to get the GlobalId.

```
python -m compas_ifc list building.ifc --type IfcBuildingStorey
```

Step 2: filter elements by containment.

```
python -m compas_ifc list building.ifc --type IfcWindow --in <storey_global_id>
```

## Inline attribute values

When you need IDs *and* attributes in one call:

```
python -m compas_ifc query building.ifc --type IfcWindow \
    --where "OverallHeight>2" --select OverallHeight,OverallWidth
```

## Fuzzy search by name

```
python -m compas_ifc find building.ifc "Casement"
python -m compas_ifc find building.ifc "Level 1"
```

## Show an entity in detail

```
python -m compas_ifc show building.ifc <global_id>
python -m compas_ifc show building.ifc <global_id> --depth 3
python -m compas_ifc psets building.ifc <global_id>
```

Default `show` is one level deep — nested entities (`OwnerHistory`,
`ObjectPlacement`, `Representation`, ...) appear as `{"$ref": <id>,
"type": <IfcClass>}` stubs. Raise `--depth` to inline successive levels
of the attribute tree; cycles are broken so depth doesn't blow up on
recursive placement chains.

## Visualise

Always `--detach`. Selections preserve spatial hierarchy by default, so
elements render at their real world position; add `--no-keep-hierarchy`
for a parts-library view at the origin:

```
python -m compas_ifc visualize building.ifc --detach
python -m compas_ifc visualize building.ifc --type IfcWindow --in <storey_id> --detach
python -m compas_ifc visualize building.ifc --type IfcWindow --no-keep-hierarchy --detach
```

## Clash / interference detection

Find pairs of elements that volumetrically overlap. The default filter
excludes expected overlaps (wall → opening → window/door).

```
python -m compas_ifc clash building.ifc
python -m compas_ifc clash building.ifc --type IfcBeam,IfcWall,IfcWallStandardCase
python -m compas_ifc clash building.ifc --json
```

Visualise: each pair gets a unique colour, penetration points are marked.
Always pair `--show` with `--detach`:

```
python -m compas_ifc clash building.ifc --show --detach
python -m compas_ifc clash building.ifc --type IfcBeam,IfcColumn,IfcWall --show --detach
```

Useful tunables: `--tolerance` (numerical), `--min-depth` (excludes
touching pairs), `--include-related` (keep the wall→opening→filler
chains the default filter strips), `--limit N` (cap text listing).

## Export a subset as standalone IFC

```
python -m compas_ifc export-ifc building.ifc --type IfcWindow --out windows.ifc
python -m compas_ifc export-ifc building.ifc --in <storey_id> --out level1.ifc
python -m compas_ifc export-ifc building.ifc --type IfcWindow --out windows.ifc --flat
```

By default the source's real Project/Site/Building/Storey ancestors come
along. `--flat` instead anchors the selection under a fresh placeholder
Project/Site/Building/Storey ("Placeholder Project" etc.) — use it when
you want a self-contained component snippet without dragging the original
spatial metadata. World positions are preserved either way.

## Export geometry

```
python -m compas_ifc export building.ifc --type IfcWall --to walls.obj
```

`.obj` and `.json` (COMPAS mesh format) are supported.

## Introspect the library API

```
python -m compas_ifc docs BuildingInformationModel --brief
python -m compas_ifc docs --list BuildingInformationModel --brief
python -m compas_ifc docs get_element_by_global_id
```

## Introspect the IFC schema

```
python -m compas_ifc schema IfcWindow
python -m compas_ifc schema IfcWindow --depth 5
python -m compas_ifc schema IfcWall --schema IFC4X3
```

`schema` reads the bundled `.pyi` stubs, so its attribute list already
includes Python members added by `@extends` (e.g. `parent`, `frame`,
`property_sets`). Default `--depth 1` lists this class's own + inherited
attributes flat; raise depth to recurse into each entity-typed attribute
(stops at primitives, enums, and cycle hits).

## When CLI isn't enough — fall back to Python

```python
from compas_ifc.bim import BuildingInformationModel

# For attribute / pset / relationship work, mirror the CLI's defaults:
# disable both geometry loading and placement rectification.
# Enable them only when the work needs geometry (bbox, mesh export,
# viewer rendering, clash detection).
model = BuildingInformationModel(
    "building.ifc",
    load_geometries=False,
    rectify_placements=False,
)

walls = model.get_elements_by_type("IfcWall")
for wall in walls:
    # .name, .ifc_type, .global_id are on the GenericElement wrapper.
    # The Base-wrapped IFC entity is at wall._ifc_entity — that's where
    # the @extends mixins live: .property_sets, .parent (storey), .frame,
    # plus any EXPRESS attribute on the class.
    psets = wall._ifc_entity.property_sets
    storey = wall._ifc_entity.parent  # IfcBuildingStorey wrapper
    print(wall.name, storey.Name, psets.get("Pset_WallCommon", {}))
```

**Don't drop to raw `ifcopenshell` to "skip geometry loading."** The
`load_geometries=False` flag above does exactly that, and going through
`BuildingInformationModel` keeps `@extends` mixins (`.property_sets`,
`.parent`, `.frame`, unit scaling) available.
