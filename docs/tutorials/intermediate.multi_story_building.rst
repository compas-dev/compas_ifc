********************************************************************************
Intermediate - Multi-storey building
********************************************************************************

.. rst-class:: lead 

This tutorial shows how to paramtrically create a multi-storey building from scratch using COMPAS geometry types, as well adding custom properties to each relevant IFC entity.

Model Template
==============

Valid IFC files need to follow a regulated spatial hierarchy like this: 

``IfcProject`` -> ``IfcSite`` -> ``IfcBuilding`` -> ``IfcBuildingStorey`` -> ``IfcBuildingElement``.

COMPAS IFC provide a convenient way to create setup this hierarchy in a single function call.

::

    >>> from compas_ifc.model import Model
    >>> model = Model.template(building_count=1, storey_count=3, unit="m", schema="IFC4")
    IFC file created in schema: IFC4
    >>> model.print_spatial_hierarchy()
    ================================================================================
    Spatial hierarchy of <#1 IfcProject "Default Project">
    ================================================================================
    └── <#1 IfcProject "Default Project">
        └── <#17 IfcSite "Default Site">
            └── <#19 IfcBuilding "Default Building 1">
                ├── <#21 IfcBuildingStorey "Default Storey 1">
                ├── <#23 IfcBuildingStorey "Default Storey 2">
                └── <#25 IfcBuildingStorey "Default Storey 3">

The created entities can be easily updated:

::

    >>> model.project.Name = "My Custom Project Name"
    >>> model.sites[0].Name = "My Custom Site Name"
    >>> model.buildings[0].Name = "My Custom Building Name"
    >>> model.building_storeys[0].Name = "UnderGroundFloor"
    >>> model.building_storeys[1].Name = "GroundFloor"
    >>> model.building_storeys[2].Name = "FirstFloor"
    >>> model.print_spatial_hierarchy()
    ================================================================================
    Spatial hierarchy of <#1 IfcProject "My Custom Project Name">
    ================================================================================
    └── <#1 IfcProject "My Custom Project Name">
        └── <#17 IfcSite "My Custom Site Name">
            └── <#19 IfcBuilding "My Custom Building Name">
                ├── <#21 IfcBuildingStorey "UnderGroundFloor">
                ├── <#23 IfcBuildingStorey "GroundFloor">
                └── <#25 IfcBuildingStorey "FirstFloor">

Creating Entities
=================

``Model.create()`` can be used to create entities in the model.

::

    >>> model.create(IfcWall, Name="My Custom slab", parent=model.building_storeys[0])

