import ifcopenshell

# TODO: use polymorphism to simplify the class inheritance.
# TODO: pre-generate all classes.

class Factory:

    def __init__(self, schema: str = "IFC4") -> None:
        self.schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema)
    
    def create_class(self, name):

        declaration = self.schema.declaration_by_name(name)

        def init(self, entity):
            self._entity = entity

        attributes = {
            "__init__": init,
        }

        for attribute in declaration.all_attributes():
            name = attribute.name()
            attributes[name] = self.create_getter(attribute)

        for attribute in declaration.all_inverse_attributes():
            name = attribute.name()
            attributes[name] = self.create_getter(attribute, setter=False)
        
        return type(name, (), attributes)

    def create_getter(self, attribute, setter=True):

        name = attribute.name()

        @property
        def prop(self):
            return getattr(self._entity, name)

        if setter:
            @prop.setter
            def prop(self, value):
                if not hasattr(self._entity, name):
                    raise AttributeError(f"Attribute <{name}> does not exist")

                attribute_type = attribute.type_of_attribute()
                if attribute_type.as_aggregation_type():
                    value = list(value)
                    lower = attribute_type.bound1()
                    upper = attribute_type.bound2()
                    if lower > 0 and upper > 0:
                        if len(value) < lower or len(value) > upper:
                            raise ValueError(f"Expected <{name}> to have between {lower} and {upper} elements")
                    # TODO: check type of elements

                if attribute_type.as_named_type():
                    declared_type = attribute_type.declared_type()
                    type_name = declared_type.name()
                    # TODO: take care of non-entity situations
                    if declared_type.as_entity() and value.is_a() != type_name:
                        raise TypeError(f"Expected <{name}> to be of type {type_name}, got {value.is_a()}")

                setattr(self._entity, name, value)

        
        return prop

if __name__ == "__main__":

    file = ifcopenshell.open("data/wall-with-opening-and-window.ifc")
    _entity = file[3]
    declaration = _entity.is_a()

    factory = Factory()
    Entity = factory.create_class(declaration)

    entity = Entity(_entity)
    print(entity.ThePerson)
    # entity.ThePerson = "some wrong value type"
    entity.ThePerson = file[3]

    print(entity.ThePerson)
    print(entity)