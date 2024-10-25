*******************************************************************************
Basics.3 Spatial Hierarchy
*******************************************************************************

This example shows how to traverse the spatial and inheritance hierarchy of an IFC model.

.. code-block:: python

    from compas_ifc.model import Model

    model = Model("data/wall-with-opening-and-window.ifc")

    project = model.project

    print("\n" + "*" * 53)
    print("Hierarchy")
    print("*" * 53 + "\n")


    print("\nModel spatial hierarchy")
    print("=" * 53 + "\n")

    model.print_spatial_hierarchy()


    print("\nClass inheritance hierarchy")
    print("=" * 53 + "\n")

    project = model.project
    project.print_inheritance()

    print("\nShortcut APIs")
    print("=" * 53 + "\n")

    print("Project contains:")
    print(model.sites)
    print(model.buildings)
    print(model.building_storeys)
    print(model.elements[:3])


    print("\nSite contains:")
    site = model.sites[0]
    print(site.buildings)
    print(site.geographic_elements)

    print("\nBuilding contains:")
    building = model.buildings[0]
    print(building.building_storeys)
    print(building.spaces)
    print(building.building_elements[:3])


    print("\nTraverse spatial hierarchy")
    print("=" * 53 + "\n")

    print(building)

    print("\nParent")
    print(building.parent)

    print("\nChildren")
    print(building.children)

    print("\nAncestors")
    for ancestor in building.traverse_ancestor():
        print(ancestor)

    print("\nDescendants")
    for descendant in building.traverse():
        print(descendant)

Example Output:

.. code-block:: none

    *****************************************************
    Hierarchy
    *****************************************************


    Model spatial hierarchy
    =====================================================

    <Project:IfcProject Name: Default Project, GlobalId: 28hypXUBvBefc20SI8kfA$>
    ---- <Site:IfcSite Name: Default Site, GlobalId: 1cwlDi_hLEvPsClAelBNnz>
    -------- <Building:IfcBuilding Name: Default Building, GlobalId: 0AqAhXVxvCy9m0OX1nxY1A>
    ------------ <BuildingStorey:IfcBuildingStorey Name: Default Building Storey, GlobalId: 2GNgSHJ5j9BRUjqT$7tE8w>
    ---------------- <Window:IfcWindow Name: Window for Test Example, GlobalId: 0tA4DSHd50le6Ov9Yu0I9X>
    ---------------- <Wall:IfcWallStandardCase Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>

    Class inheritance hierarchy
    =====================================================

    - IfcRoot
    -- IfcObjectDefinition
    --- IfcContext
    ---- IfcProject

    Shortcut APIs
    =====================================================

    Project contains:
    [<Site:IfcSite Name: Default Site, GlobalId: 1cwlDi_hLEvPsClAelBNnz>]
    [<Building:IfcBuilding Name: Default Building, GlobalId: 0AqAhXVxvCy9m0OX1nxY1A>]
    [<BuildingStorey:IfcBuildingStorey Name: Default Building Storey, GlobalId: 2GNgSHJ5j9BRUjqT$7tE8w>]
    [<Window:IfcWindow Name: Window for Test Example, GlobalId: 0tA4DSHd50le6Ov9Yu0I9X>, <Element:IfcOpeningElement Name: Opening Element for Test Example, GlobalId: 2bJiss68D6hvLKV8O1xmqJ>, <Wall:IfcWall Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>]

    Site contains:
    [<Building:IfcBuilding Name: Default Building, GlobalId: 0AqAhXVxvCy9m0OX1nxY1A>]
    []

    Building contains:
    [<BuildingStorey:IfcBuildingStorey Name: Default Building Storey, GlobalId: 2GNgSHJ5j9BRUjqT$7tE8w>]
    []
    [<Window:IfcWindow Name: Window for Test Example, GlobalId: 0tA4DSHd50le6Ov9Yu0I9X>, <Wall:IfcWall Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>]

    Traverse spatial hierarchy
    =====================================================

    <Building:IfcBuilding Name: Default Building, GlobalId: 0AqAhXVxvCy9m0OX1nxY1A>

    Parent
    <Site:IfcSite Name: Default Site, GlobalId: 1cwlDi_hLEvPsClAelBNnz>

    Children
    [<BuildingStorey:IfcBuildingStorey Name: Default Building Storey, GlobalId: 2GNgSHJ5j9BRUjqT$7tE8w>]

    Ancestors
    <Project:IfcProject Name: Default Project, GlobalId: 28hypXUBvBefc20SI8kfA$>
    <Site:IfcSite Name: Default Site, GlobalId: 1cwlDi_hLEvPsClAelBNnz>

    Descendants
    <BuildingStorey:IfcBuildingStorey Name: Default Building Storey, GlobalId: 2GNgSHJ5j9BRUjqT$7tE8w>
    <Window:IfcWindow Name: Window for Test Example, GlobalId: 0tA4DSHd50le6Ov9Yu0I9X>
    <Wall:IfcWall Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>