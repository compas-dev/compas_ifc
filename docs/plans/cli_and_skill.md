# Plan: `compas_ifc` CLI + Agent Skill

Status: phases 1–5 + 7 landed on branch `cli-and-skill`. Phase 6 (mutation),
8 (Codex), 9 (thumbnail) deferred.
Branch: `cli-and-skill`

## Goal

Turn `compas_ifc` into a first-class **command-line tool** and ship an
**agent skill** so AI coding agents (Claude Code first, Codex later) can drive
the library through structured commands rather than ad-hoc scripts.

Two surfaces, one source of truth:

1. A `python -m compas_ifc <command>` CLI exposed via `__main__.py` and a
   `cli/` subpackage. Every command supports `--json` for agent consumption.
2. A skill folder bundled inside the package (`src/compas_ifc/skill/`)
   installed into `~/.claude/skills/compas_ifc/` (or the Codex equivalent)
   by `python -m compas_ifc install-skill`. The skill is **version-coupled** to
   the installed library: recipes always match the API the user actually has.

## Design decisions (locked)

| Topic | Decision |
| --- | --- |
| CLI framework | `typer` |
| State file location | Inside the skill: `~/.claude/skills/compas_ifc/state.json` |
| State contents | User's *choice* of env (python path, env name) — not install state. Re-probe every run. |
| Tutorial bundling | Add `scripts/tutorials/` to `pyproject.toml` `package-data` (no folder move) |
| `export-ifc` default | Preserve spatial parents. `--flat` opt-in for bare project. |
| Visualize blocking | CLI has `--detach`; skill always invokes with `--detach` |
| `compas_viewer` install | Lazy — gated on first `visualize` call, not base onboarding |
| Codex support | Deferred. Track as Phase 8. |

## Shared selection grammar

Used by `list`, `query`, `visualize`, `export-ifc`. One implementation reused
everywhere:

```
--type IfcWindow             # by IFC class
--where "Name~'casement'"    # simple key/op/value filter (op: =, !=, >, <, ~)
--in <storey_global_id>      # contained-in spatial element
--ids id1,id2,...            # explicit GlobalId list
```

These compose: `--type IfcWindow --in <storey_id>` returns windows on that
storey. Grow toward a richer DSL only if usage demands it.

## Command surface

### Inspect (Phase 1)
- `info <file>` — schema, units, project name, entity counts, byte size
- `tree <file> [--depth N]` — spatial hierarchy
- `list <file>` — entities matching a selection
- `show <file> <global_id>` — full entity dump
- `psets <file> <global_id>` — property sets

### Search (Phase 2)
- `query <file>` — selection grammar, structured output
- `find <file> <pattern>` — fuzzy name / GlobalId lookup

### Geometry & export (Phase 3)
- `export <file> --to mesh.obj [+ selection]` — geometry export
- `thumbnail <file> out.png` — visual snapshot
- `export-ifc <file> --out subset.ifc [+ selection] [--flat]` — IFC subset
  (wraps `ifcpatch`'s `ExtractElements` recipe; preserves parents by default)

### Visualize (Phase 4)
- `visualize <file> [+ selection] [--detach]`
- Probes for `compas_viewer` on first use; if missing, walks user through
  install before invoking
- Catches viewer import/runtime errors (e.g. freetype) and surfaces a
  clean message rather than a traceback

### Docs & introspection (Phase 5)
- `docs <symbol> [--brief] [--list <parent>]` — `inspect`/`pydoc` wrapper
  over the installed `compas_ifc`; `--brief` returns
  `signature -> return : first_docstring_line`; `--list IfcElement`
  enumerates members
- `schema <IfcClass>` — wraps `ifcopenshell` schema introspection:
  attributes, inverses, derived attrs in the file's schema version
- `tutorials list` / `tutorials show <name>` — surface
  `scripts/tutorials/` shipped as package data

### Mutation (Phase 6, gated)
- `set-pset`, `set-attr`, `remove` — behind explicit `--write` flag

### Skill management (Phase 7)
- `install-skill [--target claude|codex|both] [--uninstall]`

## Skill layout

```
src/compas_ifc/skill/
├── SKILL.md
├── references/
│   ├── cookbook.md         # ~3–5KB hand-curated recipes
│   └── workflows.md        # common multi-step patterns
```

Installed to `~/.claude/skills/compas_ifc/`, plus `state.json` written there
on first run.

### Onboarding flow (in SKILL.md)

1. Read `state.json` if present; otherwise:
2. Detect environment — `$CONDA_DEFAULT_ENV`, `$VIRTUAL_ENV`,
   `python -c "import sys; print(sys.executable, sys.prefix)"`. Surface the
   result.
3. Probe — `python -c "import compas_ifc"`.
4. If missing: ask user (PyPI / editable clone / new conda env), recommend
   conda for native deps, execute, re-probe.
5. Persist the **choice** to `state.json`. Subsequent runs: read state →
   probe → silent pass-through on success.

### Other skill rules

- `visualize` always invoked with `--detach`; tell user the viewer is open
- For requests not covered by CLI, write Python directly — consult
  `docs --brief` and `schema` first; reference `tutorials show <N>` for
  worked examples
- Read `references/cookbook.md` on first use

## Phases

1. ✅ **CLI foundation** — `__main__.py`, typer scaffolding, `info`/`tree`/
   `list`/`show`/`psets`, `--json` everywhere
2. ✅ **Selection grammar + search** — shared filter implementation, `query`,
   `find`
3. ✅ **Geometry export** — `export` (compas Mesh → .obj/.json),
   `export-ifc` (wraps `IFCFile.export`, preserves parents by default)
4. ✅ **Visualization** — `visualize` with lazy `compas_viewer` probe,
   `--detach` via `subprocess.Popen` (Windows: `CREATE_NEW_PROCESS_GROUP |
   DETACHED_PROCESS`; POSIX: `start_new_session=True`)
5. ✅ **Docs introspection** — `docs` (signature + docstring,
   `--brief`/`--list`), `schema` (ifcopenshell schema dump), `tutorials`
   (subcommands `list`/`show`)
6. ⏸ **Mutation** — `set-pset`, `set-attr`, `remove` behind `--write`
   (deferred; design needs care around in-place vs new-file writes)
7. ✅ **Skill (Claude target)** — `src/compas_ifc/skill/` with `SKILL.md` +
   `references/cookbook.md` + `references/workflows.md`; `install-skill`
   subcommand installs to `~/.claude/skills/compas_ifc/`; uninstall and
   force-overwrite supported
8. ⏸ **Codex target** — deferred; current `install-skill --target codex`
   exits with a clear "not yet implemented" message
9. ⏸ **Thumbnail** — deferred; needs offscreen rendering setup

## Open items

- **Codex layout**: Codex's `AGENTS.md` conventions are still moving.
  Verify the current spec before Phase 8. Likely project-local rather than
  global; cookbook content may need flattening (no `references/`
  progressive-disclosure mechanism).
- **Marketplace publication**: separate to bundled-in-package install.
  Decide later whether to also publish via a Claude Code plugin
  marketplace for discovery.
- **Visualize on Windows**: `--detach` needs `CREATE_NEW_PROCESS_GROUP +
  DETACHED_PROCESS` flags. Test on Win11 before locking default.
