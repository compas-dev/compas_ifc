from compas_ifc.entities.element import Element
from compas_ifc.entities.spatialelement import SpatialElement


class BuildingElement(Element):
    """
    Base class for all building elements.

    References
    ----------
    * Spatial Containment: :ifc:`spatial-containment`

    """

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


class Stair(BuildingElement):
    pass


class BuildingElementProxy(BuildingElement):
    pass
