********************************************************************************
Basics - Hello World
********************************************************************************

.. rst-class:: lead
This is a hello-world tutorial for the COMPAS IFC package. It shows how to load an IFC file and and inspect its contents.

Installation
================================


A minimal version of COMPAS IFC can be installed directly with pip.

.. code-block:: bash

    pip install compas_ifc

If you want to visualize the IFC model, install COMPAS Viewer as well.

.. code-block:: bash

    pip install compas_viewer

If you need to interact with IFC geometry using OCC Brep or CGAL for boolean operations, install COMPAS OCC and COMPAS CGAL througn conda-forge.

.. code-block:: bash

    conda install compas_occ compas_occ -c conda-forge


Load IFC model
================================

::

    >>> from compas_ifc.model import Model
    >>> model = Model("data/wall-with-opening-and-window.ifc")
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

For geomtric information, you can use the ``geometry`` property of an entity, if you have ``compas_occ`` installed, the geometry will be in form of ``Brep``.

::
    
    >>> geometry = wall.geometry
    >>> print(geometry)
    <compas_occ.brep.brep.BRep object at 0x000001F7480C97F0>
    >>> print(geometry.is_solid)
    True
    >>> print(geometry.volume)
    1.8




Visualisation
================================

If you have ``compas_viewer`` installed, you can visualize the model using the ``model.show()`` function.

::

    >>> model.show()

.. image:: _images/visualisation.jpg
    :width: 100%


More Examples
=============

Below are more examples of how to use the COMPAS IFC package.
(Please note these are still under construction)


.. toctree::
   :maxdepth: 1
   :titlesonly:
   :glob:

   tutorials/Basics.1_overview.rst
   tutorials/Basics.2_query_entities.rst
   tutorials/Basics.3_spatial_hierarchy.rst
   tutorials/Basics.4_element_info.rst
   tutorials/Basics.5_visualization.rst
   tutorials/Basics.6_edit_export.rst
   tutorials/Basics.7_create_new.rst
   tutorials/Advanced.1_units.rst
   tutorials/Advanced.2_sessions.rst
   tutorials/Advanced.3_custom_extensions.rst
