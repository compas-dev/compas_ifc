from functools import reduce
from operator import mul

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import Vector
from compas_ifc.model import Model
from compas_ifc.entities.base import Base


def create_IfcAxis2Placement3D(model: Model, point: Point = None, dir1: Vector = None, dir2: Vector = None) -> Base:
    """
    Create an IFC Axis2Placement3D from a point, a direction and a second direction.
    """
    point = model.create("IfcCartesianPoint", Coordinates=point or [0.0, 0.0, 0.0])
    dir1 = model.create("IfcDirection", DirectionRatios=dir1 or [0.0, 0.0, 1.0])
    dir2 = model.create("IfcDirection", DirectionRatios=dir2 or [1.0, 0.0, 0.0])
    axis2placement = model.create("IfcAxis2Placement3D", Location=point, Axis=dir1, RefDirection=dir2)
    return axis2placement


def frame_to_ifc_axis2_placement_3d(model: Model, frame: Frame) -> Base:
    return create_IfcAxis2Placement3D(model, point=frame.point, dir1=frame.zaxis, dir2=frame.xaxis)


def assign_entity_frame(entity: Base, frame: Frame):
    local_placement = frame_to_ifc_axis2_placement_3d(entity.model, frame)
    placement = entity.model.create("IfcLocalPlacement", RelativePlacement=local_placement)
    entity.ObjectPlacement = placement


def IfcLocalPlacement_to_transformation(placement: Base, scale: float = 1) -> Transformation:
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


def IfcLocalPlacement_to_frame(placement: Base) -> Frame:
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


def IfcGridPlacement_to_transformation(placement: Base) -> Transformation:
    pass
