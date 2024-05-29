# from typing import Iterator
from typing import Dict
from typing import List

from compas.geometry import Frame
from compas.geometry import Vector

from compas_ifc.entities.objectdefinition import ObjectDefinition
from compas_ifc.entities.site import Building
from compas_ifc.entities.site import Site
from compas_ifc.resources import IfcAxis2Placement3D_to_frame


class Project(ObjectDefinition):
    """
    Class representing IFC projects.

    Attributes
    ----------
    sites : List[:class:`Site`]
        The sites contained in the project.
    buildings : List[:class:`Building`]
        The buildings contained in the project.
        Note that this list is empty if ``sites`` is not empty.
    units : List[Dict]
        The SI units used in the project.
    contexts : List[Dict]
        The representation contexts included in the project.
        Each representation context defines a coordinates system, a "true north" vector, and numerical precision.
    frame : :class:`compas.geometry.Frame` or None
        The reference frame, defined by the "Model" context, if that context exists.
    north : :class:`compas.geometry.Vector` or None
        The north vector with respect to the reference frame.
    gps : ???
        Positioning of the reference frame on earth.

    Notes
    -----
    The order of spatial structure elements being included in the concept for builing projects are from high to low level:
    IfcProject, IfcSite, IfcBuilding, IfcBuildingStorey, and IfcSpace with IfcSite, IfcBuildingStorey and IfcSpace being optional levels.
    Therefore an spatial structure element can only be part of an element at the same or higher level [2]_.

    This means the minimum spatial structure of a project is:

    * IfcProject
      * IfcBuilding

    Therefore, a project will contain one or more sites, or one or more buildings.
    If the project defines sites, the buildings will be contained in the sites.

    .. code-block:: python

        model = Model(filepath)
        for project in model.projects:
            if not project.sites:
                for building in project.buildings:
                    # ...
            else:
                for site in project.sites:
                    for building in site.buildings:
                        # ...

    References
    ----------
    .. [1] :ifc:`project-context`
    .. [2] :ifc:`spatial-composition`

    """

    def __init__(self, entity, model):
        super().__init__(entity, model)
        self._units = None
        self._contexts = None
        self._sites = None
        self._buildings = None
        self._length_unit = {"type": "LENGTHUNIT", "name": "METRE", "prefix": "MILLI"}
        # TODO: deal with other units

    @property
    def sites(self) -> List[Site]:
        return [entity for entity in self.children if entity.is_a("IfcSite")]

    @property
    def buildings(self) -> List[Building]:
        return [entity for entity in self.traverse() if entity.is_a("IfcBuilding")]

    @property
    def contexts(self) -> List[Dict]:
        if self._contexts is None:
            self._contexts = []
            for context in self._entity.RepresentationContexts:
                north = Vector(*context.TrueNorth.DirectionRatios)
                wcs = IfcAxis2Placement3D_to_frame(context.WorldCoordinateSystem)
                self._contexts.append(
                    {
                        "identifier": context.ContextIdentifier,
                        "type": context.ContextType,
                        "precision": context.Precision,
                        "dimension": context.CoordinateSpaceDimension,
                        "north": north,
                        "wcs": wcs,
                    }
                )
        return self._contexts

    @property
    def units(self) -> List[Dict]:
        if self._units is None:
            self._units = []
            for unit in self._entity.UnitsInContext.Units:
                if unit.is_a("IfcSIUnit"):
                    self._units.append(
                        {
                            "type": unit.UnitType,
                            "name": unit.Name,
                            "prefix": unit.Prefix,
                        }
                    )
        return self._units

    @property
    def length_unit(self):
        if self._entity:
            for unit in self.units:
                if unit["type"] == "LENGTHUNIT":
                    return unit
        else:
            return self._length_unit

    @length_unit.setter
    def length_unit(self, unit):
        self._length_unit = unit

    @property
    def length_scale(self):
        unit = self.length_unit
        if unit:
            if unit["name"] == "METRE" and not unit["prefix"]:
                return 1.0
            if unit["name"] == "METRE" and unit["prefix"] == "CENTI":
                return 1e-2
            if unit["name"] == "METRE" and unit["prefix"] == "MILLI":
                return 1e-3
        return 1.0

    @property
    def frame(self) -> Frame:
        if self._entity:
            for context in self.contexts:
                if context["type"] == "Model":
                    return context["wcs"]

    @property
    def north(self) -> Vector:
        for context in self.contexts:
            if context["type"] == "Model":
                return context["north"]

    @property
    def gps(self):
        # global positioning of the reference frame on earth
        pass

    # @property
    # def owner(self):

    def add_site(self, site: Site) -> None:
        """
        Add a site to the project.

        Parameters
        ----------
        site : :class:`Site`

        Returns
        -------
        None

        """
        raise NotImplementedError
