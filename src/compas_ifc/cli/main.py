"""compas_ifc command-line interface — Phase 1 commands.

All commands accept ``--json`` for structured, agent-friendly output. The
human-readable default is meant for terminal users; JSON is the contract
the agent skill relies on.

Heavy imports (``compas_ifc.bim``) are deferred to command bodies so the
``--help`` path stays fast.
"""

from __future__ import annotations

import json
import os
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
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Dump a single entity's attributes by GlobalId."""
    _check_file(file)
    model = _open_model(file)

    entity = _find_by_global_id(model, global_id)
    if entity is None:
        typer.echo(f"error: no entity with GlobalId {global_id}", err=True)
        raise typer.Exit(code=1)

    raw = getattr(entity, "entity", entity)
    info_dict = raw.get_info(include_identifier=True, recursive=False)
    # Convert ifcopenshell wrapper values to JSON-friendly forms.
    attrs = {k: _scalar(v) for k, v in info_dict.items() if k != "type"}

    payload = {
        "type": raw.is_a(),
        "global_id": getattr(entity, "GlobalId", None),
        "id": raw.id(),
        "attributes": attrs,
    }
    _emit(payload, json_output)


def _scalar(value):
    """Coerce an ifcopenshell value to something JSON can serialise."""
    import ifcopenshell

    if isinstance(value, ifcopenshell.entity_instance):
        try:
            return {"$ref": value.id(), "type": value.is_a()}
        except Exception:
            return str(value)
    if isinstance(value, (list, tuple)):
        return [_scalar(v) for v in value]
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
    import subprocess
    import sys

    _check_file(file)

    if detach:
        relay = [sys.executable, "-m", "compas_ifc", "visualize", file]
        if type_:
            relay += ["--type", type_]
        if where:
            relay += ["--where", where]
        if in_:
            relay += ["--in", in_]
        if ids:
            relay += ["--ids", ids]
        if not keep_hierarchy:
            relay += ["--no-keep-hierarchy"]

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
        _emit(
            payload,
            json_output,
            lambda _: typer.echo(f"viewer launched in background (pid={proc.pid})"),
        )
        return

    # Probe for compas_viewer first so we exit with a useful message rather
    # than a deep traceback when it's missing.
    try:
        import compas_viewer  # noqa: F401
    except ImportError:
        typer.echo("error: compas_viewer is not installed.", err=True)
        typer.echo("install with: pip install compas_viewer", err=True)
        raise typer.Exit(code=1)
    except Exception as exc:  # e.g. broken freetype binding noted in MEMORY.md
        typer.echo(f"error: compas_viewer failed to import: {exc}", err=True)
        raise typer.Exit(code=1)

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
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON."),
) -> None:
    """Show schema information for an IFC class — attributes, inverses, supertype chain.

    Reads directly from ifcopenshell's schema, so the answer is authoritative
    for the requested schema version.
    """
    import ifcopenshell

    try:
        schema_obj = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema_version)
    except (RuntimeError, Exception) as exc:
        typer.echo(f"error: unknown schema: {schema_version} ({exc})", err=True)
        raise typer.Exit(code=1)

    try:
        declaration = schema_obj.declaration_by_name(ifc_class)
    except RuntimeError:
        typer.echo(f"error: {ifc_class!r} not declared in {schema_version}", err=True)
        raise typer.Exit(code=1)

    if not declaration.as_entity():
        typer.echo(f"error: {ifc_class!r} is not an entity declaration", err=True)
        raise typer.Exit(code=1)

    entity = declaration.as_entity()
    attributes = []
    for attr in entity.attributes():
        attributes.append(
            {
                "name": attr.name(),
                "type": str(attr.type_of_attribute()),
                "optional": attr.optional(),
            }
        )

    inverse_attrs = []
    for inv in entity.all_inverse_attributes():
        inverse_attrs.append(
            {
                "name": inv.name(),
                "of_entity": inv.entity_reference().name(),
            }
        )

    supertypes = []
    parent = entity.supertype()
    while parent is not None:
        supertypes.append(parent.name())
        parent = parent.supertype()

    payload = {
        "schema": schema_version,
        "class": entity.name(),
        "abstract": entity.is_abstract(),
        "supertypes": supertypes,
        "attributes": attributes,
        "inverses": inverse_attrs,
    }

    def human(_):
        typer.echo(f"{payload['class']} ({schema_version})" + ("  [abstract]" if payload["abstract"] else ""))
        if supertypes:
            typer.echo("  ← " + " ← ".join(supertypes))
        typer.echo(f"\nattributes ({len(attributes)}):")
        for attr in attributes:
            opt = " optional" if attr["optional"] else ""
            typer.echo(f"  {attr['name']:<25} {attr['type']}{opt}")
        if inverse_attrs:
            typer.echo(f"\ninverses ({len(inverse_attrs)}):")
            for inv in inverse_attrs:
                typer.echo(f"  {inv['name']:<25} of {inv['of_entity']}")

    _emit(payload, json_output, human)


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
