"""Extension for ``IfcSpatialStructureElement`` entities — children traversal.

In IFC2X3 ``IfcSpatialStructureElement`` is the parent of all spatial
containers; in IFC4+ it became a subclass of the new
``IfcSpatialElement``. This extension applies in both cases so the
``children`` API behaves uniformly across schemas.
"""

from typing import TYPE_CHECKING

from compas_ifc.entities.base import Base
from compas_ifc.entities.base import extends

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcSpatialStructureElement


@extends("IfcSpatialStructureElement")
class IfcSpatialStructureElementExtras(Base):
    """Extras applied to entities of class :class:`IfcSpatialStructureElement`."""

    @property
    def children(self: "IfcSpatialStructureElement"):
        children = super().children
        children += sum([relation.RelatedElements for relation in self.ContainsElements()], [])
        return list(set(children))
