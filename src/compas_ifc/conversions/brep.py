"""
This module contains functions for converting BREP geometry to IFC.

These need to be re-implemented with new COMPAS infrastructure.
"""

# def IfcProfileDef_to_curve(profile_def):
#     from compas_occ.brep import OCCBrepFace

#     pd = profile_def

#     if pd.is_a("IfcParameterizedProfileDef"):
#         if pd.is_a("IfcRectangleProfileDef"):
#             frame = IfcAxis2Placement2D_to_frame(pd.Position)
#             points = [
#                 frame.point + frame.xaxis * +0.5 * pd.XDim + frame.yaxis * -0.5 * pd.YDim,
#                 frame.point + frame.xaxis * +0.5 * pd.XDim + frame.yaxis * +0.5 * pd.YDim,
#                 frame.point + frame.xaxis * -0.5 * pd.XDim + frame.yaxis * +0.5 * pd.YDim,
#                 frame.point + frame.xaxis * -0.5 * pd.XDim + frame.yaxis * -0.5 * pd.YDim,
#             ]
#             return OCCBrepFace.from_polygon(points)

#         else:
#             raise NotImplementedError(pd)
#     elif pd.is_a("IfcArbitraryClosedProfileDef"):
#         return IfcCurve_to_face(pd.OuterCurve)
#     elif pd.is_a("IfcCompositeProfileDef"):
#         faces = []
#         for profile in pd.Profiles:
#             if profile.is_a("IfcArbitraryClosedProfileDef"):
#                 faces.append(IfcCurve_to_face(profile.OuterCurve))
#             else:
#                 raise NotImplementedError(profile)
#         return faces
#     else:
#         raise NotImplementedError(pd)


# def IfcCurve_to_face(curve):
#     from compas_occ.brep import OCCBrepFace

#     if curve.is_a("IfcIndexedPolyCurve"):
#         points = [(x, y, 0) for x, y in curve.Points[0]]
#         return OCCBrepFace.from_polygon(points)
#     elif curve.is_a("IfcPolyline"):
#         points = [IfcCartesianPoint_to_point(pt) for pt in curve.Points]
#         return OCCBrepFace.from_polygon(points)
#     else:
#         raise NotImplementedError(curve)

import numpy as np
from compas.geometry import Brep
from compas.geometry import Frame
from compas.tolerance import TOL

from compas_ifc.entities.base import Base
from compas_ifc.model import Model

from .primitives import frame_to_IfcAxis2Placement3D
from .primitives import frame_to_IfcPlane
from .primitives import point_to_IfcCartesianPoint
from .shapes import occ_cylinder_to_ifc_cylindrical_surface


def calculate_knots_and_multiplicities(knot_sequence):
    knots = [knot_sequence[0]]
    multiplicities = [1]

    for i in range(1, len(knot_sequence)):
        if knot_sequence[i] != knot_sequence[i - 1]:
            knots.append(knot_sequence[i])
            multiplicities.append(1)
        else:
            multiplicities[-1] += 1

    return knots, multiplicities


