# compas_ifc cookbook

Short, copy-pasteable recipes for the most common tasks. Every command takes
`--json` if you want to parse the output.

## File overview

```
python -m compas_ifc info building.ifc
```

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
python -m compas_ifc psets building.ifc <global_id>
```

## Visualise

Always `--detach`:

```
python -m compas_ifc visualize building.ifc --detach
python -m compas_ifc visualize building.ifc --type IfcWindow --in <storey_id> --detach
```

## Export a subset as standalone IFC

```
python -m compas_ifc export-ifc building.ifc --type IfcWindow --out windows.ifc
python -m compas_ifc export-ifc building.ifc --in <storey_id> --out level1.ifc
```

`--flat` strips spatial parents — use sparingly; the result is harder to
re-import in other tools.

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
python -m compas_ifc schema IfcWall --schema IFC4X3
```

## When CLI isn't enough — fall back to Python

```python
from compas_ifc.bim import BuildingInformationModel
model = BuildingInformationModel("building.ifc")

walls = model.get_elements_by_type("IfcWall")
for wall in walls:
    print(wall.name, wall.geometry)
```
