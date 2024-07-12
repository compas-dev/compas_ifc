from typing import List

from compas_ifc.entities.buildingelements import Beam
from compas_ifc.entities.buildingelements import BuildingElementProxy
from compas_ifc.entities.buildingelements import Column
from compas_ifc.entities.buildingelements import Door
from compas_ifc.entities.buildingelements import Roof
from compas_ifc.entities.buildingelements import Slab
from compas_ifc.entities.buildingelements import Stair
from compas_ifc.entities.buildingelements import Wall
from compas_ifc.entities.buildingelements import Window
from compas_ifc.entities.space import Space
from compas_ifc.entities.spatialelement import SpatialElement


class BuildingStorey(SpatialElement):
    """
    Class representing an IFC building storey.

    Attributes
    ----------
    beams : List[:class:`Beam`]
        The beams contained in this building storey.
    columns : List[:class:`Column`]
        The beams contained in this building storey.
    doors : List[:class:`Column`]
        The beams contained in this building storey.
    roofs : List[:class:`Roof`]
        The roofs contained in this building storey.
    slabs : List[:class:`Slab`]
        The slabs contained in this building storey.
    stairs : List[:class:`Stairs`]
        The stairs contained in this building storey.
    walls : List[:class:`Walls`]
        The walls contained in this building storey.
    windows : List[:class:`Windows`]
        The windows contained in this building storey.
    spaces : List[:class:`Space`]
        The spaces contained in this building storey.
    building_elements_proxies : List[:class:`BuildingElementProxy`]
        The building element proxies contained in this building storey.

    """

    @property
    def spaces(self) -> List[Space]:
        return [entity for entity in self.traverse() if entity.is_a("IfcSpace")]

    @property
    def beams(self) -> List[Beam]:
        return [entity for entity in self.traverse() if entity.is_a("IfcBeam")]

    @property
    def columns(self) -> List[Column]:
        return [entity for entity in self.traverse() if entity.is_a("IfcColumn")]

    @property
    def doors(self) -> List[Door]:
        return [entity for entity in self.traverse() if entity.is_a("IfcDoor")]

    @property
    def roofs(self) -> List[Roof]:
        return [entity for entity in self.traverse() if entity.is_a("IfcRoof")]

    @property
    def slabs(self) -> List[Slab]:
        return [entity for entity in self.traverse() if entity.is_a("IfcSlab")]

    @property
    def stairs(self) -> List[Stair]:
        return [entity for entity in self.traverse() if entity.is_a("IfcStair")]

    @property
    def walls(self) -> List[Wall]:
        return [entity for entity in self.traverse() if entity.is_a("IfcWall")]

    @property
    def windows(self) -> List[Window]:
        return [entity for entity in self.traverse() if entity.is_a("IfcWindow")]

    @property
    def building_elements_proxies(self) -> List[BuildingElementProxy]:
        return [entity for entity in self.traverse() if entity.is_a("IfcBuildingElementProxy")]
