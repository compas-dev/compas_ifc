*******************************************************************************
Basics.1 Project Overview
*******************************************************************************

This example shows how to load an IFC file and print a summary of the model.

.. code-block:: python

    from compas_ifc.model import Model

    model = Model("data/wall-with-opening-and-window.ifc")
    model.print_summary()


.. code-block:: none

    ================================================================================
    File: data/wall-with-opening-and-window.ifc
    Size: 0.01 MB
    Project: Default Project
    Description: Description of Default Project
    Number of sites: 1
    Number of buildings: 1
    Number of building elements: 2
    ================================================================================



.. code-block:: python

    from pprint import pprint
    from compas_ifc.model import Model

    model = Model("data/wall-with-opening-and-window.ifc")

    project = model.project

    # =============================================================================
    # Info
    # =============================================================================

    print("\n" + "*" * 53)
    print("Project")
    print("*" * 53 + "\n")

    project.print_inheritance()

    print("\nAttributes")
    print("=" * 53 + "\n")

    pprint(project.attributes)

    print("\nProperties")
    print("=" * 53 + "\n")

    pprint(project.properties)

    print("\nRepresentation Contexts")
    print("=" * 53 + "\n")

    pprint(project.contexts)

    print("\nUnits")
    print("=" * 53 + "\n")

    pprint(project.units)

    print("\nModel Context")
    print("=" * 53 + "\n")

    print(f"Reference Frame: {project.frame}")
    print(f"True North: {project.north}")

    print("\nSites")
    print("=" * 53 + "\n")

    print(project.sites)

    print()

Example Output:

.. code-block:: none

    *****************************************************
    Project
    *****************************************************

    - IfcRoot
    -- IfcObjectDefinition
    --- IfcContext
    ---- IfcProject

    Attributes
    =====================================================

    {'Description': 'Description of Default Project',
    'GlobalId': '28hypXUBvBefc20SI8kfA$',
    'LongName': None,
    'Name': 'Default Project',
    'ObjectType': None,
    'OwnerHistory': <Entity:IfcEntity>,
    'Phase': None,
    'RepresentationContexts': [<Entity:IfcEntity>],
    'UnitsInContext': <Entity:IfcEntity>}

    Properties
    =====================================================

    {}

    Representation Contexts
    =====================================================

    [{'dimension': 3,
    'identifier': None,
    'north': Vector(0.000, 1.000, 0.000),
    'precision': 1e-05,
    'type': 'Model',
    'wcs': Frame(Point(0.000, 0.000, 0.000), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))}]

    Units
    =====================================================

    [{'name': 'METRE', 'prefix': 'MILLI', 'type': 'LENGTHUNIT'},
    {'name': 'SQUARE_METRE', 'prefix': None, 'type': 'AREAUNIT'},
    {'name': 'CUBIC_METRE', 'prefix': None, 'type': 'VOLUMEUNIT'},
    {'name': 'STERADIAN', 'prefix': None, 'type': 'SOLIDANGLEUNIT'},
    {'name': 'GRAM', 'prefix': None, 'type': 'MASSUNIT'},
    {'name': 'SECOND', 'prefix': None, 'type': 'TIMEUNIT'},
    {'name': 'DEGREE_CELSIUS',
    'prefix': None,
    'type': 'THERMODYNAMICTEMPERATUREUNIT'},
    {'name': 'LUMEN', 'prefix': None, 'type': 'LUMINOUSINTENSITYUNIT'}]

    Model Context
    =====================================================

    Reference Frame: Frame(Point(0.000, 0.000, 0.000), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))
    True North: Vector(0.000, 1.000, 0.000)

    Sites
    =====================================================

    [<Site:IfcSite Name: Default Site, GlobalId: 1cwlDi_hLEvPsClAelBNnz>]