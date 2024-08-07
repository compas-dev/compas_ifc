*******************************************************************************
Basics.2 Query Entities
*******************************************************************************

This example shows how to query entities from an IFC model.

.. code-block:: python

    from compas_ifc.model import Model

    model = Model("data/wall-with-opening-and-window.ifc")

    print("\n" + "*" * 53)
    print("Query Examples")
    print("*" * 53 + "\n")

    print("\nEntities by type")
    print("=" * 53 + "\n")

    all_entities = model.get_all_entities()
    spatial_elements = model.get_entities_by_type("IfcSpatialElement")
    building_elements = model.get_entities_by_type("IfcBuildingElement")

    print("Total number of entities: ", len(all_entities))
    for entity in all_entities[-5:]:
        print(entity)
    print("...\n")

    print("Total number of spatial elements: ", len(spatial_elements))
    for entity in spatial_elements[-5:]:
        print(entity)
    print("...\n")

    print("Total number of building elements: ", len(building_elements))
    for entity in building_elements[-5:]:
        print(entity)
    print("...\n")


    print("\nEntities by name")
    print("=" * 53 + "\n")

    name = "Window for Test Example"
    entities = model.get_entities_by_name(name)
    print("Found entities with the name: {}".format(name))
    print(entities)


    print("\nEntities by id")
    print("=" * 53 + "\n")

    global_id = "3ZYW59sxj8lei475l7EhLU"
    entity = model.get_entity_by_global_id(global_id)
    print("Found entity with the global id: {}".format(global_id))
    print(entity, "\n")

    id = 1
    entity = model.get_entity_by_id(id)
    print("Found entity with the id: {}".format(id))
    print(entity)


Example Output:

.. code-block:: none

    *****************************************************
    Query Examples
    *****************************************************


    Entities by type
    =====================================================

    Total number of entities:  133
    <Entity:IfcOrganization>
    <Entity:IfcPerson>
    <Entity:IfcPersonAndOrganization>
    <Entity:IfcOwnerHistory>
    <Project:IfcProject Name: Default Project, GlobalId: 28hypXUBvBefc20SI8kfA$>
    ...

    Total number of spatial elements:  3
    <BuildingStorey:IfcBuildingStorey Name: Default Building Storey, GlobalId: 2GNgSHJ5j9BRUjqT$7tE8w>
    <Building:IfcBuilding Name: Default Building, GlobalId: 0AqAhXVxvCy9m0OX1nxY1A>
    <Site:IfcSite Name: Default Site, GlobalId: 1cwlDi_hLEvPsClAelBNnz>
    ...

    Total number of building elements:  2
    <Window:IfcWindow Name: Window for Test Example, GlobalId: 0tA4DSHd50le6Ov9Yu0I9X>
    <Wall:IfcWallStandardCase Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>
    ...


    Entities by name
    =====================================================

    Found entities with the name: Window for Test Example
    [<ObjectDefinition:IfcWindowType Name: Window for Test Example, GlobalId: 0Ps4H3X0nAxfqkHNemLE6f>, <Window:IfcWindow Name: Window for Test Example, GlobalId: 0tA4DSHd50le6Ov9Yu0I9X>]

    Entities by id
    =====================================================

    Found entity with the global id: 3ZYW59sxj8lei475l7EhLU
    <Wall:IfcWall Name: Wall for Test Example, GlobalId: 3ZYW59sxj8lei475l7EhLU>

    Found entity with the id: 1
    <Project:IfcProject Name: Default Project, GlobalId: 28hypXUBvBefc20SI8kfA$>