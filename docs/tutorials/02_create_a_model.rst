********************************************************************************
Create a model from scratch
********************************************************************************

``BuildingInformationModel`` provides a ``template`` classmethod that
scaffolds a project with a default site, building, and storey:

.. code-block:: python

    from compas.geometry import Box, Frame, Point, Vector
    from compas_ifc.bim import BuildingInformationModel

    model = BuildingInformationModel.template(schema="IFC4", unit="m")
    storey = model.storeys[0]

    model.create_wall(
        name="South wall",
        parent=storey,
        geometry=Box(8.0, 0.2, 3.0),
        frame=Frame(Point(0, 0, 0), Vector.Xaxis(), Vector.Yaxis()),
    )

    model.save("from_scratch.ifc")

Typed creators
==============

Convenience methods exist for the common product subtypes —
``create_wall``, ``create_slab``, ``create_beam``, ``create_column``,
``create_window``, ``create_door``, ``create_roof``. Each forwards to
``create_element`` with the corresponding ``ifc_type`` set.

Generic and custom elements
===========================

For anything else, use ``create_element`` directly. The ``ifc_type``
argument accepts flexible input:

.. code-block:: python

    # all four are equivalent — they create an IfcWall
    model.create_element(ifc_type="IfcWall", parent=storey)
    model.create_element(ifc_type="Wall",    parent=storey)
    model.create_element(ifc_type="wall",    parent=storey)
    model.create_wall(parent=storey)

    # an unknown string falls back to IfcBuildingElementProxy with
    # ObjectType set to the original string
    bracket = model.create_element(ifc_type="CustomBracket", parent=storey)
    assert bracket.properties.get("ObjectType") == "CustomBracket"

This lets you introduce project-specific element types without modifying
the IFC schema; receivers see the proxy plus the descriptive
``ObjectType`` for downstream processing.

Saving and re-opening
=====================

.. code-block:: python

    model.save("project.ifc")

    # re-open later
    reloaded = BuildingInformationModel("project.ifc")
    assert len(reloaded.storeys) == len(model.storeys)
