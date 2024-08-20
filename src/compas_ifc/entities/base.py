import importlib
from typing import TYPE_CHECKING

from compas.data import Data
from compas.datastructures import Tree
from compas.datastructures import TreeNode
from ifcopenshell import entity_instance

if TYPE_CHECKING:
    from compas_ifc.file import IFCFile
    from compas_ifc.model import Model


class TypeDefinition:
    def __init__(self, entity: entity_instance = None, file=None):
        self.file = file
        self.entity = entity

    @property
    def value(self):
        return self.entity.wrappedValue

    def __repr__(self):
        return "<{} {}>".format(self.entity.is_a(), self.value)


class Base(Data):
    """Base class for all IFC entities.

    Attributes
    ----------
    entity : entity_instance
        The IFC entity instance.
    file : Ifcfile
    """

    def __new__(cls, entity: entity_instance, file: "IFCFile" = None):
        if file is None:
            schema = "IFC4"
        else:
            schema = file._schema.name()

        try:
            classes = importlib.import_module(f"compas_ifc.entities.generated.{schema}")
        except ImportError:
            raise ImportError(f"compas_ifc classes for schema {schema} was not generated. Run `python -m compas_ifc.entities.generator`")

        cls_name = entity.is_a()
        ifc_cls = getattr(classes, cls_name, None)
        if ifc_cls:
            return super(Base, cls).__new__(ifc_cls)
        elif hasattr(entity, "wrappedValue"):
            return TypeDefinition(entity, file)

    def __init__(self, entity: entity_instance = None, file=None):
        super().__init__()
        self.file = file
        self.entity = entity

    def __repr__(self):
        return "<#{} {}>".format(self.entity.id(), self.__class__.__name__)

    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        return iter(self.all_attribute_names())

    def _get_attribute(self, name=None, entity: entity_instance = None):
        if name is not None:
            attr = getattr(self.entity, name)
        else:
            attr = entity
        if isinstance(attr, entity_instance):
            # NOTE: Double check.
            # if hasattr(attr, "wrappedValue"):
            #     return attr.wrappedValue
            return self.file.from_entity(attr)
        if isinstance(attr, (list, tuple)):
            return [self._get_attribute(entity=item) for item in attr]
        else:
            return attr

    def _set_attribute(self, name, value):
        # TODO: re-enable strong type checking
        # cls = self.__class__
        # getter_type_hints = get_type_hints(getattr(cls, name).fget)
        # value_type = getter_type_hints["return"]

        # if hasattr(value_type, "__origin__"):
        #     # deal parameterized generic types
        #     origin = value_type.__origin__
        #     if origin == list:
        #         if not isinstance(value, (list, tuple)):
        #             raise TypeError(f"Expected {value_type}, got {type(value)} for {cls.__name__}.{name}")
        #         value_type = getter_type_hints["return"].__args__[0]
        #         if not all(isinstance(item, value_type) for item in value):
        #             raise TypeError(f"Expected {value_type}, got {type(value)} for {cls.__name__}.{name}")
        #     else:
        #         raise NotImplementedError(f"Unsupported generic type {origin}")

        # elif not isinstance(value, value_type):
        #     raise TypeError(f"Expected {value_type}, got {type(value)} for {cls.__name__}.{name}")

        def prepare_value(value):
            if isinstance(value, Base):
                return value.entity
            elif isinstance(value, TypeDefinition):
                return value.entity
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

    @property
    def model(self) -> "Model":
        return self.file.model  # TODO: rather convoluted.

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
        # all_attributes = []
        # def get_attr_names(cls):
        #     if cls.__name__ == "Base":
        #         return
        #     all_attributes.extend(cls.attributes)
        #     for base in cls.__bases__:
        #         get_attr_names(base)
        # get_attr_names(self.__class__)
        # return all_attributes
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
        IfcObjectDefinition = getattr(importlib.import_module(f"compas_ifc.entities.generated.{self.schema}"), "IfcObjectDefinition")

        if not isinstance(self, IfcObjectDefinition):
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
        IfcObject = getattr(importlib.import_module(f"compas_ifc.entities.generated.{self.schema}"), "IfcObject")

        if not isinstance(self, IfcObject):
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
        add_property(self.properties, root)

        print("=" * 80 + "\n" + f"Properties of {self}\n" + "=" * 80)
        print(tree.get_hierarchy_string(max_depth=max_depth))
        print("")

    def show(self):
        self.model.show(self)


class EntityNode(TreeNode):
    def __repr__(self):
        return self.name
