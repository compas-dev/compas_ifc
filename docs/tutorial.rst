********************************************************************************
Tutorial
********************************************************************************

This is a hello-world tutorial for the COMPAS IFC package. It shows how to load an IFC file and and inspect its contents.

Load IFC model
================================

::

    >>> import os
    >>> from compas_ifc.model import Model
    >>> model = Model("wall-with-opening-and-window.ifc")
    Opened file: d:\Github\compas_ifc\scripts\..\data\wall-with-opening-and-window.ifc
    >>> print(model.schema)
    <schema IFC4>

Query entities
================================

With ``model.get_all_entities()`` function, you can get a list of all entities in the model.

::

    >>> all_entities = model.get_all_entities()
    >>> print("Total number of entities: ", len(all_entities))
    Total number of entities:  133
    >>> for entity in all_entities[:5]:
    >>>     print(entity)
    <Entity:IfcAxis2Placement3D>
    <Entity:IfcCartesianPoint>
    <Entity:IfcCartesianPoint>
    <Entity:IfcCartesianPoint>
    <Entity:IfcCartesianPoint>

Use ``model.get_entities_by_type()`` function to get a list of entities of a specific type (including their inherent ones).

::

    >>> building_elements = model.get_entities_by_type("IfcBuildingElement")
    >>> print("Total number of building elements: ", len(building_elements))
    Total number of building elements:  2
    >>> for entity in building_elements:
    >>>     print(entity)
    <Window:IfcWindow Name: Window for Test Example, GlobalId: 0tA4DSHd50le6Ov9Yu0I9X>
    <Wall:IfcWallStandardCase Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>

You can also use ``model.get_entities_by_name()`` function search elements with a specific name.

::

    >>> name = "Wall for Test Example"
    >>> walls = model.get_entities_by_name(name)
    >>> print("Found {} entities with the name: {}".format(len(walls), name))
    Found 1 entities with the name: Wall for Test Example
    >>> print(walls)
    [<Wall:IfcWall Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>]

Entity attributes
================================

You can access the attributes of an entity using the ``attributes`` property.

::

    >>> wall = walls[0]
    >>> print(wall.attributes)
    {'GlobalId': '3ZYW59sxj8lei475l7EhLU', 'OwnerHistory': <Entity:IfcOwnerHistory>, 'Name': 'Wall for Test Example', 'Description': 'Description of Wall', 'ObjectType': None, 'ObjectPlacement': <Entity:IfcLocalPlacement>, 'Representation': <Entity:IfcProductDefinitionShape>, 'Tag': None, 'PredefinedType': None}

You can also inspect the spatial hierarchy of the model. For example, you can get the parent of an entity using the ``parent`` property, or get the children of an entity using the ``children`` property.

::
    
    >>> print("parent:", wall.parent)
    parent: <BuildingStorey:IfcBuildingStorey Name: Default Building Storey, GlobalId: 2GNgSHJ5j9BRUjqT$7tE8w>
    >>> print("children", wall.children)
    children: []

For geomtric information, you can use the ``body`` property of an entity. This will extract the representation of the entity (if exists) as a ``compas_occ BRep``.

::
    
    >>> brep = wall.body[0]
    >>> print(brep)
    <compas_occ.brep.brep.BRep object at 0x000001F7480C97F0>
    >>> print(brep.is_solid)
    True
    >>> print(brep.volume)
    1.8

For more in-depth tutorials, please head to the next *Examples* section.
