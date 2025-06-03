from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from compas_ifc.entities.base import Base
from compas_ifc.model import Model


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


def point_to_IfcCartesianPoint(model: Model, point: Point) -> Base:
    """
    Convert a COMPAS point to an IFC CartesianPoint.
    """
    return model.create("IfcCartesianPoint", Coordinates=(float(point.x), float(point.y), float(point.z)))


def vector_to_IfcDirection(model: Model, vector: Vector) -> Base:
    """
    Convert a COMPAS vector to an IFC Direction.
    """
    return model.create("IfcDirection", DirectionRatios=(float(vector.x), float(vector.y), float(vector.z)))


def frame_to_IfcAxis2Placement3D(model: Model, frame: Frame) -> Base:
    """
    Convert a COMPAS frame to an IFC Axis2Placement3D.
    """
    return model.create(
        "IfcAxis2Placement3D",
        Location=point_to_IfcCartesianPoint(model, frame.point),
        Axis=vector_to_IfcDirection(model, frame.zaxis),
        RefDirection=vector_to_IfcDirection(model, frame.xaxis),
    )


def frame_to_IfcPlane(model: Model, frame: Frame) -> Base:
    """
    Convert a COMPAS frame to an IFC Plane.
    """
    return model.create("IfcPlane", Position=frame_to_IfcAxis2Placement3D(model, frame))
