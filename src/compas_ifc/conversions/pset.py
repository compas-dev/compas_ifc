from ifcopenshell.util.element import get_psets

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


def from_psets_to_dict(element: Base) -> dict:
    psets = get_psets(element.entity, psets_only=True)

    def _convert_property(property):
        if isinstance(property, dict):
            if property.get("UsageName", None) == "[]":
                return [_convert_property(value) for value in property["properties"].values()]
            elif property.get("UsageName", None) == "{}":
                return {key: _convert_property(value) for key, value in property["properties"].items()}
            else:
                if "id" in property:
                    del property["id"]
                return {key: _convert_property(value) for key, value in property.items()}
        else:
            return property

    return _convert_property(psets)
