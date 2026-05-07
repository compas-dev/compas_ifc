"""Extension for ``IfcSite`` entities — site-level accessors."""

from __future__ import annotations

from typing import TYPE_CHECKING

from compas_ifc.conversions.unit import IfcCompoundPlaneAngleMeasure_to_degrees
from compas_ifc.entities.base import Base
from compas_ifc.entities.base import extends

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcSite


@extends("IfcSite")
class IfcSiteExtras(Base):
    """Extras applied to entities of class :class:`IfcSite`.

    Adds ``buildings``, ``building_elements``, ``geographic_elements``,
    and ``location`` accessors.
    """

    @property
    def buildings(self):
        return self.children_by_type("IfcBuilding", recursive=True)

    @property
    def building_elements(self):
        return self.children_by_type("IfcBuildingElement", recursive=True)

    @property
    def geographic_elements(self):
        return self.children_by_type("IfcGeographicElement", recursive=True)

    @property
    def location(self: "IfcSite"):
        if self.RefLatitude and self.RefLongitude:
            return (
                IfcCompoundPlaneAngleMeasure_to_degrees(self.RefLatitude),
                IfcCompoundPlaneAngleMeasure_to_degrees(self.RefLongitude),
            )
        return None
