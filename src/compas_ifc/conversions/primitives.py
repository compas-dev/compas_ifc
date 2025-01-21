from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from compas_ifc.entities.base import Base


def IfcCartesianPoint_to_point(cartesian_point: Base) -> Point:
    """
    Convert an IFC CartesianPoint [cartesianpoint]_ to a COMPAS point.

    """
    return Point(*cartesian_point.Coordinates)


def IfcDirection_to_vector(direction: Base) -> Vector:
    """
    Convert an IFC Direction [direction]_ to a COMPAS vector.

    """
    return Vector(*direction.DirectionRatios)


def IfcVector_to_vector(vector: Base) -> Vector:
    """
    Convert an IFC Vector [vector]_ to a COMPAS vector.

    """
    direction = IfcDirection_to_vector(vector.Orientation)
    direction.scale(vector.Magnitude)
    return direction


def IfcLine_to_line(line: Base) -> Line:
    """
    Convert an IFC Line [line]_ to a COMPAS line.

    """
    point = IfcCartesianPoint_to_point(line.Pnt)
    vector = IfcDirection_to_vector(line.Dir)
    return Line(point, point + vector)


def IfcPlane_to_plane(plane: Base) -> Plane:
    """
    Convert an IFC Plane [plane]_ to a COMPAS plane.

    """
    point = IfcCartesianPoint_to_point(plane.Position.Location)
    normal = IfcDirection_to_vector(plane.Position.P[3])
    return Plane(point, normal)
