"""
Read functions for converting IFC representation entities to COMPAS geometry.

This module parses the raw IFC entity graph (via ``Base.__getattr__`` delegation)
and returns native COMPAS geometry objects that preserve parametric data.

Every reader function returns ``None`` on failure so the caller can fall back
to the evaluated visual geometry.
"""

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Transformation
from compas.geometry import Vector

from compas_ifc.conversions.frame import IfcAxis2Placement2D_to_frame
from compas_ifc.conversions.frame import IfcAxis2Placement3D_to_frame
from compas_ifc.conversions.primitives import IfcCartesianPoint_to_point
from compas_ifc.conversions.primitives import IfcDirection_to_vector
from compas_ifc.representations import BooleanResult
from compas_ifc.representations import ClippedExtrusion
from compas_ifc.representations import Extrusion
from compas_ifc.representations import HalfSpace
from compas_ifc.representations import Pipe
from compas_ifc.representations import Revolution

# ==========================================================================
# Top-level entry point
# ==========================================================================


def read_body_representation(entity):
    """Parse the body representation of an IfcProduct into COMPAS geometry.

    Iterates over the ``"Body"`` representation items and returns the first
    successfully parsed geometry.  Returns ``None`` when nothing is parseable.

    Parameters
    ----------
    entity : :class:`~compas_ifc.entities.base.Base`
        An IfcProduct entity (wrapped by the Base class).

    Returns
    -------
    :class:`~compas.geometry.Geometry` | :class:`~compas.datastructures.Mesh` | None
    """
    rep = entity.Representation
    if rep is None:
        return None

    for shape_rep in rep.Representations:
        if shape_rep.RepresentationIdentifier == "Body":
            for item in shape_rep.Items:
                try:
                    result = read_representation_item(item)
                    if result is not None:
                        return result
                except Exception:
                    continue

    return None


def read_axis_representation(entity):
    """Parse the axis representation of an IfcProduct into a :class:`Polyline`.

    Looks for a representation with ``RepresentationIdentifier == "Axis"``
    and parses its curve items into a COMPAS Polyline.

    Parameters
    ----------
    entity : :class:`~compas_ifc.entities.base.Base`
        An IfcProduct entity (wrapped by the Base class).

    Returns
    -------
    :class:`~compas.geometry.Polyline` | None
    """
    rep = entity.Representation
    if rep is None:
        return None

    for shape_rep in rep.Representations:
        if shape_rep.RepresentationIdentifier == "Axis":
            for item in shape_rep.Items:
                try:
                    result = read_curve_to_polyline(item)
                    if result is not None:
                        return result
                except Exception:
                    continue

    return None


# ==========================================================================
# Item dispatcher
# ==========================================================================


def read_representation_item(item):
    """Dispatch a single IfcRepresentationItem to the appropriate reader.

    Parameters
    ----------
    item : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`~compas.geometry.Geometry` | :class:`~compas.datastructures.Mesh` | None
    """
    type_name = item.is_a()

    if type_name == "IfcExtrudedAreaSolid":
        return read_IfcExtrudedAreaSolid(item)
    elif type_name == "IfcCsgSolid":
        return read_IfcCsgSolid(item)
    elif type_name == "IfcFaceBasedSurfaceModel":
        return read_IfcFaceBasedSurfaceModel(item)
    elif type_name == "IfcPolygonalFaceSet":
        return read_IfcPolygonalFaceSet(item)
    elif type_name == "IfcTriangulatedFaceSet":
        return read_IfcTriangulatedFaceSet(item)
    elif type_name == "IfcRevolvedAreaSolid":
        return read_IfcRevolvedAreaSolid(item)
    elif type_name == "IfcSweptDiskSolid":
        return read_IfcSweptDiskSolid(item)
    elif type_name == "IfcMappedItem":
        return read_IfcMappedItem(item)
    elif type_name in ("IfcBooleanClippingResult", "IfcBooleanResult"):
        return read_IfcBooleanResult(item)
    else:
        return None


# ==========================================================================
# Extrusion
# ==========================================================================


def read_IfcExtrudedAreaSolid(eas):
    """Parse an IfcExtrudedAreaSolid into an :class:`Extrusion`.

    Parameters
    ----------
    eas : :class:`~compas_ifc.entities.base.Base`
        Wrapped ``IfcExtrudedAreaSolid``.

    Returns
    -------
    :class:`Extrusion` | None
    """
    profile = read_profile(eas.SweptArea)
    if profile is None:
        return None

    direction = IfcDirection_to_vector(eas.ExtrudedDirection)
    depth = float(eas.Depth)

    if eas.Position:
        frame = IfcAxis2Placement3D_to_frame(eas.Position)
    else:
        frame = Frame.worldXY()

    return Extrusion(profile=profile, direction=direction, depth=depth, frame=frame)


