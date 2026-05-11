from typing import TYPE_CHECKING
from typing import Optional
from typing import Union

import ifcopenshell
from compas.data import Data
from compas.datastructures import Tree
from compas.datastructures import TreeNode
from ifcopenshell import entity_instance

if TYPE_CHECKING:
    from compas_ifc.bim import BuildingInformationModel
    from compas_ifc.file import IFCFile


# ============================================================================
# Extension registry
# ============================================================================
#
# The runtime layer composes a small synthetic class per IFC entity at
# instantiation time, mixing :class:`Base` with any extension classes whose
# target IFC class matches `entity.is_a(...)`. The registry maps an IFC class
# name to a list of `(extension_class, schemas_or_None)` pairs.
#
# Extensions register themselves through the :func:`extends` decorator
# (Phase 2). During Phase 1 of the migration to PEP 561 stubs, the existing
# hand-written extensions are bootstrapped into the registry by their class
# name in ``compas_ifc/entities/extensions/__init__.py``.

_extension_registry: dict = {}
_depth_cache: dict = {}
_inverse_cache: dict = {}
_derived_cache: dict = {}
# Synthetic ``Extended<IfcClass>`` classes are reused across entities of the
# same IFC class. Keyed by ``(schema_name, ifc_class_name)``; the entry is the
# composed class returned from ``__new__``. The cache is only consulted when
# the caller does not supply a custom ``extensions=`` kwarg.
_class_cache: dict = {}


def extends(*ifc_classes: str, schemas: Optional[set] = None):
    """Register a class as an extension of one or more IFC classes.

    The decorated class becomes part of the synthetic class composed by
    :meth:`Base.__new__` whenever the underlying IFC entity satisfies
    ``entity.is_a(<ifc_class>)``. When ``schemas`` is provided, the
    extension is only applied for entities loaded from a file that uses one
    of the listed schemas.

    Parameters
    ----------
    *ifc_classes : str
        One or more IFC class names this extension applies to.
    schemas : set of str, optional
        Restrict the extension to specific IFC schemas (for example
        ``{"IFC4", "IFC4X3"}``). Defaults to all schemas.

    Examples
    --------
    >>> from compas_ifc.entities.base import Base, extends
    >>> @extends("IfcElement")
    ... class IfcElementExtras(Base):
    ...     pass
    """

    def wrap(cls):
        for ifc_class in ifc_classes:
            _extension_registry.setdefault(ifc_class, []).append((cls, schemas))
        # Invalidate the synthetic-class cache so a script that registers an
        # extension after wrapping some entities still picks it up on the next
        # wrap.
        _class_cache.clear()
        return cls

    return wrap


def _ifc_depth(schema, ifc_class: str) -> int:
    """Compute the depth of an IFC class in its inheritance chain (cached)."""
    if schema is None:
        return 0
    key = (schema.name(), ifc_class)
    cache = _depth_cache
    if key not in cache:
        try:
            decl = schema.declaration_by_name(ifc_class)
        except Exception:
            cache[key] = 0
            return 0
        depth = 0
        while decl.supertype():
            depth += 1
            decl = decl.supertype()
        cache[key] = depth
    return cache[key]


# ============================================================================
# TypeDefinition
# ============================================================================


class TypeDefinition:
    """
    Root class for all IFC type definitions.

    Attributes
    ----------
    entity : entity_instance
        The IFC entity instance.
    file : Ifcfile
        The IFC file containing this instance of the type definition.
    value : Any
        The wrapped value of this type definition.
    """

    def __init__(self, entity: entity_instance = None, file=None):
        """Constructor for the TypeDefinition class.

        Parameters
        ----------
        entity : entity_instance
            The IFC entity instance.
        file : Ifcfile
            The IFC file containing this instance of the type definition.
        """
        self.file = file
        self.entity = entity

    @property
    def value(self):
        return self.entity.wrappedValue

    def __repr__(self):
        return "<{} {}>".format(self.entity.is_a(), self.value)


# ============================================================================
# Base
# ============================================================================


