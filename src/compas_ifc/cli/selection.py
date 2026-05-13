"""Shared selection grammar for CLI commands.

The same set of selection flags is reused by ``list``, ``query``,
``visualize``, and ``export-ifc`` so an agent can compose them the same way
across commands. Filters compose with AND semantics.

Flags:

- ``--type IfcWindow``                 IFC class (also matches subclasses)
- ``--where "Name~'casement'"``        single key/op/value comparison
- ``--in <global_id>``                 contained in a spatial element (recursive)
- ``--ids id1,id2,...``                explicit list of GlobalIds

``--where`` syntax: ``<key> <op> <value>``. Operators: ``=``, ``!=``, ``>``,
``<``, ``>=``, ``<=``, ``~`` (substring, case-insensitive). Numeric
comparisons are attempted when both sides parse as floats.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any
from typing import Optional


@dataclass
class Selection:
    """A parsed selection — what the user passed on the command line."""

    type_: Optional[str] = None
    where: Optional[str] = None
    in_: Optional[str] = None
    ids: Optional[str] = None

    def is_empty(self) -> bool:
        return not any([self.type_, self.where, self.in_, self.ids])


WHERE_RE = re.compile(r"^\s*([\w.]+)\s*(>=|<=|!=|=|>|<|~)\s*(.+?)\s*$")


def parse_where(expr: str) -> tuple[str, str, str]:
    """Parse a ``--where`` clause into ``(key, op, value)``.

    The value's surrounding single/double quotes are stripped so users can
    write ``Name='Wall A'`` without the quotes leaking into the comparison.
    """
    match = WHERE_RE.match(expr)
    if not match:
        raise ValueError(
            f"invalid --where expression: {expr!r}. "
            "Expected '<key> <op> <value>' with op in =, !=, >, <, >=, <=, ~."
        )
    key, op, value = match.group(1), match.group(2), match.group(3)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        value = value[1:-1]
    return key, op, value


def _entity_attr(entity: Any, key: str) -> Any:
    """Read an attribute from a Base-wrapped or raw ifcopenshell entity.

    Supports dotted paths like ``OwnerHistory.Owner.ThePerson.GivenName``
    so users can drill into related entities, returning ``None`` at the
    first missing link.
    """
    current: Any = entity
    for part in key.split("."):
        if current is None:
            return None
        try:
            current = getattr(current, part)
        except (AttributeError, RuntimeError):
            return None
    return current


def _coerce_comparable(a: Any, b: str) -> tuple[Any, Any]:
    """Try numeric comparison first; fall back to string."""
    try:
        return float(a), float(b)
    except (TypeError, ValueError):
        return ("" if a is None else str(a)), b


def eval_where(entity: Any, key: str, op: str, value: str) -> bool:
    """Evaluate a single ``--where`` predicate against an entity."""
    actual = _entity_attr(entity, key)
    left, right = _coerce_comparable(actual, value)
    try:
        if op == "=":
            return left == right
        if op == "!=":
            return left != right
        if op == ">":
            return left > right
        if op == "<":
            return left < right
        if op == ">=":
            return left >= right
        if op == "<=":
            return left <= right
        if op == "~":
            return str(value).lower() in ("" if actual is None else str(actual)).lower()
    except TypeError:
        return False
    return False


def _get_contained_entity_ids(raw_entity) -> set[int]:
    """All raw entity ids reachable from a container via aggregation or containment.

    Mirrors ``ifcopenshell.util.element.get_decomposition`` but is recursive
    and operates on raw entities so we can intersect with arbitrary
    candidate sets without re-wrapping.
    """
    seen: set[int] = set()
    stack = [raw_entity]
    while stack:
        node = stack.pop()
        # IfcRelContainedInSpatialStructure: spatial container -> elements
        for rel in getattr(node, "ContainsElements", None) or []:
            for child in rel.RelatedElements or []:
                if child.id() in seen:
                    continue
                seen.add(child.id())
                stack.append(child)
        # IfcRelAggregates: composite -> parts (e.g. building -> storeys)
        for rel in getattr(node, "IsDecomposedBy", None) or []:
            for child in rel.RelatedObjects or []:
                if child.id() in seen:
                    continue
                seen.add(child.id())
                stack.append(child)
    return seen


def _find_raw_by_global_id(model, global_id: str):
    """Return the raw ifcopenshell entity with the given GlobalId, or ``None``."""
    try:
        candidates = model._file._file.by_type("IfcRoot")
    except RuntimeError:
        return None
    for entity in candidates:
        if getattr(entity, "GlobalId", None) == global_id:
            return entity
    return None


def apply_selection(model, selection: Selection) -> list:
    """Resolve a :class:`Selection` against a loaded model.

    Returns a list of Base-wrapped entities. Filter order:

    1. Seed set: ``ids`` if given, else entities of ``type_`` if given, else
       all ``IfcRoot`` entities.
    2. Apply ``--in`` containment filter.
    3. Apply ``--where`` predicate.
    """
    raw_file = model._file._file

    # Seed
    if selection.ids:
        seed = []
        for gid in [g.strip() for g in selection.ids.split(",") if g.strip()]:
            raw = _find_raw_by_global_id(model, gid)
            if raw is not None:
                seed.append(raw)
    elif selection.type_:
        try:
            seed = list(raw_file.by_type(selection.type_))
        except RuntimeError as exc:
            raise ValueError(f"unknown IFC type: {selection.type_}") from exc
    else:
        # Default to IfcRoot-rooted entities so we have GlobalIds to work with.
        try:
            seed = list(raw_file.by_type("IfcRoot"))
        except RuntimeError:
            seed = list(raw_file)

    # Containment filter
    if selection.in_:
        container = _find_raw_by_global_id(model, selection.in_)
        if container is None:
            raise ValueError(f"--in container not found: {selection.in_}")
        contained_ids = _get_contained_entity_ids(container)
        # Also include the container itself so `--in X --type IfcBuildingStorey` still hits X.
        contained_ids.add(container.id())
        seed = [e for e in seed if e.id() in contained_ids]

    # Wrap into Base entities for attribute access via extensions
    wrapped = [model._file.from_entity(e) for e in seed]

    # Where filter
    if selection.where:
        key, op, value = parse_where(selection.where)
        wrapped = [e for e in wrapped if eval_where(e, key, op, value)]

    return wrapped