# ==========================================================================
# Revolution (IfcRevolvedAreaSolid)
# ==========================================================================


def read_IfcRevolvedAreaSolid(ras):
    """Parse an IfcRevolvedAreaSolid into a :class:`Revolution`.

    Parameters
    ----------
    ras : :class:`~compas_ifc.entities.base.Base`
        Wrapped ``IfcRevolvedAreaSolid``.

    Returns
    -------
    :class:`Revolution` | None
    """
    profile = read_profile(ras.SweptArea)
    if profile is None:
        return None

    # Revolution axis (IfcAxis1Placement → point + direction)
    axis_point = IfcCartesianPoint_to_point(ras.Axis.Location)
    if ras.Axis.Axis:
        axis_direction = IfcDirection_to_vector(ras.Axis.Axis)
    else:
        axis_direction = Vector.Zaxis()

    angle = float(ras.Angle)  # IFC stores angle in degrees

    if ras.Position:
        frame = IfcAxis2Placement3D_to_frame(ras.Position)
    else:
        frame = Frame.worldXY()

    return Revolution(
        profile=profile,
        axis_point=axis_point,
        axis_direction=axis_direction,
        angle=angle,
        frame=frame,
    )


# ==========================================================================
# Pipe (IfcSweptDiskSolid)
# ==========================================================================


def read_IfcSweptDiskSolid(sds):
    """Parse an IfcSweptDiskSolid into a :class:`Pipe`.

    Parameters
    ----------
    sds : :class:`~compas_ifc.entities.base.Base`
        Wrapped ``IfcSweptDiskSolid``.

    Returns
    -------
    :class:`Pipe` | None
    """
    directrix = read_curve_to_polyline(sds.Directrix)
    if directrix is None:
        return None

    radius = float(sds.Radius)
    inner_radius = float(sds.InnerRadius) if sds.InnerRadius else None

    return Pipe(
        directrix=directrix,
        radius=radius,
        inner_radius=inner_radius,
    )


# ==========================================================================
# Profiles
# ==========================================================================


def read_profile(profile_def):
    """Parse an IfcProfileDef into a COMPAS 2D geometry.

    Parameters
    ----------
    profile_def : :class:`~compas_ifc.entities.base.Base`
        Wrapped ``IfcProfileDef``.

    Returns
    -------
    :class:`Polygon` | :class:`Circle` | tuple[:class:`Polygon`, list[:class:`Polygon`]] | None
    """
    type_name = profile_def.is_a()

    if type_name == "IfcRectangleProfileDef":
        return read_IfcRectangleProfileDef(profile_def)
    elif type_name == "IfcCircleProfileDef":
        return read_IfcCircleProfileDef(profile_def)
    elif type_name == "IfcArbitraryClosedProfileDef":
        return read_IfcArbitraryClosedProfileDef(profile_def)
    elif type_name == "IfcArbitraryProfileDefWithVoids":
        return read_IfcArbitraryProfileDefWithVoids(profile_def)
    elif type_name == "IfcEllipseProfileDef":
        return read_IfcEllipseProfileDef(profile_def)
    else:
        return None


def read_IfcRectangleProfileDef(profile):
    """Parse an IfcRectangleProfileDef into a :class:`Polygon`.

    The rectangle is centred at the profile origin (before any 2D
    placement offset).

    Parameters
    ----------
    profile : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polygon`
    """
    hx = float(profile.XDim) / 2.0
    hy = float(profile.YDim) / 2.0
    pts = [
        Point(-hx, -hy, 0),
        Point(hx, -hy, 0),
        Point(hx, hy, 0),
        Point(-hx, hy, 0),
    ]

    if profile.Position:
        frame_2d = IfcAxis2Placement2D_to_frame(profile.Position)
        T = Transformation.from_frame(frame_2d)
        pts = [p.transformed(T) for p in pts]

    return Polygon(pts)


def read_IfcCircleProfileDef(profile):
    """Parse an IfcCircleProfileDef into a :class:`Circle`.

    Parameters
    ----------
    profile : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Circle`
    """
    radius = float(profile.Radius)
    if profile.Position:
        frame = IfcAxis2Placement2D_to_frame(profile.Position)
    else:
        frame = Frame.worldXY()
    return Circle(radius=radius, frame=frame)


def read_IfcEllipseProfileDef(profile):
    """Parse an IfcEllipseProfileDef into a :class:`Polygon` approximation.

    The ellipse is sampled into a polygon since COMPAS ``Ellipse`` does not
    directly support use as a profile.

    Parameters
    ----------
    profile : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polygon`
    """
    import math

    a = float(profile.SemiAxis1)
    b = float(profile.SemiAxis2)
    n = 32
    pts = [Point(a * math.cos(2 * math.pi * i / n), b * math.sin(2 * math.pi * i / n), 0) for i in range(n)]

    if profile.Position:
        frame_2d = IfcAxis2Placement2D_to_frame(profile.Position)
        T = Transformation.from_frame(frame_2d)
        pts = [p.transformed(T) for p in pts]

    return Polygon(pts)


