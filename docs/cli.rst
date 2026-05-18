********************************************************************************
Command-line interface
********************************************************************************

.. rst-class:: lead

A no-code surface for inspecting, querying, visualising, and exporting IFC
files — and the contract that AI coding agents use through the bundled
skill.

The CLI is invoked as ``python -m compas_ifc <command>``. Every command
accepts ``--json`` for structured output that downstream tools (or agents)
can parse without screen-scraping. The human-readable default is
intentionally compact so the same commands stay friendly at a terminal.

.. code-block:: bash

    python -m compas_ifc summary data/Duplex_A_20110907.ifc
    python -m compas_ifc list   data/Duplex_A_20110907.ifc --type IfcWindow --json

Two design rules run through every command:

* **Selection grammar is shared.** ``list``, ``query``, ``visualize``,
  ``export-ifc``, and ``export`` accept the same ``--type``, ``--where``,
  ``--in``, ``--ids`` filters, so a selection developed at the terminal
  carries unchanged into a visualisation or an export.
* **Geometry is opt-in.** Inspection commands open the file with
  ``load_geometries=False`` and ``rectify_placements=False``, which keeps
  startup under a second even on large files. Commands that need geometry
  (``visualize``, ``clash``, ``export``) enable it automatically.


Quick reference
===============

============================ ============================================================
Command                       Purpose
============================ ============================================================
``info``                      Schema, units, project, entity count, byte size.
``summary``                   ``info`` plus IfcSite location and spatial hierarchy.
``tree``                      Spatial hierarchy alone.
``list``                      Entities matching a selection.
``query``                     ``list`` plus inlined attributes via ``--select``.
``find``                      GlobalId exact / fuzzy name search.
``show``                      Attribute dump for one entity (recursive with ``--depth``).
``psets``                     Property sets for one entity.
``visualize``                 Open the spatial scene in ``compas_viewer``.
``clash``                     Detect volumetric interferences between elements.
``export-ifc``                Export a subset as a standalone IFC file.
``export``                    Export geometry as ``.obj`` or ``.json``.
``docs``                      Introspect ``compas_ifc`` symbols.
``schema``                    Introspect IFC classes from the bundled stubs.
``tutorials``                 List or print bundled tutorial scripts.
``install-skill``             Install the bundled agent skill.
============================ ============================================================


Output modes
============

The default rendering is a compact terminal layout — single-line entity
summaries, tree-style hierarchies, key/value blocks for entities. Adding
``--json`` switches to a stable structured shape:

.. code-block:: bash

    python -m compas_ifc list building.ifc --type IfcWindow --limit 2 --json

.. code-block:: json

    {
      "filter": {"type": "IfcWindow"},
      "count": 2,
      "entities": [
        {"global_id": "0u4w...", "type": "IfcWindow", "name": "Window:36in...", "id": 2841},
        {"global_id": "1Pj7...", "type": "IfcWindow", "name": "Window:24in...", "id": 2872}
      ]
    }

The JSON shape is the contract the bundled agent skill relies on; do not
rely on the human output for parsing.


Selection grammar
=================

The same four flags select entities across every command that operates on
a subset. They compose with AND:

============== =============================================================
Flag            Meaning
============== =============================================================
``--type``      IFC class name. Matches subclasses (``IfcWall`` returns
                ``IfcWallStandardCase`` too).
``--where``    A simple predicate ``<key> <op> <value>``. Operators:
                ``=``, ``!=``, ``>``, ``<``, ``>=``, ``<=``, ``~``
                (case-insensitive substring).
``--in``        GlobalId of a spatial container (storey, building, site).
                Restricts to its transitive contents.
``--ids``       Comma-separated GlobalIds. Overrides ``--type``.
============== =============================================================

``--where`` and ``--select`` accept dotted attribute paths
(``OwnerHistory.Owner.ThePerson.GivenName``), so values nested behind
``IfcOwnerHistory`` / ``IfcPersonAndOrganization`` etc. are reachable in
one step.

