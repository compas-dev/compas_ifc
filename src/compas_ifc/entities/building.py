from typing import List
from compas_ifc.entities.spatialelement import SpatialElement
from compas_ifc.entities.space import Space
from compas_ifc.entities.buildingelements import BuildingElement
from compas_ifc.entities.buildingstorey import BuildingStorey


class Building(SpatialElement):
    """
    Class representing an IFC building.

    Attributes
    ----------
    address : str
        The compiled address of the building.
    building_storeys : List[BuildingStorey]
        The building_storeys contained in the building.
        If the building_storeys are not properly nested, they can be found at the top level of an IFC model.
    spaces : List[Space]
        The spaces contained in the building.
    building_elements : List[BuildingElement]
        The building elements contained in the building.

    Notes
    -----
    The order of spatial structure elements being included in the concept for builing projects are from high to low level:
    IfcProject, IfcSite, IfcBuilding, IfcBuildingStorey, and IfcSpace with IfcSite, IfcBuildingStorey and IfcSpace being optional levels.
    Therefore an spatial structure element can only be part of an element at the same or higher level [1]_.

    This means the minimum spatial structure of a project is:

    * IfcProject

      * IfcBuilding

        * IfcBuildingElement

    Therefore, all building elements found in a model can be accessed through the Building class.

    .. code-block:: python

        model = Model(filepath)
        for project in model.projects:
            if project.sites:
                for site in project.sites:
                    for building in site.buildings:
                        for element in building.elements:
                            # ...
            else:
                for building in project.buildings:
                    for element in building.elements:
                        # ...

    References
    ----------
    .. [1] :ifc:`spatial-composition`

    """

    def __init__(self, entity, model):
        super().__init__(entity, model)
        self._building_storeys = None
        self._spaces = None
        self._elements = None

    @property
    def building_storeys(self) -> List[BuildingStorey]:
        return [entity for entity in self.traverse() if entity.is_a("IfcBuildingStorey")]

    @property
    def spaces(self) -> List[Space]:
        return [entity for entity in self.traverse() if entity.is_a("IfcSpace")]

    @property
    def building_elements(self) -> List[BuildingElement]:
        return [entity for entity in self.traverse() if entity.is_a("IfcBuildingElement")]

    @property
    def address(self) -> str:
        attr = self.attribute("BuildingAddress")
        address = ""
        address += ", ".join(attr["AddressLines"])
        address += f", {attr['Country']}-{attr['PostalCode']}"
        address += f" {attr['Town']}"
        return address
