*******************************************************************************
Basics.6 Edit and Export
*******************************************************************************

This example shows how to edit attributes of an entity, save to a new file or export the selected entities.

.. code-block:: python

    from compas_ifc.model import Model

    model = Model("data/wall-with-opening-and-window.ifc")


    print("\n" + "*" * 53)
    print("Export Examples")
    print("*" * 53 + "\n")


    print("\nChange Project Name and Description")
    print("=" * 53 + "\n")

    model.project["Name"] = "New Project Name"
    model.project["Description"] = "New Project Description"
    model.save("temp/change_project_name.ifc")

    print("\nExport selected entities")
    print("=" * 53 + "\n")

    window = model.get_entities_by_type("IfcWindow")[0]
    model.export([window], "temp/selected_entities.ifc")
