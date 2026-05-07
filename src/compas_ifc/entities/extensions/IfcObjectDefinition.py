"""Extension for ``IfcObjectDefinition`` entities.

Adds spatial-hierarchy traversal helpers (``parent``, ``children``,
``descendants``, ``children_by_type``) and a ``material`` accessor.
Applied to every entity that ``is_a("IfcObjectDefinition")`` across all
IFC schemas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ifcopenshell.util.element import get_material

from compas_ifc.entities.base import Base
from compas_ifc.entities.base import extends

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcObjectDefinition


@extends("IfcObjectDefinition")
class IfcObjectDefinitionExtras(Base):
    """Extras applied to entities of class :class:`IfcObjectDefinition`."""

    def __repr__(self):
        return '<#{} {} "{}">'.format(self.entity.id(), self.entity.is_a(), self.Name)

    @property
    def parent(self: "IfcObjectDefinition"):
        relations = self.Decomposes()
        if relations:
            return relations[0].RelatingObject
        return None

    @property
    def children(self: "IfcObjectDefinition"):
        return sum([relation.RelatedObjects for relation in self.IsDecomposedBy()], [])

    @property
    def descendants(self):
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.descendants)
        return descendants

    @property
    def material(self):
        material = get_material(self.entity)
        if material:
            return self.file.from_entity(material)
        return None

    def children_by_type(self, type_name, recursive=False):
        if not recursive:
            return [child for child in self.children if child.is_a(type_name)]
        return [child for child in self.descendants if child.is_a(type_name)]
