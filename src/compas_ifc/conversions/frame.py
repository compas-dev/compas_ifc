from functools import reduce
from operator import mul

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import Vector

from compas_ifc.conversions.primitives import IfcCartesianPoint_to_point
from compas_ifc.conversions.primitives import IfcDirection_to_vector
from compas_ifc.entities.base import Base
from compas_ifc.model import Model


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


def IfcAxis2Placement2D_to_frame(placement: Base) -> Frame:
    """
    Convert an IFC Axis2Placement2D [axis2placement2d]_ to a COMPAS frame.

    An Axis2Placement2D is a 2D placement based on a frame defined by a point and 2 vectors.

    """
    # use the coordinate system of the representation context to replace missing axes
    # use defaults if also those not available
    point = IfcCartesianPoint_to_point(placement.Location)
    zaxis = Vector.Zaxis()
    if placement.RefDirection:
        xaxis = IfcDirection_to_vector(placement.RefDirection)
    else:
        xaxis = Vector.Xaxis()
    yaxis = zaxis.cross(xaxis)
    return Frame(point, xaxis, yaxis)


def IfcAxis2Placement3D_to_frame(placement: Base) -> Frame:
    """
    Convert an IFC Axis2Placement3D [axis2placement3d]_ to a COMPAS frame.

    An Axis2Placement3D is a 3D placement based on a frame defined by a point and 2 vectors.

    """
    # use the coordinate system of the representation context to replace missing axes
    # use defaults if also those not available
    point = IfcCartesianPoint_to_point(placement.Location)
    if placement.Axis:
        zaxis = IfcDirection_to_vector(placement.Axis)
    else:
        zaxis = Vector.Zaxis()
    if placement.RefDirection:
        xaxis = IfcDirection_to_vector(placement.RefDirection)
    else:
        xaxis = Vector.Xaxis()
    yaxis = zaxis.cross(xaxis)
    xaxis = yaxis.cross(zaxis)
    return Frame(point, xaxis, yaxis)
