from typing import TYPE_CHECKING

from compas_ifc.conversions.unit import IfcCompoundPlaneAngleMeasure_to_degrees

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcSite
else:
    IfcSite = object


class IfcSite(IfcSite):
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
    def location(self):
        if self.RefLatitude and self.RefLongitude:
            return IfcCompoundPlaneAngleMeasure_to_degrees(self.RefLatitude), IfcCompoundPlaneAngleMeasure_to_degrees(self.RefLongitude)
        else:
            return None
