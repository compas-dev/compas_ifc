---
name: compas_ifc
description: Pythonic IFC interface for reading, querying, visualising, and exporting IFC building models. Use whenever the user references an `.ifc` file, IFC entities (IfcWall, IfcDoor, IfcBuildingStorey, etc.), BIM data, or compas_ifc itself. Invoked through `python -m compas_ifc <command>`.
---

# compas_ifc skill

You are helping the user work with IFC (Industry Foundation Classes) building
models through **compas_ifc** — a Python library wrapping `ifcopenshell` with
COMPAS geometry. The primary interface is the CLI: `python -m compas_ifc <command>`.

Every command supports `--json` for structured output you can parse.

## Onboarding (first invocation only)

Before running any command, check whether onboarding has been completed.

1. Read `state.json` in this skill folder.
   - If present and `python_executable` is set, jump to step 4.
2. **Detect the user's environment.** Run (Windows PowerShell or POSIX):
   - `$env:CONDA_DEFAULT_ENV` / `$CONDA_DEFAULT_ENV`
   - `$env:VIRTUAL_ENV` / `$VIRTUAL_ENV`
   - `python -c "import sys; print(sys.executable, sys.prefix)"`

   Report back to the user: "You're using Python at `<path>` (conda env `<name>` / venv / system)."
3. **Probe.** Run `python -c "import compas_ifc"`. If it succeeds, jump to step 5.
4. **Install.** Ask the user how they want to install:
   - **Option A** — into the detected env (`pip install compas_ifc`). Recommended if they're already in a conda env.
   - **Option B** — create a new conda env: `conda create -n compas-ifc python=3.11 -y && conda activate compas-ifc && pip install compas_ifc`. Recommended on Windows or if no env is active (`ifcopenshell` and `compas_occ` are happiest in conda).
   - **Option C** — system Python (not recommended).

   Wait for the user to choose. Run the command. Re-probe.
5. **Persist.** Write `state.json` next to this file:
   ```json
   {"python_executable": "<path from step 2>", "env_name": "<conda env or null>"}
   ```
6. On subsequent runs, read `state.json`, run the probe in the recorded env,
   and stay silent unless the probe fails (then re-run onboarding).

## Command reference

All commands: `python -m compas_ifc <command> [args] [--json]`.

| Command | Purpose |
|---|---|
| `info FILE` | Schema, units, project name, entity counts, byte size |
| `tree FILE [--depth N]` | Spatial hierarchy: Project → Site → Building → Storey → Elements |
| `list FILE [SELECTION] [--limit N]` | Entities matching the selection |
| `query FILE [SELECTION] [--select a,b,...]` | List + inline chosen attributes |
| `find FILE PATTERN` | Exact GlobalId or fuzzy name search |
| `show FILE GLOBAL_ID` | Full attribute dump for one entity |
| `psets FILE GLOBAL_ID` | Property sets for an entity |
| `visualize FILE [SELECTION] --detach` | Open the viewer (ALWAYS use `--detach`) |
| `export-ifc FILE [SELECTION] --out X.ifc [--flat]` | Export subset as a standalone IFC |
| `export FILE [SELECTION] --to X.obj` | Export geometry as `.obj` or `.json` |
| `docs SYMBOL [--brief]` | Introspect compas_ifc — signature + docstring |
| `docs --list PARENT [--brief]` | List public members of a class/module |
| `schema IFC_CLASS [--schema IFC4]` | IFC schema: attributes, inverses, supertypes |
| `tutorials list` / `tutorials show NAME` | Bundled worked-example scripts |

### Shared selection grammar

`list`, `query`, `visualize`, `export-ifc`, and `export` all accept the same
filters. They compose with AND:

- `--type IfcWindow` — IFC class (matches subclasses)
- `--where "OverallHeight>2"` — predicate (ops: `=`, `!=`, `>`, `<`, `>=`, `<=`, `~`)
- `--in <storey_global_id>` — contained inside a spatial element (transitive)
- `--ids id1,id2,...` — explicit GlobalId list

Dotted paths work in `--where` and `--select` (e.g. `--select OwnerHistory.Owner.ThePerson.GivenName`).

## Critical rules

1. **`visualize` must always be invoked with `--detach`.** Without it, the
   viewer GUI blocks the conversation until the user closes the window.
   After detaching, tell the user the viewer is open and you'll keep
   working.
2. **`compas_viewer` is a lazy dependency.** If `visualize` reports it's
   missing, walk the user through installing it (`pip install compas_viewer`).
   Mention it's heavy (Qt + freetype) and not strictly required for
   inspection/export workflows.
3. **Writes are explicit.** `export-ifc` and `export` write *new* files
   they don't modify the source. Mutation commands (`set-pset`, etc.) are
   gated behind a `--write` flag when present.

## When the CLI isn't enough

For tasks not covered by a command, write a small Python script. **Before
writing**, use the introspection commands:

1. `python -m compas_ifc docs <symbol> --brief` — see signature + first
   docstring line. Use `--list <parent>` to enumerate members.
2. `python -m compas_ifc schema <IfcClass>` — IFC schema for that class.
3. `python -m compas_ifc tutorials list` and `tutorials show <name>` —
   end-to-end worked examples.

Then write the script. Do not reconstruct library functionality from scratch
when a direct API exists. The canonical entry point is:

```python
from compas_ifc.bim import BuildingInformationModel
model = BuildingInformationModel("file.ifc")
```

## References

See `references/cookbook.md` for one-line recipes covering the 80% of tasks.
See `references/workflows.md` for multi-step patterns including the
"show then export" flow the user will frequently want.
