import ifcopenshell


class Factory:

    def __init__(self, schema: str = "IFC4") -> None:
        self.schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema)
    
    def create_class(self, name):

        declaration = self.schema.declaration_by_name(name)

        attributes = {}

        # TODO: make attributes getters and setters with type checking.
        for attribute in declaration.all_attributes():
            
            @property
            def prop(self):
                return "getter called"

            @prop.setter
            def prop(self, value):
                print("setter called")
            
            attributes[attribute.name()] = prop

        # for attribute in declaration.all_inverse_attributes():
        #     attributes[attribute.name()] = None
        
        return type(name, (object,), attributes)


if __name__ == "__main__":

    factory = Factory()
    IfcObjectDefinition = factory.create_class("IfcObjectDefinition")
    print(IfcObjectDefinition)

    od = IfcObjectDefinition()
    print(od.Name)
    od.Name = "test"