def read_IfcArbitraryClosedProfileDef(profile):
    """Parse an IfcArbitraryClosedProfileDef into a :class:`Polygon`.

    Parameters
    ----------
    profile : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polygon` | None
    """
    return read_curve_to_polygon(profile.OuterCurve)


def read_IfcArbitraryProfileDefWithVoids(profile):
    """Parse an IfcArbitraryProfileDefWithVoids.

    Parameters
    ----------
    profile : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    tuple[:class:`Polygon`, list[:class:`Polygon`]] | None
    """
    outer = read_curve_to_polygon(profile.OuterCurve)
    if outer is None:
        return None

    inners = []
    for curve in profile.InnerCurves:
        inner = read_curve_to_polygon(curve)
        if inner is not None:
            inners.append(inner)

    return (outer, inners)


# ==========================================================================
# Curve helpers
# ==========================================================================


def read_curve_to_polygon(curve):
    """Parse an IfcCurve (IfcPolyline, IfcIndexedPolyCurve, etc.) into a :class:`Polygon`.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polygon` | None
    """
    type_name = curve.is_a()

    if type_name == "IfcPolyline":
        return _read_IfcPolyline_to_polygon(curve)
    elif type_name == "IfcIndexedPolyCurve":
        return _read_IfcIndexedPolyCurve_to_polygon(curve)
    elif type_name == "IfcCompositeCurve":
        return _read_IfcCompositeCurve_to_polygon(curve)
    elif type_name == "IfcTrimmedCurve":
        return _read_IfcTrimmedCurve_to_polygon(curve)
    else:
        return None


def _read_IfcPolyline_to_polygon(polyline):
    """Parse IfcPolyline into a :class:`Polygon`.

    Parameters
    ----------
    polyline : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polygon` | None
    """
    points = []
    for pt in polyline.Points:
        coords = list(pt.Coordinates)
        if len(coords) == 2:
            coords.append(0.0)
        points.append(Point(*coords))

    # Remove closing point if first == last
    if len(points) > 1 and points[0].distance_to_point(points[-1]) < 1e-10:
        points = points[:-1]

    if len(points) < 3:
        return None

    return Polygon(points)


def _read_IfcIndexedPolyCurve_to_polygon(curve):
    """Parse IfcIndexedPolyCurve into a :class:`Polygon`.

    Arc segments (IfcArcIndex) are linearised by connecting their
    endpoints.  A future revision could sample intermediate points.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polygon` | None
    """
    coord_list = curve.Points.CoordList

    if curve.Segments:
        ordered_indices = []
        for segment in curve.Segments:
            # Segments can be IfcLineIndex or IfcArcIndex, both are
            # wrapped as entity_instance with .wrappedValue
            seg = segment.wrappedValue if hasattr(segment, "wrappedValue") else segment
            # For IfcArcIndex (3 indices), take first and last to linearise
            if len(seg) == 3:
                indices = [seg[0], seg[2]]
            else:
                indices = list(seg)
            for idx in indices:
                if not ordered_indices or ordered_indices[-1] != idx:
                    ordered_indices.append(idx)
        points = []
        for i in ordered_indices:
            coords = list(coord_list[i - 1])
            if len(coords) == 2:
                coords.append(0.0)
            points.append(Point(*coords))
    else:
        points = []
        for c in coord_list:
            coords = list(c)
            if len(coords) == 2:
                coords.append(0.0)
            points.append(Point(*coords))

    # Remove closing point
    if len(points) > 1 and points[0].distance_to_point(points[-1]) < 1e-10:
        points = points[:-1]

    if len(points) < 3:
        return None

    return Polygon(points)


def _read_IfcCompositeCurve_to_polygon(curve):
    """Parse IfcCompositeCurve into a :class:`Polygon`.

    Iterates over the curve segments and extracts points from each
    parent curve.  Handles ``IfcTrimmedCurve`` segments (arcs/fillets)
    by sampling intermediate points.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polygon` | None
    """
    points = []
    for segment in curve.Segments:
        parent_curve = segment.ParentCurve
        segment_points = _read_curve_to_points(parent_curve)
        if segment_points:
            # Check Transition flag for orientation (SameSense)
            same_sense = getattr(segment, "SameSense", True)
            if not same_sense:
                segment_points = list(reversed(segment_points))
            for pt in segment_points:
                if not points or Point(*pt).distance_to_point(Point(*points[-1])) > 1e-10:
                    points.append(pt)

    # Remove closing point
    if len(points) > 1 and Point(*points[0]).distance_to_point(Point(*points[-1])) < 1e-10:
        points = points[:-1]

    if len(points) < 3:
        return None

    return Polygon(points)


