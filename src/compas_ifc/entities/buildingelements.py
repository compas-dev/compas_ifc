from compas_ifc.entities.element import Element
from compas_ifc.entities.spatialelement import SpatialElement


class BuildingElement(Element):
    """
    Base class for all building elements.

    References
    ----------
    * Spatial Containment: :ifc:`spatial-containment`

    """

    def __init__(self, entity, model) -> None:
        super().__init__(entity, model)
        self._composite_body = None
        self._composite_opening = None
        self._composite_body_with_opening = None

    def is_contained(self) -> bool:
        """
        Verify that this building element is contained in a spatial structure.

        Returns
        -------
        bool

        """
        return len(self._entity.ContainedInStructure) == 1

    def is_containment_hierarchical(self) -> bool:
        """
        Verify that the spatial containment of this building element is hierarchical,
        meaning that the element is contained in no more than one (1) spatial element.

        Returns
        -------
        bool

        """
        if len(self._entity.ContainedInStructure) > 1:
            return False
        return True

    def container(self) -> SpatialElement:
        """
        Get the container of the building element.

        Containment is hierarchical, meaning that the element can only be contained in one spatial element.

        Returns
        -------
        :class:`SpatialElement`

        """
        return self.parent

    @property
    def building_element_parts(self):
        return [part for part in self.children if part.is_a("IfcBuildingElementPart")]

    @property
    def composite_body(self):
        bodies = []
        for part in self.building_element_parts:
            bodies.extend(part.body)
        self._composite_body = bodies
        return self._composite_body

    @composite_body.setter
    def composite_body(self, value):
        self._composite_body = value

    @property
    def composite_opening(self):
        voids = self.opening
        for part in self.building_element_parts:
            voids.extend(part.opening)
        self._composite_opening = voids
        return self._composite_opening

    @property
    def composite_body_with_opening(self):
        from compas_ifc.representation import entity_body_with_opening_geometry

        if not self._composite_body_with_opening:
            self._composite_body_with_opening = entity_body_with_opening_geometry(
                entity=self, bodies=self.composite_body, voids=self.composite_opening
            )
        return self._composite_body_with_opening

    @composite_body_with_opening.setter
    def composite_body_with_opening(self, value):
        self._composite_body_with_opening = value


class Beam(BuildingElement):
    pass


class Column(BuildingElement):
    pass


class Wall(BuildingElement):
    @property
    def gross_area(self):
        self.properties.get("GrossSideArea")


class Window(BuildingElement):
    pass


class Roof(BuildingElement):
    pass


class Slab(BuildingElement):
    pass


class Door(BuildingElement):
    pass


class Railing(BuildingElement):
    pass


class Stair(BuildingElement):
    pass


class BuildingElementProxy(BuildingElement):
    pass
