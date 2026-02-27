"""
This module contains functions for converting BREP geometry to IFC.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from compas.geometry import Brep
from compas.geometry import Frame
from compas.tolerance import TOL

from compas_ifc.entities.base import Base

if TYPE_CHECKING:
    from compas_ifc.bim import BuildingInformationModel

from .frame import create_IfcAxis2Placement3D
from .primitives import frame_to_IfcAxis2Placement3D
from .primitives import frame_to_IfcPlane
from .primitives import point_to_IfcCartesianPoint
from .shapes import occ_cylinder_to_ifc_cylindrical_surface
from .shapes import occ_sphere_to_ifc_spherical_surface
from .shapes import occ_torus_to_ifc_toroidal_surface


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


def brep_to_IfcAdvancedBrep(model: BuildingInformationModel, brep: Brep) -> list[Base]:
    brep.fix()
    # Only sew and promote to solid when there are no solids yet.
    # BRepBuilderAPI_Sewing merges all faces into a single shell, destroying
    # inner/outer shell topology of boolean-cut bodies with voids.
    if not brep.solids:
        brep.sew()
        brep.make_solid()

    # Cache dicts to deduplicate IFC entities across all edges/faces.
    # points:   geometric_key -> IfcCartesianPoint
    # vertices: geometric_key -> IfcVertexPoint
    # curves:   occ_curve object -> IfcEdgeCurve  (BSpline edges)
    # lines:    "start_key-end_key" -> IfcEdgeCurve  (line edges, both directions)
    # circles:  "cx,cy,cz-r" -> IfcEdgeCurve  (circle edges)
    # ellipses: "cx,cy,cz-a-b" -> IfcEdgeCurve  (ellipse edges)
    points = {}
    vertices = {}
    curves = {}
    lines = {}
    circles = {}
    ellipses = {}

    def get_ifc_point(point):
        key = TOL.geometric_key(point)
        if key not in points:
            points[key] = point_to_IfcCartesianPoint(model, point)
        return points[key]

    def get_ifc_vertex(point):
        key = TOL.geometric_key(point)
        if key not in vertices:
            vertices[key] = model.create("IfcVertexPoint", VertexGeometry=get_ifc_point(point))
        return vertices[key]

    def get_ifc_bspline_edge(edge):
        curve = edge.curve
        for occ_curve, ifc_edge in curves.items():
            if occ_curve.IsEqual(curve.occ_curve, 1e-6):
                return ifc_edge
        return None

    def get_ifc_line_edge(edge):
        key = TOL.geometric_key(edge.first_vertex.point) + "-" + TOL.geometric_key(edge.last_vertex.point)
        rev_key = TOL.geometric_key(edge.last_vertex.point) + "-" + TOL.geometric_key(edge.first_vertex.point)
        return lines.get(key) or lines.get(rev_key)

    def get_ifc_circle_edge(edge):
        c = edge.curve
        sv = TOL.geometric_key(edge.first_vertex.point)
        ev = TOL.geometric_key(edge.last_vertex.point)
        key = "{:.6f},{:.6f},{:.6f}-{:.6f}-{}-{}".format(*c.frame.point, c.radius, sv, ev)
        return circles.get(key), key

    def get_ifc_ellipse_edge(edge):
        from OCC.Core.GeomAbs import GeomAbs_Ellipse

        adaptor = edge.occ_adaptor
        if adaptor.GetType() != GeomAbs_Ellipse:
            return None, None
        ellipse = adaptor.Ellipse()
        loc = ellipse.Location().Coord()
        a = ellipse.MajorRadius()
        b = ellipse.MinorRadius()
        sv = TOL.geometric_key(edge.first_vertex.point)
        ev = TOL.geometric_key(edge.last_vertex.point)
        key = "{:.6f},{:.6f},{:.6f}-{:.6f}-{:.6f}-{}-{}".format(*loc, a, b, sv, ev)
        return ellipses.get(key), key

    # ------------------------------------------------------------------ #
    # Pre-pass: create all edge geometry (IfcEdgeCurve) before faces,     #
    # so every face loop can look them up by cache.                        #
    # ------------------------------------------------------------------ #
    from OCC.Core.BRep import BRep_Tool as _BRep_Tool

    degenerate_edges = set()

    for edge in brep.edges:
        if _BRep_Tool.Degenerated(edge.occ_edge):
            # Degenerate edges (e.g. poles of sphere/cone) have no geometry
            # and are skipped — they are not included in IfcEdgeLoop.
            degenerate_edges.add(id(edge.occ_edge))
            continue
        if edge.is_bspline:
            if get_ifc_bspline_edge(edge):
                continue

            start_vertex = get_ifc_vertex(edge.first_vertex.point)
            is_closed = TOL.geometric_key(edge.first_vertex.point) == TOL.geometric_key(edge.last_vertex.point)
            end_vertex = start_vertex if is_closed else get_ifc_vertex(edge.last_vertex.point)

            curve = edge.curve
            control_points = [get_ifc_point(point) for point in curve.points]
            weights = curve.weights

            # OCC simplifies knots/multiplicities for periodic curves; restore
            # the full sequence and duplicate the first control point/weight.
            knots, multiplicities = calculate_knots_and_multiplicities(curve.knotsequence)
            if curve.is_closed:
                control_points.append(control_points[0])
                weights.append(weights[0])

            IfcBSplineCurve = model.create(
                "IfcRationalBSplineCurveWithKnots",
                Degree=curve.degree,
                ControlPointsList=control_points,
                CurveForm="UNSPECIFIED",
                ClosedCurve=curve.is_closed,
                SelfIntersect=False,
                KnotMultiplicities=multiplicities,
                Knots=knots,
                KnotSpec="UNSPECIFIED",
                WeightsData=weights,
            )

            IfcEdgeCurve = model.create(
                "IfcEdgeCurve",
                EdgeStart=start_vertex,
                EdgeEnd=end_vertex,
                EdgeGeometry=IfcBSplineCurve,
                SameSense=True,
            )
            curves[curve.occ_curve] = IfcEdgeCurve

        elif edge.is_line:
            if get_ifc_line_edge(edge):
                continue

            start_pt = get_ifc_point(edge.first_vertex.point)
            end_pt = get_ifc_point(edge.last_vertex.point)  # noqa: F841 — used implicitly via vertex
            start_vertex = get_ifc_vertex(edge.first_vertex.point)
            end_vertex = get_ifc_vertex(edge.last_vertex.point)

            # IfcLine: parametric infinite line defined by a point and direction vector.
            # Do not use IfcPolyLine (polyline approximation) for straight edges.
            direction = model.create(
                "IfcDirection",
                DirectionRatios=list(edge.to_line().direction.unitized()),
            )
            ifc_vector = model.create("IfcVector", Orientation=direction, Magnitude=1.0)
            IfcLine = model.create("IfcLine", Pnt=start_pt, Dir=ifc_vector)

            IfcEdgeCurve = model.create(
                "IfcEdgeCurve",
                EdgeStart=start_vertex,
                EdgeEnd=end_vertex,
                EdgeGeometry=IfcLine,
                SameSense=True,
            )
            key = TOL.geometric_key(edge.first_vertex.point) + "-" + TOL.geometric_key(edge.last_vertex.point)
            lines[key] = IfcEdgeCurve

        elif edge.is_circle:
            _, key = get_ifc_circle_edge(edge)
            if circles.get(key):
                continue

            c = edge.curve
            start_vertex = get_ifc_vertex(edge.first_vertex.point)
            is_closed = TOL.geometric_key(edge.first_vertex.point) == TOL.geometric_key(edge.last_vertex.point)
            end_vertex = start_vertex if is_closed else get_ifc_vertex(edge.last_vertex.point)

            IfcCircle = model.create(
                "IfcCircle",
                Position=frame_to_IfcAxis2Placement3D(model, c.frame),
                Radius=c.radius,
            )
            # IfcOrientedEdge.EdgeElement must be an IfcEdge (IfcEdgeCurve),
            # not an IfcConic directly — wrap IfcCircle in IfcEdgeCurve.
            IfcEdgeCurve = model.create(
                "IfcEdgeCurve",
                EdgeStart=start_vertex,
                EdgeEnd=end_vertex,
                EdgeGeometry=IfcCircle,
                SameSense=True,
            )
            circles[key] = IfcEdgeCurve

        elif edge.is_ellipse:
            _, key = get_ifc_ellipse_edge(edge)
            if key and ellipses.get(key):
                continue

            from OCC.Core.GeomAbs import GeomAbs_Ellipse

            adaptor = edge.occ_adaptor
            if adaptor.GetType() == GeomAbs_Ellipse:
                ellipse = adaptor.Ellipse()
                loc = ellipse.Location().Coord()
                xdir = ellipse.XAxis().Direction().Coord()
                zdir = ellipse.Axis().Direction().Coord()
                placement = create_IfcAxis2Placement3D(model, loc, zdir, xdir)

                start_vertex = get_ifc_vertex(edge.first_vertex.point)
                is_closed = TOL.geometric_key(edge.first_vertex.point) == TOL.geometric_key(edge.last_vertex.point)
                end_vertex = start_vertex if is_closed else get_ifc_vertex(edge.last_vertex.point)

                IfcEllipse = model.create(
                    "IfcEllipse",
                    Position=placement,
                    SemiAxis1=ellipse.MajorRadius(),
                    SemiAxis2=ellipse.MinorRadius(),
                )
                IfcEdgeCurve = model.create(
                    "IfcEdgeCurve",
                    EdgeStart=start_vertex,
                    EdgeEnd=end_vertex,
                    EdgeGeometry=IfcEllipse,
                    SameSense=True,
                )
                if key:
                    ellipses[key] = IfcEdgeCurve

        else:
            raise NotImplementedError(f"Unsupported edge type: {edge}")

    # ------------------------------------------------------------------ #
    # Main pass: build faces → shells → IfcAdvancedBrep / WithVoids       #
    # ------------------------------------------------------------------ #
    ifc_breps = []

    for solid in brep.solids:
        shells = list(solid.shells)

        def build(shell):
            return _build_shell_faces(shell, model, get_ifc_bspline_edge, get_ifc_line_edge, get_ifc_circle_edge, get_ifc_ellipse_edge, degenerate_edges)

        # Merge all shells (outer + inner voids) into one IfcClosedShell.
        # IfcAdvancedBrepWithVoids is correct per spec but poorly supported
        # by viewers, so we flatten everything into a single IfcAdvancedBrep.
        all_faces = []
        for shell in shells:
            all_faces.extend(build(shell))
        ifc_shell = model.create("IfcClosedShell", CfsFaces=all_faces)
        ifc_brep = model.create("IfcAdvancedBrep", Outer=ifc_shell)

        ifc_breps.append(ifc_brep)

    if not ifc_breps:
        # compas_occ may lose solid topology (e.g. for boolean-cut bodies
        # or compounds).  Fall back to treating each shell as a separate solid.
        # BRepBuilderAPI_Sewing can also leave inner-void faces as orphans
        # (not inside any shell).  Detect these and merge them into the shell.
        shells = list(brep.shells)
        if not shells:
            raise ValueError("No solids or shells found in Brep — cannot create IfcAdvancedBrep")

        def build(shell):
            return _build_shell_faces(shell, model, get_ifc_bspline_edge, get_ifc_line_edge, get_ifc_circle_edge, get_ifc_ellipse_edge, degenerate_edges)

        # Detect orphan faces: faces in the compound but not in any shell.
        orphan_faces = _find_orphan_faces(brep)

        if orphan_faces and len(shells) == 1:
            # Single outer shell + orphan void faces → merge into one IfcAdvancedBrep.
            all_faces = build(shells[0])
            all_faces.extend(
                _build_orphan_faces(
                    orphan_faces,
                    model,
                    get_ifc_bspline_edge,
                    get_ifc_line_edge,
                    get_ifc_circle_edge,
                    get_ifc_ellipse_edge,
                    degenerate_edges,
                )
            )
            ifc_shell = model.create("IfcClosedShell", CfsFaces=all_faces)
            ifc_brep = model.create("IfcAdvancedBrep", Outer=ifc_shell)
            ifc_breps.append(ifc_brep)
        else:
            for shell in shells:
                outer_ifc_shell = model.create("IfcClosedShell", CfsFaces=build(shell))
                ifc_brep = model.create("IfcAdvancedBrep", Outer=outer_ifc_shell)
                ifc_breps.append(ifc_brep)

    return ifc_breps


def _build_shell_faces(shell, model, get_bspline, get_line, get_circle, get_ellipse, degenerate_edges=None):
    """Build the list of IfcAdvancedFace entities for one shell."""
    from OCC.Core.BRep import BRep_Tool as _BRep_Tool

    if degenerate_edges is None:
        degenerate_edges = set()

    ifc_faces = []

    for face in shell.faces:
        face_bounds = []
        is_outer_bound = True

        for loop in face.loops:
            ifc_oriented_edges = []

            for edge in loop.edges:
                # Skip degenerate edges (e.g. poles of spheres/cones) — they
                # have no geometric curve and must not appear in IfcEdgeLoop.
                if id(edge.occ_edge) in degenerate_edges or _BRep_Tool.Degenerated(edge.occ_edge):
                    continue

                oriented = edge.occ_edge.Orientation() == 0

                if edge.is_bspline:
                    IfcEdgeCurve = get_bspline(edge)
                elif edge.is_line:
                    IfcEdgeCurve = get_line(edge)
                elif edge.is_circle:
                    IfcEdgeCurve, _ = get_circle(edge)
                elif edge.is_ellipse:
                    IfcEdgeCurve, _ = get_ellipse(edge)
                else:
                    raise NotImplementedError(f"Unsupported edge type in face loop: {edge}")

                if IfcEdgeCurve is None:
                    raise ValueError(f"Edge not found in cache: {edge}")

                ifc_oriented_edges.append(model.create("IfcOrientedEdge", EdgeElement=IfcEdgeCurve, Orientation=oriented))

            if not ifc_oriented_edges:
                # Loop has no non-degenerate edges (e.g. degenerate pole loop); skip it.
                continue

            edge_loop = model.create("IfcEdgeLoop", EdgeList=ifc_oriented_edges)
            if is_outer_bound:
                face_bounds.append(model.create("IfcFaceOuterBound", Bound=edge_loop, Orientation=True))
                is_outer_bound = False
            else:
                face_bounds.append(model.create("IfcFaceBound", Bound=edge_loop, Orientation=False))

        same_sense = face.orientation == 0
        ifc_surface = _face_to_ifc_surface(face, model)
        ifc_faces.append(model.create("IfcAdvancedFace", Bounds=face_bounds, FaceSurface=ifc_surface, SameSense=same_sense))

    return ifc_faces


def _face_to_ifc_surface(face, model):
    """Convert one OCC BRep face to the appropriate IFC surface entity."""
    if face.is_plane:
        occ_plane = face.occ_adaptor.Plane()
        location = occ_plane.Location().Coord()
        x_axis = occ_plane.XAxis().Direction().Coord()
        y_axis = occ_plane.YAxis().Direction().Coord()
        return frame_to_IfcPlane(model, Frame(location, x_axis, y_axis))

    if face.is_cylinder:
        return occ_cylinder_to_ifc_cylindrical_surface(model, face.occ_adaptor.Cylinder())

    # IfcConicalSurface does not exist in IFC4 or IFC4X3; cones fall through to NURBS.

    if face.is_sphere:
        return occ_sphere_to_ifc_spherical_surface(model, face.occ_adaptor.Sphere())

    if face.is_torus:
        return occ_torus_to_ifc_toroidal_surface(model, face.occ_adaptor.Torus())

    # All other surface types fall through to NURBS representation
    return _face_to_ifc_nurbs_surface(face, model)


def _face_to_ifc_nurbs_surface(face, model):
    """Convert an OCC face to IfcRationalBSplineSurfaceWithKnots.

    Works directly with the OCC BSpline surface, converting the face via
    BRepBuilderAPI_NurbsConvert first if needed (e.g. for cone faces).
    """
    from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_NurbsConvert
    from OCC.Core.GeomAbs import GeomAbs_BSplineSurface

    # Convert to NURBS if not already BSpline.
    occ_face = face.occ_face
    adaptor = BRepAdaptor_Surface(occ_face)
    if adaptor.GetType() != GeomAbs_BSplineSurface:
        conv = BRepBuilderAPI_NurbsConvert(occ_face)
        conv.Build()
        occ_face = conv.Shape()
        adaptor = BRepAdaptor_Surface(occ_face)

    bspline = adaptor.BSpline()

    nu = bspline.NbUPoles()
    nv = bspline.NbVPoles()

    # Use the raw ifcopenshell file to create nested entity lists, since
    # model.create() only unwraps one level of Base wrappers.
    ifc_file = model._file._file

    def make_pt(u1, v1):
        pole = bspline.Pole(u1, v1)
        return ifc_file.create_entity("IfcCartesianPoint", Coordinates=(pole.X(), pole.Y(), pole.Z()))

    # ControlPointsList[u][v] in IFC matches Pole(u+1, v+1) in OCC (1-based)
    ifc_control_points = [[make_pt(u + 1, v + 1) for v in range(nv)] for u in range(nu)]

    u_knots, u_mults = calculate_knots_and_multiplicities(list(bspline.UKnotSequence()))
    v_knots, v_mults = calculate_knots_and_multiplicities(list(bspline.VKnotSequence()))

    is_periodic_u = bspline.IsUPeriodic()
    is_periodic_v = bspline.IsVPeriodic()

    if is_periodic_u:
        ifc_control_points.append(ifc_control_points[0])

    if is_periodic_v:
        for i, row in enumerate(ifc_control_points):
            row.append(ifc_control_points[i % nu][0])

    ifc_weights = [[bspline.Weight(u + 1, v + 1) for v in range(nv)] for u in range(nu)]

    if is_periodic_u:
        ifc_weights.append(ifc_weights[0])
    if is_periodic_v:
        for row in ifc_weights:
            row.append(row[0])

    entity = ifc_file.create_entity(
        "IfcRationalBSplineSurfaceWithKnots",
        UDegree=bspline.UDegree(),
        VDegree=bspline.VDegree(),
        ControlPointsList=ifc_control_points,
        SurfaceForm="UNSPECIFIED",
        UClosed=is_periodic_u,
        VClosed=is_periodic_v,
        SelfIntersect=False,
        UMultiplicities=u_mults,
        VMultiplicities=v_mults,
        UKnots=u_knots,
        VKnots=v_knots,
        KnotSpec="UNSPECIFIED",
        WeightsData=ifc_weights,
    )
    return model._file.from_entity(entity)


def _find_orphan_faces(brep):
    """Return a list of OCC faces present in the brep compound but not in any shell.

    After BRepBuilderAPI_Sewing, inner-void faces of a boolean-cut solid may be
    left as loose faces in the compound rather than being included in a shell.
    """
    from OCC.Core.TopAbs import TopAbs_FACE
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.TopoDS import topods

    shell_face_hashes = set()
    for shell in brep.shells:
        exp = TopExp_Explorer(shell.occ_shape, TopAbs_FACE)
        while exp.More():
            shell_face_hashes.add(exp.Current().__hash__())
            exp.Next()

    orphans = []
    exp = TopExp_Explorer(brep.occ_shape, TopAbs_FACE)
    while exp.More():
        face = exp.Current()
        if face.__hash__() not in shell_face_hashes:
            orphans.append(topods.Face(face))
        exp.Next()
    return orphans


def _build_orphan_faces(orphan_faces, model, get_bspline, get_line, get_circle, get_ellipse, degenerate_edges):
    """Convert orphan OCC faces (not in any shell) to IfcAdvancedFace entities."""
    from compas_occ.brep import OCCBrep
    from OCC.Core.BRep import BRep_Builder
    from OCC.Core.TopoDS import TopoDS_Shell

    builder = BRep_Builder()
    shell = TopoDS_Shell()
    builder.MakeShell(shell)
    for face in orphan_faces:
        builder.Add(shell, face)

    shell_brep = OCCBrep.from_native(shell)
    return _build_shell_faces(
        shell_brep,
        model,
        get_bspline,
        get_line,
        get_circle,
        get_ellipse,
        degenerate_edges,
    )
