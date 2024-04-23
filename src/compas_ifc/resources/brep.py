import ifcopenshell
import numpy as np

from typing import List
from compas.tolerance import TOL

from .primities import point_to_ifc_cartesian_point
from .primities import occ_plane_to_frame
from .primities import frame_to_ifc_plane

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


def brep_to_ifc_advanced_brep(file: ifcopenshell.file, brep) -> List[ifcopenshell.entity_instance]:
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
        points[key] = point_to_ifc_cartesian_point(file, point)
        return points[key]

    def get_ifc_line(edge):
        line_key = TOL.geometric_key(edge.first_vertex.point) + "-" + TOL.geometric_key(edge.last_vertex.point)
        return lines.get(line_key)

    def get_ifc_curve(edge):
        curve = edge.nurbscurve
        for occ_curve in curves:
            if occ_curve.IsEqual(curve.occ_curve, 1e-6):
                return curves[occ_curve]

    ifc_breps = []

    for edge in brep.edges:
        if edge.is_bspline:
            if get_ifc_curve(edge):
                continue

            start_vertex = file.create_entity("IfcVertexPoint", get_ifc_point(edge.first_vertex.point))
            if edge.nurbscurve.is_closed:
                end_vertex = start_vertex
            else:
                end_vertex = file.create_entity("IfcVertexPoint", get_ifc_point(edge.last_vertex.point))

            curve = edge.nurbscurve
            control_points = [get_ifc_point(point) for point in curve.points]
            weights = curve.weights

            # OCC will simplify the knot and multiplicity when the curver or surface is periodic,
            # so we need to recalculate the knot and multiplicity from the knot sequence.
            # Additonally, we will need to add back the duplicated control point and weight value.
            knots, multiplicities = calculate_knots_and_multiplicities(curve.knotsequence)
            if curve.is_closed:
                control_points.append(control_points[0])
                weights.append(weights[0])

            IfcBSpline = file.create_entity(
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

            IfcEdgeCurve = file.create_entity(
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
            start_vertex = file.create_entity("IfcVertexPoint", get_ifc_point(edge.first_vertex.point))
            end_vertex = file.create_entity("IfcVertexPoint", get_ifc_point(edge.last_vertex.point))

            IfcPolyLine = file.create_entity(
                "IfcPolyLine",
                Points=[start_point, end_point],
            )

            IfcEdgeCurve = file.create_entity(
                "IfcEdgeCurve",
                EdgeStart=start_vertex,
                EdgeEnd=end_vertex,
                EdgeGeometry=IfcPolyLine,
                SameSense=True,
            )

            line_key = TOL.geometric_key(edge.first_vertex.point) + "-" + TOL.geometric_key(edge.last_vertex.point)
            lines[line_key] = IfcEdgeCurve

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
                        else:
                            raise NotImplementedError("Only BSpline and Line edges are supported")

                        if not IfcEdgeCurve:
                            raise ValueError("Edge not found")

                        ifc_oriented_edge = file.create_entity(
                            "IFCORIENTEDEDGE", EdgeElement=IfcEdgeCurve, Orientation=oriented
                        )
                        ifc_oriented_edges.append(ifc_oriented_edge)

                    edge_loop = file.create_entity("IfcEdgeLoop", ifc_oriented_edges)
                    if is_outer:
                        ifc_face_bound = file.create_entity("IfcFaceOuterBound", edge_loop, True)
                        is_outer = False
                    else:
                        ifc_face_bound = file.create_entity("IfcFaceBound", edge_loop, True)
                    face_bounds.append(ifc_face_bound)

                same_sense = face.orientation == 0
                if face.is_plane:
                    occ_plane = face.occ_adaptor.Plane()
                    frame = occ_plane_to_frame(occ_plane)
                    ifc_plane = frame_to_ifc_plane(file, frame)
                    IfcAdvancedFace = file.create_entity(
                        "IfcAdvancedFace", face_bounds, ifc_plane, SameSense=same_sense
                    )
                elif face.is_cylinder:
                    cylinder = face.occ_adaptor.Cylinder()
                    IfcCylindricalSurface = occ_cylinder_to_ifc_cylindrical_surface(file, cylinder)
                    IfcAdvancedFace = file.create_entity(
                        "IfcAdvancedFace", face_bounds, IfcCylindricalSurface, SameSense=same_sense
                    )
                else:
                    control_points = np.array(face.nurbssurface.points.points, dtype=float)
                    control_points = control_points.swapaxes(0, 1)
                    ifc_control_points = []

                    u_knots, u_mults = calculate_knots_and_multiplicities(
                        list(face.nurbssurface.occ_surface.UKnotSequence())
                    )
                    v_knots, v_mults = calculate_knots_and_multiplicities(
                        list(face.nurbssurface.occ_surface.VKnotSequence())
                    )

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

                    IfcBSplineSurfaceWithKnots = file.create_entity(
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

                    IfcAdvancedFace = file.create_entity(
                        "IfcAdvancedFace", face_bounds, IfcBSplineSurfaceWithKnots, SameSense=same_sense
                    )

                ifc_faces.append(IfcAdvancedFace)

            ifc_shell = file.create_entity("IFCCLOSEDSHELL", ifc_faces)

        ifc_brep = file.create_entity("IFCADVANCEDBREP", ifc_shell)
        ifc_breps.append(ifc_brep)

    return ifc_breps
