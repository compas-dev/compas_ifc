"""Stub generator for ``compas_ifc.entities.generated``.

Emits one PEP 561 stub file per IFC schema:

    src/compas_ifc/entities/generated/IFC2X3.pyi
    src/compas_ifc/entities/generated/IFC4.pyi
    src/compas_ifc/entities/generated/IFC4X3.pyi

Each stub declares every IFC entity and enumeration in the schema, with
type-annotated direct and inverse attributes, plus the public members of
any extension classes registered through ``@extends`` against that IFC
class. The runtime layer never imports these files; they exist purely to
give IDEs / type checkers schema-aware autocomplete on entities returned
from ``compas_ifc``.

This module is run by maintainers when bumping schema support:

    python -m compas_ifc.entities.generator
"""

from __future__ import annotations

import inspect
import os
import types
from typing import Iterable

import ifcopenshell

# Importing the extensions package executes the ``@extends`` decorators
# and populates the registry consumed by ``StubGenerator``.
from compas_ifc.entities import extensions  # noqa: F401
from compas_ifc.entities.base import _extension_registry


class Generator:
    """Generate a ``.pyi`` stub for a single IFC schema.

    Parameters
    ----------
    schema : str
        Schema name passed to :func:`ifcopenshell.ifcopenshell_wrapper.schema_by_name`.

    """

    def __init__(self, schema: str = "IFC4"):
        self.schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema)

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def generate(self) -> None:
        here = os.path.dirname(__file__)
        out_path = os.path.join(here, "generated", f"{self.schema.name()}.pyi")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        lines: list[str] = []
        lines.append(f'"""Type stubs for {self.schema.name()} entities (auto-generated).')
        lines.append("")
        lines.append("Do not edit by hand. Regenerate with:")
        lines.append("    python -m compas_ifc.entities.generator")
        lines.append('"""')
        lines.append("")
        lines.append("from typing import Optional")
        lines.append("from typing import Union")
        lines.append("")

        # Enums first — they're terminal (no inheritance to other entities).
        enum_decls = [d for d in self.schema.declarations() if d.as_enumeration_type()]
        for decl in sorted(enum_decls, key=lambda d: d.name()):
            lines.extend(self._emit_enum(decl))

        # Entities, sorted so parents precede children.
        entity_decls = [d for d in self.schema.declarations() if d.as_entity()]
        for decl in sorted(entity_decls, key=lambda d: (_depth(d), d.name())):
            lines.extend(self._emit_entity(decl))

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Wrote {out_path} ({len(entity_decls)} entities, {len(enum_decls)} enums).")

    # ------------------------------------------------------------------
    # Enums
    # ------------------------------------------------------------------

    def _emit_enum(self, decl) -> list[str]:
        items = tuple(decl.enumeration_items())
        return [
            f"class {decl.name()}(str):",
            f"    items: tuple = {items!r}",
            "",
            "",
        ]

    # ------------------------------------------------------------------
    # Entities
    # ------------------------------------------------------------------

    def _emit_entity(self, decl) -> list[str]:
        name = decl.name()
        parent = decl.supertype().name() if decl.supertype() else None
        base = parent if parent else ""

        header = f"class {name}({base}):" if base else f"class {name}:"
        body: list[str] = []
        body.append(f'    """Wrapper class for {name}."""')

        # Direct attributes (own only — parent attrs come via inheritance).
        derived_flags = decl.derived()
        own_attr_names = {a.name() for a in decl.attributes()}
        attr_lines: list[str] = []
        all_attrs = decl.all_attributes()
        for i, attr in enumerate(all_attrs):
            if attr.name() not in own_attr_names:
                continue
            annotation = _attribute_annotation(attr)
            if derived_flags[i]:
                attr_lines.append("    @property")
                attr_lines.append(f"    def {attr.name()}(self) -> {annotation}: ...")
            else:
                attr_lines.append(f"    {attr.name()}: {annotation}")

        # Inverse attributes — own only.
        parent_inverse: set[str] = set()
        if decl.supertype():
            for ia in decl.supertype().all_inverse_attributes():
                parent_inverse.add(ia.name())
        inverse_lines: list[str] = []
        for ia in decl.all_inverse_attributes():
            if ia.name() in parent_inverse:
                continue
            target = ia.entity_reference().name()
            inverse_lines.append(
                f'    def {ia.name()}(self) -> tuple["{target}", ...]: ...'
            )

        # Extension members merged from `_extension_registry`.
        ext_lines = self._emit_extension_members(name)

        body.extend(attr_lines)
        body.extend(inverse_lines)
        body.extend(ext_lines)

        if len(body) == 1:  # only the docstring
            body.append("    ...")

        return [header, *body, "", ""]

    # ------------------------------------------------------------------
    # Extension merging
    # ------------------------------------------------------------------

    def _emit_extension_members(self, ifc_class_name: str) -> list[str]:
        registered = _extension_registry.get(ifc_class_name, [])
        if not registered:
            return []

        schema_name = self.schema.name()
        # Skip extension if its target class doesn't exist in this schema.
        try:
            self.schema.declaration_by_name(ifc_class_name)
        except Exception:
            return []

        lines: list[str] = []
        for ext_cls, schemas in registered:
            if schemas is not None and schema_name not in schemas:
                continue
            lines.extend(_format_extension_class(ext_cls))
        return lines


# ----------------------------------------------------------------------
# Module-level helpers
# ----------------------------------------------------------------------


_depth_cache: dict = {}


