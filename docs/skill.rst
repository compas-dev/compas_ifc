********************************************************************************
Agent skill (Claude Code)
********************************************************************************

.. rst-class:: lead

A bundled skill that lets AI coding agents drive ``compas_ifc`` through
structured CLI commands rather than ad-hoc scripts.

The skill lives at ``src/compas_ifc/skill/`` inside the installed package
and is **version-coupled** to the library: the recipes the agent reads
always match the API the user actually has. There is no separate
download, no out-of-date marketplace copy, no version drift.

Today the skill targets `Claude Code <https://claude.com/product/claude-code>`_
specifically. A Codex target is planned; the ``install-skill`` command
already accepts ``--target codex`` and reports "not yet implemented" so
that scripts written today won't silently break later.


What the skill does
===================

Claude Code skills are short instruction sets, scoped to a topic, that
the agent loads on demand when a user request matches the skill's
description. The ``compas_ifc`` skill activates whenever a conversation
references an ``.ifc`` file, an IFC entity type (``IfcWall``,
``IfcBuildingStorey``, …), BIM data, or the library by name.

Once active, the skill:

* runs a one-time onboarding pass to detect the user's Python
  environment, probe for ``compas_ifc``, and persist the choice to
  ``state.json``,
* prefers the :doc:`CLI <cli>` for any task the CLI covers — file
  summaries, listings, queries, visualisations, exports — and parses
  ``--json`` output rather than scraping human-readable text,
* drops to Python (``BuildingInformationModel``) when the CLI doesn't
  cover the task, using ``docs`` and ``schema`` for API introspection
  first to avoid guessing,
* always invokes ``visualize`` and ``clash --show`` with ``--detach``,
  so the viewer doesn't block the conversation.


Install
=======

.. code-block:: bash

    python -m compas_ifc install-skill

This copies the bundled skill into ``~/.claude/skills/compas_ifc``. The
next Claude Code session in any directory will load it on demand.

Re-running the command without ``--force`` refuses to overwrite an
existing install, so a manually edited copy is never clobbered by
accident. To intentionally refresh after a library upgrade:

.. code-block:: bash

    python -m compas_ifc install-skill --force

To remove:

.. code-block:: bash

    python -m compas_ifc install-skill --uninstall

A future ``--target codex`` will install into the Codex equivalent.
``--target both`` will fan out to every supported target in one call.


What's inside
=============

Once installed, the skill folder contains three files:

============================== =============================================
File                           Role
============================== =============================================
``SKILL.md``                   The agent's entry point. Declares the skill
                               name and description (used for activation),
                               the onboarding flow, the command reference,
                               and the critical rules (``--detach`` always,
                               lazy ``compas_viewer``).
``references/cookbook.md``     Copy-pasteable recipes for the 80% of tasks:
                               file summary, listing, queries, visualisation,
                               clash, export, and the canonical Python
                               fallback when the CLI isn't enough.
``references/workflows.md``    Multi-step patterns — the "show me X on the
                               first floor, then export it" flow,
                               cross-referencing schema and library docs,
                               diffing two files.
``state.json`` (after first    User's choice of Python interpreter and
run)                           environment name. Re-probed on each run.
============================== =============================================

The skill never installs ``compas_ifc`` itself without asking. On first
use it detects whether the library is importable in the active
environment, and if not, asks the user how they want to install — into
the current env, into a fresh conda env, or via system pip.


Sample interactions
===================

A few examples of what the skill enables once it's installed:

* **"What's in this IFC file?"**
  The agent runs ``python -m compas_ifc summary <file> --json``, reads
  project name, site location, schema, units, and the spatial
  hierarchy, then summarises in prose.

* **"Show me all the windows on Level 1."**
  The agent runs ``list --type IfcBuildingStorey`` to find the storey's
  GlobalId, then ``visualize --type IfcWindow --in <id> --detach`` to
  open the viewer. It tells the user the viewer is open and keeps
  chatting.

* **"Find clashes between beams and walls and export the offenders."**
  The agent runs ``clash --type IfcBeam,IfcWall --json``, parses the
  pair list, collects the unique GlobalIds, and runs ``export-ifc
  --ids <gid1>,<gid2>,... --out clashes.ifc``. If asked to visualise,
  ``clash --show --detach`` with the same filter.

* **"What can an IfcDoor do?"**
  The agent runs ``schema IfcDoor`` for the EXPRESS attributes and
  ``docs IfcDoor --brief`` (plus ``--list`` for members) for the
  Python helpers added via ``@extends``.

In each case the agent goes through the CLI rather than spelunking the
library source. That keeps its behaviour predictable and its
explanations grounded in the actual installed version.


Building on the skill manually
==============================

The bundled skill is a starting point, not a fixed contract. The same
files can be edited in place at ``~/.claude/skills/compas_ifc/`` after
install — add project-specific recipes to ``references/``, change the
onboarding flow, or restrict commands the agent uses. Re-running
``install-skill --force`` will overwrite the customisations, so keep
significant edits in version control.

For brand-new skills outside the bundled one, the
`Claude Code skills documentation <https://docs.claude.com/en/docs/claude-code/skills>`_
covers the file format, activation rules, and progressive disclosure.
