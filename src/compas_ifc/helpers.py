"""
********************************************************************************
helpers
********************************************************************************

.. currentmodule:: compas_ifc.helpers

Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    public_attributes

"""

import ifcopenshell


def public_attributes(o):
    public = [name for name in dir(o) if not name.startswith("_")]
    return public


def print_schema_ref_tree(schema, declaration, indent=0, only_required=True):
    """Prints a tree view of the schema references."""

    if indent == 0:
        print(declaration)

    indent += 4

    if declaration.as_entity():
        for attribute in declaration.all_attributes():
            if only_required and attribute.optional():
                continue

            if attribute.type_of_attribute().as_named_type():
                print(" " * indent, attribute)
                print_schema_ref_tree(schema, attribute.type_of_attribute().declared_type(), indent)
            elif attribute.type_of_attribute().as_aggregation_type():
                print(" " * indent, attribute)
            else:
                raise NotImplementedError


def print_entity_ref_tree(entity, indent=0):
    """Prints a tree view of the entity references."""
    info = entity.get_info()
    print(" " * indent, "<", entity.id(), entity.is_a(), ">")
    for key, value in info.items():
        if key.lower() == "type" or key.lower() == "id":
            continue
        if isinstance(value, ifcopenshell.entity_instance):
            print(" " * indent, key, ":")
            print_entity_ref_tree(value, indent + 4)
        else:
            print(" " * indent, key, ":", value)