.. code-block:: bash

    # All windows on a specific storey, taller than 2 metres, projecting
    # height + width onto each row.
    python -m compas_ifc query building.ifc \
        --type IfcWindow \
        --in 0u4wQrR2X9aOPmZRSh8aBd \
        --where "OverallHeight>2" \
        --select OverallHeight,OverallWidth


Inspection
==========

``info``
--------

.. code-block:: bash

    python -m compas_ifc info building.ifc

Schema version, units, project metadata, total entity count, byte size.
Used as a fast "what is this file?" probe.

``summary``
-----------

.. code-block:: bash

    python -m compas_ifc summary building.ifc
    python -m compas_ifc summary building.ifc --depth 5

Same fields as ``info`` plus the IfcSite's geographic location (when
present) and the spatial hierarchy down to a configurable depth (default
3 stops at storey level). Best single command for getting oriented in
an unfamiliar file.

``tree``
--------

.. code-block:: bash

    python -m compas_ifc tree building.ifc --depth 4

The spatial hierarchy alone. ``--depth`` defaults to 10; raise it to walk
deeper into nested aggregates.


Search and listing
==================

``list``
--------

.. code-block:: bash

    python -m compas_ifc list building.ifc                          # everything
    python -m compas_ifc list building.ifc --type IfcWall
    python -m compas_ifc list building.ifc --type IfcWindow --in <storey_id>
    python -m compas_ifc list building.ifc --where "Name~partition"

``query``
---------

The structured-output sibling of ``list``. Accepts the same filters plus
``--select`` for inlining specific attribute values on each row:

.. code-block:: bash

    python -m compas_ifc query building.ifc \
        --type IfcWindow --where "OverallHeight>2" \
        --select OverallHeight,OverallWidth --json

``find``
--------

.. code-block:: bash

    python -m compas_ifc find building.ifc 3cUkl32yn9qRSPvBJZ3dB2   # exact GlobalId
    python -m compas_ifc find building.ifc "Casement"               # name substring
    python -m compas_ifc find building.ifc "Level 1"                # fuzzy ranking

GlobalId matches return immediately. Other patterns scan ``IfcRoot``
names case-insensitively, with a fuzzy-ratio tiebreaker for near misses.


Entity detail
=============

``show``
--------

.. code-block:: bash

    python -m compas_ifc show building.ifc <global_id>
    python -m compas_ifc show building.ifc <global_id> --depth 3

Dump one entity's attributes. ``--depth 1`` (default) renders nested
entity references as ``{"$ref": <id>, "type": <IfcClass>}`` stubs;
raising the depth inlines each referenced entity recursively, with cycle
breaking, so a single command can walk ``ObjectPlacement →
RelativePlacement → RelPlacement → ...`` without blowing up.

``psets``
---------

.. code-block:: bash

    python -m compas_ifc psets building.ifc <global_id> --json

Property sets attached to one entity, including type-inherited psets and
quantity sets.


Visualisation
=============

``visualize``
-------------

.. code-block:: bash

    python -m compas_ifc visualize building.ifc --detach
    python -m compas_ifc visualize building.ifc \
        --type IfcWindow --in <storey_id> --detach

Opens the spatial scene in ``compas_viewer``. The default mode preserves
spatial hierarchy so each selected element appears at its real world
position; pass ``--no-keep-hierarchy`` for a parts-library view at the
origin instead.

The ``--detach`` flag spawns the viewer in a background process and
returns immediately — essential when the CLI is being driven by an
agent or a script, since the viewer's event loop would otherwise block.

``compas_viewer`` is a lazy dependency. If it isn't installed, the
command exits with an install hint rather than a traceback.

``clash``
---------

.. code-block:: bash

    python -m compas_ifc clash building.ifc
    python -m compas_ifc clash building.ifc --type IfcBeam,IfcColumn,IfcWall
    python -m compas_ifc clash building.ifc --show --detach

Volumetric interference detection. Two-stage broadphase (BVH + tight
AABB) plus ray-cast narrowphase. By default skips spatially-related
pairs like ``wall → opening → window/door`` where overlap is expected
by construction; pass ``--include-related`` to keep them.

