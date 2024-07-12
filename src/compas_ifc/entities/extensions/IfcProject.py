from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcProject
else:
    IfcProject = object


class IfcProject(IfcProject):
    @property
    def sites(self):
        return self.children_by_type("IfcSite", recursive=True)

    @property
    def buildings(self):
        return self.children_by_type("IfcBuilding", recursive=True)

    @property
    def building_elements(self):
        return self.children_by_type("IfcBuildingElement", recursive=True)

    @property
    def geographic_elements(self):
        return self.children_by_type("IfcGeographicElement", recursive=True)

    @property
    def contexts(self):
        from compas.geometry import Vector

        from compas_ifc.resources import IfcAxis2Placement3D_to_frame

        contexts = []

        for context in self.RepresentationContexts:
            north = Vector(*context.TrueNorth.DirectionRatios) if context.TrueNorth else None
            wcs = IfcAxis2Placement3D_to_frame(context.WorldCoordinateSystem)
            contexts.append(
                {
                    "identifier": context.ContextIdentifier,
                    "type": context.ContextType,
                    "precision": context.Precision,
                    "dimension": context.CoordinateSpaceDimension,
                    "north": north,
                    "wcs": wcs,
                }
            )
        return contexts

    @property
    def units(self):
        units = []
        units_in_context = self.UnitsInContext or self.file.get_entities_by_type("IfcUnitAssignment")[0]
        for unit in units_in_context.Units:
            if unit.is_a("IfcSIUnit"):
                units.append(
                    {
                        "type": unit.UnitType,
                        "name": unit.Name,
                        "prefix": unit.Prefix,
                    }
                )
        return units

    @property
    def length_unit(self):
        for unit in self.units:
            if unit["type"] == "LENGTHUNIT":
                return unit

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
    def frame(self):
        for context in self.contexts:
            if context["type"] == "Model":
                return context["wcs"]

    @property
    def north(self):
        for context in self.contexts:
            if context["type"] == "Model":
                return context["north"]