# ==========================================================================
# Polyline helpers (for axis / path representations)
# ==========================================================================


def read_curve_to_polyline(curve):
    """Parse an IfcCurve into a :class:`Polyline` (open curve with 2+ points).

    Unlike :func:`read_curve_to_polygon` (for closed profiles), this returns
    a :class:`Polyline` suitable for axis/path representations.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polyline` | None
    """
    type_name = curve.is_a()

    if type_name == "IfcPolyline":
        return _read_IfcPolyline_to_polyline(curve)
    elif type_name == "IfcIndexedPolyCurve":
        return _read_IfcIndexedPolyCurve_to_polyline(curve)
    elif type_name == "IfcCompositeCurve":
        return _read_IfcCompositeCurve_to_polyline(curve)
    elif type_name == "IfcTrimmedCurve":
        return _read_IfcTrimmedCurve_to_polyline(curve)
    else:
        return None


def _read_IfcPolyline_to_polyline(polyline):
    """Parse IfcPolyline into a :class:`Polyline`.

    Parameters
    ----------
    polyline : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polyline` | None
    """
    points = []
    for pt in polyline.Points:
        coords = list(pt.Coordinates)
        if len(coords) == 2:
            coords.append(0.0)
        points.append(Point(*coords))

    if len(points) < 2:
        return None

    return Polyline(points)


def _read_IfcIndexedPolyCurve_to_polyline(curve):
    """Parse IfcIndexedPolyCurve into a :class:`Polyline`.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polyline` | None
    """
    coord_list = curve.Points.CoordList

    if curve.Segments:
        ordered_indices = []
        for segment in curve.Segments:
            seg = segment.wrappedValue if hasattr(segment, "wrappedValue") else segment
            if len(seg) == 3:
                indices = [seg[0], seg[2]]
            else:
                indices = list(seg)
            for idx in indices:
                if not ordered_indices or ordered_indices[-1] != idx:
                    ordered_indices.append(idx)
        points = []
        for i in ordered_indices:
            coords = list(coord_list[i - 1])
            if len(coords) == 2:
                coords.append(0.0)
            points.append(Point(*coords))
    else:
        points = []
        for c in coord_list:
            coords = list(c)
            if len(coords) == 2:
                coords.append(0.0)
            points.append(Point(*coords))

    if len(points) < 2:
        return None

    return Polyline(points)


def _read_IfcCompositeCurve_to_polyline(curve):
    """Parse IfcCompositeCurve into a :class:`Polyline`.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polyline` | None
    """
    points = []
    for segment in curve.Segments:
        parent_curve = segment.ParentCurve
        segment_points = _read_curve_to_points(parent_curve)
        if segment_points:
            same_sense = getattr(segment, "SameSense", True)
            if not same_sense:
                segment_points = list(reversed(segment_points))
            for pt in segment_points:
                if not points or Point(*pt).distance_to_point(Point(*points[-1])) > 1e-10:
                    points.append(pt)

    if len(points) < 2:
        return None

    return Polyline(points)


def _read_IfcTrimmedCurve_to_polyline(curve):
    """Parse IfcTrimmedCurve into a :class:`Polyline`.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polyline` | None
    """
    pts = _read_trimmed_curve_points(curve)
    if pts and len(pts) >= 2:
        return Polyline(pts)
    return None


def _read_IfcTrimmedCurve_to_polygon(curve):
    """Parse IfcTrimmedCurve into a :class:`Polygon`.

    Samples the trimmed curve (usually a circular arc) into line
    segments.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Polygon` | None
    """
    pts = _read_trimmed_curve_points(curve)
    if pts and len(pts) >= 3:
        return Polygon(pts)
    return None


def _read_curve_to_points(curve):
    """Extract ordered points from a curve segment.

    Used by ``_read_IfcCompositeCurve_to_polygon`` for each segment's
    ParentCurve.

    Parameters
    ----------
    curve : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    list[:class:`Point`]
    """
    type_name = curve.is_a()

    if type_name == "IfcPolyline":
        points = []
        for pt in curve.Points:
            coords = list(pt.Coordinates)
            if len(coords) == 2:
                coords.append(0.0)
            points.append(Point(*coords))
        return points

    elif type_name == "IfcTrimmedCurve":
        return _read_trimmed_curve_points(curve)

    elif type_name == "IfcLine":
        # A line segment doesn't make sense standalone in a composite curve
        # but we handle it for robustness
        pnt = Point(*curve.Pnt.Coordinates)
        d = Vector(*curve.Dir.Orientation.DirectionRatios)
        d *= float(curve.Dir.Magnitude)
        return [pnt, pnt + d]

    else:
        # Unsupported curve type — try to recurse via polygon helper
        poly = read_curve_to_polygon(curve)
        if poly is not None:
            return [Point(*p) for p in poly.points]
        return []