class Base(Data):
    """
    Root class for all IFC entity wrappers.

    Every entity in a loaded IFC file is wrapped in a :class:`Base` (or a
    synthetic ``Extended<IfcClass>`` subclass that mixes in matched
    extensions). Direct attribute access is proxied to the underlying
    ``ifcopenshell.entity_instance`` through :meth:`__getattr__`. Inverse
    attributes are exposed as zero-argument callables to mark the syntactic
    distinction from direct attributes.

    Attributes
    ----------
    entity : entity_instance
        The IFC entity instance.
    file : Ifcfile
        The IFC file containing this instance of the class.
    """

    def __new__(cls, entity: entity_instance, file: "IFCFile" = None, extensions: dict = None):
        # TypeDefinition fallback for simple-type wrappers (IfcLengthMeasure etc).
        if hasattr(entity, "wrappedValue") and not entity.is_a("IfcRoot"):
            return TypeDefinition(entity, file)

        schema = file._schema if file is not None else None
        schema_name = schema.name() if schema is not None else "IFC4"
        ifc_class_name = entity.is_a()

        # Fast path: most calls use no custom ``extensions=`` kwarg, so the
        # composed class depends only on ``(schema, ifc_class)`` and can be
        # cached. This avoids creating a fresh ``type(...)`` object for every
        # wrapped entity — files with thousands of walls/slabs would otherwise
        # produce thousands of identical synthetic classes.
        if not extensions:
            cache_key = (schema_name, ifc_class_name)
            cached = _class_cache.get(cache_key)
            if cached is not None:
                return object.__new__(cached)

        # Collect (depth, ifc_class, ext_cls) triples; de-dupe on ext_cls.
        matched: list = []
        seen_classes = set()

        # 1. Registered extensions
        for ifc_class, registered in _extension_registry.items():
            if entity.is_a(ifc_class):
                for ext_cls, ext_schemas in registered:
                    if ext_cls in seen_classes:
                        continue
                    if ext_schemas is not None and schema_name not in ext_schemas:
                        continue
                    seen_classes.add(ext_cls)
                    matched.append((_ifc_depth(schema, ifc_class), ifc_class, ext_cls))

        # 2. User-supplied extensions via `extensions=` kwarg
        if extensions:
            for ifc_class, ext_cls in extensions.items():
                if entity.is_a(ifc_class) and ext_cls not in seen_classes:
                    seen_classes.add(ext_cls)
                    matched.append((_ifc_depth(schema, ifc_class), ifc_class, ext_cls))

        if matched:
            # Sort deepest-first so super() walks parents toward IfcRoot.
            matched.sort(key=lambda triple: -triple[0])
            ordered_exts = [ext_cls for _, _, ext_cls in matched]
            extension_name = f"Extended{ifc_class_name}"
            bases = tuple(ordered_exts + [Base])
            extended_cls = type(extension_name, bases, {})
        else:
            extended_cls = Base

        if not extensions:
            _class_cache[(schema_name, ifc_class_name)] = extended_cls
        return object.__new__(extended_cls)

    def __init__(self, entity: entity_instance = None, file=None, **kwargs):
        super().__init__()
        self.file = file
        self.entity = entity

    def __repr__(self):
        # Use the IFC class name rather than the synthetic ``Extended<X>``
        # subclass name produced by :meth:`__new__`.
        return "<#{} {}>".format(self.entity.id(), self.entity.is_a())

    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        return iter(self.all_attribute_names())

    # ------------------------------------------------------------------
    # Dynamic attribute access
    # ------------------------------------------------------------------

    def __getattr__(self, name):
        # Avoid recursion during partial initialisation.
        if name.startswith("_") or name in {"entity", "file"}:
            raise AttributeError(name)
        try:
            entity = object.__getattribute__(self, "entity")
        except AttributeError:
            raise AttributeError(name)
        if entity is None:
            raise AttributeError(name)
        # Inverse attribute: return a zero-arg callable (preserves the parens
        # convention that distinguishes inverse from direct access).
        if name in self._inverse_attribute_names():
            return lambda: self._get_inverse_attribute(name)
        try:
            return self._get_attribute(name)
        except (AttributeError, RuntimeError):
            raise AttributeError(name)

    def __setattr__(self, name, value):
        # IFC schema attributes are PascalCase; route them to ifcopenshell.
        # Internal/runtime fields use snake_case or underscore prefix and
        # fall through to the normal attribute setter.
        if name and name[0].isupper():
            entity = self.__dict__.get("entity")
            if entity is not None:
                self._set_attribute(name, value)
                return
        super().__setattr__(name, value)

    # ------------------------------------------------------------------
    # Schema introspection
    # ------------------------------------------------------------------

    def _inverse_attribute_names(self):
        """Set of inverse attribute names defined on this entity's IFC class."""
        if self.file is None:
            return frozenset()
        schema = self.file._schema
        key = (schema.name(), self.entity.is_a())
        cache = _inverse_cache
        if key not in cache:
            try:
                decl = schema.declaration_by_name(self.entity.is_a())
                cache[key] = frozenset(ia.name() for ia in decl.all_inverse_attributes())
            except Exception:
                cache[key] = frozenset()
        return cache[key]

    def _derived_attribute_names(self):
        """Set of derived attribute names defined on this entity's IFC class.

        Derived attributes are computed from other fields and cannot be set
        directly. Writes to them are silently ignored to match the behaviour
        of the previous generator-driven layer.
        """
        if self.file is None:
            return frozenset()
        schema = self.file._schema
        key = (schema.name(), self.entity.is_a())
        cache = _derived_cache
        if key not in cache:
            try:
                decl = schema.declaration_by_name(self.entity.is_a())
                derived_flags = decl.derived()
                attrs = decl.all_attributes()
                cache[key] = frozenset(
                    a.name() for a, is_derived in zip(attrs, derived_flags) if is_derived
                )
            except Exception:
                cache[key] = frozenset()
        return cache[key]

    def _get_attribute(self, name=None, entity: entity_instance = None):
        if name is not None:
            attr = getattr(self.entity, name)
        else:
            attr = entity
        if isinstance(attr, entity_instance):
            return self.file.from_entity(attr)
        if isinstance(attr, (list, tuple)):
            return [self._get_attribute(entity=item) for item in attr]
        return attr

    def _set_attribute(self, name, value):
        # Derived attributes are computed from other fields; matching the
        # behaviour of the old generator's TEMPLATE_DERIVED, writes are
        # silently ignored.
        if name in self._derived_attribute_names():
            return

        def prepare_value(value):
            if isinstance(value, Base):
                return value.entity
            elif isinstance(value, TypeDefinition):
                return value.entity
            elif isinstance(value, (list, tuple)):
                return [prepare_value(v) for v in value]
            else:
                return value

        if isinstance(value, (list, tuple)):
            value = [prepare_value(v) for v in value]
        else:
            value = prepare_value(value)

        if getattr(self.entity, name) != value:
            try:
                setattr(self.entity, name, value)
            except Exception as e:
                print(f"Error setting {name} of {self} to {value}")
                raise e

    def _get_inverse_attribute(self, name):
        return [self.file.from_entity(attr) for attr in getattr(self.entity, name)]

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def model(self) -> "BuildingInformationModel":
        return self.file.model

    @property
    def schema(self):
        return self.file._schema.name()

    def id(self):
        return self.entity.id()

    def is_a(self, type_name=None):
        if type_name:
            return self.entity.is_a(type_name)
        else:
            return self.entity.is_a()

    def all_attribute_names(self):
        info = self.entity.get_info(include_identifier=False)
        del info["type"]
        return list(info.keys())

    @property
    def attributes(self):
        return self.to_dict()

    def to_dict(self, recursive=False, ignore_fields=[], include_fields=[], convert_type_definitions=False):
        def iter_list(values):
            _values = []
            for value in values:
                if isinstance(value, Base):
                    value = value.to_dict(recursive=recursive, ignore_fields=ignore_fields, include_fields=include_fields, convert_type_definitions=convert_type_definitions)
                elif convert_type_definitions and isinstance(value, TypeDefinition):
                    value = value.value
                elif isinstance(value, (list, tuple)):
                    value = iter_list(value)
                _values.append(value)
            return _values

        data = {}
        for key in self:
            if key in ignore_fields:
                continue

            if include_fields and key not in include_fields:
                continue

            value = getattr(self, key)

            if recursive and isinstance(value, Base):
                value = value.to_dict(recursive=recursive, ignore_fields=ignore_fields, include_fields=include_fields, convert_type_definitions=convert_type_definitions)
            elif recursive and isinstance(value, (list, tuple)):
                value = iter_list(value)
            elif convert_type_definitions and isinstance(value, TypeDefinition):
                value = value.value

            data[key] = value

        return data

    def print_attributes(self, max_depth=2):
        attr_tree = Tree()
        root = EntityNode(name=f"ROOT: {self} [{self.__class__.__name__}]")
        attr_tree.add(root)

        def add_entity(entity, node, depth):
            if depth < max_depth:
                if isinstance(entity, list):
                    entity = dict(enumerate(entity))
                for key in entity:
                    sub_entity = entity[key]
                    sub_node = EntityNode(name=f"{key}: {sub_entity} [{sub_entity.__class__.__name__}]")
                    node.add(sub_node)
                    if isinstance(sub_entity, (Base, list)):
                        add_entity(sub_entity, sub_node, depth + 1)

        add_entity(self, root, 0)

        print("=" * 80 + "\n" + f"Attributes of {self}\n" + "=" * 80)
        print(attr_tree.get_hierarchy_string(max_depth=max_depth))
        print("")

    def attribute_info(self):
        raise NotImplementedError

    def print_spatial_hierarchy(self, max_depth=5):
        if not self.entity.is_a("IfcObjectDefinition"):
            raise TypeError("Only IfcObjectDefinition has spatial hierarchy")

        top = self
        while top.parent:
            top = top.parent

        spatial_tree = Tree()

        def add_entity(entity, parent_node):
            for child_entity in entity.children:
                name = f"{child_entity}"
                if child_entity == self:
                    name = "**" + name + "**"
                node = EntityNode(name=name)
                parent_node.add(node)
                add_entity(child_entity, node)

        root_node = EntityNode(name=f"{top}")
        spatial_tree.add(root_node)
        add_entity(top, root_node)

        print("=" * 80 + "\n" + f"Spatial hierarchy of {self}\n" + "=" * 80)
        print(spatial_tree.get_hierarchy_string(max_depth=max_depth))
        print("")

    def print_properties(self, max_depth=2):
        if not self.entity.is_a("IfcObject"):
            raise TypeError("Only IfcObject has properties")

        def add_property(item, parent_node):
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, dict):
                        node = EntityNode(name=f"{key}")
                        parent_node.add(node)
                        add_property(value, node)
                    else:
                        node = EntityNode(name=f"{key}: {value}")
                        parent_node.add(node)

        tree = Tree()
        root = EntityNode(name=f"{self}")
        tree.add(root)
        add_property(self.property_sets, root)

        print("=" * 80 + "\n" + f"Properties of {self}\n" + "=" * 80)
        print(tree.get_hierarchy_string(max_depth=max_depth))
        print("")

    def show(self):
        self.model.show(self)

    def validate(self, schema):
        raise NotImplementedError

    def validate_geometry(self, schema):
        raise NotImplementedError

    def validate_relationships(self, schema):
        raise NotImplementedError

    def validate_properties(self, schema: Union[str, dict], verbose: bool = True) -> bool:
        """Validate the properties of the entity against a schema.

        Parameters
        ----------
        schema : Union[str, dict]
            The schema to validate against. Either a path to a JSON file or a dictionary for schemas for each property set.
        verbose : bool, optional
            Whether to print the validation results.

        Returns
        -------
        bool
            True if the validation passes, False otherwise.
        """

        from compas import json_load
        from jsonschema import Draft202012Validator

        if isinstance(schema, str):
            validator = Draft202012Validator(json_load(schema))  # type: ignore
            validator.validate(self.property_sets)

            if verbose:
                print(f"Schema validation passed on {self}.property_sets")

        elif isinstance(schema, dict):
            for pset_name, path in schema.items():
                validator = Draft202012Validator(json_load(path))
                validator.validate(self.property_sets[pset_name])

                if verbose:
                    print(f"Schema validation passed on {self}.property_sets[{pset_name}]")

        else:
            raise TypeError("Invalid schema type, expected str or dict")

        return True


class EntityNode(TreeNode):
    def __repr__(self):
        return self.name


# Force ifcopenshell symbol to be present at module-import time so that
# `isinstance(x, entity_instance)` checks work without re-importing.
__all__ = ["Base", "TypeDefinition", "EntityNode", "extends", "ifcopenshell"]
