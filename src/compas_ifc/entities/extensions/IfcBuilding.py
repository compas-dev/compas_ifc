from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcBuilding
else:
    IfcBuilding = object


class IfcBuilding(IfcBuilding):

    @property
    def building_elements(self):
        return self.children_by_type("IfcBuildingElement", recursive=True)
    
    @property
    def geographic_elements(self):
        return self.children_by_type("IfcGeographicElement", recursive=True)