def _read_trimmed_curve_points(trimmed_curve, n=8):
    """Sample points from an IfcTrimmedCurve.

    For circular arcs, samples *n* intermediate points between the
    trim parameters.  For other basis curves, returns the trim
    endpoints only.

    Parameters
    ----------
    trimmed_curve : :class:`~compas_ifc.entities.base.Base`
    n : int
        Number of segments for arc sampling.

    Returns
    -------
    list[:class:`Point`]
    """
    import math

    basis = trimmed_curve.BasisCurve
    sense = trimmed_curve.SenseAgreement
    trim1 = trimmed_curve.Trim1
    trim2 = trimmed_curve.Trim2

    if basis.is_a() == "IfcCircle":
        # Extract circle parameters
        radius = float(basis.Radius)
        if basis.Position:
            frame = IfcAxis2Placement2D_to_frame(basis.Position) if basis.Position.is_a("IfcAxis2Placement2D") else IfcAxis2Placement3D_to_frame(basis.Position)
        else:
            frame = Frame.worldXY()

        # Extract parameter values from Trim1/Trim2
        # Trims can be IfcParameterValue (float angle in radians/degrees)
        # or IfcCartesianPoint
        angle1 = _extract_trim_parameter(trim1, frame, radius)
        angle2 = _extract_trim_parameter(trim2, frame, radius)

        if angle1 is None or angle2 is None:
            return _extract_trim_points(trim1, trim2)

        # Ensure correct sweep direction
        if sense:
            if angle2 <= angle1:
                angle2 += 2 * math.pi
        else:
            if angle1 <= angle2:
                angle1 += 2 * math.pi

        # Sample arc points
        T = Transformation.from_frame(frame)
        points = []
        for i in range(n + 1):
            t = angle1 + (angle2 - angle1) * i / n
            px = radius * math.cos(t)
            py = radius * math.sin(t)
            pt = Point(px, py, 0.0)
            pt.transform(T)
            points.append(pt)

        return points

    else:
        # For non-circle basis curves, just return the endpoints
        return _extract_trim_points(trim1, trim2)


def _extract_trim_parameter(trim, frame, radius):
    """Extract a parameter angle from an IfcTrimmingSelect.

    Parameters
    ----------
    trim : list
        The Trim1 or Trim2 value (list of IfcTrimmingSelect).
    frame : :class:`Frame`
    radius : float

    Returns
    -------
    float | None
        Angle in radians, or None if only a point was provided.
    """
    import math

    for t in trim:
        # Check if it's a parameter value (float)
        if isinstance(t, (int, float)):
            # IFC angles may be in degrees or radians depending on context
            # Most common is degrees for IfcTrimmedCurve
            return math.radians(float(t))
        # Check for wrapped value (ifcopenshell wrapping)
        if hasattr(t, "wrappedValue"):
            val = t.wrappedValue
            if isinstance(val, (int, float)):
                return math.radians(float(val))

    # Try extracting from Cartesian point
    for t in trim:
        if hasattr(t, "Coordinates"):
            coords = list(t.Coordinates)
            if len(coords) >= 2:
                # Compute angle from center
                T_inv = Transformation.from_frame(frame).inverse()
                pt = Point(*coords, 0.0) if len(coords) == 2 else Point(*coords)
                pt.transform(T_inv)
                return math.atan2(pt.y, pt.x)

    return None


def _extract_trim_points(trim1, trim2):
    """Extract Cartesian endpoints from IfcTrimmingSelect values.

    Parameters
    ----------
    trim1 : list
    trim2 : list

    Returns
    -------
    list[:class:`Point`]
    """
    points = []
    for trim in [trim1, trim2]:
        for t in trim:
            if hasattr(t, "Coordinates"):
                coords = list(t.Coordinates)
                if len(coords) == 2:
                    coords.append(0.0)
                points.append(Point(*coords))
                break
    return points


# ==========================================================================
# CSG primitives
# ==========================================================================


def read_IfcCsgSolid(csg):
    """Parse an IfcCsgSolid into COMPAS geometry.

    Handles two cases for ``TreeRootExpression``:

    * **Primitive** — ``IfcBlock``, ``IfcSphere``, ``IfcRightCircularCone``,
      ``IfcRightCircularCylinder`` are converted to COMPAS shape primitives.
    * **Boolean tree** — ``IfcBooleanResult`` or ``IfcBooleanClippingResult``
      is parsed recursively into a :class:`BooleanResult` (or
      :class:`ClippedExtrusion` when the clipping pattern matches).

    Parameters
    ----------
    csg : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Box` | :class:`Sphere` | :class:`Cone` | :class:`Cylinder` | :class:`BooleanResult` | :class:`ClippedExtrusion` | None
    """
    root = csg.TreeRootExpression
    type_name = root.is_a()

    if type_name == "IfcBlock":
        return read_IfcBlock(root)
    elif type_name == "IfcSphere":
        return read_IfcSphere(root)
    elif type_name == "IfcRightCircularCone":
        return read_IfcRightCircularCone(root)
    elif type_name == "IfcRightCircularCylinder":
        return read_IfcRightCircularCylinder(root)
    elif type_name in ("IfcBooleanResult", "IfcBooleanClippingResult"):
        return read_IfcBooleanResult(root)
    else:
        return None


