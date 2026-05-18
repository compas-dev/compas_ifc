"""compas_ifc command-line interface — Phase 1 commands.

All commands accept ``--json`` for structured, agent-friendly output. The
human-readable default is meant for terminal users; JSON is the contract
the agent skill relies on.

Heavy imports (``compas_ifc.bim``) are deferred to command bodies so the
``--help`` path stays fast.
"""

from __future__ import annotations

import ast
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Optional

import typer

app = typer.Typer(
    name="compas_ifc",
    help="Pythonic IFC interface — command-line tools and agent surface.",
    no_args_is_help=True,
    add_completion=False,
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _check_file(filepath: str) -> None:
    if not os.path.exists(filepath):
        typer.echo(f"error: file not found: {filepath}", err=True)
        raise typer.Exit(code=1)


def _open_model(filepath: str, load_geometries: bool = False, rectify_placements: bool = False):
    """Open an IFC file as a BuildingInformationModel.

    Geometry loading and placement rectification are opt-in because CLI
    commands rarely need them and they dominate startup cost on large files.
    Stdout chatter from the library load (rectification stats, graph-edge
    counts) is redirected so JSON consumers see a clean stream.
    """
    import contextlib
    import io

    from compas_ifc.bim import BuildingInformationModel

    with contextlib.redirect_stdout(io.StringIO()):
        return BuildingInformationModel(
            filepath=filepath,
            load_geometries=load_geometries,
            rectify_placements=rectify_placements,
        )


def _emit(data: Any, json_output: bool, human: Optional[Callable] = None) -> None:
    """Emit a payload either as JSON or as a human-readable rendering.

    ``human`` is an optional callable that receives ``data`` and prints to
    stdout for terminal use; when missing, a generic pretty-printer is used.
    """
    if json_output:
        typer.echo(json.dumps(data, indent=2, default=_jsonable))
        return
    if human is not None:
        human(data)
    else:
        _default_human(data)


def _jsonable(obj: Any) -> Any:
    """Last-resort serialiser for objects ``json.dumps`` can't handle."""
    try:
        return str(obj)
    except Exception:
        return repr(obj)


def _default_human(data: Any, indent: int = 0) -> None:
    pad = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)) and value:
                typer.echo(f"{pad}{key}:")
                _default_human(value, indent + 1)
            else:
                typer.echo(f"{pad}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                _default_human(item, indent)
                typer.echo("")
            else:
                typer.echo(f"{pad}- {item}")
    else:
        typer.echo(f"{pad}{data}")


def _entity_summary(entity) -> dict:
    """A compact, agent-friendly summary of a single IFC entity."""
    raw = getattr(entity, "entity", entity)
    return {
        "global_id": getattr(entity, "GlobalId", None),
        "type": raw.is_a() if hasattr(raw, "is_a") else None,
        "name": getattr(entity, "Name", None),
        "id": raw.id() if hasattr(raw, "id") else None,
    }


def _require_compas_viewer() -> None:
    """Probe compas_viewer and exit cleanly with an install hint if missing.

    Some environments have a half-installed compas_viewer (e.g. the freetype
    binding bug noted in MEMORY.md) that imports raise on; catch both cases.
    """
    try:
        import compas_viewer  # noqa: F401
    except ImportError:
        typer.echo("error: compas_viewer is not installed.", err=True)
        typer.echo("install with: pip install compas_viewer", err=True)
        raise typer.Exit(code=1)
    except Exception as exc:
        typer.echo(f"error: compas_viewer failed to import: {exc}", err=True)
        raise typer.Exit(code=1)


def _detach_relay(subcommand: str, file: str, extra_args: list, json_output: bool, message: str) -> None:
    """Spawn `python -m compas_ifc <subcommand> <file> <extra_args...>` detached.

    Used by every command that opens a viewer so the CLI returns immediately
    and the GUI doesn't block the parent shell or an agent session.
    """
    import subprocess
    import sys

    relay = [sys.executable, "-m", "compas_ifc", subcommand, file, *extra_args]

    kwargs: dict = {}
    if sys.platform == "win32":
        # CREATE_NEW_PROCESS_GROUP + DETACHED_PROCESS: child runs without a console
        # and survives the parent exiting.
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008  # DETACHED_PROCESS
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
    else:
        kwargs["start_new_session"] = True
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL

    proc = subprocess.Popen(relay, **kwargs)
    payload = {"detached": True, "pid": proc.pid, "filepath": os.path.abspath(file)}
    _emit(payload, json_output, lambda _: typer.echo(message.format(pid=proc.pid)))


# ---------------------------------------------------------------------------
# info
# ---------------------------------------------------------------------------


@app.command()
def info(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Summarise an IFC file: schema, units, project, entity counts, size."""
    _check_file(file)
    model = _open_model(file)
    project = model.project

    raw_file = model._file._file
    entity_count = sum(1 for _ in raw_file)

    project_data: Optional[dict] = None
    if project is not None:
        project_data = {
            "global_id": getattr(project, "GlobalId", None),
            "name": getattr(project, "Name", None),
            "description": getattr(project, "Description", None),
        }

    data = {
        "filepath": os.path.abspath(file),
        "schema": model.schema_name,
        "size_mb": model._file.file_size(),
        "unit": model.unit,
        "project": project_data,
        "entity_count": entity_count,
    }
    _emit(data, json_output)


# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------


@app.command()
def summary(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    depth: int = typer.Option(
        3,
        "--depth",
        help="Maximum spatial-hierarchy depth (default 3 stops at storey level).",
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """High-level overview: project, location, file size, and spatial hierarchy.

    The go-to command for the question 'what is this IFC file?'. Bundles
    project name + description, geographic location (when present on
    IfcSite), file size, schema, units, and the spatial hierarchy down to
    a configurable depth.
    """
    _check_file(file)
    model = _open_model(file)

    project = model.project
    project_data: Optional[dict] = None
    if project is not None:
        project_data = {
            "global_id": getattr(project, "GlobalId", None),
            "name": getattr(project, "Name", None),
            "description": getattr(project, "Description", None),
        }

    sites_data: list[dict] = []
    for site in model.sites:
        # Geographic location lives on the IFC entity (extension property).
        ifc_site = getattr(site, "_ifc_entity", None)
        location = getattr(ifc_site, "location", None) if ifc_site is not None else None
        sites_data.append(
            {
                "global_id": getattr(site, "global_id", None),
                "name": getattr(site, "name", None),
                "location": list(location) if location else None,
            }
        )

    roots = _build_hierarchy(model, depth)

    payload = {
        "filepath": os.path.abspath(file),
        "size_mb": model._file.file_size(),
        "schema": model.schema_name,
        "unit": model.unit,
        "project": project_data,
        "sites": sites_data,
        "hierarchy": roots,
    }

    def human(_):
        typer.echo(f"File:        {payload['filepath']}")
        typer.echo(f"Size:        {payload['size_mb']} MB")
        typer.echo(f"Schema:      {payload['schema']}")
        typer.echo(f"Units:       {payload['unit']}")
        if project_data:
            typer.echo("")
            typer.echo(f"Project:     {project_data.get('name') or '(unnamed)'}")
            typer.echo(f"Description: {project_data.get('description') or '(none)'}")
        for site in sites_data:
            loc = site.get("location")
            loc_str = f"{loc[0]:.6f}, {loc[1]:.6f}  (lat, lng)" if loc else "(not specified)"
            typer.echo("")
            typer.echo(f"Site:        {site.get('name') or '(unnamed)'}")
            typer.echo(f"Location:    {loc_str}")
        typer.echo("")
        typer.echo("Spatial hierarchy:")
        _render_tree(roots, level=1)

    _emit(payload, json_output, human)


def _build_hierarchy(model, depth: int) -> list:
    """Walk ``model.tree`` and emit nested dicts up to ``depth`` levels deep."""

    def node_dict(element, current_depth):
        if current_depth > depth:
            return None
        children = []
        for child in getattr(element, "children", []) or []:
            child_node = node_dict(child, current_depth + 1)
            if child_node is not None:
                children.append(child_node)
        return {
            "type": getattr(element, "ifc_type", None),
            "name": getattr(element, "name", None),
            "global_id": getattr(getattr(element, "_ifc_entity", None), "GlobalId", None),
            "children": children,
        }

    roots = []
    for node in model.tree.root.children:
        rendered = node_dict(node.element, 1)
        if rendered is not None:
            roots.append(rendered)
    return roots


# ---------------------------------------------------------------------------
# tree
# ---------------------------------------------------------------------------


@app.command()
def tree(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    depth: int = typer.Option(10, "--depth", help="Maximum spatial-hierarchy depth."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Print the spatial hierarchy: Project → Site → Building → Storey → Elements."""
    _check_file(file)
    model = _open_model(file)
    roots = _build_hierarchy(model, depth)

    payload = {"model": model.name, "roots": roots}

    def human(_):
        typer.echo(f"BuildingInformationModel: {model.name}")
        _render_tree(roots, level=1)

    _emit(payload, json_output, human)


def _render_tree(nodes, level: int) -> None:
    pad = "  " * level
    for n in nodes:
        gid = n.get("global_id")
        suffix = f"  [{gid}]" if gid else ""
        typer.echo(f"{pad}{n.get('type')}: {n.get('name')}{suffix}")
        children = n.get("children") or []
        if children:
            _render_tree(children, level + 1)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def _selection_filter(payload_filter: dict, selection) -> dict:
    """Drop empty selection fields from a payload's filter block."""
    return {k: v for k, v in payload_filter.items() if v is not None}


@app.command(name="list")
def list_(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    type_: str = typer.Option(None, "--type", help="IFC class (matches subclasses)."),
    where: str = typer.Option(None, "--where", help="Predicate: '<key> <op> <value>' (ops: =, !=, >, <, >=, <=, ~)."),
    in_: str = typer.Option(None, "--in", help="GlobalId of a spatial container; restricts to its (transitive) contents."),
    ids: str = typer.Option(None, "--ids", help="Comma-separated GlobalIds — overrides --type as the seed set."),
    limit: int = typer.Option(0, "--limit", help="Limit number of results (0 = no limit)."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """List entities matching a selection.

    Filters compose with AND. With no flags, lists all IfcRoot-rooted
    entities in the file.
    """
    from compas_ifc.cli.selection import Selection
    from compas_ifc.cli.selection import apply_selection

    _check_file(file)
    model = _open_model(file)

    selection = Selection(type_=type_, where=where, in_=in_, ids=ids)
    try:
        entities = apply_selection(model, selection)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1)

    if limit and limit > 0:
        entities = entities[:limit]

    filter_block = _selection_filter(
        {"type": type_, "where": where, "in": in_, "ids": ids},
        selection,
    )
    payload = {
        "filter": filter_block or None,
        "count": len(entities),
        "entities": [_entity_summary(e) for e in entities],
    }

    def human(_):
        descriptor = filter_block if filter_block else "no filter"
        typer.echo(f"{len(entities)} entities ({descriptor}):")
        for summary in payload["entities"]:
            gid = summary.get("global_id") or f"#{summary.get('id')}"
            typer.echo(f"  {summary.get('type'):<30} {gid}  {summary.get('name') or ''}")

    _emit(payload, json_output, human)


# ---------------------------------------------------------------------------
# query
# ---------------------------------------------------------------------------


@app.command()
def query(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    type_: str = typer.Option(None, "--type", help="IFC class (matches subclasses)."),
    where: str = typer.Option(None, "--where", help="Predicate: '<key> <op> <value>' (ops: =, !=, >, <, >=, <=, ~)."),
    in_: str = typer.Option(None, "--in", help="GlobalId of a spatial container; restricts to its (transitive) contents."),
    ids: str = typer.Option(None, "--ids", help="Comma-separated GlobalIds — overrides --type as the seed set."),
    select: str = typer.Option(None, "--select", help="Comma-separated attribute names to inline on each result (dotted paths allowed)."),
    limit: int = typer.Option(0, "--limit", help="Limit number of results (0 = no limit)."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Filter entities with the selection grammar and inline chosen attributes.

    ``query`` is the structured-output sibling of ``list``: it accepts the
    same filters, plus ``--select`` for pulling specific attributes onto
    each row so an agent can answer "which windows are taller than 2m and
    what are their widths" in one call.
    """
    from compas_ifc.cli.selection import Selection
    from compas_ifc.cli.selection import _entity_attr
    from compas_ifc.cli.selection import apply_selection

    _check_file(file)
    model = _open_model(file)

    selection = Selection(type_=type_, where=where, in_=in_, ids=ids)
    try:
        entities = apply_selection(model, selection)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1)

    if limit and limit > 0:
        entities = entities[:limit]

    select_keys = [k.strip() for k in (select.split(",") if select else []) if k.strip()]

    rows = []
    for entity in entities:
        row = _entity_summary(entity)
        for key in select_keys:
            row[key] = _scalar(_entity_attr(entity, key))
        rows.append(row)

    filter_block = _selection_filter(
        {"type": type_, "where": where, "in": in_, "ids": ids},
        selection,
    )
    payload = {
        "filter": filter_block or None,
        "select": select_keys or None,
        "count": len(entities),
        "entities": rows,
    }

    def human(_):
        descriptor = filter_block if filter_block else "no filter"
        typer.echo(f"{len(entities)} entities ({descriptor}):")
        if not select_keys:
            for row in rows:
                gid = row.get("global_id") or f"#{row.get('id')}"
                typer.echo(f"  {row.get('type'):<30} {gid}  {row.get('name') or ''}")
        else:
            headers = ["type", "global_id", "name", *select_keys]
            typer.echo("  " + "  ".join(headers))
            for row in rows:
                cells = [str(row.get(h, "")) for h in headers]
                typer.echo("  " + "  ".join(cells))

    _emit(payload, json_output, human)


# ---------------------------------------------------------------------------
# find
# ---------------------------------------------------------------------------


@app.command()
def find(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    pattern: str = typer.Argument(..., help="GlobalId (exact) or name substring (case-insensitive)."),
    limit: int = typer.Option(20, "--limit", help="Limit number of results."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Find entities by GlobalId (exact) or name (substring + fuzzy ranking)."""
    from difflib import SequenceMatcher

    from compas_ifc.cli.selection import _find_raw_by_global_id

    _check_file(file)
    model = _open_model(file)

    # Exact GlobalId match — short-circuit.
    raw = _find_raw_by_global_id(model, pattern)
    if raw is not None:
        wrapped = model._file.from_entity(raw)
        payload = {
            "pattern": pattern,
            "match": "global_id_exact",
            "count": 1,
            "entities": [_entity_summary(wrapped)],
        }
        _emit(payload, json_output)
        return

    # Otherwise scan names of IfcRoot entities.
    needle = pattern.lower()
    try:
        candidates = list(model._file._file.by_type("IfcRoot"))
    except RuntimeError:
        candidates = []

    def score(name: str) -> float:
        return SequenceMatcher(None, needle, name.lower()).ratio()

    hits: list[tuple[float, Any]] = []
    for entity in candidates:
        name = getattr(entity, "Name", None) or ""
        if needle in name.lower():
            hits.append((1.0, entity))
        else:
            ratio = score(name) if name else 0.0
            if ratio >= 0.6:
                hits.append((ratio, entity))

    hits.sort(key=lambda pair: pair[0], reverse=True)
    hits = hits[:limit] if limit > 0 else hits

    rows = [_entity_summary(model._file.from_entity(e)) for _, e in hits]

    payload = {
        "pattern": pattern,
        "match": "name_substring_or_fuzzy",
        "count": len(rows),
        "entities": rows,
    }

    def human(_):
        if not rows:
            typer.echo(f"no matches for {pattern!r}")
            return
        typer.echo(f"{len(rows)} match(es) for {pattern!r}:")
        for row in rows:
            gid = row.get("global_id") or f"#{row.get('id')}"
            typer.echo(f"  {row.get('type'):<30} {gid}  {row.get('name') or ''}")

    _emit(payload, json_output, human)


# ---------------------------------------------------------------------------
# show
# ---------------------------------------------------------------------------


@app.command()
def show(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    global_id: str = typer.Argument(..., help="IFC GlobalId of the entity to dump."),
    depth: int = typer.Option(
        1,
        "--depth",
        help=(
            "How many levels deep to expand referenced entities. 1 (default) "
            "shows direct attributes only — nested entities appear as "
            "$ref pointers. Raise to inline successive levels of the "
            "attribute tree."
        ),
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Dump a single entity's attributes by GlobalId.

    With ``--depth 1`` (default), nested entity attributes are returned as
    ``{"$ref": <id>, "type": <IfcClass>}`` stubs. Raising ``--depth`` inlines
    each referenced entity's own attributes, recursively, up to the limit.
    Cycles are broken: any entity already on the current expansion path is
    rendered as a ``$ref`` regardless of remaining depth.
    """
    _check_file(file)
    model = _open_model(file)

    entity = _find_by_global_id(model, global_id)
    if entity is None:
        typer.echo(f"error: no entity with GlobalId {global_id}", err=True)
        raise typer.Exit(code=1)

    raw = getattr(entity, "entity", entity)
    info_dict = raw.get_info(include_identifier=True, recursive=False)
    seen = frozenset([raw.id()])
    attrs = {k: _scalar(v, depth=depth - 1, seen=seen) for k, v in info_dict.items() if k != "type"}

    payload = {
        "type": raw.is_a(),
        "global_id": getattr(entity, "GlobalId", None),
        "id": raw.id(),
        "depth": depth,
        "attributes": attrs,
    }
    _emit(payload, json_output)


def _scalar(value, depth: int = 0, seen: frozenset = frozenset()):
    """Coerce an ifcopenshell value to something JSON can serialise.

    When ``depth > 0`` and ``value`` is an ``entity_instance`` not yet on
    the current expansion path, recursively inlines its attributes; the
    children get ``depth - 1`` and an extended ``seen`` set.
    """
    import ifcopenshell

    if isinstance(value, ifcopenshell.entity_instance):
        try:
            eid = value.id()
        except Exception:
            return str(value)
        if depth <= 0 or eid in seen:
            return {"$ref": eid, "type": value.is_a()}
        child_seen = seen | {eid}
        info = value.get_info(include_identifier=True, recursive=False)
        expanded = {"type": value.is_a(), "id": eid}
        for k, v in info.items():
            if k in ("type", "id"):
                continue
            expanded[k] = _scalar(v, depth=depth - 1, seen=child_seen)
        return expanded
    if isinstance(value, (list, tuple)):
        return [_scalar(v, depth=depth, seen=seen) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _find_by_global_id(model, global_id: str):
    """Return any Base-wrapped entity matching ``global_id``, not just spatial elements."""
    # First try the model's GenericElement index — fast path for spatial elements.
    found = model.get_element_by_global_id(global_id)
    if found is not None and found._ifc_entity is not None:
        return found._ifc_entity
    # Fall back to scanning IfcRoot entities in the file.
    try:
        for entity in model._file._file.by_type("IfcRoot"):
            if getattr(entity, "GlobalId", None) == global_id:
                return model._file.from_entity(entity)
    except RuntimeError:
        pass
    return None


# ---------------------------------------------------------------------------
# psets
# ---------------------------------------------------------------------------


@app.command()
def psets(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    global_id: str = typer.Argument(..., help="IFC GlobalId of the entity."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Show property sets for an entity."""
    _check_file(file)
    model = _open_model(file)

    entity = _find_by_global_id(model, global_id)
    if entity is None:
        typer.echo(f"error: no entity with GlobalId {global_id}", err=True)
        raise typer.Exit(code=1)

    # property_sets only exists on IfcObject and its subclasses.
    raw = getattr(entity, "entity", entity)
    if not raw.is_a("IfcObject"):
        typer.echo(
            f"error: entity {global_id} is {raw.is_a()}, not an IfcObject — no property sets",
            err=True,
        )
        raise typer.Exit(code=1)

    property_sets = getattr(entity, "property_sets", {}) or {}
    payload = {
        "global_id": global_id,
        "type": raw.is_a(),
        "property_sets": property_sets,
    }
    _emit(payload, json_output)


# ---------------------------------------------------------------------------
# visualize
# ---------------------------------------------------------------------------


@app.command()
def visualize(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    type_: str = typer.Option(None, "--type", help="IFC class (matches subclasses)."),
    where: str = typer.Option(None, "--where", help="Predicate: '<key> <op> <value>'."),
    in_: str = typer.Option(None, "--in", help="GlobalId of a spatial container."),
    ids: str = typer.Option(None, "--ids", help="Comma-separated GlobalIds."),
    detach: bool = typer.Option(
        False,
        "--detach",
        help="Launch the viewer in a background process and return immediately. The skill should always use this.",
    ),
    keep_hierarchy: bool = typer.Option(
        True,
        "--keep-hierarchy/--no-keep-hierarchy",
        help=(
            "Preserve the spatial hierarchy (Project/Site/Building/Storey/...) "
            "so selected elements appear at their world position. Disable for a "
            "parts-library view at the origin."
        ),
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Open the spatial scene (or a subset) in compas_viewer.

    Without ``--detach``, this blocks until the viewer window is closed.
    With ``--detach``, a child process is spawned, the viewer opens
    independently, and the CLI returns right away.

    ``compas_viewer`` is a lazy dependency. If it's not installed, this
    command exits with an install hint rather than a traceback.
    """
    _check_file(file)

    if detach:
        extra = []
        if type_:
            extra += ["--type", type_]
        if where:
            extra += ["--where", where]
        if in_:
            extra += ["--in", in_]
        if ids:
            extra += ["--ids", ids]
        if not keep_hierarchy:
            extra += ["--no-keep-hierarchy"]
        _detach_relay("visualize", file, extra, json_output, "viewer launched in background (pid={pid})")
        return

    _require_compas_viewer()

    # Geometry is required for visualisation; placement rectification keeps
    # the scene's transforms aligned with the spatial hierarchy.
    model = _open_model(file, load_geometries=True, rectify_placements=True)

    from compas_ifc.cli.selection import Selection
    from compas_ifc.cli.selection import apply_selection

    selection = Selection(type_=type_, where=where, in_=in_, ids=ids)
    elements = None
    if not selection.is_empty():
        try:
            entities = apply_selection(model, selection)
        except ValueError as exc:
            typer.echo(f"error: {exc}", err=True)
            raise typer.Exit(code=1)
        elements = []
        for entity in entities:
            gid = getattr(entity, "GlobalId", None)
            if not gid:
                continue
            elem = model.get_element_by_global_id(gid)
            if elem is not None:
                elements.append(elem)
        if not elements:
            typer.echo("error: selection matched no displayable elements", err=True)
            raise typer.Exit(code=1)

    model.show(elements=elements, keep_hierarchy=keep_hierarchy)


# ---------------------------------------------------------------------------
# clash
# ---------------------------------------------------------------------------


@app.command()
def clash(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    type_: str = typer.Option(
        None,
        "--type",
        help="IFC class(es) to include — single name or comma-separated list (e.g. 'IfcBeam,IfcWall').",
    ),
    tolerance: float = typer.Option(1e-6, "--tolerance", help="Numerical tolerance for ray-triangle intersection."),
    min_depth: float = typer.Option(1e-4, "--min-depth", help="Minimum penetration depth to count as a clash (excludes touching pairs)."),
    include_related: bool = typer.Option(
        False,
        "--include-related",
        help="Include spatially-related pairs (wall→opening→window/door etc.). Filtered out by default.",
    ),
    show: bool = typer.Option(False, "--show", help="Open compas_viewer with each clash pair in a unique colour."),
    detach: bool = typer.Option(
        False,
        "--detach",
        help="With --show, launch the viewer in a background process and return immediately. The skill should always use this.",
    ),
    limit: int = typer.Option(20, "--limit", help="Max pairs to list in human-readable output. 0 = unlimited."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Detect volumetric collisions (interferences) between building elements.

    Two-stage broadphase (BVH + tight AABB) plus ray-cast narrowphase. By
    default skips spatially-related pairs like ``wall → opening → window/door``
    where overlap is expected by construction.

    With ``--show``, opens compas_viewer with each pair in a unique colour
    and penetration points marked. Combine with ``--detach`` so the viewer
    runs in the background and the CLI returns.
    """
    _check_file(file)
    if detach and not show:
        raise typer.BadParameter("--detach requires --show")

    element_types = [t.strip() for t in type_.split(",") if t.strip()] if type_ else None

    if show and detach:
        extra = ["--show"]
        if type_:
            extra += ["--type", type_]
        if tolerance != 1e-6:
            extra += ["--tolerance", str(tolerance)]
        if min_depth != 1e-4:
            extra += ["--min-depth", str(min_depth)]
        if include_related:
            extra += ["--include-related"]
        _detach_relay("clash", file, extra, json_output, "clash viewer launched in background (pid={pid})")
        return

    if show:
        _require_compas_viewer()

    model = _open_model(file, load_geometries=True, rectify_placements=True)

    if show:
        model.show_collision_pairs(
            tolerance=tolerance,
            min_depth=min_depth,
            element_types=element_types,
            skip_related=not include_related,
        )
        return

    model.compute_collisions(
        tolerance=tolerance,
        min_depth=min_depth,
        element_types=element_types,
        skip_related=not include_related,
        create_ifc_relations=False,
    )

    pairs = []
    for edge in model.interferences:
        a, b = model._edge_elements(edge)
        pts = model.graph.edge_attribute(edge, "penetrating_points") or []
        pairs.append(
            {
                "a": {"ifc_type": a.ifc_type, "name": a.name, "global_id": a.global_id},
                "b": {"ifc_type": b.ifc_type, "name": b.name, "global_id": b.global_id},
                "penetrating_points": len(pts),
            }
        )

    payload = {
        "count": len(pairs),
        "candidate_types": element_types,
        "tolerance": tolerance,
        "min_depth": min_depth,
        "skip_related": not include_related,
        "pairs": pairs,
    }

    def _human(data):
        typer.echo(f"Found {data['count']} clash pair(s).")
        if not data["pairs"]:
            return
        shown = data["pairs"] if limit == 0 else data["pairs"][:limit]
        for p in shown:
            typer.echo(
                f"  {p['a']['ifc_type']} '{p['a']['name']}'  <->  "
                f"{p['b']['ifc_type']} '{p['b']['name']}'  ({p['penetrating_points']} pts)"
            )
        if len(shown) < len(data["pairs"]):
            typer.echo(f"  ... and {len(data['pairs']) - len(shown)} more (use --limit 0 to see all)")

    _emit(payload, json_output, _human)


# ---------------------------------------------------------------------------
# export-ifc
# ---------------------------------------------------------------------------


@app.command(name="export-ifc")
def export_ifc(
    file: str = typer.Argument(..., help="Path to the source IFC file."),
    out: str = typer.Option(..., "--out", help="Output IFC file path."),
    type_: str = typer.Option(None, "--type", help="IFC class (matches subclasses)."),
    where: str = typer.Option(None, "--where", help="Predicate: '<key> <op> <value>'."),
    in_: str = typer.Option(None, "--in", help="GlobalId of a spatial container."),
    ids: str = typer.Option(None, "--ids", help="Comma-separated GlobalIds."),
    flat: bool = typer.Option(False, "--flat", help="Anchor selected entities under a fresh placeholder Project/Site/Building/Storey instead of the source's real spatial hierarchy. The output is still a valid IFC; element world positions are preserved."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Export the selected entities as a standalone IFC file.

    By default, the entities' real spatial ancestors (IfcProject / IfcSite /
    IfcBuilding / IfcBuildingStorey) are copied into the output so the result
    stays anchored under the original hierarchy. With ``--flat``, a minimal
    placeholder hierarchy is built in the output instead, and each selected
    entity is contained under the placeholder storey with its world position
    preserved. Either mode produces a valid, self-contained IFC file.
    """
    from compas_ifc.cli.selection import Selection
    from compas_ifc.cli.selection import apply_selection

    _check_file(file)
    model = _open_model(file)

    selection = Selection(type_=type_, where=where, in_=in_, ids=ids)
    if selection.is_empty():
        typer.echo(
            "error: refusing to export the whole file — pass at least one of --type/--where/--in/--ids",
            err=True,
        )
        raise typer.Exit(code=1)

    try:
        entities = apply_selection(model, selection)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1)

    if not entities:
        typer.echo("error: selection matched zero entities — nothing to export", err=True)
        raise typer.Exit(code=1)

    # IFCFile.export writes Base entities and handles ancestor preservation / linked info.
    import contextlib
    import io

    with contextlib.redirect_stdout(io.StringIO()):
        model._file.export(out, entities=entities, as_snippet=flat)

    payload = {
        "output": os.path.abspath(out),
        "count": len(entities),
        "mode": "placeholder-hierarchy" if flat else "preserve-hierarchy",
        "filter": {k: v for k, v in {"type": type_, "where": where, "in": in_, "ids": ids}.items() if v},
    }

    def human(_):
        typer.echo(f"wrote {len(entities)} entities to {payload['output']} ({payload['mode']})")

    _emit(payload, json_output, human)


# ---------------------------------------------------------------------------
# export (geometry)
# ---------------------------------------------------------------------------


@app.command()
def export(
    file: str = typer.Argument(..., help="Path to an IFC file."),
    to: str = typer.Option(..., "--to", help="Output mesh file (.obj or .json)."),
    type_: str = typer.Option(None, "--type", help="IFC class (matches subclasses)."),
    where: str = typer.Option(None, "--where", help="Predicate: '<key> <op> <value>'."),
    in_: str = typer.Option(None, "--in", help="GlobalId of a spatial container."),
    ids: str = typer.Option(None, "--ids", help="Comma-separated GlobalIds."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Export geometry of selected elements to a single mesh file (.obj or .json)."""
    from compas.datastructures import Mesh

    from compas_ifc.cli.selection import Selection
    from compas_ifc.cli.selection import apply_selection

    _check_file(file)
    suffix = os.path.splitext(to)[1].lower()
    if suffix not in (".obj", ".json"):
        typer.echo(f"error: unsupported extension {suffix!r} — use .obj or .json", err=True)
        raise typer.Exit(code=1)

    model = _open_model(file, load_geometries=True)

    selection = Selection(type_=type_, where=where, in_=in_, ids=ids)
    try:
        entities = apply_selection(model, selection)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1)

    combined = Mesh()
    exported_count = 0
    skipped: list[dict] = []

    for entity in entities:
        gid = getattr(entity, "GlobalId", None)
        element = model.get_element_by_global_id(gid) if gid else None
        if element is None or element.geometry is None:
            skipped.append({"global_id": gid, "reason": "no geometry"})
            continue
        try:
            mesh = _element_to_mesh(element)
        except Exception as exc:
            skipped.append({"global_id": gid, "reason": f"mesh conversion failed: {exc}"})
            continue
        if mesh is None:
            skipped.append({"global_id": gid, "reason": "no convertible mesh"})
            continue
        _merge_mesh(combined, mesh)
        exported_count += 1

    if exported_count == 0:
        typer.echo("error: no exportable geometry in selection", err=True)
        raise typer.Exit(code=1)

    if suffix == ".obj":
        combined.to_obj(to)
    else:
        combined.to_json(to)

    payload = {
        "output": os.path.abspath(to),
        "format": suffix.lstrip("."),
        "exported": exported_count,
        "skipped": skipped,
    }

    def human(_):
        typer.echo(f"wrote {exported_count} element(s) to {payload['output']}")
        if skipped:
            typer.echo(f"skipped {len(skipped)} (no geometry or conversion error)")

    _emit(payload, json_output, human)


def _element_to_mesh(element):
    """Coerce an element's geometry into a :class:`compas.datastructures.Mesh`.

    Handles the shapes the library produces:

    - :class:`compas.datastructures.Mesh` — used as-is.
    - ``TessellatedBrep`` and the parametric ``representations.*`` classes
      (``Extrusion``, ``Revolution``, ``Pipe``, ``ClippedExtrusion``,
      ``BooleanResult``) all expose ``to_mesh()``.
    - Anything with ``vertices`` / ``faces`` attributes as a final fallback.
    """
    from compas.datastructures import Mesh

    geometry = element.geometry
    if geometry is None:
        return None
    if isinstance(geometry, Mesh):
        return geometry
    if hasattr(geometry, "to_mesh"):
        result = geometry.to_mesh()
        if isinstance(result, Mesh):
            return result
        if isinstance(result, tuple) and len(result) == 2:
            vertices, faces = result
            return Mesh.from_vertices_and_faces(vertices, faces)
        if result is not None:
            return result
    vertices = getattr(geometry, "vertices", None)
    faces = getattr(geometry, "faces", None)
    if vertices is not None and faces is not None:
        return Mesh.from_vertices_and_faces(list(vertices), list(faces))
    return None


def _merge_mesh(target, source) -> None:
    """Merge ``source`` mesh vertices/faces into ``target``."""
    offset = target.number_of_vertices()
    index_map = {}
    for key, attr in source.vertices(data=True):
        new_key = target.add_vertex(x=attr["x"], y=attr["y"], z=attr["z"])
        index_map[key] = new_key
    for face_key in source.faces():
        vertices = [index_map[v] for v in source.face_vertices(face_key)]
        target.add_face(vertices)
    _ = offset  # offset kept for callers that want a starting index later


# ---------------------------------------------------------------------------
# docs
# ---------------------------------------------------------------------------


@app.command()
def docs(
    symbol: str = typer.Argument(None, help="Symbol to document (e.g. 'BuildingInformationModel', 'bim', 'conversions.brep')."),
    brief: bool = typer.Option(False, "--brief", help="Signature + first docstring line only."),
    list_parent: str = typer.Option(None, "--list", help="List public members of the given parent symbol."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Introspect compas_ifc symbols — signature, docstring, members.

    ``--brief`` returns just ``signature -> return : first_docstring_line``,
    the format an agent wants while scanning. ``--list PARENT`` enumerates
    public members of a class or module so an agent can discover the API
    in one call.
    """
    if list_parent:
        target = _resolve_symbol(list_parent)
        if target is None:
            typer.echo(f"error: cannot resolve symbol: {list_parent}", err=True)
            raise typer.Exit(code=1)
        members = _list_members(target, brief=brief)
        payload = {"parent": list_parent, "count": len(members), "members": members}

        def human(_):
            typer.echo(f"{len(members)} member(s) of {list_parent}:")
            for member in members:
                typer.echo(f"  {member.get('brief') or member.get('name')}")

        _emit(payload, json_output, human)
        return

    if not symbol:
        typer.echo("error: pass a symbol, or --list <parent>", err=True)
        raise typer.Exit(code=1)

    target = _resolve_symbol(symbol)
    if target is None:
        typer.echo(f"error: cannot resolve symbol: {symbol}", err=True)
        raise typer.Exit(code=1)

    payload = _describe(target, symbol, brief=brief)

    def human(_):
        if brief and "brief" in payload:
            typer.echo(payload["brief"])
            return
        if "signature" in payload:
            typer.echo(payload["signature"])
        if payload.get("docstring"):
            typer.echo("")
            typer.echo(payload["docstring"])

    _emit(payload, json_output, human)


def _resolve_symbol(symbol: str):
    """Best-effort lookup of a symbol in the compas_ifc namespace.

    Tries (in order): the package's ``__all__`` re-exports, ``compas_ifc.bim``
    as the canonical entry-point module, a full dotted import, and finally a
    breadth-first scan of submodule attributes.
    """
    import importlib

    import compas_ifc
    import compas_ifc.bim as bim_module

    # 1) Direct attribute on top-level package.
    if hasattr(compas_ifc, symbol):
        return getattr(compas_ifc, symbol)
    # 2) Canonical entry-point module.
    if hasattr(bim_module, symbol):
        return getattr(bim_module, symbol)
    # 3) Dotted path: try importing as a module, then as attribute-on-module.
    if "." in symbol:
        try:
            return importlib.import_module(symbol)
        except ImportError:
            pass
        head, _, tail = symbol.rpartition(".")
        try:
            module = importlib.import_module(head)
            if hasattr(module, tail):
                return getattr(module, tail)
        except ImportError:
            pass
        # Try compas_ifc-prefixed dotted path.
        try:
            return importlib.import_module(f"compas_ifc.{symbol}")
        except ImportError:
            pass
    else:
        # 4) Try as a submodule of compas_ifc.
        try:
            return importlib.import_module(f"compas_ifc.{symbol}")
        except ImportError:
            pass
    return None


def _describe(target, name: str, brief: bool) -> dict:
    """Render a symbol's signature/docstring into a payload."""
    import inspect

    docstring = inspect.getdoc(target) or ""
    first_line = docstring.split("\n", 1)[0] if docstring else ""

    signature = None
    if inspect.isclass(target) or inspect.isfunction(target) or inspect.ismethod(target):
        try:
            sig = inspect.signature(target)
            signature = f"{name}{sig}"
        except (TypeError, ValueError):
            signature = name
    elif inspect.ismodule(target):
        signature = f"module {target.__name__}"

    if brief:
        return {
            "symbol": name,
            "brief": f"{signature}  —  {first_line}" if signature else first_line,
            "kind": _kind(target),
        }
    return {
        "symbol": name,
        "kind": _kind(target),
        "signature": signature,
        "docstring": docstring,
    }


def _kind(target) -> str:
    import inspect

    if inspect.ismodule(target):
        return "module"
    if inspect.isclass(target):
        return "class"
    if inspect.ismethod(target):
        return "method"
    if inspect.isfunction(target):
        return "function"
    return type(target).__name__


def _list_members(target, brief: bool = False) -> list:
    import inspect

    members = []
    for name in dir(target):
        if name.startswith("_"):
            continue
        try:
            member = getattr(target, name)
        except AttributeError:
            continue
        if inspect.ismodule(member):
            # Skip submodules when listing a module's members — too noisy.
            continue
        members.append(_describe(member, name, brief=True))
    return members


# ---------------------------------------------------------------------------
# schema
# ---------------------------------------------------------------------------


@app.command()
def schema(
    ifc_class: str = typer.Argument(..., help="IFC class name (e.g. IfcWall)."),
    schema_version: str = typer.Option("IFC4", "--schema", help="IFC schema: IFC2X3, IFC4, or IFC4X3."),
    depth: int = typer.Option(
        1,
        "--depth",
        help=(
            "How many levels deep to expand entity-typed attributes. 1 "
            "(default) lists this class's attributes only. Raise to inline "
            "each attribute's referenced class — and its attributes, "
            "recursively. Cycles are broken automatically."
        ),
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Show schema information for an IFC class — supertype chain, attributes, inverses.

    Reads from the bundled PEP 561 stubs at ``compas_ifc.entities.generated``,
    so the attribute set includes members added by ``@extends`` extensions in
    addition to the raw EXPRESS schema. Available schemas: ``IFC2X3``,
    ``IFC4``, ``IFC4X3``.
    """
    index = _load_schema_stub(schema_version)
    if not index:
        typer.echo(f"error: stub not found for schema: {schema_version}", err=True)
        raise typer.Exit(code=1)

    if ifc_class not in index:
        typer.echo(f"error: {ifc_class!r} not declared in {schema_version}", err=True)
        raise typer.Exit(code=1)

    supertypes = _mro(ifc_class, index)[1:]  # skip self
    tree = _class_tree(ifc_class, index, depth=depth, seen=frozenset())

    payload = {
        "schema": schema_version,
        "class": ifc_class,
        "depth": depth,
        "supertypes": supertypes,
        **tree,
    }

    def human(_):
        typer.echo(f"{ifc_class}  ({schema_version})")
        if supertypes:
            typer.echo("  ↑ " + " → ".join(reversed(supertypes)) + f" → {ifc_class}")
        typer.echo(f"\nattributes ({len(payload['attributes'])}):")
        name_w = min(_max_name_width(payload["attributes"]), 30)
        _render_attr_tree(payload["attributes"], prefix="", self_class=ifc_class, name_w=name_w)
        if payload["inverses"]:
            typer.echo(f"\ninverses ({len(payload['inverses'])}):")
            inv_w = max((len(inv["name"]) for inv in payload["inverses"]), default=0)
            for inv in payload["inverses"]:
                origin = "" if inv["from"] == ifc_class else f"  · {inv['from']}"
                typer.echo(f"  {inv['name']:<{inv_w}}  → {_pretty_type(inv['return_type'])}{origin}")

    _emit(payload, json_output, human)


def _pretty_type(ann: str) -> str:
    """Compress a Python type annotation string for human display.

    Drops the ``Optional[...]`` wrapper for a trailing ``?``, strips the
    forward-ref quotes around class names, collapses ``list[X]`` to
    ``[X]``, ``tuple[X, ...]`` to ``(X…)``, and renders ``Union[A, B]``
    as ``A | B``.
    """
    s = ann.strip()
    if s.startswith("Optional[") and s.endswith("]"):
        return _pretty_type(s[9:-1]) + "?"
    if s.startswith("Union["):
        parts = _split_top_level(s[6:-1], ",")
        return " | ".join(_pretty_type(p.strip()) for p in parts)
    if s.startswith("list[") and s.endswith("]"):
        return "[" + _pretty_type(s[5:-1]) + "]"
    if s.startswith("tuple[") and s.endswith("]"):
        inner = s[6:-1]
        if inner.endswith(", ..."):
            return "(" + _pretty_type(inner[:-5].strip()) + "…)"
        return "(" + ", ".join(_pretty_type(p.strip()) for p in _split_top_level(inner, ",")) + ")"
    if len(s) >= 2 and ((s[0] == "'" and s[-1] == "'") or (s[0] == '"' and s[-1] == '"')):
        return s[1:-1]
    return s


def _split_top_level(s: str, sep: str) -> list:
    """Split ``s`` on ``sep`` ignoring delimiters inside brackets."""
    parts, depth, current = [], 0, []
    for ch in s:
        if ch in "[({":
            depth += 1
        elif ch in "])}":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    parts.append("".join(current))
    return parts


def _max_name_width(attrs: list) -> int:
    """Walk the attribute tree once to find the longest name (for column alignment)."""
    w = 0
    for attr in attrs:
        w = max(w, len(attr["name"]))
        inline = attr.get("inline")
        if inline and inline.get("expanded"):
            w = max(w, _max_name_width(inline["attributes"]))
    return w


def _render_attr_tree(attrs: list, prefix: str, self_class: str, name_w: int) -> None:
    """Render an attribute tree with ├── / └── / │   connectors and a consistent name column."""
    if not attrs:
        return
    last_idx = len(attrs) - 1
    for i, attr in enumerate(attrs):
        is_last = i == last_idx
        connector = "└── " if is_last else "├── "
        type_str = _pretty_type(attr["type"])
        origin = ""
        if "from" in attr and attr["from"] != self_class:
            origin = f"  · {attr['from']}"
        typer.echo(f"{prefix}{connector}{attr['name']:<{name_w}}  {type_str}{origin}")

        inline = attr.get("inline")
        if not inline:
            continue
        child_prefix = prefix + ("    " if is_last else "│   ")
        if inline.get("expanded"):
            _render_attr_tree(inline["attributes"], child_prefix, self_class=inline["class"], name_w=name_w)
        elif inline.get("reason") == "cycle":
            typer.echo(f"{child_prefix}↻ {inline['class']}  [cycle]")


# ---------------------------------------------------------------------------
# schema stub parsing
# ---------------------------------------------------------------------------


@lru_cache(maxsize=4)
def _load_schema_stub(schema_version: str) -> dict:
    """Parse the bundled .pyi stub for ``schema_version`` and index classes by name."""
    import compas_ifc

    stub_path = Path(compas_ifc.__file__).parent / "entities" / "generated" / f"{schema_version}.pyi"
    if not stub_path.exists():
        return {}
    tree = ast.parse(stub_path.read_text(encoding="utf-8"))
    return {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}


def _mro(class_name: str, index: dict) -> list:
    """Return ``[self, parent, grandparent, ...]`` walking the first base class.

    Single-inheritance assumption — true of the IFC stubs.
    """
    chain = []
    cur = class_name
    while cur and cur in index:
        chain.append(cur)
        bases = index[cur].bases
        if bases and isinstance(bases[0], ast.Name):
            cur = bases[0].id
        else:
            cur = None
    return chain


def _extract_entity_ref(annotation, index: dict) -> Optional[str]:
    """Walk a type annotation AST and return the first referenced class name in ``index``.

    Examples:
        Optional["IfcOwnerHistory"]                       -> "IfcOwnerHistory"
        tuple["IfcProduct", ...]                          -> "IfcProduct"
        Optional[float]                                   -> None
        Optional["IfcWindowTypeEnum"]                     -> "IfcWindowTypeEnum"
    """
    if isinstance(annotation, ast.Subscript):
        return _extract_entity_ref(annotation.slice, index)
    if isinstance(annotation, ast.Tuple):
        for elt in annotation.elts:
            ref = _extract_entity_ref(elt, index)
            if ref:
                return ref
        return None
    if isinstance(annotation, ast.Constant) and isinstance(annotation.value, str):
        return annotation.value if annotation.value in index else None
    if isinstance(annotation, ast.Name):
        return annotation.id if annotation.id in index else None
    return None


def _class_tree(class_name: str, index: dict, depth: int, seen: frozenset) -> dict:
    """Recursively build an attribute tree for an IFC class.

    Walks the MRO root-first so attributes appear in supertype-then-self order
    — same as ifcopenshell's all_attributes().
    """
    if class_name in seen:
        return {"class": class_name, "expanded": False, "reason": "cycle"}
    if depth <= 0:
        return {"class": class_name, "expanded": False, "reason": "max depth"}
    if class_name not in index:
        return {"class": class_name, "expanded": False, "reason": "unknown class"}

    seen = seen | {class_name}
    chain = _mro(class_name, index)

    attrs = []
    inverses = []
    seen_inverses: set = set()  # dedupe property getter/setter overloads
    for ancestor in reversed(chain):
        cls = index.get(ancestor)
        if cls is None:
            continue
        for item in cls.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                # Skip type-alias attributes like `items: tuple = (...)` on enums.
                if item.target.id == "items":
                    continue
                ann_str = ast.unparse(item.annotation)
                ref = _extract_entity_ref(item.annotation, index)
                entry = {
                    "name": item.target.id,
                    "type": ann_str,
                    "from": ancestor,
                }
                # Only inline when there is depth budget left — keeps depth=1 output
                # identical to the pre-recursion shape (no "max depth" stubs).
                if ref is not None and depth > 1:
                    entry["inline"] = _class_tree(ref, index, depth=depth - 1, seen=seen)
                attrs.append(entry)
            elif isinstance(item, ast.FunctionDef) and item.returns is not None:
                ret_type = ast.unparse(item.returns)
                key = (item.name, ret_type)
                if key in seen_inverses:
                    continue
                seen_inverses.add(key)
                inverses.append(
                    {
                        "name": item.name,
                        "return_type": ret_type,
                        "from": ancestor,
                    }
                )

    return {
        "class": class_name,
        "expanded": True,
        "attributes": attrs,
        "inverses": inverses,
    }


# ---------------------------------------------------------------------------
# tutorials
# ---------------------------------------------------------------------------


tutorials_app = typer.Typer(name="tutorials", help="Browse the bundled tutorial scripts.")
app.add_typer(tutorials_app, name="tutorials")


def _tutorials_dir() -> Optional[str]:
    """Locate the tutorials directory across dev and installed layouts."""
    import compas_ifc

    candidates = [
        os.path.join(compas_ifc.HOME, "scripts", "tutorials"),
        os.path.join(os.path.dirname(compas_ifc.__file__), "tutorials"),
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    return None


@tutorials_app.command("list")
def tutorials_list_cmd(
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """List bundled tutorial scripts."""
    directory = _tutorials_dir()
    if directory is None:
        typer.echo("error: tutorials directory not found", err=True)
        raise typer.Exit(code=1)

    entries = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".py"):
            continue
        full = os.path.join(directory, name)
        first_line = ""
        try:
            with open(full, encoding="utf-8") as handle:
                first_line = handle.readline().strip().lstrip("#").strip()
        except OSError:
            pass
        entries.append({"name": os.path.splitext(name)[0], "summary": first_line, "path": full})

    payload = {"directory": directory, "count": len(entries), "tutorials": entries}

    def human(_):
        typer.echo(f"{len(entries)} tutorial(s) in {directory}:")
        for entry in entries:
            typer.echo(f"  {entry['name']:<28} {entry['summary']}")

    _emit(payload, json_output, human)


@tutorials_app.command("show")
def tutorials_show_cmd(
    name: str = typer.Argument(..., help="Tutorial name or prefix (e.g. '3.1' or 'model_view')."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Print the source of a tutorial script. Match by name prefix or substring."""
    directory = _tutorials_dir()
    if directory is None:
        typer.echo("error: tutorials directory not found", err=True)
        raise typer.Exit(code=1)

    needle = name.lower()
    matches = []
    for entry in sorted(os.listdir(directory)):
        if not entry.endswith(".py"):
            continue
        stem = os.path.splitext(entry)[0].lower()
        if stem == needle or stem.startswith(needle) or needle in stem:
            matches.append(entry)

    if not matches:
        typer.echo(f"error: no tutorial matches {name!r}", err=True)
        raise typer.Exit(code=1)
    if len(matches) > 1:
        typer.echo(f"error: {name!r} matches multiple tutorials: {', '.join(matches)}", err=True)
        raise typer.Exit(code=1)

    full = os.path.join(directory, matches[0])
    with open(full, encoding="utf-8") as handle:
        source = handle.read()

    payload = {"name": os.path.splitext(matches[0])[0], "path": full, "source": source}

    def human(_):
        typer.echo(f"# {payload['name']}  ({payload['path']})\n")
        typer.echo(source)

    _emit(payload, json_output, human)


# ---------------------------------------------------------------------------
# install-skill
# ---------------------------------------------------------------------------


@app.command(name="install-skill")
def install_skill(
    target: str = typer.Option("claude", "--target", help="Where to install: claude, codex, both."),
    uninstall: bool = typer.Option(False, "--uninstall", help="Remove an already-installed skill."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing install without prompting."),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Install the bundled agent skill into Claude Code (and, eventually, Codex).

    The skill content lives under ``compas_ifc.skill`` and is shipped as
    package data, so the version on disk always matches the installed
    library.
    """
    import shutil

    target = target.lower()
    targets = {"claude": _install_target_claude}
    if target == "both":
        chosen = list(targets.keys())
    elif target == "codex":
        typer.echo("error: codex target is not yet implemented (tracked in docs/plans/cli_and_skill.md, Phase 8)", err=True)
        raise typer.Exit(code=1)
    else:
        if target not in targets:
            typer.echo(f"error: unknown target {target!r}. Use claude, codex, or both.", err=True)
            raise typer.Exit(code=1)
        chosen = [target]

    source = _skill_source_dir()
    if source is None:
        typer.echo("error: bundled skill not found in installed package", err=True)
        raise typer.Exit(code=1)

    results = []
    for name in chosen:
        destination = targets[name]()
        if uninstall:
            removed = _uninstall_dir(destination)
            results.append({"target": name, "action": "uninstall", "path": destination, "removed": removed})
            continue
        if os.path.exists(destination) and not force:
            typer.echo(f"{destination} already exists. Re-run with --force to overwrite, or --uninstall first.", err=True)
            raise typer.Exit(code=1)
        if os.path.exists(destination):
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        results.append({"target": name, "action": "install", "path": destination, "source": source})

    payload = {"results": results}

    def human(_):
        for result in results:
            action = result["action"]
            if action == "install":
                typer.echo(f"installed skill -> {result['path']}")
            elif action == "uninstall":
                if result["removed"]:
                    typer.echo(f"removed skill <- {result['path']}")
                else:
                    typer.echo(f"nothing to remove at {result['path']}")

    _emit(payload, json_output, human)


def _skill_source_dir() -> Optional[str]:
    """Locate the bundled skill directory inside the installed package."""
    import compas_ifc

    candidate = os.path.join(os.path.dirname(compas_ifc.__file__), "skill")
    return candidate if os.path.isdir(candidate) else None


def _install_target_claude() -> str:
    return os.path.expanduser(os.path.join("~", ".claude", "skills", "compas_ifc"))


def _uninstall_dir(path: str) -> bool:
    import shutil

    if not os.path.exists(path):
        return False
    shutil.rmtree(path)
    return True


def main() -> None:
    """Console-script entry point."""
    app()


if __name__ == "__main__":
    main()
