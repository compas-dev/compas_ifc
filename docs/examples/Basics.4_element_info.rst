*******************************************************************************
Basics.4 Element info
*******************************************************************************

This example shows how to get information of a building element, such as a window.

.. code-block:: python

    from pprint import pprint
    from compas_ifc.model import Model

    model = Model("data/wall-with-opening-and-window.ifc")

    assert len(model.projects) > 0

    project = model.projects[0]
    assert len(project.sites) > 0

    site = project.sites[0]
    assert len(site.buildings) > 0

    building = site.buildings[0]
    assert len(building.building_storeys) > 0

    storey = building.building_storeys[0]
    assert len(storey.windows) > 0

    window = storey.windows[0]

    # =============================================================================
    # Info
    # =============================================================================

    print("\n" + "*" * 53)
    print("Window")
    print("*" * 53 + "\n")

    window.print_inheritance()

    print("\nAttributes")
    print("=" * 53 + "\n")

    pprint(window.attributes)

    print("\nProperties")
    print("=" * 53 + "\n")

    pprint(window.property_sets)


Example Output:

.. code-block:: none

    *****************************************************
    Window
    *****************************************************

    - IfcRoot
    -- IfcObjectDefinition
    --- IfcObject
    ---- IfcProduct
    ----- IfcElement
    ------ IfcBuildingElement
    ------- IfcWindow

    Attributes
    =====================================================

    {'Description': 'Description of Window',
    'GlobalId': '0tA4DSHd50le6Ov9Yu0I9X',
    'Name': 'Window for Test Example',
    'ObjectPlacement': <Entity:IfcEntity>,
    'ObjectType': None,
    'OverallHeight': 1000.0,
    'OverallWidth': 1000.0,
    'OwnerHistory': <Entity:IfcEntity>,
    'PartitioningType': 'SINGLE_PANEL',
    'PredefinedType': 'WINDOW',
    'Representation': <Entity:IfcEntity>,
    'Tag': None,
    'UserDefinedPartitioningType': None}

    Properties
    =====================================================

    {'AcousticRating': '',
    'FireRating': '',
    'GlazingAreaFraction': 0.7,
    'Infiltration': 0.3,
    'IsExternal': True,
    'Reference': '',
    'SecurityRating': '',
    'SmokeStop': False,
    'ThermalTransmittance': 0.24,
    'id': 113}