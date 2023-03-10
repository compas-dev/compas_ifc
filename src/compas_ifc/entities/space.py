from typing import List

from compas_ifc.entities.buildingelements import BuildingElement
from compas_ifc.entities.spatialelement import SpatialElement


class Space(SpatialElement):
    """
    Class representing an IFC space.

    Attributes
    ----------
    building_elements : List[:class:`BuildingElement`]
        The building elements contained in this space.

    """

    def __init__(self, entity, model):
        super().__init__(entity, model)
        self._building_elements = None

    @property
    def building_elements(self) -> List[BuildingElement]:
        if not self._building_elements:
            self._building_elements = [entity for entity in self.traverse() if entity.is_a("IfcBuildingElement")]
        return self._building_elements
