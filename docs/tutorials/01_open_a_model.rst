********************************************************************************
Open a model
********************************************************************************

The :class:`~compas_ifc.bim.BuildingInformationModel` class is the entry
point. Pass it the path to an IFC file:

.. code-block:: python

    from compas_ifc.bim import BuildingInformationModel

    model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

The schema version (IFC2X3, IFC4, or IFC4X3) is detected automatically.

Browsing the spatial hierarchy
==============================

The model owns an explicit spatial tree (``model.tree``). Sites, buildings,
and storeys are exposed as direct properties; every element provides
``parent`` and ``children`` pointers:

.. code-block:: python

    for site in model.sites:
        for building in site.children:
            for storey in building.children:
                print(f"{storey.name}: {len(list(storey.children))} children")

You can also pretty-print the entire hierarchy:

.. code-block:: python

    model.print_hierarchy(max_depth=3)

Querying elements
=================

.. code-block:: python

    walls = model.get_elements_by_type("IfcWall")            # by IFC type
    by_name = model.get_elements_by_name("Basic Wall:Generic - 200mm")
    by_id = model.get_element_by_global_id("3cUkl32yn9qRSPvBJZ3dB2")

``get_elements_by_type`` matches subclasses too — querying
``"IfcProduct"`` returns walls, slabs, beams, doors, and any other
``IfcProduct`` descendant.

Reading geometry
================

Each element owns a parametric geometry plus a transformation:

.. code-block:: python

    wall = walls[0]
    print(wall.geometry.type)        # e.g. "Extrusion"
    print(wall.volume)               # m³
    print(wall.surface_area)         # m²
    print(wall.transformation)       # 4×4 placement

The geometry is computed lazily on first access. ``volume`` and
``surface_area`` route to the appropriate kernel (COMPAS core or
OpenCascade) depending on representation type.

Visualising the model
=====================

Optional dependency: ``compas_viewer``.

.. code-block:: python

    model.show()

You can also visualise a subtree by passing one or more elements:

.. code-block:: python

    model.show(model.storeys[0])
