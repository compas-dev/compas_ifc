import inspect
import os
import types

import ifcopenshell

from compas_ifc.entities import extensions


class Generator:
    """
    Generator class for generating all IFC classes and type definitions as strongly typed Python classes.
    They are generated in the `compas_ifc.entities.generated.[schema_name]` folder.

    Attributes
    ----------
    schema : :class:`ifcopenshell.ifcopenshell_wrapper.schema`
        The IfcOpenShell schema to generate classes for.

    """

    def __init__(self, schema="IFC4"):
        self.schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema)

    def generate(self):
        """Generate all classes and type definitions for the given schema."""
        HERE = os.path.dirname(__file__)
        FOLDER = os.path.join(HERE, "generated", self.schema.name())
        if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)

        doc_string = """
.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: class.rst

"""
        init_string = ""

        count = 0

        for declaration in self.schema.declarations():
            class_string = None
            if declaration.as_entity():
                entity_generator = EntityGenerator(declaration)
                class_string = entity_generator.generate()
                name = entity_generator.name

            # if declaration.as_type_declaration():
            #     type_declaration_generator = TypeDeclarationGenerator(declaration)
            #     class_string = type_declaration_generator.generate()
            #     name = type_declaration_generator.name

            if declaration.as_enumeration_type():
                enum_generator = EnumGenerator(declaration)
                class_string = enum_generator.generate()
                name = enum_generator.name

            if class_string:
                init_string += f"from .{name.lower()} import {name}\n"
                doc_string += f"    {name}\n"

                with open(os.path.join(FOLDER, f"{name.lower()}.py"), "w") as f:
                    f.write(class_string)
                    count += 1

        init_string = f'"""{doc_string}"""\n\n{init_string}'

        with open(os.path.join(FOLDER, "__init__.py"), "w") as f:
            f.write(init_string)

        print(f"Generated {count} classes for at {FOLDER}.")


class EntityGenerator:
    """
    Generator class for generating a single IFC entityclass.

    Attributes
    ----------
    declaration : :class:`ifcopenshell.ifcopenshell_wrapper.declaration`
        The IfcOpenShell declaration to generate a class for.
    name : str
        The name of the class to generate.
    imports : set
        The imports required for the class.
    attribute_imports : set
        The imports required for the attributes of the class.
    parent : str
        The parent class of the class to generate.
    extension : str
        The extension class of the class to generate.
    attributes : list[:class:`AttributeGenerator`]
        The attributes of the class to generate.
    inverse_attributes : list[:class:`InverseAttributeGenerator`]
        The inverse attributes of the class to generate.
    description : str
        The description of the class to generate.
    TEMPLATE : str
        The template python code for the class to generate.

    """

    TEMPLATE = """IMPORTS
class CLASS_NAME(PARENT_NAME):
    \"\"\"DESCRIPTION\"\"\"
"""

    def __init__(self, declaration):
        self.declaration = declaration
        self.name = declaration.name()
        self.imports = set()
        self.attribute_imports = set()
        self.parent = None
        self.extension = None
        self.attributes = []
        self.inverse_attributes = []
        self.description = ""

    def get_parent(self):
        if self.declaration.supertype():
            self.parent = self.declaration.supertype().name()
            self.imports.add(f"from .{self.parent.lower()} import {self.parent}")
        else:
            self.parent = "Base"
            self.imports.add("from compas_ifc.entities.base import Base")

        extension = getattr(extensions, self.name, None)
        if extension:
            print("Found extension class:", extension)
            self.imports.add(f"from compas_ifc.entities.extensions import {self.name} as {self.name}_Ext   # type: ignore")
            self.extension = f"{self.name}_Ext"

    def get_description(self):
        self.description = f"Wrapper class for {self.name}."

    def get_attributes(self):
        # attributes = self.declaration.attributes()
        # direved = self.declaration.derived()
        # all_attributes = self.declaration.all_attributes()
        # all_inverse_attributes = self.declaration.all_inverse_attributes()

        derived = self.declaration.derived()
        attribute_names = [attr.name() for attr in self.declaration.attributes()]

        for i, attribute in enumerate(self.declaration.all_attributes()):
            if attribute.name() in attribute_names:
                self.attributes.append(AttributeGenerator(attribute, self, False))
            elif derived[i]:
                self.attributes.append(AttributeGenerator(attribute, self, True))

        inverse_attributes_from_supertype = []
        if self.declaration.supertype():
            for ia in self.declaration.supertype().all_inverse_attributes():
                inverse_attributes_from_supertype.append(ia.name())

        for inverse_attribute in self.declaration.all_inverse_attributes():
            if inverse_attribute.name() not in inverse_attributes_from_supertype:
                self.inverse_attributes.append(InverseAttributeGenerator(inverse_attribute, self))

    def get_attribute_imports_string(self):
        if not self.attribute_imports:
            return ""

        attribute_imports_string = "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n"
        for import_string in sorted(self.attribute_imports):
            attribute_imports_string += f"    {import_string}\n"
        return attribute_imports_string

    def get_extension_methods(self, class_name):
        extension = getattr(extensions, class_name, None)
        if extension is None:
            return ""

        print("Extension classes:", extension)

        extension_methods_string = ""
        for method in dir(extension):
            method = getattr(extension, method)
            if isinstance(method, types.FunctionType):
                extension_methods_string += f"\n{inspect.getsource(method)}"
            elif isinstance(method, property):
                if method.fget is not None:
                    extension_methods_string += f"\n{inspect.getsource(method.fget)}"
                if method.fset is not None:
                    extension_methods_string += f"\n{inspect.getsource(method.fset)}"

        return extension_methods_string

    def generate(self):
        self.get_parent()
        self.get_description()
        self.get_attributes()

        class_string = self.TEMPLATE.replace("CLASS_NAME", self.name)
        if self.extension:
            class_string = class_string.replace("PARENT_NAME", f"{self.extension}, {self.parent}")
        else:
            class_string = class_string.replace("PARENT_NAME", self.parent)
        class_string = class_string.replace("DESCRIPTION", self.description)

        for attribute in self.attributes:
            class_string += attribute.generate()
            self.attribute_imports.update(attribute.imports)

        for inverse_attribute in self.inverse_attributes:
            class_string += inverse_attribute.generate()
            self.attribute_imports.update(inverse_attribute.imports)

        if class_string.find("Union") != -1:
            self.imports.add("from typing import Union")

        import_strings = "\n".join(sorted(self.imports)) + "\n\n" + self.get_attribute_imports_string()

        class_string = class_string.replace("IMPORTS", import_strings)

        # class_string += self.get_extension_methods(self.name)

        return class_string