def read_IfcBlock(block):
    """Parse an IfcBlock into a :class:`Box`.

    ``IfcBlock.Position`` is at the corner.
    ``Box.frame`` is at the centre.  We offset accordingly.

    Parameters
    ----------
    block : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Box`
    """
    frame = IfcAxis2Placement3D_to_frame(block.Position)
    x = float(block.XLength)
    y = float(block.YLength)
    z = float(block.ZLength)

    # Shift from corner to centre in local coordinates
    offset = frame.xaxis * (x / 2) + frame.yaxis * (y / 2) + frame.zaxis * (z / 2)
    center = frame.point + offset
    box_frame = Frame(center, frame.xaxis, frame.yaxis)

    return Box(xsize=x, ysize=y, zsize=z, frame=box_frame)


def read_IfcSphere(sphere):
    """Parse an IfcSphere into a :class:`Sphere`.

    Parameters
    ----------
    sphere : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Sphere`
    """
    frame = IfcAxis2Placement3D_to_frame(sphere.Position)
    return Sphere(radius=float(sphere.Radius), frame=frame)


def read_IfcRightCircularCone(cone):
    """Parse an IfcRightCircularCone into a :class:`Cone`.

    Parameters
    ----------
    cone : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Cone`
    """
    frame = IfcAxis2Placement3D_to_frame(cone.Position)
    return Cone(radius=float(cone.BottomRadius), height=float(cone.Height), frame=frame)


def read_IfcRightCircularCylinder(cylinder):
    """Parse an IfcRightCircularCylinder into a :class:`Cylinder`.

    Parameters
    ----------
    cylinder : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Cylinder`
    """
    frame = IfcAxis2Placement3D_to_frame(cylinder.Position)
    return Cylinder(radius=float(cylinder.Radius), height=float(cylinder.Height), frame=frame)


# ==========================================================================
# Boolean clipping
# ==========================================================================


def read_IfcBooleanResult(item):
    """Parse an ``IfcBooleanResult`` or ``IfcBooleanClippingResult`` into
    parametric COMPAS geometry.

    First tries the :class:`ClippedExtrusion` fast-path (extrusion clipped
    by half-space planes).  If that pattern does not match, falls back to
    a generic :class:`BooleanResult` that preserves the full CSG tree.

    Parameters
    ----------
    item : :class:`~compas_ifc.entities.base.Base`
        Wrapped ``IfcBooleanClippingResult`` or ``IfcBooleanResult``.

    Returns
    -------
    :class:`ClippedExtrusion` | :class:`BooleanResult` | None
    """
    # Fast path: try ClippedExtrusion (extrusion + half-space chain)
    clipped = _try_clipped_extrusion(item)
    if clipped is not None:
        return clipped

    # Generic path: recursive BooleanResult tree
    return _read_boolean_result_generic(item)


def _try_clipped_extrusion(bcr):
    """Try to parse a boolean chain as a :class:`ClippedExtrusion`.

    Walks the ``FirstOperand`` chain collecting ``IfcHalfSpaceSolid``
    clipping planes.  Succeeds only if *every* ``SecondOperand`` is a
    half-space and the leaf ``FirstOperand`` is an ``IfcExtrudedAreaSolid``.

    Parameters
    ----------
    bcr : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`ClippedExtrusion` | None
    """
    clipping_planes = []

    # Walk the recursive chain
    current = bcr
    while current.is_a() in ("IfcBooleanClippingResult", "IfcBooleanResult"):
        second = current.SecondOperand
        plane_data = _read_half_space_tuple(second)
        if plane_data is None:
            return None  # non-half-space operand -> not a ClippedExtrusion
        clipping_planes.append(plane_data)
        current = current.FirstOperand

    # The leaf must be an IfcExtrudedAreaSolid
    if current.is_a() != "IfcExtrudedAreaSolid":
        return None

    extrusion = read_IfcExtrudedAreaSolid(current)
    if extrusion is None:
        return None

    return ClippedExtrusion(
        extrusion=extrusion,
        clipping_planes=clipping_planes,
    )