With ``--show``, ``compas_viewer`` opens with each clashing pair drawn
in a unique colour and penetration points marked. Combine with
``--detach`` so the viewer runs in the background.

Tunables: ``--tolerance`` (numerical), ``--min-depth`` (excludes
touching pairs), ``--limit`` (cap the text listing).


Export
======

``export-ifc``
--------------

.. code-block:: bash

    python -m compas_ifc export-ifc building.ifc \
        --type IfcWindow --out windows.ifc

    python -m compas_ifc export-ifc building.ifc \
        --type IfcWindow --out windows.ifc --flat

Writes the selected entities as a standalone, valid IFC file. The
default (``--preserve-hierarchy``) keeps each entity anchored under its
original ``IfcProject / IfcSite / IfcBuilding / IfcBuildingStorey``
ancestors. ``--flat`` instead builds a placeholder Project/Site/
Building/Storey in the output and anchors the selection under it.
Either mode preserves world positions.

``export-ifc`` refuses to export the whole file — pass at least one
selection flag.

``export``
----------

.. code-block:: bash

    python -m compas_ifc export building.ifc --type IfcWall --to walls.obj
    python -m compas_ifc export building.ifc --in <storey_id> --to level.json

Exports the geometry of the selected elements as a single mesh file
(``.obj`` or COMPAS ``.json``).


Library introspection
=====================

The next three commands are designed to keep agents (and people)
honest about the API surface: instead of guessing attribute names or
class hierarchies, ask the installed library directly.

``docs``
--------

.. code-block:: bash

    python -m compas_ifc docs BuildingInformationModel --brief
    python -m compas_ifc docs --list BuildingInformationModel --brief
    python -m compas_ifc docs get_element_by_global_id

A pydoc-style introspector for the installed ``compas_ifc``. ``--brief``
returns ``signature → return : first_docstring_line`` for quick scans;
``--list <parent>`` enumerates public members.

``schema``
----------

.. code-block:: bash

    python -m compas_ifc schema IfcWindow
    python -m compas_ifc schema IfcWindow --depth 3
    python -m compas_ifc schema IfcWall --schema IFC4X3

Pretty-prints an IFC class: supertype chain, attributes (annotated with
the ancestor they came from), and inverse attributes. The data comes
from the bundled PEP 561 stubs, so ``@extends``-added members
(``parent``, ``frame``, ``property_sets``) appear alongside the
EXPRESS-defined attributes. ``--depth`` recurses into each entity-typed
attribute's referenced class, with cycle breaking.

``tutorials``
-------------

.. code-block:: bash

    python -m compas_ifc tutorials list
    python -m compas_ifc tutorials show 0.1_overview

The ``scripts/tutorials/`` directory is shipped as package data. The
``list`` subcommand surfaces every tutorial with its one-line summary;
``show`` prints the source of a named tutorial so it can be pasted into
a new script or copied to disk.


Skill management
================

``install-skill``
-----------------

.. code-block:: bash

    python -m compas_ifc install-skill                          # claude
    python -m compas_ifc install-skill --target both --force
    python -m compas_ifc install-skill --uninstall

Copies the bundled agent skill (``src/compas_ifc/skill/``) into the
target agent's skill folder. The Claude Code target installs to
``~/.claude/skills/compas_ifc``. See :doc:`skill` for what the skill
contains and how it's used.


Working with the JSON contract
==============================

The JSON shape is intended to be stable enough to script against. Two
conventions help here:

* **Counts and filters echo the request.** Every command that selects
  entities returns a top-level ``count`` and a ``filter`` block
  reflecting which flags were applied. This makes it trivial to compare
  two runs or to confirm that a filter wasn't silently dropped.
* **Nested entities resolve as ``$ref`` stubs.** ``show`` and ``schema``
  use ``{"$ref": <id>, "type": <IfcClass>}`` for cross-references at
  the depth limit. Raise the depth to inline them, but expect the
  output size to grow super-linearly on heavily-referenced classes.

Errors are written to stderr with a non-zero exit code; the agent
skill reads stderr and surfaces the message verbatim. Where a command
needs a dependency that isn't installed (e.g. ``compas_viewer``), the
error message includes the install hint.
