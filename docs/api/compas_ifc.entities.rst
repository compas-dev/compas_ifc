*******************************************************************************
compas_ifc.entities
*******************************************************************************

Internal IFC entity wrappers. The user-facing API does not require touching
these directly — see :doc:`compas_ifc.bim` and :doc:`compas_ifc.element` —
but they are documented for contributors and for advanced workflows that
need raw IFC entity access through ``element._ifc_entity``.

Architecture
============

Every IFC entity loaded through ``compas_ifc`` is wrapped in a
:class:`~compas_ifc.entities.base.Base`. Direct attribute access proxies
through :meth:`~compas_ifc.entities.base.Base.__getattr__` to the
underlying ``ifcopenshell.entity_instance``. Inverse attributes are
exposed as zero-argument callables (``wall.ContainedInStructure()``) to
mark the syntactic distinction from direct attributes (``wall.Name``).

Type information for the IFC class hierarchy is provided through PEP 561
stubs at ``compas_ifc/entities/generated/{IFC2X3,IFC4,IFC4X3}.pyi``.
These stubs are consumed by IDEs and type checkers; there is no runtime
class per IFC type. Schema-class attributes added by hand-written
extensions are merged into the matching stub class so they appear in
autocomplete alongside the EXPRESS-defined attributes.

.. currentmodule:: compas_ifc.entities

Base
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    base.Base
    base.TypeDefinition
    base.extends

Extensions
==========

Hand-written extensions registered via the
:func:`~compas_ifc.entities.base.extends` decorator. Each adds
Python-friendly properties to entities of a particular IFC class.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    extensions.IfcObjectDefinitionExtras
    extensions.IfcObjectExtras
    extensions.IfcContextExtras
    extensions.IfcProjectExtras
    extensions.IfcProductExtras
    extensions.IfcElementExtras
    extensions.IfcSpatialContainerExtras
    extensions.IfcSiteExtras
    extensions.IfcBuildingExtras

Stub generator
==============

The stub generator under ``compas_ifc.entities.generator`` writes one
``.pyi`` file per supported schema. Run by maintainers when adding
support for a new IFC schema version; not typically invoked by users.

.. code-block:: bash

    python -m compas_ifc.entities.generator

.. autosummary::
    :toctree: generated/
    :nosignatures:

    generator.Generator