class AttributeGenerator:
    """
    Generator class for generating a single IFC attribute.

    Attributes
    ----------
    attribute : :class:`ifcopenshell.ifcopenshell_wrapper.attribute`
        The IfcOpenShell attribute to generate a property for.
    parent : :class:`EntityGenerator`
        The parent class of the attribute to generate.
    is_derived : bool
        Whether the attribute is derived.
    name : str
        The name of the attribute to generate.
    imports : set
        The imports required for the attribute.
    type : str
        The type of the attribute to generate.
    description : str
        The description of the attribute to generate.

    TEMPLATE : str
        The template python code for the attribute to generate.
    TEMPLATE_DERIVED : str
        The template python code for the derived attribute to generate.

    """

    TEMPLATE = """
    @property
    def ATTRIBUTE_NAME(self)-> ATTRIBUTE_TYPE:
        \"\"\"DESCRIPTION\"\"\"
        return self._get_attribute("ATTRIBUTE_NAME")

    @ATTRIBUTE_NAME.setter
    def ATTRIBUTE_NAME(self, value: ATTRIBUTE_TYPE):
        return self._set_attribute("ATTRIBUTE_NAME", value)
"""
    TEMPLATE_DERIVED = """
    @property
    def ATTRIBUTE_NAME(self)-> ATTRIBUTE_TYPE:
        \"\"\"DESCRIPTION\"\"\"
        return self._get_attribute("ATTRIBUTE_NAME")

    @ATTRIBUTE_NAME.setter
    def ATTRIBUTE_NAME(self, value: ATTRIBUTE_TYPE):
        # Derived attribute
        pass
"""

    TYPE_MAP = {
        "DOUBLE": "float",
        "INT": "int",
        "STRING": "str",
        "LOGICAL": "bool",
        "BOOL": "bool",
        "BINARY": "bytes",
    }

    def __init__(self, attribute, parent, is_derived):
        self.parent = parent
        self.attribute = attribute
        self.is_derived = is_derived
        self.name = attribute.name()
        self.imports = set()
        self.type = None
        self.description = str(attribute)

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
            declared_type = type_of_element.declared_type()
            if isinstance(declared_type, str):
                # TODO: this duplicates the code
                TYPE_MAP = {
                    "integer": "int",
                    "logical": "bool",
                    "boolean": "bool",
                    "real": "float",
                    "binary": "bytes",
                }
                type_of_element_string = TYPE_MAP[declared_type]
            else:
                if type_of_element.declared_type().as_select_type():
                    type_of_element_string = self.get_select_type(type_of_element)
                elif type_of_element.declared_type().as_type_declaration():
                    type_of_element_string = self.get_type_declaration(type_of_element)
                else:
                    type_of_element_string = type_of_element.declared_type().name()
                    if type_of_element_string != self.parent.name:
                        self.imports.add(f"from .{type_of_element_string.lower()} import {type_of_element_string}")
                    type_of_element_string = f'"{type_of_element_string}"'
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
        class_names = set()
        for item in select_list:
            if item.as_type_declaration():
                class_names.add(self.get_type_declaration(item))
            else:
                class_names.add(f'"{item.name()}"')
                if item.name() != self.parent.name:
                    self.imports.add(f"from .{item.name().lower()} import {item.name()}")
        select_string = "Union[" + ", ".join(class_names) + "]"
        return select_string

    def get_type_declaration(self, attribute_type):
        if hasattr(attribute_type, "argument_types"):
            declared_type = attribute_type
        else:
            declared_type = attribute_type.declared_type()

        ifc_type = declared_type.argument_types()[0]
        if ifc_type.startswith("AGGREGATE OF"):
            value_type = ifc_type.split("OF ")[1]
            if value_type == "ENTITY INSTANCE":
                python_type = "list"  # TODO: handle this
            else:
                python_type = f"list[{self.TYPE_MAP[value_type]}]"
        else:
            python_type = self.TYPE_MAP[ifc_type]
        return python_type

    def get_attribute_type(self):
        attribute_type = self.attribute.type_of_attribute()
        if attribute_type.as_aggregation_type():
            self.type = self.get_aggregation_type(attribute_type)
        elif attribute_type.as_simple_type():
            attribute_type = attribute_type.declared_type()
            TYPE_MAP = {
                "integer": "int",
                "logical": "bool",
                "boolean": "bool",
                "real": "float",
                "string": "str",
            }
            self.type = TYPE_MAP[attribute_type]
        elif attribute_type.declared_type().as_select_type():
            self.type = self.get_select_type(attribute_type)
        elif attribute_type.declared_type().as_type_declaration():
            self.type = self.get_type_declaration(attribute_type)
        else:
            # Entity, Enumeration
            type_name = attribute_type.declared_type().name()
            if type_name != self.parent.name:
                self.imports.add(f"from .{type_name.lower()} import {type_name}")
            self.type = f'"{type_name}"'

    def generate(self):
        self.get_attribute_type()
        if self.is_derived:
            attribute_string = self.TEMPLATE_DERIVED.replace("ATTRIBUTE_NAME", self.name)
        else:
            attribute_string = self.TEMPLATE.replace("ATTRIBUTE_NAME", self.name)
        attribute_string = attribute_string.replace("ATTRIBUTE_TYPE", str(self.type))
        attribute_string = attribute_string.replace("DESCRIPTION", self.description)

        return attribute_string


