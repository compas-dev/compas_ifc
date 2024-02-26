import ifcopenshell
from compas_ifc.entities import extensions
import inspect
import types
import os

schema_name = "IFC4"
schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema_name)

# TODO: maybe make attribute class??


def get_extension_methods(class_name):
    extension = getattr(extensions, class_name, None)
    if extension is None:
        return ""

    print("Extension methods:", extension)

    extension_methods_string = ""
    for method in dir(extension):
        method = getattr(extension, method)
        if type(method) is types.FunctionType:
            extension_methods_string += f"\n{inspect.getsource(method)}\n"

    return extension_methods_string


init_template = "from .CLASS_NAME import CLASS_NAME\n"

template = """from typing import Union, List

class CLASS_NAME(PARENT_NAME):
    \"\"\"Wrapper class for CLASS_NAME.\"\"\"
"""

attribute_template = """
    @property
    def ATTRIBUTE_NAME(self)-> ATTRIBUTE_TYPE:
        return self._get_attribute("ATTRIBUTE_NAME")

    @ATTRIBUTE_NAME.setter
    def ATTRIBUTE_NAME(self, value: ATTRIBUTE_TYPE):
        return self._set_attribute("ATTRIBUTE_NAME", value)
"""

def get_aggregation_type(attribute_type):
        # type_aggragation = attribute_type.type_of_aggregation()
        # bound1 = attribute_type.bound1()
        # bound2 = attribute_type.bound2()
        # TODO: add support for bounds etc.

        type_of_element = attribute_type.type_of_element()
        if type_of_element.as_aggregation_type():
            aggregation_string, type_of_element_string = get_aggregation_type(type_of_element)
            return f"List[{aggregation_string}]", type_of_element_string
        else:
            type_of_element_string = type_of_element.declared_type().name()
            return f"List[{type_of_element_string}]", type_of_element_string

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

if __name__ == "__main__":
    init_string = ""

    folder = f"src/compas_ifc/entities/generated/{schema_name}/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    for declaration in schema.declarations():
        class_string = template

        if declaration.as_entity():
            name = declaration.name()
            parent = declaration.supertype()
            if parent:
                parent = parent.name()
                class_string = f"from .{parent} import {parent}\n\n" + class_string
            else:
                parent = "Base"
                class_string = f"from compas_ifc.entities.base import Base\n\n" + class_string

            class_string = class_string.replace("CLASS_NAME", name)
            class_string = class_string.replace("PARENT_NAME", parent)

            for attribute in declaration.attributes():
                attribute_string = attribute_template
                attribute_string = attribute_string.replace("ATTRIBUTE_NAME", attribute.name())
                attribute_type = attribute.type_of_attribute()
                if attribute_type.as_aggregation_type():
                    
                    type_aggragation = attribute_type.type_of_aggregation()
                    bound1 = attribute_type.bound1()
                    bound2 = attribute_type.bound2()
                    type_of_element = attribute_type.type_of_element()
                    aggregation_string, type_of_element_string = get_aggregation_type(attribute_type)
                    attribute_string = attribute_string.replace("ATTRIBUTE_TYPE", aggregation_string)
                    class_string = init_template.replace("CLASS_NAME", type_of_element_string) + class_string
                elif attribute_type.as_simple_type():
                    attribute_type = attribute_type.declared_type()
                    TYPE_MAP = {
                        "integer": "int",
                        "logical": "bool",
                    }
                    attribute_string = attribute_string.replace("ATTRIBUTE_TYPE", TYPE_MAP[attribute_type])
                elif attribute_type.declared_type().as_select_type():
                    select_list = flaten_select_list(attribute_type.declared_type())
                    select_string = "Union["
                    for index, item in enumerate(select_list):
                        if index == 0:
                            select_string += f"\"{item.name()}\""
                        else:
                            select_string += f", \"{item.name()}\""
                        class_string = init_template.replace("CLASS_NAME", item.name()) + class_string
                    select_string += "]"
                    attribute_string = attribute_string.replace("ATTRIBUTE_TYPE", select_string)                
                else:
                    if attribute_type.declared_type().as_entity():
                        class_string = init_template.replace("CLASS_NAME", attribute_type.declared_type().name()) + class_string
                    elif attribute_type.declared_type().as_type_declaration():
                        class_string = init_template.replace("CLASS_NAME", attribute_type.declared_type().name()) + class_string
                    elif attribute_type.declared_type().as_enumeration_type():
                        class_string = init_template.replace("CLASS_NAME", attribute_type.declared_type().name()) + class_string
                    attribute_string = attribute_string.replace("ATTRIBUTE_TYPE", attribute_type.declared_type().name())
                
                init_string += f"from .{name} import {name}\n"

                # attribute_optional = attribute.optional()
                # attribute_string = attribute_string.replace("ATTRIBUTE_OPTIONAL", str(attribute_optional))
                class_string += attribute_string

            class_string += get_extension_methods(name)

            init_string += init_template.replace("CLASS_NAME", name)

            with open(f"src/compas_ifc/entities/generated/{schema_name}/{name}.py", "w") as f:
                f.write(class_string)

    with open(f"src/compas_ifc/entities/generated/{schema_name}/__init__.py", "w") as f:
        f.write(init_string)
