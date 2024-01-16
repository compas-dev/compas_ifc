import ifcopenshell

schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4")


template = """from enum import Enum

class CLASS_NAME(Enum):
    \"\"\"Wrapper class for CLASS_NAME.\"\"\"
"""

enum_template = "    NAME=INDEX\n"

if __name__ == "__main__":
    init_string = ""

    for declaration in schema.declarations():
        class_string = template

        if declaration.as_enumeration_type():

            name = declaration.name()
            class_string = class_string.replace("CLASS_NAME", name)

            for index, item in enumerate(declaration.enumeration_items()):
                enum_string = enum_template
                enum_string = enum_string.replace("NAME", item)
                enum_string = enum_string.replace("INDEX", str(index))
                class_string += enum_string

            print(class_string)
            # break

            with open(f"src/compas_ifc/entities/generated/{name}.py", "w") as f:
                f.write(class_string)

