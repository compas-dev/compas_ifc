import ifcopenshell
from compas_ifc.entities import extensions
import inspect
import types

schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4")

init_template = "from .CLASS_NAME import CLASS_NAME\n"

template = """class CLASS_NAME(TYPE_NAME):
    \"\"\"Wrapper class for CLASS_NAME.\"\"\"
"""

TYPE_MAP = {
    "DOUBLE": "float",
    "INT": "int",
    "STRING": "str",
    "LOGICAL": "bool",
    "BOOL": "bool",
    "BINARY": "bytes",
}


if __name__ == "__main__":
    init_string = ""

    for declaration in schema.declarations():
        class_string = template

        if declaration.as_type_declaration():

            name = declaration.name()

            print(name)

            class_string = class_string.replace("CLASS_NAME", name)

            ifc_type = declaration.argument_types()[0]
            if ifc_type.startswith("AGGREGATE OF"):
                value_type = ifc_type.split("OF ")[1]
                if value_type == "ENTITY INSTANCE":
                    python_type = "list" # TODO: handle this
                else:
                    python_type = f"list[{TYPE_MAP[value_type]}]"
            else:
                python_type = TYPE_MAP[ifc_type]

            class_string = class_string.replace("TYPE_NAME", python_type)

            print(class_string)
            # break

            with open(f"src/compas_ifc/entities/generated/{name}.py", "w") as f:
                f.write(class_string)

    # with open(f"src/compas_ifc/entities/generated/__init__.py", "w") as f:
    #     f.write(init_string)


