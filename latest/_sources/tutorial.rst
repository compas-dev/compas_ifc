********************************************************************************
Tutorial
********************************************************************************

This is a hello-world tutorial for the COMPAS IFC package. It shows how to load an IFC file and and inspect its contents.

.. code-block:: python

    import os
    from compas_ifc.model import Model

    HERE = os.path.dirname(__file__)
    FILE = os.path.join(
        HERE,
        "..",
        "data",
        "wall-with-opening-and-window.ifc",
    )

    # Load the IFC file into a model
    model = Model(FILE)

    # Print the schema of the model
    print(model.schema)

You should see following output:

.. code-block:: none

    Opened file: d:\Github\compas_ifc\scripts\..\data\wall-with-opening-and-window.ifc
    <schema IFC4>

With ``model.get_all_entities()`` function, you can get a list of all entities in the model.

.. code-block:: python

    all_entities = model.get_all_entities()

    print("Total number of entities: ", len(all_entities))
    for entity in all_entities[:5]:
        print(entity)
    print("...\n")


.. code-block:: none

    Total number of entities:  133
    <Entity:IfcAxis2Placement3D>
    <Entity:IfcCartesianPoint>
    <Entity:IfcCartesianPoint>
    <Entity:IfcCartesianPoint>
    <Entity:IfcCartesianPoint>
    ...

Use ``model.get_entities_by_type()`` function to get a list of entities of a specific type (including their inherent ones).

.. code-block:: python

    building_elements = model.get_entities_by_type("IfcBuildingElement")

    print("Total number of building elements: ", len(building_elements))
    for entity in building_elements:
        print(entity)

.. code-block:: none

    Total number of building elements:  2
    <Window:IfcWindow Name: Window for Test Example, GlobalId: 0tA4DSHd50le6Ov9Yu0I9X>
    <Wall:IfcWallStandardCase Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>


You can also use ``model.get_entities_by_name()`` function search elements with a specific name.

.. code-block:: python

    name = "Wall for Test Example"
    walls = model.get_entities_by_name(name)
    print("Found entities with the name: {}".format(name))
    print(walls)

.. code-block:: none

    Found entities with the name: Wall for Test Example
    [<Wall:IfcWall Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>]

You can access the attributes of an entity using the ``attributes`` property.

.. code-block:: python
    
    wall = walls[0]
    print(wall.attributes)


.. code-block:: none

    {'GlobalId': '3ZYW59sxj8lei475l7EhLU', 'OwnerHistory': <Entity:IfcOwnerHistory>, 'Name': 'Wall for Test Example', 'Description': 'Description of Wall', 'ObjectType': None, 'ObjectPlacement': <Entity:IfcLocalPlacement>, 'Representation': <Entity:IfcProductDefinitionShape>, 'Tag': None, 'PredefinedType': None}


You can also inspect the spatial hierarchy of the model. For example, you can get the parent of an entity using the ``parent`` property, or get the children of an entity using the ``children`` property.

.. code-block:: python
    
    print("parent:", wall.parent)
    print("children", wall.children)

.. code-block:: none

    parent: <BuildingStorey:IfcBuildingStorey Name: Default Building Storey, GlobalId: 2GNgSHJ5j9BRUjqT$7tE8w>
    children: []

For geomtric information, you can use the ``body`` property of an entity. This will extract the representation of the entity (if exists) as a ``compas_occ BRep``.

.. code-block:: python
    
    brep = wall.body[0]
    print(brep)
    print(brep.is_solid)
    print(brep.volume)

.. code-block:: none

    <compas_occ.brep.brep.BRep object at 0x000001F7480C97F0>
    True
    1.8

For more information, please head to the next *Examples* section.