def _read_boolean_result_generic(item):
    """Parse a boolean result node into a :class:`BooleanResult`.

    Recursively reads both operands via :func:`_read_boolean_operand`.

    Parameters
    ----------
    item : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`BooleanResult` | None
    """
    type_name = item.is_a()
    if type_name not in ("IfcBooleanClippingResult", "IfcBooleanResult"):
        return None

    operator = str(item.Operator)

    first = _read_boolean_operand(item.FirstOperand)
    if first is None:
        return None

    second = _read_boolean_operand(item.SecondOperand)
    if second is None:
        return None

    return BooleanResult(
        operator=operator,
        first_operand=first,
        second_operand=second,
    )


def _read_boolean_operand(item):
    """Read a boolean operand into COMPAS geometry.

    Dispatches based on the IFC entity type.  Supports all solid model
    types that can appear as ``IfcBooleanOperand``.

    Parameters
    ----------
    item : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`~compas.geometry.Geometry` | None
    """
    type_name = item.is_a()

    # Recursive boolean
    if type_name in ("IfcBooleanClippingResult", "IfcBooleanResult"):
        return read_IfcBooleanResult(item)

    # Half-space solids
    if type_name in ("IfcHalfSpaceSolid", "IfcPolygonalBoundedHalfSpace"):
        return _read_half_space(item)

    # Extrusion
    if type_name == "IfcExtrudedAreaSolid":
        return read_IfcExtrudedAreaSolid(item)

    # Revolution
    if type_name == "IfcRevolvedAreaSolid":
        return read_IfcRevolvedAreaSolid(item)

    # Swept disk
    if type_name == "IfcSweptDiskSolid":
        return read_IfcSweptDiskSolid(item)

    # CSG primitives
    if type_name == "IfcBlock":
        return read_IfcBlock(item)
    if type_name == "IfcSphere":
        return read_IfcSphere(item)
    if type_name == "IfcRightCircularCone":
        return read_IfcRightCircularCone(item)
    if type_name == "IfcRightCircularCylinder":
        return read_IfcRightCircularCylinder(item)

    # CSG solid container
    if type_name == "IfcCsgSolid":
        return read_IfcCsgSolid(item)

    # Unsupported operand type
    return None


def _read_half_space(item):
    """Read an ``IfcHalfSpaceSolid`` into a :class:`HalfSpace` geometry.

    Also handles ``IfcPolygonalBoundedHalfSpace`` (ignores the boundary
    polygon — the boundary is a precision optimisation, not essential
    for parametric data).

    Parameters
    ----------
    item : :class:`~compas_ifc.entities.base.Base`
        Wrapped ``IfcHalfSpaceSolid`` or ``IfcPolygonalBoundedHalfSpace``.

    Returns
    -------
    :class:`HalfSpace` | None
    """
    from compas.geometry import Plane

    type_name = item.is_a()
    if type_name not in ("IfcHalfSpaceSolid", "IfcPolygonalBoundedHalfSpace"):
        return None

    surface = item.BaseSurface
    frame = IfcAxis2Placement3D_to_frame(surface.Position)
    plane = Plane(frame.point, frame.zaxis)
    agreement = bool(item.AgreementFlag)
    return HalfSpace(plane=plane, agreement_flag=agreement)


def _read_half_space_tuple(item):
    """Read an ``IfcHalfSpaceSolid`` into a ``(Plane, agreement_flag)`` tuple.

    Used by :func:`_try_clipped_extrusion` for backwards compatibility
    with the :class:`ClippedExtrusion` data format.

    Parameters
    ----------
    item : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    tuple[:class:`Plane`, bool] | None
    """
    from compas.geometry import Plane

    type_name = item.is_a()
    if type_name not in ("IfcHalfSpaceSolid", "IfcPolygonalBoundedHalfSpace"):
        return None

    # Read the IfcPlane.Position (IfcAxis2Placement3D) -> Frame -> Plane
    # We use the frame approach instead of IfcPlane_to_plane because
    # the .P derived attribute is not available through the Base wrapper.
    surface = item.BaseSurface
    frame = IfcAxis2Placement3D_to_frame(surface.Position)
    plane = Plane(frame.point, frame.zaxis)
    agreement = bool(item.AgreementFlag)
    return (plane, agreement)


# ==========================================================================
# Mesh readers
# ==========================================================================


def read_IfcFaceBasedSurfaceModel(fbsm):
    """Parse an IfcFaceBasedSurfaceModel into a :class:`Mesh`.

    Parameters
    ----------
    fbsm : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Mesh`
    """
    mesh = Mesh()
    vertex_map = {}

    for face_set in fbsm.FbsmFaces:
        for face in face_set.CfsFaces:
            face_vertices = []
            for bound in face.Bounds:
                loop = bound.Bound
                for pt in loop.Polygon:
                    coords = tuple(round(float(c), 10) for c in pt.Coordinates)
                    if coords not in vertex_map:
                        vertex_map[coords] = mesh.add_vertex(x=coords[0], y=coords[1], z=coords[2])
                    face_vertices.append(vertex_map[coords])
            if len(face_vertices) >= 3:
                try:
                    mesh.add_face(face_vertices)
                except Exception:
                    pass
    return mesh


