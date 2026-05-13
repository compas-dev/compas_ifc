# compas_ifc multi-step workflows

Patterns where you chain several commands together.

## "Show me X on the first floor, then export them"

This is the canonical agent workflow. The user says "show me all windows on
the first floor of this building", then "okay, now export those windows as a
standalone IFC."

Steps:

1. **Find the storey.** "First floor" is ambiguous — match by name
   (`"Level 1"`, `"Ground Floor"`) or by `Elevation` (lowest non-basement).
   ```
   python -m compas_ifc list building.ifc --type IfcBuildingStorey --json
   ```
   If multiple plausible matches, confirm with the user before proceeding.
2. **Visualise the selection.** Capture the storey's GlobalId, then:
   ```
   python -m compas_ifc visualize building.ifc \
       --type IfcWindow --in <storey_id> --detach
   ```
   Tell the user: "Showing N windows on Level 1 in the viewer — keep
   chatting whenever you're ready."
3. **Export the same selection.** Reuse the filter from step 2 — the agent
   holds it in conversation context, not in any state file:
   ```
   python -m compas_ifc export-ifc building.ifc \
       --type IfcWindow --in <storey_id> --out windows.ifc
   ```

## "What can a thing do?"

When the user asks about an IFC class or a library object and you don't
remember the exact API:

1. Schema for the IFC side:
   ```
   python -m compas_ifc schema IfcDoor
   ```
2. compas_ifc API for the Python side:
   ```
   python -m compas_ifc docs IfcDoor --brief
   python -m compas_ifc docs --list IfcDoor --brief
   ```

The two together give you the EXPRESS-defined attributes (from `schema`)
plus the Python helpers compas_ifc adds via `@extends` (from `docs`).

## "Write a custom script"

When no CLI command fits — e.g. building geometry analysis, batch property
mutation, bespoke export format:

1. Pull a working example as a starting point:
   ```
   python -m compas_ifc tutorials list
   python -m compas_ifc tutorials show 4.1_edit_export
   ```
2. Look up the specific APIs you need:
   ```
   python -m compas_ifc docs BuildingInformationModel --brief
   python -m compas_ifc docs get_elements_by_type
   ```
3. Write the script using `BuildingInformationModel` as the entry point.

Avoid reconstructing library functionality from scratch when the library
already exposes it.

## "Compare two files"

There is no `diff` command. Use two `info` + two `list` calls and compare
in your head (or in JSON):

```
python -m compas_ifc info a.ifc --json
python -m compas_ifc info b.ifc --json
python -m compas_ifc list a.ifc --type IfcWall --json
python -m compas_ifc list b.ifc --type IfcWall --json
```

Diff the resulting JSON to surface added/removed entities.
