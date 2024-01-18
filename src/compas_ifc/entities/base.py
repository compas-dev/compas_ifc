from compas.data import Data
from ifcopenshell import entity_instance
import inspect
from compas.datastructures import Tree, TreeNode


class Base(Data):
    """Base class for all IFC entities.

    Attributes
    ----------
    entity : entity_instance
        The IFC entity instance.
    reader : IfcReader
    """

    def __new__(cls, entity, *args, **kwargs):
        # try:
        #     from . import generated
        # except ImportError:
        #     raise ImportError("compas_ifc classes was not generated. Run `python -m compas_ifc.entities.generator`")

        from . import generated

        cls_name = entity.is_a()
        ifc_cls = getattr(generated, cls_name, None)
        return super(Base, cls).__new__(ifc_cls)

    def __init__(self, entity=None, reader=None, **kwargs):
        self.reader = reader
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
            return self.reader.from_entity(attr)
        if isinstance(attr, (list, tuple)):
            return [self._get_attribute(entity=item) for item in attr]
        else:
            return attr

    def _get_inverse_attribute(self, name):
        return [self.reader.from_entity(attr) for attr in getattr(self.entity, name)]

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

    def print_attributes(self, max_depth=2):
        attr_tree = Tree()
        root = EntityNode(name=f"ROOT: {self} [{self.__class__.__name__}]")
        attr_tree.add(root)

        def add_entity(entity, node, depth):
            if depth < max_depth:
                for key in entity:
                    sub_entity = entity[key]
                    sub_node = EntityNode(name=f"{key}: {sub_entity} [{sub_entity.__class__.__name__}]")
                    node.add(sub_node)
                    if isinstance(sub_entity, Base):
                        add_entity(sub_entity, sub_node, depth + 1)

        add_entity(self, root, 0)

        print("=" * 80 + "\n" + f"Attributes of {self}\n" + "=" * 80)
        attr_tree.print_hierarchy()
        print("")

    def attribute_info(self):
        raise NotImplementedError

    def print_spatial_hierarchy(self):
        from compas_ifc.entities.generated import IfcObjectDefinition

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
                    name += "*"
                node = EntityNode(name=name)
                parent_node.add(node)
                add_entity(child_entity, node)

        root_node = EntityNode(name=f"{top}")
        spatial_tree.add(root_node)
        add_entity(top, root_node)

        print("=" * 80 + "\n" + f"Spatial hierarchy of {self}\n" + "=" * 80)
        spatial_tree.print_hierarchy()
        print("")

    def print_properties(self):
        from compas_ifc.entities.generated import IfcObject

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
        tree.print_hierarchy()
        print("")


class EntityNode(TreeNode):
    def __repr__(self):
        return self.name