def read_IfcPolygonalFaceSet(pfs):
    """Parse an IfcPolygonalFaceSet into a :class:`Mesh`.

    Parameters
    ----------
    pfs : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Mesh`
    """
    coord_list = pfs.Coordinates.CoordList
    vertices = [[float(x), float(y), float(z)] for x, y, z in coord_list]
    faces = [[i - 1 for i in face.CoordIndex] for face in pfs.Faces]
    return Mesh.from_vertices_and_faces(vertices, faces)


def read_IfcTriangulatedFaceSet(tfs):
    """Parse an IfcTriangulatedFaceSet into a :class:`Mesh`.

    Parameters
    ----------
    tfs : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Mesh`
    """
    coord_list = tfs.Coordinates.CoordList
    vertices = [[float(x), float(y), float(z)] for x, y, z in coord_list]
    faces = [[a - 1, b - 1, c - 1] for a, b, c in tfs.CoordIndex]
    return Mesh.from_vertices_and_faces(vertices, faces)


# ==========================================================================
# Mapped item
# ==========================================================================

_MAPPED_GEOMETRY_CACHE = {}  # IfcRepresentationMap entity id -> parsed template geometry


def read_IfcMappedItem(mapped_item):
    """Unwrap an IfcMappedItem and return the parsed inner geometry.

    Template geometry is cached by ``IfcRepresentationMap`` entity id so that
    multiple instances sharing the same map parse the inner geometry only once.
    Each call returns a *copy* of the template with the per-instance transform
    applied.

    Parameters
    ----------
    mapped_item : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`~compas.geometry.Geometry` | :class:`~compas.datastructures.Mesh` | None
    """
    source = mapped_item.MappingSource
    target = mapped_item.MappingTarget
    map_id = source.entity.id()

    # Look up or parse the template geometry (once per IfcRepresentationMap)
    if map_id in _MAPPED_GEOMETRY_CACHE:
        geom = _MAPPED_GEOMETRY_CACHE[map_id]
    else:
        inner_rep = source.MappedRepresentation
        geom = None
        for item in inner_rep.Items:
            try:
                geom = read_representation_item(item)
                if geom is not None:
                    break
            except Exception:
                continue
        _MAPPED_GEOMETRY_CACHE[map_id] = geom

    if geom is None:
        return None

    # Always copy since the template is shared across instances
    geom_copy = geom.copy() if hasattr(geom, "copy") else geom

    # Apply the per-instance transform
    T = _mapped_item_transformation(source.MappingOrigin, target)
    if T is not None:
        geom_copy.transform(T)

    return geom_copy


def _mapped_item_transformation(mapping_origin, mapping_target):
    """Compute the combined transformation from MappingOrigin and MappingTarget.

    Parameters
    ----------
    mapping_origin : :class:`~compas_ifc.entities.base.Base`
        ``IfcAxis2Placement3D`` from the representation map.
    mapping_target : :class:`~compas_ifc.entities.base.Base`
        ``IfcCartesianTransformationOperator3D`` from the mapped item.

    Returns
    -------
    :class:`Transformation` | None
    """
    T_origin = Transformation()
    T_target = Transformation()

    if mapping_origin:
        try:
            frame_origin = IfcAxis2Placement3D_to_frame(mapping_origin)
            T_origin = Transformation.from_frame(frame_origin)
        except Exception:
            pass

    if mapping_target:
        try:
            T_target = _cartesian_transform_operator_to_transformation(mapping_target)
        except Exception:
            pass

    combined = T_target * T_origin

    # Skip identity transforms
    if combined == Transformation():
        return None

    return combined


def _cartesian_transform_operator_to_transformation(op):
    """Convert an IfcCartesianTransformationOperator3D to a :class:`Transformation`.

    Parameters
    ----------
    op : :class:`~compas_ifc.entities.base.Base`

    Returns
    -------
    :class:`Transformation`
    """
    origin = Point(*op.LocalOrigin.Coordinates)

    ax1 = Vector(*op.Axis1.DirectionRatios) if op.Axis1 else Vector.Xaxis()
    ax2 = Vector(*op.Axis2.DirectionRatios) if op.Axis2 else Vector.Yaxis()

    # For 3D operators, Axis3 may be present
    if getattr(op, "Axis3", None) and op.Axis3:
        # ax3 provided
        pass
    # Otherwise Z is derived from X cross Y (already handled by Frame)

    scale = float(op.Scale) if op.Scale else 1.0

    frame = Frame(origin, ax1, ax2)
    T = Transformation.from_frame(frame)

    if abs(scale - 1.0) > 1e-10:
        from compas.geometry import Scale as ScaleTransform

        S = ScaleTransform.from_factors([scale, scale, scale])
        T = T * S

    return T
