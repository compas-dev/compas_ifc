from functools import reduce
from operator import mul

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import Vector


def IfcLocalPlacement_to_transformation(placement, scale=1) -> Transformation:
    """
    Convert an IFC LocalPlacement [localplacement]_ to a COMPAS transformation.
    This will resolve all relative placements into one transformation wrt the global coordinate system.

    """
    stack = []
    while True:
        Location = placement.RelativePlacement.Location
        Axis = placement.RelativePlacement.Axis
        RefDirection = placement.RelativePlacement.RefDirection

        if Axis and RefDirection:
            zaxis = Vector(*Axis.DirectionRatios)
            xaxis = Vector(*RefDirection.DirectionRatios)
            yaxis = zaxis.cross(xaxis)
            xaxis = yaxis.cross(zaxis)
        else:
            xaxis = Vector.Xaxis()
            yaxis = Vector.Yaxis()

        point = Point(*Location.Coordinates) * scale
        frame = Frame(point, xaxis, yaxis)
        stack.append(frame)

        if not placement.PlacementRelTo:
            break

        placement = placement.PlacementRelTo

    matrices = [Transformation.from_frame(f) for f in stack]
    return reduce(mul, matrices[::-1])


def IfcLocalPlacement_to_frame(placement) -> Frame:
    """
    Convert an IFC LocalPlacement to a COMPAS frame.
    """

    Location = placement.RelativePlacement.Location
    Axis = placement.RelativePlacement.Axis
    RefDirection = placement.RelativePlacement.RefDirection

    if Axis and RefDirection:
        zaxis = Vector(*Axis.DirectionRatios)
        xaxis = Vector(*RefDirection.DirectionRatios)
        yaxis = zaxis.cross(xaxis)
        xaxis = yaxis.cross(zaxis)
    else:
        xaxis = Vector.Xaxis()
        yaxis = Vector.Yaxis()

    point = Point(*Location.Coordinates)
    return Frame(point, xaxis, yaxis)


def IfcGridPlacement_to_transformation(placement) -> Transformation:
    pass
