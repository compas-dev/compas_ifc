from typing import List

from compas_ifc.entities.building import Building
from compas_ifc.entities.geographicelement import GeographicElement
from compas_ifc.entities.spatialelement import SpatialElement


class Site(SpatialElement):
    """
    Class representing an IFC site.

    Attributes
    ----------
    buildings : List[:class:`Building`]
        The buildings contained in the site.
        If the buildings are not properly nested, they can be found at the top level of an IFC model.
    address : str
        The compiled address of the site.
    geographic_elements : List[:class:`GeographicElement`]
        The geographic elements contained in the site.

    """

    def __init__(self, entity, model):
        super().__init__(entity, model)
        self._buildings = None
        self._geographic_elements = None

    @property
    def buildings(self) -> List[Building]:
        return [entity for entity in self.traverse() if entity.is_a("IfcBuilding")]

    @property
    def geographic_elements(self) -> List[GeographicElement]:
        return [entity for entity in self.traverse() if entity.is_a("IfcGeographicElement")]

    @property
    def address(self) -> str:
        attr = self.attribute("SiteAddress")
        address = ""
        address += ", ".join(attr["AddressLines"])
        address += f", {attr['Country']}-{attr['PostalCode']}"
        address += f" {attr['Town']}"
        return address

    def add_building(self, building: Building) -> None:
        """
        Add a building to this site.

        Parameters
        ----------
        building : :class:`Building`

        Returns
        -------
        None

        """
        raise NotImplementedError
