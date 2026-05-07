"""Extension for ``IfcElement`` entities — spatial-parent resolution."""

from typing import TYPE_CHECKING

from compas_ifc.entities.base import Base
from compas_ifc.entities.base import extends

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcElement


@extends("IfcElement")
class IfcElementExtras(Base):
    """Extras applied to entities of class :class:`IfcElement`."""

    @property
    def parent(self: "IfcElement"):
        relations = self.ContainedInStructure()
        if relations:
            return relations[0].RelatingStructure
        return super().parent
