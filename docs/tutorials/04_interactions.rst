********************************************************************************
Work with interactions
********************************************************************************

Spatial containment is captured by ``model.tree``. Everything else —
structural connections, MEP system flows, material associations, geometric
dependencies — lives in ``model.graph``, the *interaction graph*.

Importing existing relationships
================================

When an IFC file is loaded, the front-end automatically translates
``IfcRel...`` instances into typed graph edges. Edge categories are
grouped into three families:

============== =====================================================
Group           Categories
============== =====================================================
``topology``    ``connection``, ``space_boundary``, ``covering``,
                ``interference``, ``projection``
``structural``  ``structural``
``mep``         ``port_connection``, ``port_element``,
                ``flow_control``, ``services``,
                ``spatial_reference``
============== =====================================================

Querying interactions
=====================

.. code-block:: python

    from compas_ifc.bim import BuildingInformationModel

    model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

    # by category
    connections = model.connections
    boundaries = model.space_boundaries
    interferences = model.interferences

    # by group
    structural = model.get_interactions_by_group("structural")
    mep = model.get_interactions_by_group("mep")

    # custom category
    coverings = model.get_interactions_by_category("covering")

Each result is a list of graph edges; the underlying ``GenericElement``
objects are recovered via the graph's ``node_element`` accessor.

Computing connections from geometry
===================================

When the source IFC file does not declare the connections you need, the
front-end can detect them from the geometry. ``compute_connections``
runs a vectorised broadphase (BVH + tight AABB filter) followed by
face-level contact detection:

.. code-block:: python

    n = model.compute_connections(
        element_types=["IfcWall", "IfcWallStandardCase"],
        tolerance=1e-3,
        minimum_area=1e-2,
    )
    print(f"{n} new connection edges")

Computed contacts are added to the same interaction graph (with
``source="computed"``) and, by default, persisted as
``IfcRelConnectsElements`` instances in the underlying IFC file so they
survive a save/reload.

Detecting clashes
=================

``compute_collisions`` performs ray-cast point-in-mesh detection for
volumetric overlap. Penetrating points are stored on graph edges in the
``interference`` category:

.. code-block:: python

    n = model.compute_collisions(element_types=["IfcWall", "IfcSlab"])
    print(f"{n} collisions")

    model.show_collisions()  # interactive viewer
