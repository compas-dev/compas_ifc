"""
********************************************************************************
entities
********************************************************************************

.. currentmodule:: compas_ifc.entities

Classes representing rooted entities (entities inheriting from IfcRoot).
Three types of entities are of particular interest:

* IfcContext :: **IfcProject**
* IfcObject :: IfcProduct :: IfcElement :: **IfcSpatialElement**

  * IfcSite
  * IfcBuilding
  * IfcBuildingStorey
  * IfcSpace

* IfcObject :: IfcProduct :: IfcElement :: **IfcBuildingElement**

  * IfcBeam
  * IfcColumn
  * IfcDoor
  * IfcRoof
  * IfcSlab
  * IfcStair
  * IfcWall
  * IfcWindow


Associations
============

Classifications
---------------

See also :ifc:`classification`.

Objects like building and spatial elements can be further described by associating references to external sources of information.
The source of information can be:

* a classification system;
* a dictionary server;
* any external catalogue that classifies the object further;
* a service that combine the above features.

These "associations" are called "classifications".

.. code-block:: python

    for association in entity.HasAssociations:
        if association.is_a('IfcRelAssociatesClassification'):
            ...

Material Associations
---------------------

See also :ifc:`material-association`.

Material associations indicate the physical composition of an object.
Materials can have representations for surface styles indicating colors, textures, and light reflectance for 3D rendering.
Materials can have representations for fill styles indicating colors, tiles, and hatch patterns for 2D rendering.
Materials can have properties such as density, elasticity, thermal resistance, and others as defined in this specification.
Materials can also be classified according to a referenced industry standard.

.. code-block:: python

    for association in entity.HasAssociations:
        if association.is_a('IfcRelAssociatesMaterial'):
            ...

Object Composition
==================

Objects may be composed into parts to indicate levels of detail, such as a building having multiple storeys, a framed wall having studs, or a task having subtasks.
Composition may form a hierarchy of multiple levels, where an object must have single parent, or if a top-level object then declared within the single project or a project library.

Element Composition
-------------------

See also :ifc:`element-composition`.

Provision of an aggregation structure where the element is part of another element representing the composite.
The part then provides, if such concepts are in scope of the Model View Definition, exclusively the following:

* Body Geometry — The partial body shape representation and its placement;
* Material — The material information for the part.

The part may also provide, in addition to the aggregate, more specifically the following:

* Property Sets — The parts may have individual property sets assigned, solely or in addition to the composite;
* Quantity Sets — The parts may have individual quantity sets assigned, solely or in addition to the composite.

The part should not be contained in the spatial hierarchy, i.e. the concept Spatial Containment shall not be used at the level of parts.
The part is contained in the spatial structure by the spatial containment of its composite.

.. code-block:: python

    for element in entity.ContainsElements:
        # ...


Spatial Composition
-------------------

...

.. code-block:: python

    for element in entity.IsDecomposedBy:
        # ...


Classes
=======

Bases
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Entity

Context
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Project

Spatial Elements
----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Site
    Building
    BuildingStorey
    Space

Building Elements
-----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Beam
    Column
    Door
    Roof
    Slab
    Stair
    Wall
    Window

"""

from .entity import Entity
from .root import Root
from .objectdefinition import ObjectDefinition
from .element import Element
from .spatialelement import SpatialElement
from .buildingelements import Beam
from .buildingelements import Column
from .buildingelements import Door
from .buildingelements import Roof
from .buildingelements import Slab
from .buildingelements import Stair
from .buildingelements import Wall
from .buildingelements import Window
from .buildingelements import BuildingElementProxy

from .space import Space
from .buildingstorey import BuildingStorey
from .building import Building
from .site import Site
from .geographicelement import GeographicElement

from .project import Project

DEFAULT_ENTITY_TYPES = {
    "IfcRoot": Root,
    "IfcObjectDefinition": ObjectDefinition,
    "IfcElement": Element,
    "IfcSpatialElement": SpatialElement,
    "IfcBeam": Beam,
    "IfcColumn": Column,
    "IfcDoor": Door,
    "IfcRoof": Roof,
    "IfcSlab": Slab,
    "IfcStair": Stair,
    "IfcWall": Wall,
    "IfcWindow": Window,
    "IfcSpace": Space,
    "IfcBuildingStorey": BuildingStorey,
    "IfcBuilding": Building,
    "IfcSite": Site,
    "IfcProject": Project,
    "IfcBuildingElementProxy": BuildingElementProxy,
    "IfcGeographicElement": GeographicElement,
}


def factory(entity, model, entity_types=None) -> Entity:
    """Factory function for creating an compas_ifc entity object from an Ifc entity, the function finds closest matched class from the bottom of inherentance.

    Parameters
    ----------
    entity : IfcEntity
        An IfcEntity object.
    model : IfcModel
        An IfcModel object.

    Returns
    -------
    Entity
        An Entity object.

    """
    entity_types = entity_types or DEFAULT_ENTITY_TYPES

    declaration = model.schema.declaration_by_name(entity.is_a())
    inheritance = [declaration.name()]
    while hasattr(declaration, "supertype") and declaration.supertype():
        inheritance.append(declaration.supertype().name())
        declaration = declaration.supertype()

    for ifc_type in inheritance:
        if ifc_type in entity_types:
            return entity_types[ifc_type](entity, model)
    return Entity(entity, model)


Entity.factory = staticmethod(factory)
