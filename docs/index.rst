********************************************************************************
COMPAS IFC
********************************************************************************

.. rst-class:: lead

A front-end data model for the
`Industry Foundation Classes (IFC) <https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/>`_,
the open exchange format for Building Information Modelling.

.. image:: _images/compas_ifc.png
    :width: 100%


Why
===

The IFC schema accommodates virtually any building concept, but its breadth
makes it costly to work with: a small piece of geometry must navigate dozens
of class hierarchies and reach across several relationship entities.
COMPAS IFC presents one container class
(:class:`~compas_ifc.bim.BuildingInformationModel`) and one element class
(:class:`~compas_ifc.element.GenericElement`) on top of that schema, plus an
explicit spatial tree, an interaction graph, an integrated geometry kernel,
and a Pydantic-based validation engine. The resulting front-end exposes
fewer than fifty user-facing members for the operations a typical workflow
needs.


How it differs
==============

* **Integrated geometry kernel.** Geometric definitions are not just stored;
  they are *computed*. Volumes, surface areas, bounding boxes, and contact
  detection work uniformly across primitives, swept solids, B-Reps, and
  meshes — backed by COMPAS core, OpenCascade, and CGAL.

* **Explicit spatial hierarchy.** Containment is materialised as a tree with
  direct ``parent`` / ``children`` pointers. Placement chains that diverge
  from the spatial hierarchy on import are rectified automatically while
  preserving global positions.

* **Unified element strategy.** Every IFC product subclass is represented
  by the same Python class, distinguished by an ``ifc_type`` string.
  Custom strings without a matching IFC class fall back gracefully to
  ``IfcBuildingElementProxy``.

* **Structured customisation.** Custom property requirements are declared
  as `Pydantic <https://docs.pydantic.dev/>`_ schemas, enforced at
  insertion time, and exportable to JSON Schema for downstream tooling.

* **Lossless round-trip.** IFC2X3, IFC4, and IFC4X3 files survive a
  load → modify → save cycle without representational degradation.

* **Three coherent surfaces.** The same data model is reachable from
  Python, from a :doc:`command-line interface <cli>` with stable
  ``--json`` output, and through an :doc:`agent skill <skill>` that
  ships with the package — so AI coding agents drive the library
  through real commands rather than synthesising scripts.


Quick start — Python
====================

.. code-block:: python

   from compas_ifc.bim import BuildingInformationModel

   model = BuildingInformationModel("data/Duplex_A_20110907.ifc")
   for storey in model.storeys:
       print(storey.name, "->", len(list(storey.children)), "children")

   walls = model.get_elements_by_type("IfcWall")
   print(sum(w.volume or 0 for w in walls), "m³ of wall volume")

   model.save("modified.ifc")

See :doc:`tutorials` and :doc:`examples` for more.


Quick start — command line
==========================

Every command takes ``--json`` for parseable output; without it, the
default is a compact terminal rendering.

.. code-block:: bash

   python -m compas_ifc summary data/Duplex_A_20110907.ifc
   python -m compas_ifc list    data/Duplex_A_20110907.ifc --type IfcWindow
   python -m compas_ifc visualize data/Duplex_A_20110907.ifc \
       --type IfcWindow --detach

See :doc:`cli` for the full command reference.


Quick start — Claude Code skill
===============================

Install the bundled agent skill once, then any Claude Code session can
drive ``compas_ifc`` on your behalf:

.. code-block:: bash

   python -m compas_ifc install-skill

The skill ships inside the package, so the recipes Claude follows are
always aligned with the library version you actually have installed.
See :doc:`skill` for what the skill contains.


Standing on giants' shoulders
=============================

COMPAS IFC builds on:

* `COMPAS framework <https://compas.dev/>`_ — geometry, data structures,
  and visualisation.
* `IfcOpenShell <https://ifcopenshell.org/>`_ — schema-aware low-level IFC
  parsing and writing.
* `compas_occ <https://github.com/compas-dev/compas_occ>`_ — OpenCascade
  bindings for B-Rep and NURBS.
* `compas_cgal <https://github.com/compas-dev/compas_cgal>`_ — CGAL
  bindings for boolean operations and predicates.
* `Pydantic <https://docs.pydantic.dev/>`_ — declarative schema validation.


Provenance
==========

COMPAS IFC is the open-source artefact described in chapter 4 of *Future
Data Models for AEC: From Simplicity for Humans to Interoperability by AI*
(Li Chen, ETH Zürich, 2026). The reproducible evaluation suite that backs
the chapter's claims lives in ``thesis/appendix/A/`` of the source
repository.

For questions or contributions please open an issue on
`GitHub <https://github.com/compas-dev/compas_ifc/issues>`_ or contact
li.chen@arch.ethz.ch.


Table of contents
=================

.. toctree::
   :maxdepth: 2
   :titlesonly:

   Introduction <self>
   Architecture <architecture>
   Installation <installation>
   Command line <cli>
   Agent skill <skill>
   Tutorials <tutorials>
   Examples <examples>
   API <api>
   license
