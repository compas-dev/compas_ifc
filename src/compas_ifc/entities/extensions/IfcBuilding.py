from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcBuilding
    from compas_ifc.entities.generated.IFC4 import IfcBuildingElement
    from compas_ifc.entities.generated.IFC4 import IfcGeographicElement
    from compas_ifc.entities.generated.IFC4 import IfcBuildingStorey
else:
    IfcBuilding = object


class IfcBuilding(IfcBuilding):

    @property
    def building_elements(self) -> list["IfcBuildingElement"]:
        return self.children_by_type("IfcBuildingElement", recursive=True)
    
    @property
    def geographic_elements(self) -> list["IfcGeographicElement"]:
        return self.children_by_type("IfcGeographicElement", recursive=True)
    
    @property
    def storeys(self) -> list["IfcBuildingStorey"]:
        return self.children_by_type("IfcBuildingStorey", recursive=True)