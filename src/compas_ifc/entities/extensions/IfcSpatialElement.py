"""Extension for ``IfcSpatialElement`` entities — children traversal.

``IfcSpatialElement`` exists in IFC4 and IFC4X3 only; in IFC2X3 the
equivalent is ``IfcSpatialStructureElement`` (handled separately).
``entity.is_a("IfcSpatialElement")`` returns False for IFC2X3 entities,
so this extension is automatically scoped to IFC4+ schemas without an
explicit ``schemas=`` argument.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from compas_ifc.entities.base import Base
from compas_ifc.entities.base import extends

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcSpatialElement


@extends("IfcSpatialElement")
class IfcSpatialElementExtras(Base):
    """Extras applied to entities of class :class:`IfcSpatialElement`."""

    @property
    def children(self: "IfcSpatialElement"):
        children = super().children
        children += sum([relation.RelatedElements for relation in self.ContainsElements()], [])
        return list(set(children))
