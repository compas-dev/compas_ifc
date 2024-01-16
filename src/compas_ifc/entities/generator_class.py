import ifcopenshell


class Generator:
    def __init__(self, schema="IFC4"):
        self.schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema)

    def generate(self):
        for declaration in self.schema.declarations():
            class_string = None
            if declaration.as_entity():
                entity_generator = EntityGenerator(declaration)
                class_string = entity_generator.generate()
                name = entity_generator.name

            if declaration.as_type_declaration():
                type_declaration_generator = TypeDeclarationGenerator(declaration)
                class_string = type_declaration_generator.generate()
                name = type_declaration_generator.name

            if declaration.as_enumeration_type():
                enum_generator = EnumGenerator(declaration)
                class_string = enum_generator.generate()
                name = enum_generator.name
            
            if class_string:
                with open(f"src/compas_ifc/entities/generated/{name}.py", "w") as f:
                    f.write(class_string)

class EntityGenerator:
    TEMPLATE = """IMPORTS

class CLASS_NAME(PARENT_NAME):
    \"\"\"DESCRIPTION\"\"\"
"""

    def __init__(self, declaration):
        self.declaration = declaration
        self.name = declaration.name()
        self.imports = set()
        self.parent = None
        self.attributes = []
        self.description = ""

    def get_parent(self):
        if self.declaration.supertype():
            self.parent = self.declaration.supertype().name()
            self.imports.add(f"from .{self.parent} import {self.parent}")
        else:
            self.parent = "Base"
            self.imports.add("from compas_ifc.entities.base import Base")

    def get_description(self):
        self.description = f"Wrapper class for {self.name}."

    def get_attributes(self):
        for attribute in self.declaration.attributes():
            self.attributes.append(AtrtributeGenerator(attribute))

    def generate(self):
        self.get_parent()
        self.get_description()
        self.get_attributes()

        class_string = self.TEMPLATE.replace("CLASS_NAME", self.name)
        class_string = class_string.replace("PARENT_NAME", self.parent)
        class_string = class_string.replace("DESCRIPTION", self.description)

        for attribute in self.attributes:
            class_string += attribute.generate()
            self.imports.update(attribute.imports)

        class_string = class_string.replace("IMPORTS", "\n".join(sorted(self.imports)))

        return class_string


class AtrtributeGenerator:
    TEMPLATE = """
    @property
    def ATTRIBUTE_NAME(self)-> ATTRIBUTE_TYPE:
        \"\"\"DESCRIPTION\"\"\"
        return self._get_attribute("ATTRIBUTE_NAME")

    @ATTRIBUTE_NAME.setter
    def ATTRIBUTE_NAME(self, value: ATTRIBUTE_TYPE):
        return self._set_attribute("ATTRIBUTE_NAME", value)
"""

    def __init__(self, attribute):
        self.attribute = attribute
        self.name = attribute.name()
        self.imports = set()
        self.type = None
        self.description = "Would say something about the attribute here."

    def get_aggregation_type(self, attribute_type):
        # type_aggragation = attribute_type.type_of_aggregation()
        # bound1 = attribute_type.bound1()
        # bound2 = attribute_type.bound2()
        # TODO: add support for bounds etc.

        type_of_element = attribute_type.type_of_element()
        if type_of_element.as_aggregation_type():
            aggregation_string = self.get_aggregation_type(type_of_element)
            return f"list[{aggregation_string}]"
        else:
            if type_of_element.declared_type().as_select_type():
                type_of_element_string = self.get_select_type(type_of_element)
            else:
                type_of_element_string = type_of_element.declared_type().name()
                self.imports.add(f"from .{type_of_element_string} import {type_of_element_string}")
            return f"list[{type_of_element_string}]"

    def get_select_type(self, attribute_type):
        def flaten_select_list(select_type, initial_list=None):
            if initial_list is None:
                initial_list = []
            select_list = select_type.select_list()
            for item in select_list:
                if item.as_select_type():
                    initial_list = flaten_select_list(item, initial_list)
                else:
                    initial_list.append(item)
            return initial_list

        select_list = flaten_select_list(attribute_type.declared_type())
        select_string = "Union[" + ", ".join([f"{item.name()}" for item in select_list]) + "]"
        for item in select_list:
            self.imports.add(f"from .{item.name()} import {item.name()}")
        self.imports.add("from typing import Union")
        return select_string

    def get_attribute_type(self):
        attribute_type = self.attribute.type_of_attribute()
        if attribute_type.as_aggregation_type():
            self.type = self.get_aggregation_type(attribute_type)
        elif attribute_type.as_simple_type():
            attribute_type = attribute_type.declared_type()
            TYPE_MAP = {
                "integer": "int",
                "logical": "bool",
            }
            self.type = TYPE_MAP[attribute_type]
        elif attribute_type.declared_type().as_select_type():
            self.type = self.get_select_type(attribute_type)
        else:
            # Entity, Enumeration, or Type declaration
            self.type = attribute_type.declared_type().name()
            self.imports.add(f"from .{self.type} import {self.type}")

    def generate(self):
        self.get_attribute_type()
        attribute_string = self.TEMPLATE.replace("ATTRIBUTE_NAME", self.name)
        attribute_string = attribute_string.replace("ATTRIBUTE_TYPE", str(self.type))
        attribute_string = attribute_string.replace("DESCRIPTION", self.description)

        return attribute_string


class TypeDeclarationGenerator:
    TEMPLATE = """class CLASS_NAME(PARENT_NAME):
    \"\"\"Some description.\"\"\"
"""

    TYPE_MAP = {
        "DOUBLE": "float",
        "INT": "int",
        "STRING": "str",
        "LOGICAL": "bool",
        "BOOL": "bool",
        "BINARY": "bytes",
    }

    def __init__(self, declaration):
        self.declaration = declaration
        self.name = declaration.name()
        self.parent = None

    def get_parent(self):
        ifc_type = self.declaration.argument_types()[0]
        if ifc_type.startswith("AGGREGATE OF"):
            value_type = ifc_type.split("OF ")[1]
            if value_type == "ENTITY INSTANCE":
                python_type = "list"  # TODO: handle this
            else:
                python_type = f"list[{self.TYPE_MAP[value_type]}]"
        else:
            python_type = self.TYPE_MAP[ifc_type]
        self.parent = python_type

    def generate(self):
        self.get_parent()

        class_string = self.TEMPLATE.replace("CLASS_NAME", self.name)
        class_string = class_string.replace("PARENT_NAME", self.parent)

        return class_string


class EnumGenerator:
    TEMPLATE = """class CLASS_NAME(str):
    items = ITEMS
"""
    def __init__(self, declaration):
        self.declaration = declaration
        self.name = declaration.name()
        self.items = []
    
    def get_items(self):
        for item in self.declaration.enumeration_items():
            self.items.append(item)
        
    def generate(self):
        self.get_items()

        class_string = self.TEMPLATE.replace("CLASS_NAME", self.name)
        class_string = class_string.replace("ITEMS", str(self.items))

        return class_string

if __name__ == "__main__":
    generator = Generator()
    generator.generate()
