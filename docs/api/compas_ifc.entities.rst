*******************************************************************************
compas_ifc.entities
*******************************************************************************

Internal IFC entity wrappers. The user-facing API does not require touching
these directly — see :doc:`compas_ifc.bim` and :doc:`compas_ifc.element` —
but they are documented for contributors and for advanced workflows that
need raw IFC entity access through ``element._ifc_entity``.

.. currentmodule:: compas_ifc.entities

Base
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    base.Base
    base.TypeDefinition

Extensions
==========

Hand-written extensions that add Python-friendly properties to the most
frequently used IFC types.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    extensions.IfcObjectDefinition
    extensions.IfcObject
    extensions.IfcContext
    extensions.IfcProject
    extensions.IfcProduct
    extensions.IfcElement
    extensions.IfcSpatialElement
    extensions.IfcSpatialStructureElement
    extensions.IfcSite
    extensions.IfcBuilding

Generators
==========

Code-generation utilities that build the per-schema entity wrappers under
``compas_ifc.entities.generated``. Run by maintainers when adding support
for a new IFC schema version; not typically invoked by users.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    generator.Generator
    generator.EntityGenerator
    generator.AttributeGenerator
    generator.InverseAttributeGenerator
    generator.TypeDeclarationGenerator
    generator.EnumGenerator
