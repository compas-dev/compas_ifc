from ifcopenshell import entity_instance

class Attribute:

    def __init__(self, name, type, optional):
        self.name = name
        self.type = type
        self.optional = optional

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        else:
            return self._get_attribute(obj, self.name)

    def __set__(self, obj, value):
        pass
    
    def _get_attribute(self, obj, name):
        attr = getattr(obj.entity, name)
        if isinstance(attr, (list, tuple)):
            return [self._get_attribute_value(obj, item) for item in attr]
        else:
            return self._get_attribute_value(obj, attr)
    
    def _get_attribute_value(self, obj, attr):
        if isinstance(attr, entity_instance):
            return obj.reader.from_entity(attr)
        else:
            return attr