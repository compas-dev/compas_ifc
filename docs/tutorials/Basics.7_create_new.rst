*******************************************************************************
Basics.7 Create New IFC Model
*******************************************************************************

This example shows how to create a new IFC model from scratch.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Sphere
    from compas.geometry import Frame
    from compas_ifc.model import Model


    model = Model.template(storey_count=1)

    # Default unit is mm
    box = Box.from_width_height_depth(5000, 5000, 50)
    sphere = Sphere(2000)
    mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
    mesh.scale(1000)

    storey = model.building_storeys[0]

    element1 = model.create("IfcWall", geometry=box, frame=Frame([0, 0, 0]), Name="Wall", parent=storey)
    element3 = model.create("IfcRoof", geometry=mesh, frame=Frame([0, 0, 5000]), Name="Roof", parent=storey)
    element2 = model.create(geometry=sphere, frame=Frame([0, 5000, 0]), Name="Sphere", parent=storey)

    model.show()
    model.save("temp/create_geometry.ifc")