def brep_to_IfcAdvancedBrep(model: Model, brep: Brep) -> Base:
    brep.fix()
    brep.sew()
    brep.make_solid()

    points = {}
    curves = {}
    lines = {}

    def get_ifc_point(point):
        key = TOL.geometric_key(point)
        if key in points:
            return points[key]
        points[key] = point_to_IfcCartesianPoint(model, point)
        return points[key]

    def get_ifc_line(edge):
        line_key = TOL.geometric_key(edge.first_vertex.point) + "-" + TOL.geometric_key(edge.last_vertex.point)
        return lines.get(line_key)

    def get_ifc_curve(edge):
        curve = edge.curve
        for occ_curve in curves:
            if occ_curve.IsEqual(curve.occ_curve, 1e-6):
                return curves[occ_curve]

    ifc_breps = []

    for edge in brep.edges:
        if edge.is_bspline:
            if get_ifc_curve(edge):
                continue

            start_vertex = model.create("IfcVertexPoint", VertexGeometry=get_ifc_point(edge.first_vertex.point))
            if edge.curve.is_closed:
                end_vertex = start_vertex
            else:
                end_vertex = model.create("IfcVertexPoint", VertexGeometry=get_ifc_point(edge.last_vertex.point))

            curve = edge.curve
            control_points = [get_ifc_point(point) for point in curve.points]
            weights = curve.weights

            # OCC will simplify the knot and multiplicity when the curver or surface is periodic,
            # so we need to recalculate the knot and multiplicity from the knot sequence.
            # Additonally, we will need to add back the duplicated control point and weight value.
            knots, multiplicities = calculate_knots_and_multiplicities(curve.knotsequence)
            if curve.is_closed:
                control_points.append(control_points[0])
                weights.append(weights[0])

            IfcBSpline = model.create(
                "IfcRationalBSplineCurveWithKnots",
                Degree=curve.degree,
                ControlPointsList=control_points,
                CurveForm="UNSPECIFIED",
                ClosedCurve=curve.is_closed,
                SelfIntersect=False,
                KnotMultiplicities=multiplicities,
                Knots=knots,
                WeightsData=weights,
            )

            IfcEdgeCurve = model.create(
                "IfcEdgeCurve",
                EdgeStart=start_vertex,
                EdgeEnd=end_vertex,
                EdgeGeometry=IfcBSpline,
                SameSense=True,
            )

            curves[curve.occ_curve] = IfcEdgeCurve

        elif edge.is_line:
            if get_ifc_line(edge):
                continue

            start_point = get_ifc_point(edge.first_vertex.point)
            end_point = get_ifc_point(edge.last_vertex.point)
            start_vertex = model.create("IfcVertexPoint", VertexGeometry=start_point)
            end_vertex = model.create("IfcVertexPoint", VertexGeometry=end_point)

            IfcPolyLine = model.create(
                "IfcPolyLine",
                Points=[start_point, end_point],
            )

            IfcEdgeCurve = model.create(
                "IfcEdgeCurve",
                EdgeStart=start_vertex,
                EdgeEnd=end_vertex,
                EdgeGeometry=IfcPolyLine,
                SameSense=True,
            )

            line_key = TOL.geometric_key(edge.first_vertex.point) + "-" + TOL.geometric_key(edge.last_vertex.point)
            lines[line_key] = IfcEdgeCurve

        elif edge.is_circle:
            pass
        else:
            raise NotImplementedError("Only BSpline and Line edges are supported")

    for solid in brep.solids:
        for shell in solid.shells:
            ifc_faces = []
            for face in shell.faces:
                face_bounds = []
                is_outer = True

                for loop in face.loops:
                    ifc_oriented_edges = []

                    for edge in loop.edges:
                        if edge.is_bspline:
                            oriented = edge.occ_edge.Orientation() == 0
                            IfcEdgeCurve = get_ifc_curve(edge)
                        elif edge.is_line:
                            oriented = edge.occ_edge.Orientation() == 0
                            IfcEdgeCurve = get_ifc_line(edge)
                        elif edge.is_circle:
                            oriented = edge.occ_edge.Orientation() == 0
                            circle = edge.curve
                            IfcCircle = model.create("IfcCircle", Position=frame_to_IfcAxis2Placement3D(model, circle.frame), Radius=circle.radius)
                            IfcEdgeCurve = IfcCircle
                        else:
                            raise NotImplementedError("Only BSpline and Line edges are supported")

                        if not IfcEdgeCurve:
                            raise ValueError("Edge not found")

                        ifc_oriented_edge = model.create("IfcOrientedEdge", EdgeElement=IfcEdgeCurve, Orientation=oriented)
                        ifc_oriented_edges.append(ifc_oriented_edge)

                    edge_loop = model.create("IfcEdgeLoop", EdgeList=ifc_oriented_edges)
                    if is_outer:
                        ifc_face_bound = model.create("IfcFaceOuterBound", Bound=edge_loop, Orientation=True)
                        is_outer = False
                    else:
                        ifc_face_bound = model.create("IfcFaceBound", Bound=edge_loop, Orientation=False)
                    face_bounds.append(ifc_face_bound)

                same_sense = face.orientation == 0
                if face.is_plane:
                    occ_plane = face.occ_adaptor.Plane()
                    location = occ_plane.Location().Coord()
                    x_axis = occ_plane.XAxis().Direction().Coord()
                    y_axis = occ_plane.YAxis().Direction().Coord()
                    frame = Frame(location, x_axis, y_axis)
                    ifc_plane = frame_to_IfcPlane(model, frame)
                    IfcAdvancedFace = model.create("IfcAdvancedFace", Bounds=face_bounds, FaceSurface=ifc_plane, SameSense=same_sense)
                elif face.is_cylinder:
                    cylinder = face.occ_adaptor.Cylinder()
                    IfcCylindricalSurface = occ_cylinder_to_ifc_cylindrical_surface(model, cylinder)
                    IfcAdvancedFace = model.create("IfcAdvancedFace", Bounds=face_bounds, FaceSurface=IfcCylindricalSurface, SameSense=same_sense)
                else:
                    control_points = np.array(face.nurbssurface.points.points, dtype=float)
                    control_points = control_points.swapaxes(0, 1)
                    ifc_control_points = []

                    u_knots, u_mults = calculate_knots_and_multiplicities(list(face.nurbssurface.occ_surface.UKnotSequence()))
                    v_knots, v_mults = calculate_knots_and_multiplicities(list(face.nurbssurface.occ_surface.VKnotSequence()))

                    for row in control_points:
                        ifc_row = []
                        for point in row:
                            ifc_row.append(get_ifc_point(point))
                        ifc_control_points.append(ifc_row)

                    if face.nurbssurface.is_periodic_u:
                        new_row = []
                        for point in control_points[0]:
                            new_row.append(get_ifc_point(point))
                        ifc_control_points.append(new_row)

                    if face.nurbssurface.is_periodic_v:
                        for i, row in enumerate(ifc_control_points):
                            row.append(get_ifc_point(control_points[i % len(control_points)][0]))

                    weights = face.nurbssurface.weights
                    weights = np.array(weights, dtype=float)
                    weights = weights.swapaxes(0, 1)

                    ifc_weights = []
                    for row in weights:
                        ifc_row = []
                        for weight in row:
                            ifc_row.append(float(weight))
                        ifc_weights.append(ifc_row)

                    if face.nurbssurface.is_periodic_u:
                        ifc_weights.append(ifc_weights[0])
                    if face.nurbssurface.is_periodic_v:
                        for i, row in enumerate(ifc_weights):
                            row.append(row[0])

                    IfcBSplineSurfaceWithKnots = model.create(
                        "IfcRationalBSplineSurfaceWithKnots",
                        UDegree=face.nurbssurface.degree_u,
                        VDegree=face.nurbssurface.degree_v,
                        ControlPointsList=ifc_control_points,
                        SurfaceForm="UNSPECIFIED",
                        UClosed=face.nurbssurface.is_periodic_u,
                        VClosed=face.nurbssurface.is_periodic_v,
                        SelfIntersect=False,  # Seems no way to get this from OCC
                        UMultiplicities=u_mults,
                        VMultiplicities=v_mults,
                        UKnots=u_knots,
                        VKnots=v_knots,
                        WeightsData=ifc_weights,
                    )

                    IfcAdvancedFace = model.create("IfcAdvancedFace", Bounds=face_bounds, FaceSurface=IfcBSplineSurfaceWithKnots, SameSense=same_sense)

                ifc_faces.append(IfcAdvancedFace)

            ifc_shell = model.create("IfcClosedShell", CfsFaces=ifc_faces)

        ifc_brep = model.create("IfcAdvancedBrep", Outer=ifc_shell)
        ifc_breps.append(ifc_brep)

    if len(ifc_breps) == 0:
        print("WARNING: No BREPs found")

    return ifc_breps
