"""Adds Python-side helpers to IFC entities via the @extends decorator.

The ``@extends("IfcClass")`` decorator registers a class whose members
are mixed into the synthetic wrapper composed by ``Base.__new__``
whenever ``entity.is_a("IfcClass")`` matches. Once registered, the new
property/method is available on every wrapped entity of that class — in
this and any future model loaded in the same process.

Scope the extension to specific IFC schemas with the optional ``schemas=``
argument, e.g. ``@extends("IfcWall", schemas={"IFC4", "IFC4X3"})``.
"""

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.entities.base import Base
from compas_ifc.entities.base import extends


@extends("IfcWall")
class IfcWallExtras(Base):
    """Adds an ``axis_length`` accessor to every IfcWall entity."""

    @property
    def axis_length(self):
        """Length of the wall's axis representation in model units, or None."""
        axis = self.axis
        if axis is None or len(axis.points) < 2:
            return None
        return axis.length


@extends("IfcWindow")
class IfcWindowExtras(Base):
    """Adds an ``area`` accessor computed from OverallWidth x OverallHeight."""

    @property
    def area(self):
        if self.OverallWidth and self.OverallHeight:
            return self.OverallWidth * self.OverallHeight
        return None


# ----------------------------------------------------------------------
# The extensions are now registered globally. Open a model and use them.
# ----------------------------------------------------------------------

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

# Walls — accessed via the file-level API which returns Base wrappers.
walls = model._file.get_entities_by_type("IfcWall")
print(f"Walls: {len(walls)}")
for wall in walls[:5]:
    print(f"  {wall.Name}: axis_length = {wall.axis_length}")

# Windows
windows = model._file.get_entities_by_type("IfcWindow")
print(f"\nWindows: {len(windows)}")
for window in windows[:5]:
    print(f"  {window.Name}: area = {window.area}")
