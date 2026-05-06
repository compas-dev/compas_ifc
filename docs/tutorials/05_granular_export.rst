********************************************************************************
Granular export
********************************************************************************

For discipline-specific exchanges you often need to send only a portion
of a model — a single storey, the curtain-wall family, the structural
elements — but as a self-contained valid IFC file with the surrounding
spatial scaffolding intact.

Using ``model.extract``
=======================

.. code-block:: python

    from compas_ifc.bim import BuildingInformationModel

    model = BuildingInformationModel("data/Duplex_A_20110907.ifc")
    storey = next(s for s in model.storeys if s.name == "Level 2")

    # Returns a new self-contained BuildingInformationModel
    sub = model.extract(storey, path="level_2.ifc")

    print(len(list(sub.elements())), "elements in the extract")
    print(sub.storeys[0].name)              # "Level 2"
    print(sub.project is not None)          # IfcProject scaffolding present

What is preserved
=================

By default, ``extract`` carries over:

* the spatial scaffolding required for the file to validate
  (``IfcProject`` → ``IfcSite`` → ``IfcBuilding`` → ``IfcBuildingStorey``),
* element geometries, materials, property sets, and visual styles,
* type definitions (``IfcRelDefinesByType``),
* non-spatial relationships (connections, space boundaries, …) where
  *both* endpoints are inside the extracted set.

Each of these is opt-out via boolean flags on ``extract``.

Discipline-only subsets
=======================

You can pass any iterable of elements:

.. code-block:: python

    walls = model.get_elements_by_type("IfcWallStandardCase")
    sub = model.extract(walls, path="walls_only.ifc")

Hosted elements (openings, fillers) attached to the extracted walls are
included automatically.

Placement chain rectification
=============================

Extracted files inherit the placement-chain rectification performed on
import: each element's ``IfcLocalPlacement.PlacementRelTo`` points to its
spatial parent and the ``RelativePlacement`` holds the local frame, so
the file opens cleanly in any IFC viewer without "exploded" geometry.