class InverseAttributeGenerator(AttributeGenerator):
    """
    Generator class for generating a single IFC inverse attribute.

    Attributes
    ----------
    See :class:`AttributeGenerator`

    TEMPLATE : str
        The template python code for the inverse attribute to generate.

    """

    TEMPLATE = """
    def ATTRIBUTE_NAME(self)-> list[ATTRIBUTE_TYPE]:
        \"\"\"DESCRIPTION\"\"\"
        return self._get_inverse_attribute("ATTRIBUTE_NAME")
"""

    def __init__(self, attribute, parent):
        self.parent = parent
        self.attribute = attribute
        self.name = attribute.name()
        self.imports = set()
        self.type = None
        self.description = str(attribute)

    def get_attribute_type(self):
        # TODO: handle bound1, bound2 etc. for the aggregation
        entity_reference = self.attribute.entity_reference()
        self.type = entity_reference.name()
        self.imports.add(f"from .{self.type.lower()} import {self.type}")

    def generate(self):
        self.get_attribute_type()
        attribute_string = self.TEMPLATE.replace("ATTRIBUTE_NAME", self.name)
        attribute_string = attribute_string.replace("ATTRIBUTE_TYPE", f'"{self.type}"')
        attribute_string = attribute_string.replace("DESCRIPTION", self.description)

        return attribute_string


class TypeDeclarationGenerator:
    """
    Generator class for generating a single IFC type declaration.
    """

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
    """
    Generator class for generating a single IFC enumeration type.
    """

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
    generator = Generator(schema="IFC2X3")
    generator.generate()

    generator = Generator(schema="IFC4")
    generator.generate()
