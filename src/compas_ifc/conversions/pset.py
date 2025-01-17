from compas_ifc.entities.base import Base
from compas_ifc.model import Model

PRIMARY_MEASURE_TYPES = {
    str: "IfcLabel",
    float: "IfcReal",
    bool: "IfcBoolean",
    int: "IfcInteger",
}


def from_dict_to_ifc_properties(model: Model, properties: dict) -> list[Base]:
    """Convert a dictionary to a list of IfcProperties"""

    ifc_properties = []

    for key, value in properties.items():
        if isinstance(value, dict):
            subproperties = from_dict_to_ifc_properties(model, value)
            ifc_property = model.create("IfcComplexProperty", Name=key, UsageName="{}", HasProperties=subproperties)
            ifc_properties.append(ifc_property)

        elif isinstance(value, list):
            subproperties = from_dict_to_ifc_properties(model, {str(k): v for k, v in enumerate(value)})
            ifc_property = model.create("IfcComplexProperty", Name=key, UsageName="[]", HasProperties=subproperties)
            ifc_properties.append(ifc_property)

        elif isinstance(value, (str, float, bool, int)):
            nominal_value = model.create_value(value)
            ifc_property = model.create("IfcPropertySingleValue", Name=key, NominalValue=nominal_value)
            ifc_properties.append(ifc_property)
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return ifc_properties


def from_dict_to_pset(model: Model, properties: dict, name: str = None) -> Base:

    ifc_properties = from_dict_to_ifc_properties(model, properties)
    pset = model.create("IfcPropertySet", Name=name, HasProperties=ifc_properties)
    return pset
