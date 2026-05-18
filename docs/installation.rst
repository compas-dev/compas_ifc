Installation
================================

A minimal version of COMPAS IFC can be installed directly with pip.

.. code-block:: bash

    pip install compas_ifc

If you want to use the built-in viewer, install COMPAS Viewer as well.

.. code-block:: bash

    pip install compas_viewer

If you need to interact with IFC geometry using OCC Brep, install COMPAS
OCC through conda-forge.

.. code-block:: bash

    conda install compas_occ -c conda-forge


Install the Claude Code agent skill
-----------------------------------

The package ships with a Claude Code skill so AI coding agents can drive
``compas_ifc`` through its :doc:`command-line interface <cli>`. Install
it with:

.. code-block:: bash

    python -m compas_ifc install-skill

The skill is copied into ``~/.claude/skills/compas_ifc`` and will be
picked up by any subsequent Claude Code session. To remove it, pass
``--uninstall``. See :doc:`skill` for what's inside.

Next steps
----------

Three reasonable starting points depending on how you intend to use the
library:

* :doc:`tutorials/01_open_a_model` — Python API tour, from opening a file
  to visualisation.
* :doc:`cli` — full command-line reference for terminal users and
  scripting.
* :doc:`skill` — what the bundled agent skill does and how it activates.
