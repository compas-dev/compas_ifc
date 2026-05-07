"""Extension for ``IfcBuilding`` entities — building-level accessors."""

from typing import TYPE_CHECKING

from compas_ifc.entities.base import Base
from compas_ifc.entities.base import extends

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcBuildingElement
    from compas_ifc.entities.generated import IfcBuildingStorey
    from compas_ifc.entities.generated import IfcGeographicElement


@extends("IfcBuilding")
class IfcBuildingExtras(Base):
    """Extras applied to entities of class :class:`IfcBuilding`."""

    @property
    def building_elements(self) -> list["IfcBuildingElement"]:
        return self.children_by_type("IfcBuildingElement", recursive=True)

    @property
    def geographic_elements(self) -> list["IfcGeographicElement"]:
        return self.children_by_type("IfcGeographicElement", recursive=True)

    @property
    def storeys(self) -> list["IfcBuildingStorey"]:
        return self.children_by_type("IfcBuildingStorey", recursive=True)
