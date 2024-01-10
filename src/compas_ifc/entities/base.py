from compas.data import Data
from ifcopenshell import entity_instance
from .attribute import Attribute
import inspect


class Base(Data):
    def __new__(cls, entity, *args, **kwargs):
        try:
            from . import generated
        except ImportError:
            raise ImportError("compas_ifc classes was not generated. Run `python -m compas_ifc.entities.generator`")

        cls_name = entity.is_a()
        ifc_cls = getattr(generated, cls_name, None)
        return super(Base, cls).__new__(ifc_cls)

    def __init__(self, entity=None, reader=None, **kwargs):
        self.reader = reader
        self.entity = entity

    def __repr__(self):
        return "<#{} {}>".format(self.entity.id(), self.__class__.__name__)

    def print_attributes(self, max_depth=1):
        raise NotImplementedError
    
    def attribute_names(self):
        raise NotImplementedError
    
    def attribute_info(self):
        raise NotImplementedError