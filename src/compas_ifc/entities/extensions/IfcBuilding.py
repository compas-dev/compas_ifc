from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcBuilding
    from compas_ifc.entities.generated.IFC4 import IfcBuildingElement
    from compas_ifc.entities.generated.IFC4 import IfcBuildingStorey
    from compas_ifc.entities.generated.IFC4 import IfcGeographicElement
else:
    IfcBuilding = object


class IfcBuilding(IfcBuilding):
    """Extension class for :class:`IfcBuilding`.

    Attributes
    ----------
    building_elements : list[:class:`IfcBuildingElement`]
        The building elements of the building.
    geographic_elements : list[:class:`IfcGeographicElement`]
        The geographic elements of the building.
    storeys : list[:class:`IfcBuildingStorey`]
        The storeys of the building.

    """

    @property
    def building_elements(self) -> list["IfcBuildingElement"]:
        return self.children_by_type("IfcBuildingElement", recursive=True)

    @property
    def geographic_elements(self) -> list["IfcGeographicElement"]:
        return self.children_by_type("IfcGeographicElement", recursive=True)

    @property
    def storeys(self) -> list["IfcBuildingStorey"]:
        return self.children_by_type("IfcBuildingStorey", recursive=True)
