import ifcopenshell
from compas_ifc.entities import extensions
import inspect
import types

schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4")

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

template = """from compas_ifc.entities.attribute import Attribute

class CLASS_NAME(PARENT_NAME):
    \"\"\"Wrapper class for CLASS_NAME.\"\"\"
"""

attribute_template = """
    @property
    def ATTRIBUTE_NAME(self)-> "ATTRIBUTE_TYPE":
        return self._get_attribute("ATTRIBUTE_NAME")

    @ATTRIBUTE_NAME.setter
    def ATTRIBUTE_NAME(self, value: "ATTRIBUTE_TYPE"):
        return self._set_attribute("ATTRIBUTE_NAME", value)
"""

if __name__ == "__main__":
    init_string = ""

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
                    attribute_type = "AGREGATION_TYPE"
                    # TODO: add aggregation type
                elif attribute_type.as_simple_type():
                    attribute_type = attribute_type.declared_type()
                else:
                    if attribute_type.declared_type().as_entity():
                        class_string = init_template.replace("CLASS_NAME", attribute_type.declared_type().name()) + class_string
                    attribute_type = attribute_type.declared_type().name()
                
                attribute_string = attribute_string.replace("ATTRIBUTE_TYPE", attribute_type)
                init_string += f"from .{name} import {name}\n"

                # attribute_optional = attribute.optional()
                # attribute_string = attribute_string.replace("ATTRIBUTE_OPTIONAL", str(attribute_optional))
                class_string += attribute_string

            class_string += get_extension_methods(name)

            init_string += init_template.replace("CLASS_NAME", name)

            with open(f"src/compas_ifc/entities/generated/{name}.py", "w") as f:
                f.write(class_string)

    with open(f"src/compas_ifc/entities/generated/__init__.py", "w") as f:
        f.write(init_string)
