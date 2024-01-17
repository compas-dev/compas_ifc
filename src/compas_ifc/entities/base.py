from compas.data import Data
from ifcopenshell import entity_instance
import inspect
from compas.datastructures import Tree, TreeNode


class Base(Data):
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
        attr_tree.print_hierarchy()

    def attribute_info(self):
        raise NotImplementedError


class EntityNode(TreeNode):
    def __repr__(self):
        return self.name
