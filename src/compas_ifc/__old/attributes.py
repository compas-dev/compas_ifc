"""
********************************************************************************
"attributes"
********************************************************************************

.. currentmodule:: compas_ifc.attributes

Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    is_attribute_aggregation
    is_attribute_enumeration
    attribute_enumeration_items
    declared_object_attributes
    declared_context_attributes
    declared_product_attributes
    declared_building_element_attributes
    declared_spatial_element_attributes

"""


def is_attribute_aggregation(attribute):
    """
    Verify that an attribute is an aggregation type.

    Parameters
    ----------
    attribute

    Returns
    -------
    bool

    """
    return attribute.type_of_attribute().as_aggregation_type()


def is_attribute_enumeration(attribute):
    """
    Verify that an attribute is an enumeration type.

    Parameters
    ----------
    attribute

    Returns
    -------
    bool

    """
    if attribute.type_of_attribute().as_named_type():
        return attribute.type_of_attribute().declared_type().as_enumeration_type()
    return False


def attribute_enumeration_items(attribute):
    """
    Get the value options of an enumeration type.

    Parameters
    ----------
    attribute

    Returns
    -------
    tuple

    """
    enumeration = attribute.type_of_attribute().declared_type().as_enumeration_type()
    return enumeration.enumeration_items()


def declared_object_attributes(schema):
    """
    Get all declared attributes of an IFC object.

    Parameters
    ----------
    schema

    Returns
    -------
    tuple

    """
    declaration = schema.declaration_by_name("IfcObject")
    return declaration.all_attributes()


def declared_context_attributes(schema):
    declaration = schema.declaration_by_name("IfcContext")
    return declaration.all_attributes()


def declared_product_attributes(schema):
    declaration = schema.declaration_by_name("IfcProduct")
    return declaration.all_attributes()


def declared_building_element_attributes(schema, exclude_product=True):
    declaration = schema.declaration_by_name("IfcBuildingElement")
    if not exclude_product:
        return declaration.all_attributes()

    attributes = []
    product = [attr.name() for attr in declared_product_attributes(schema)]
    for attribute in declaration.all_attributes():
        if attribute.name() not in product:
            attributes.append(attribute)
    return attributes


def declared_spatial_element_attributes(schema, exclude_product=True):
    declaration = schema.declaration_by_name("IfcSpatialElement")
    if not exclude_product:
        return declaration.all_attributes()

    attributes = []
    product = declared_product_attributes(schema)
    for attribute in declaration.all_attributes():
        if attribute not in product:
            attributes.append(attribute)
    return attributes
