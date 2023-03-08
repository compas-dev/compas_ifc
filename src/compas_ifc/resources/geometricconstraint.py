from operator import mul
from functools import reduce

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Transformation


def IfcLocalPlacement_to_transformation(placement) -> Transformation:
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

        point = Point(*Location.Coordinates)
        frame = Frame(point, xaxis, yaxis)
        stack.append(frame)

        if not placement.PlacementRelTo:
            break

        placement = placement.PlacementRelTo

    matrices = [Transformation.from_frame(f) for f in stack]
    return reduce(mul, matrices[::-1])


def IfcGridPlacement_to_transformation(placement) -> Transformation:
    pass