def _depth(decl) -> int:
    """Inheritance depth of an entity declaration (0 for IfcRoot-less roots)."""
    name = decl.name()
    if name in _depth_cache:
        return _depth_cache[name]
    d = 0
    cur = decl
    while cur.supertype():
        d += 1
        cur = cur.supertype()
    _depth_cache[name] = d
    return d


_TYPE_MAP = {
    "DOUBLE": "float",
    "INT": "int",
    "STRING": "str",
    "LOGICAL": "bool",
    "BOOL": "bool",
    "BINARY": "bytes",
    "integer": "int",
    "logical": "bool",
    "boolean": "bool",
    "real": "float",
    "string": "str",
    "binary": "bytes",
}


def _attribute_annotation(attr) -> str:
    """Compute a Python type-annotation string for an EXPRESS attribute."""
    attribute_type = attr.type_of_attribute()
    optional = attr.optional()
    base = _attribute_type_string(attribute_type)
    if optional:
        return f"Optional[{base}]"
    return base


def _attribute_type_string(attribute_type) -> str:
    if attribute_type.as_aggregation_type():
        return _aggregation_type_string(attribute_type)
    if attribute_type.as_simple_type():
        return _TYPE_MAP[attribute_type.declared_type()]
    declared = attribute_type.declared_type()
    if declared.as_select_type():
        return _select_type_string(declared)
    if declared.as_type_declaration():
        return _type_declaration_string(declared)
    # Entity or enumeration — forward-referenced as a string.
    return f'"{declared.name()}"'


def _aggregation_type_string(attribute_type) -> str:
    type_of_element = attribute_type.type_of_element()
    if type_of_element.as_aggregation_type():
        return f"list[{_aggregation_type_string(type_of_element)}]"
    declared = type_of_element.declared_type()
    if isinstance(declared, str):
        return f"list[{_TYPE_MAP[declared]}]"
    if declared.as_select_type():
        return f"list[{_select_type_string(declared)}]"
    if declared.as_type_declaration():
        return f"list[{_type_declaration_string(declared)}]"
    return f'list["{declared.name()}"]'


def _select_type_string(select_decl) -> str:
    items: list[str] = []
    seen: set[str] = set()

    def walk(decl):
        for item in decl.select_list():
            if item.as_select_type():
                walk(item)
            else:
                if item.as_type_declaration():
                    s = _type_declaration_string(item)
                else:
                    s = f'"{item.name()}"'
                if s not in seen:
                    seen.add(s)
                    items.append(s)

    walk(select_decl)
    if not items:
        return "object"
    if len(items) == 1:
        return items[0]
    return f"Union[{', '.join(items)}]"


def _type_declaration_string(type_decl) -> str:
    ifc_type = type_decl.argument_types()[0]
    if ifc_type.startswith("AGGREGATE OF"):
        value_type = ifc_type.split("OF ")[1]
        if value_type == "ENTITY INSTANCE":
            return "list"
        return f"list[{_TYPE_MAP[value_type]}]"
    return _TYPE_MAP[ifc_type]


def _format_extension_class(ext_cls) -> list[str]:
    """Walk an extension class and emit its public members as stub lines.

    Dunder methods and underscore-prefixed members are skipped — they're
    implementation details that don't belong in the IDE-facing stub.
    """
    out: list[str] = []
    for name, member in ext_cls.__dict__.items():
        if name.startswith("_"):
            continue
        if isinstance(member, property):
            ret = _signature_return(member.fget) if member.fget else "object"
            out.append("    @property")
            out.append(f"    def {name}(self) -> {ret}: ...")
            if member.fset is not None:
                out.append(f"    @{name}.setter")
                ret = _signature_return(member.fset, default="None")
                # For setters, the value parameter type is best-effort.
                out.append(f"    def {name}(self, value) -> None: ...")
        elif isinstance(member, types.FunctionType):
            out.append(f"    {_format_method_signature(name, member)}")
    return out


def _format_method_signature(name: str, func: types.FunctionType) -> str:
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return f"def {name}(self, *args, **kwargs) -> object: ..."

    params: list[str] = []
    for i, (pname, param) in enumerate(sig.parameters.items()):
        if i == 0 and pname == "self":
            params.append("self")
            continue
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            params.append(f"*{pname}")
            continue
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            params.append(f"**{pname}")
            continue
        ann = _annotation_str(param.annotation) if param.annotation is not param.empty else None
        if param.default is not param.empty:
            default = repr(param.default)
            params.append(f"{pname}: {ann} = {default}" if ann else f"{pname}={default}")
        else:
            params.append(f"{pname}: {ann}" if ann else pname)

    ret = _annotation_str(sig.return_annotation) if sig.return_annotation is not sig.empty else "object"
    return f"def {name}({', '.join(params)}) -> {ret}: ..."


def _signature_return(func, default: str = "object") -> str:
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return default
    if sig.return_annotation is sig.empty:
        return default
    return _annotation_str(sig.return_annotation)


def _annotation_str(annotation) -> str:
    if annotation is None or annotation is type(None):
        return "None"
    if isinstance(annotation, str):
        # Forward-referenced — already a string. Quote-strip if double-wrapped.
        s = annotation.strip("\"'")
        return f'"{s}"' if not s.startswith(("Optional", "Union", "list", "tuple", "dict", "int", "str", "float", "bool")) else s
    # Class — use its qualified name; fall back to repr.
    try:
        return getattr(annotation, "__name__", repr(annotation))
    except Exception:
        return "object"


# ----------------------------------------------------------------------
# CLI entry point
# ----------------------------------------------------------------------


def generate_all(schemas: Iterable[str] = ("IFC2X3", "IFC4", "IFC4X3")) -> None:
    for schema in schemas:
        Generator(schema=schema).generate()


if __name__ == "__main__":
    generate_all()
