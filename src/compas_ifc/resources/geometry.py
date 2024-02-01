# from compas_occ.geometry import OCCNurbsCurve
from compas_occ.brep import OCCBrepFace

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

# from compas.geometry import Transformation


def IfcCartesianPoint_to_point(cartesian_point) -> Point:
    """
    Convert an IFC CartesianPoint [cartesianpoint]_ to a COMPAS point.

    """
    return Point(*cartesian_point.Coordinates)


def IfcDirection_to_vector(direction) -> Vector:
    """
    Convert an IFC Direction [direction]_ to a COMPAS vector.

    """
    return Vector(*direction.DirectionRatios)


def IfcVector_to_vector(vector) -> Vector:
    """
    Convert an IFC Vector [vector]_ to a COMPAS vector.

    """
    direction = IfcDirection_to_vector(vector.Orientation)
    direction.scale(vector.Magnitude)
    return direction


def IfcLine_to_line(line) -> Line:
    """
    Convert an IFC Line [line]_ to a COMPAS line.

    """
    point = IfcCartesianPoint_to_point(line.Pnt)
    vector = IfcDirection_to_vector(line.Dir)
    return Line(point, point + vector)


def IfcPlane_to_plane(plane) -> Plane:
    """
    Convert an IFC Plane [plane]_ to a COMPAS plane.

    """
    point = IfcCartesianPoint_to_point(plane.Position.Location)
    normal = IfcDirection_to_vector(plane.Position.P[3])
    return Plane(point, normal)


def IfcAxis2Placement2D_to_frame(placement, context=None) -> Frame:
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


def IfcAxis2Placement3D_to_frame(placement, context=None) -> Frame:
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


# this needs to output a transformation
# not a frame
def IfcCartesianTransformationOperator3D_to_frame(operator) -> Frame:
    """
    Convert an IFC CartesianTransformationOperator3D to a COMPAS Frame.

    """
    Axis1 = operator.Axis1
    Axis2 = operator.Axis2
    # Axis3 = operator.Axis3
    LocalOrigin = operator.LocalOrigin
    # Scale = operator.Scale

    xaxis = Vector.Xaxis() if not Axis1 else IfcDirection_to_vector(Axis1)
    yaxis = Vector.Yaxis() if not Axis2 else IfcDirection_to_vector(Axis2)
    # zaxis = Vector.Zaxis() if not Axis3 else IfcDirection_to_vector(Axis3)
    point = IfcCartesianPoint_to_point(LocalOrigin)
    return Frame(point, xaxis, yaxis)


def IfcProfileDef_to_curve(profile_def) -> OCCBrepFace:
    pd = profile_def

    if pd.is_a("IfcParameterizedProfileDef"):
        if pd.is_a("IfcRectangleProfileDef"):
            frame = IfcAxis2Placement2D_to_frame(pd.Position)
            points = [
                frame.point + frame.xaxis * +0.5 * pd.XDim + frame.yaxis * -0.5 * pd.YDim,
                frame.point + frame.xaxis * +0.5 * pd.XDim + frame.yaxis * +0.5 * pd.YDim,
                frame.point + frame.xaxis * -0.5 * pd.XDim + frame.yaxis * +0.5 * pd.YDim,
                frame.point + frame.xaxis * -0.5 * pd.XDim + frame.yaxis * -0.5 * pd.YDim,
            ]
            return OCCBrepFace.from_polygon(points)

        else:
            raise NotImplementedError(pd)
    elif pd.is_a("IfcArbitraryClosedProfileDef"):
        return IfcCurve_to_face(pd.OuterCurve)
    elif pd.is_a("IfcCompositeProfileDef"):
        faces = []
        for profile in pd.Profiles:
            if profile.is_a("IfcArbitraryClosedProfileDef"):
                faces.append(IfcCurve_to_face(profile.OuterCurve))
            else:
                raise NotImplementedError(profile)
        return faces
    else:
        raise NotImplementedError(pd)


def IfcCurve_to_face(curve):
    if curve.is_a("IfcIndexedPolyCurve"):
        points = [(x, y, 0) for x, y in curve.Points[0]]
        return OCCBrepFace.from_polygon(points)
    elif curve.is_a("IfcPolyline"):
        points = [IfcCartesianPoint_to_point(pt) for pt in curve.Points]
        return OCCBrepFace.from_polygon(points)
    else:
        raise NotImplementedError(curve)
