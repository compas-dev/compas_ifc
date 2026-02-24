"""
This module contains functions for converting geometry representations between COMPAS and IFC.
"""

from typing import Union

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Shape
from compas.geometry import Sphere
from compas.geometry import Torus

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Polygon
from compas.geometry import Polyline

from compas_ifc.conversions.brep import brep_to_IfcAdvancedBrep
from compas_ifc.conversions.mesh import mesh_to_IfcFaceBasedSurfaceModel
from compas_ifc.conversions.mesh import mesh_to_IfcPolygonalFaceSet
from compas_ifc.conversions.shapes import box_to_IfcBlock
from compas_ifc.conversions.shapes import cone_to_IfcRightCircularCone
from compas_ifc.conversions.shapes import cylinder_to_IfcRightCircularCylinder
from compas_ifc.conversions.shapes import sphere_to_IfcSphere
from compas_ifc.entities.extensions import IfcProduct
from compas_ifc.model import Model
from compas_ifc.representations import BooleanResult
from compas_ifc.representations import ClippedExtrusion
from compas_ifc.representations import Extrusion
from compas_ifc.representations import HalfSpace
from compas_ifc.representations import Pipe
from compas_ifc.representations import Revolution

REPRESENTATION_CACHE = {}
SHAPE_REP_CACHE = {}
REPRESENTATION_MAP_CACHE = {}


def assign_body_representation(entity: IfcProduct, representation: Union[Shape, Mesh, Brep]):
    """Assign a body representation to an entity.

    When the same geometry Python object (same ``id()``) is assigned to
    multiple entities, proper IFC instancing is used automatically:

    - **1st use**: creates a direct ``IfcShapeRepresentation`` with the
      geometry items and stores the inner shape rep for potential reuse.
    - **2nd use**: promotes the geometry to an instanced representation by
      creating an ``IfcRepresentationMap`` from the stored inner shape rep,
      then assigns an ``IfcMappedItem`` to this entity.
    - **3rd+ use**: reuses the existing map and creates a new
      ``IfcMappedItem`` for each additional entity.

    Parameters
    ----------
    entity : :class:`IfcProduct`
    representation : :class:`Shape` | :class:`Mesh` | :class:`Brep` | :class:`Extrusion`
    """
    model: Model = entity.model
    geom_id = id(representation)

    if geom_id in REPRESENTATION_MAP_CACHE:
        # 3rd+ use: reuse existing map -> new MappedItem
        _assign_mapped_body(model, entity, REPRESENTATION_MAP_CACHE[geom_id])
        return

    if geom_id in SHAPE_REP_CACHE:
        # 2nd use: promote to instanced representation
        inner_rep = SHAPE_REP_CACHE[geom_id]
        rep_map = _create_representation_map(model, inner_rep)
        REPRESENTATION_MAP_CACHE[geom_id] = rep_map
        _assign_mapped_body(model, entity, rep_map)
        return

    # 1st use: direct representation (no map overhead for single-use geometry)
    items, representation_type = _geometry_to_ifc_items(model, representation)

    ifc_shape_representation = model.create(
        "IfcShapeRepresentation",
        ContextOfItems=model.file.default_body_context,
        RepresentationIdentifier="Body",
        RepresentationType=representation_type,
        Items=items,
    )

    SHAPE_REP_CACHE[geom_id] = ifc_shape_representation

    ifc_product_definition_shape = model.create(
        "IfcProductDefinitionShape",
        Representations=[ifc_shape_representation],
    )

    entity.Representation = ifc_product_definition_shape
    REPRESENTATION_CACHE[geom_id] = ifc_product_definition_shape


def _geometry_to_ifc_items(model: Model, representation):
    """Convert a COMPAS geometry object to IFC representation items.

    Parameters
    ----------
    model : :class:`Model`
    representation : :class:`Shape` | :class:`Mesh` | :class:`Brep` | :class:`Extrusion`

    Returns
    -------
    tuple[list, str]
        A tuple of ``(items, representation_type)`` where *items* is a list
        of IFC representation items and *representation_type* is the IFC
        representation type string (e.g. ``"SweptSolid"``, ``"CSG"``).
    """
    if isinstance(representation, BooleanResult):
        ifc_boolean = boolean_result_to_IfcBooleanResult(model, representation)
        return [ifc_boolean], "CSG"

    if isinstance(representation, ClippedExtrusion):
        ifc_boolean = clipped_extrusion_to_IfcBooleanClippingResult(model, representation)
        return [ifc_boolean], "Clipping"

    if isinstance(representation, Extrusion):
        ifc_extruded = extrusion_to_IfcExtrudedAreaSolid(model, representation)
        return [ifc_extruded], "SweptSolid"

    if isinstance(representation, Revolution):
        ifc_revolved = revolution_to_IfcRevolvedAreaSolid(model, representation)
        return [ifc_revolved], "SweptSolid"

    if isinstance(representation, Pipe):
        ifc_pipe = pipe_to_IfcSweptDiskSolid(model, representation)
        return [ifc_pipe], "SweptSolid"

    if isinstance(representation, Shape):
        if isinstance(representation, Box):
            ifc_csg_primitive3d = box_to_IfcBlock(model, representation)
        elif isinstance(representation, Sphere):
            ifc_csg_primitive3d = sphere_to_IfcSphere(model, representation)
        elif isinstance(representation, Cone):
            ifc_csg_primitive3d = cone_to_IfcRightCircularCone(model, representation)
        elif isinstance(representation, Cylinder):
            ifc_csg_primitive3d = cylinder_to_IfcRightCircularCylinder(model, representation)
        elif isinstance(representation, (Torus, Capsule)):
            # No CSG primitive in IFC — try B-Rep via OCC, fall back to mesh
            try:
                brep = representation.to_brep()
                items = brep_to_IfcAdvancedBrep(model, brep)
                return items, "SolidModel"
            except NotImplementedError:
                vertices, faces = representation.to_vertices_and_faces()
                mesh = Mesh.from_vertices_and_faces(vertices, faces)
                ifc_representation = mesh_to_IfcPolygonalFaceSet(model, mesh)
                return [ifc_representation], "Tessellation"
        else:
            raise NotImplementedError(f"Conversion of {type(representation)} to IFC not implemented.")

        ifc_csg_solid = model.create("IfcCsgSolid", TreeRootExpression=ifc_csg_primitive3d)
        return [ifc_csg_solid], "CSG"

    if isinstance(representation, Mesh):
        ifc_representation = mesh_to_IfcPolygonalFaceSet(model, representation)
        return [ifc_representation], "Tessellation"

    if isinstance(representation, Brep):
        if model.file.use_occ:
            items = brep_to_IfcAdvancedBrep(model, representation)
            return items, "SolidModel"
        else:
            mesh, _ = representation.to_tesselation()
            ifc_representation = mesh_to_IfcPolygonalFaceSet(model, mesh)
            return [ifc_representation], "Tessellation"

    raise NotImplementedError(f"Conversion of {type(representation)} to IFC not implemented.")


def read_representation(model: Model, entity: IfcProduct):
    """Read the body representation of an entity into COMPAS geometry.

    See :func:`compas_ifc.conversions.reading.read_body_representation`
    for the full implementation.
    """
    from compas_ifc.conversions.reading import read_body_representation

    return read_body_representation(entity)


# ==========================================================================
# Instancing helpers
# ==========================================================================


def _create_representation_map(model: Model, inner_shape_rep):
    """Create an ``IfcRepresentationMap`` wrapping an inner ``IfcShapeRepresentation``.

    The mapping origin is set to the world origin (identity placement).

    Parameters
    ----------
    model : :class:`Model`
    inner_shape_rep : :class:`~compas_ifc.entities.base.Base`
        The ``IfcShapeRepresentation`` containing the actual geometry items.

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
        The ``IfcRepresentationMap``.
    """
    from compas_ifc.conversions.frame import create_IfcAxis2Placement3D

    origin = create_IfcAxis2Placement3D(model)
    return model.create(
        "IfcRepresentationMap",
        MappingOrigin=origin,
        MappedRepresentation=inner_shape_rep,
    )


def _create_identity_transform_operator(model: Model):
    """Create an identity ``IfcCartesianTransformationOperator3D``.

    Parameters
    ----------
    model : :class:`Model`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    return model.create(
        "IfcCartesianTransformationOperator3D",
        Axis1=model.create("IfcDirection", DirectionRatios=(1.0, 0.0, 0.0)),
        Axis2=model.create("IfcDirection", DirectionRatios=(0.0, 1.0, 0.0)),
        LocalOrigin=model.create("IfcCartesianPoint", Coordinates=(0.0, 0.0, 0.0)),
        Scale=1.0,
        Axis3=model.create("IfcDirection", DirectionRatios=(0.0, 0.0, 1.0)),
    )


def _assign_mapped_body(model: Model, entity: IfcProduct, rep_map):
    """Create an ``IfcMappedItem`` referencing a shared map and assign to entity.

    Creates the full chain: ``IfcMappedItem`` -> ``IfcShapeRepresentation``
    (type ``"MappedRepresentation"``) -> ``IfcProductDefinitionShape``.

    Parameters
    ----------
    model : :class:`Model`
    entity : :class:`IfcProduct`
    rep_map : :class:`~compas_ifc.entities.base.Base`
        The ``IfcRepresentationMap`` to reference.
    """
    target = _create_identity_transform_operator(model)
    mapped_item = model.create(
        "IfcMappedItem",
        MappingSource=rep_map,
        MappingTarget=target,
    )

    outer_rep = model.create(
        "IfcShapeRepresentation",
        ContextOfItems=model.file.default_body_context,
        RepresentationIdentifier="Body",
        RepresentationType="MappedRepresentation",
        Items=[mapped_item],
    )

    pds = model.create(
        "IfcProductDefinitionShape",
        Representations=[outer_rep],
    )
    entity.Representation = pds


def transformation_to_IfcCartesianTransformationOperator3D(model: Model, transformation):
    """Convert a :class:`Transformation` to an ``IfcCartesianTransformationOperator3D``.

    Parameters
    ----------
    model : :class:`Model`
    transformation : :class:`~compas.geometry.Transformation`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    frame = Frame.from_transformation(transformation)
    return model.create(
        "IfcCartesianTransformationOperator3D",
        Axis1=model.create("IfcDirection", DirectionRatios=(float(frame.xaxis.x), float(frame.xaxis.y), float(frame.xaxis.z))),
        Axis2=model.create("IfcDirection", DirectionRatios=(float(frame.yaxis.x), float(frame.yaxis.y), float(frame.yaxis.z))),
        LocalOrigin=model.create("IfcCartesianPoint", Coordinates=(float(frame.point.x), float(frame.point.y), float(frame.point.z))),
        Scale=1.0,
        Axis3=model.create("IfcDirection", DirectionRatios=(float(frame.zaxis.x), float(frame.zaxis.y), float(frame.zaxis.z))),
    )


# ==========================================================================
# Axis representation
# ==========================================================================


def assign_axis_representation(entity: IfcProduct, curve):
    """Assign an axis (centerline) representation to an IfcProduct.

    The axis representation is stored alongside the body representation
    and uses ``RepresentationIdentifier="Axis"`` with ``RepresentationType="Curve2D"``.

    Parameters
    ----------
    entity : :class:`IfcProduct`
    curve : :class:`Polyline` | :class:`Line` | :class:`Polygon`
        The axis curve.  A Polyline or Line is written as an open IfcPolyline;
        a Polygon is written as a closed IfcPolyline.
    """
    model: Model = entity.model

    if isinstance(curve, Line):
        curve = Polyline([curve.start, curve.end])

    if isinstance(curve, Polygon):
        ifc_polyline = polygon_to_IfcPolyline(model, curve)
    elif isinstance(curve, Polyline):
        ifc_polyline = polyline_to_IfcPolyline(model, curve)
    else:
        raise NotImplementedError(f"Unsupported axis curve type: {type(curve)}")

    ifc_shape_representation = model.create(
        "IfcShapeRepresentation",
        ContextOfItems=model.file.default_axis_context,
        RepresentationIdentifier="Axis",
        RepresentationType="Curve2D",
        Items=[ifc_polyline],
    )

    # Add to existing ProductDefinitionShape or create a new one
    existing_rep = entity.Representation
    if existing_rep is not None:
        reps = list(existing_rep.Representations)
        # Remove any existing Axis representation
        reps = [r for r in reps if r.RepresentationIdentifier != "Axis"]
        reps.append(ifc_shape_representation)
        existing_rep.Representations = reps
    else:
        ifc_product_definition_shape = model.create(
            "IfcProductDefinitionShape",
            Representations=[ifc_shape_representation],
        )
        entity.Representation = ifc_product_definition_shape


# ==========================================================================
# Standalone curve writers
# ==========================================================================


def polyline_to_IfcPolyline(model: Model, polyline: Polyline):
    """Convert a :class:`Polyline` to an ``IfcPolyline`` (open curve).

    Parameters
    ----------
    model : :class:`Model`
    polyline : :class:`Polyline`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    points = []
    for p in polyline.points:
        points.append(model.create("IfcCartesianPoint", Coordinates=(float(p[0]), float(p[1]), float(p[2]))))
    return model.create("IfcPolyline", Points=points)


def polygon_to_IfcPolyline(model: Model, polygon: Polygon):
    """Convert a :class:`Polygon` to an ``IfcPolyline`` (closed curve).

    The first point is repeated at the end to close the polyline.

    Parameters
    ----------
    model : :class:`Model`
    polygon : :class:`Polygon`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    points = []
    for p in polygon.points:
        points.append(model.create("IfcCartesianPoint", Coordinates=(float(p[0]), float(p[1]), float(p[2]))))
    # Close the polyline
    points.append(points[0])
    return model.create("IfcPolyline", Points=points)


# ==========================================================================
# Extrusion write helpers
# ==========================================================================


def extrusion_to_IfcExtrudedAreaSolid(model: Model, extrusion: Extrusion):
    """Convert an :class:`Extrusion` to an ``IfcExtrudedAreaSolid``.

    Parameters
    ----------
    model : :class:`Model`
    extrusion : :class:`Extrusion`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    from compas_ifc.conversions.frame import create_IfcAxis2Placement3D

    # Profile
    swept_area = _profile_to_ifc(model, extrusion.profile)

    # Position
    f = extrusion.frame
    position = create_IfcAxis2Placement3D(model, f.point, f.zaxis, f.xaxis)

    # Direction
    d = extrusion.direction
    direction = model.create("IfcDirection", DirectionRatios=(float(d.x), float(d.y), float(d.z)))

    return model.create(
        "IfcExtrudedAreaSolid",
        SweptArea=swept_area,
        Position=position,
        ExtrudedDirection=direction,
        Depth=float(extrusion.depth),
    )


def clipped_extrusion_to_IfcBooleanClippingResult(model: Model, clipped: ClippedExtrusion):
    """Convert a :class:`ClippedExtrusion` to an ``IfcBooleanClippingResult`` chain.

    Builds the recursive chain from inside out: the leaf is an
    ``IfcExtrudedAreaSolid``, and each clipping plane wraps it in an
    ``IfcBooleanClippingResult`` with ``Operator=DIFFERENCE``.

    Parameters
    ----------
    model : :class:`Model`
    clipped : :class:`ClippedExtrusion`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    from compas_ifc.conversions.primitives import frame_to_IfcPlane

    # Build the leaf extrusion
    current = extrusion_to_IfcExtrudedAreaSolid(model, clipped.extrusion)

    # Wrap in clipping results (reversed so innermost clip first)
    for plane, agreement in reversed(clipped.clipping_planes):
        frame = Frame.from_plane(plane)
        ifc_plane = frame_to_IfcPlane(model, frame)
        half_space = model.create(
            "IfcHalfSpaceSolid",
            BaseSurface=ifc_plane,
            AgreementFlag=agreement,
        )
        current = model.create(
            "IfcBooleanClippingResult",
            Operator="DIFFERENCE",
            FirstOperand=current,
            SecondOperand=half_space,
        )

    return current


# ==========================================================================
# BooleanResult write helpers
# ==========================================================================


def boolean_result_to_IfcBooleanResult(model: Model, bool_result: BooleanResult):
    """Convert a :class:`BooleanResult` to an ``IfcBooleanResult``.

    Recursively converts both operands and wraps them in an
    ``IfcBooleanResult`` with the appropriate operator.

    Parameters
    ----------
    model : :class:`Model`
    bool_result : :class:`BooleanResult`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    first = _geometry_to_ifc_operand(model, bool_result.first_operand)
    second = _geometry_to_ifc_operand(model, bool_result.second_operand)

    return model.create(
        "IfcBooleanResult",
        Operator=bool_result.operator,
        FirstOperand=first,
        SecondOperand=second,
    )


def half_space_to_IfcHalfSpaceSolid(model: Model, half_space: HalfSpace):
    """Convert a :class:`HalfSpace` to an ``IfcHalfSpaceSolid``.

    Parameters
    ----------
    model : :class:`Model`
    half_space : :class:`HalfSpace`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    from compas_ifc.conversions.primitives import frame_to_IfcPlane

    frame = Frame.from_plane(half_space.plane)
    ifc_plane = frame_to_IfcPlane(model, frame)
    return model.create(
        "IfcHalfSpaceSolid",
        BaseSurface=ifc_plane,
        AgreementFlag=half_space.agreement_flag,
    )


def _geometry_to_ifc_operand(model: Model, geometry):
    """Convert a COMPAS geometry object to an IFC boolean operand entity.

    Dispatches based on the geometry type.  Supports all types that
    can appear as ``IfcBooleanOperand``.

    Parameters
    ----------
    model : :class:`Model`
    geometry : :class:`~compas.geometry.Geometry`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`

    Raises
    ------
    NotImplementedError
        If the geometry type is not supported as a boolean operand.
    """
    if isinstance(geometry, BooleanResult):
        return boolean_result_to_IfcBooleanResult(model, geometry)

    if isinstance(geometry, ClippedExtrusion):
        return clipped_extrusion_to_IfcBooleanClippingResult(model, geometry)

    if isinstance(geometry, HalfSpace):
        return half_space_to_IfcHalfSpaceSolid(model, geometry)

    if isinstance(geometry, Extrusion):
        return extrusion_to_IfcExtrudedAreaSolid(model, geometry)

    if isinstance(geometry, Revolution):
        return revolution_to_IfcRevolvedAreaSolid(model, geometry)

    if isinstance(geometry, Pipe):
        return pipe_to_IfcSweptDiskSolid(model, geometry)

    # CSG primitives
    if isinstance(geometry, Box):
        return box_to_IfcBlock(model, geometry)
    if isinstance(geometry, Sphere):
        return sphere_to_IfcSphere(model, geometry)
    if isinstance(geometry, Cone):
        return cone_to_IfcRightCircularCone(model, geometry)
    if isinstance(geometry, Cylinder):
        return cylinder_to_IfcRightCircularCylinder(model, geometry)

    raise NotImplementedError(f"Cannot convert {type(geometry).__name__} to IFC boolean operand.")


def _profile_to_ifc(model, profile):
    """Convert a COMPAS profile (Circle, Polygon, or tuple with voids) to an IFC profile def.

    Shared helper used by both extrusion and revolution writers.

    Parameters
    ----------
    model : :class:`Model`
    profile : :class:`Circle` | :class:`Polygon` | tuple

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    if isinstance(profile, tuple):
        outer, inners = profile
        return _profile_with_voids_to_ifc(model, outer, inners)
    elif isinstance(profile, Circle):
        return _circle_to_IfcCircleProfileDef(model, profile)
    elif isinstance(profile, Polygon):
        return _polygon_to_IfcArbitraryClosedProfileDef(model, profile)
    else:
        raise NotImplementedError(f"Unsupported profile type: {type(profile)}")


# ==========================================================================
# Revolution write helpers
# ==========================================================================


def revolution_to_IfcRevolvedAreaSolid(model: Model, revolution: Revolution):
    """Convert a :class:`Revolution` to an ``IfcRevolvedAreaSolid``.

    Parameters
    ----------
    model : :class:`Model`
    revolution : :class:`Revolution`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    from compas_ifc.conversions.frame import create_IfcAxis1Placement
    from compas_ifc.conversions.frame import create_IfcAxis2Placement3D

    # Profile
    swept_area = _profile_to_ifc(model, revolution.profile)

    # Position (frame)
    f = revolution.frame
    position = create_IfcAxis2Placement3D(model, f.point, f.zaxis, f.xaxis)

    # Axis (IfcAxis1Placement)
    ap = revolution.axis_point
    ad = revolution.axis_direction
    axis = create_IfcAxis1Placement(
        model,
        point=[float(ap.x), float(ap.y), float(ap.z)],
        direction=[float(ad.x), float(ad.y), float(ad.z)],
    )

    return model.create(
        "IfcRevolvedAreaSolid",
        SweptArea=swept_area,
        Position=position,
        Axis=axis,
        Angle=float(revolution.angle),
    )


# ==========================================================================
# Pipe write helpers
# ==========================================================================


def pipe_to_IfcSweptDiskSolid(model: Model, pipe: Pipe):
    """Convert a :class:`Pipe` to an ``IfcSweptDiskSolid``.

    Parameters
    ----------
    model : :class:`Model`
    pipe : :class:`Pipe`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    # Directrix → IfcPolyline
    directrix = polyline_to_IfcPolyline(model, pipe.directrix)

    kwargs = {
        "Directrix": directrix,
        "Radius": float(pipe.radius),
    }
    if pipe.inner_radius is not None:
        kwargs["InnerRadius"] = float(pipe.inner_radius)

    return model.create("IfcSweptDiskSolid", **kwargs)


def _polygon_to_IfcArbitraryClosedProfileDef(model: Model, polygon: Polygon):
    """Convert a :class:`Polygon` to an ``IfcArbitraryClosedProfileDef``.

    Parameters
    ----------
    model : :class:`Model`
    polygon : :class:`Polygon`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    points = []
    for p in polygon.points:
        points.append(model.create("IfcCartesianPoint", Coordinates=(float(p[0]), float(p[1]), float(p[2]))))
    # Close the polyline
    points.append(points[0])
    polyline = model.create("IfcPolyline", Points=points)
    return model.create(
        "IfcArbitraryClosedProfileDef",
        ProfileType="AREA",
        OuterCurve=polyline,
    )


def _circle_to_IfcCircleProfileDef(model: Model, circle: Circle):
    """Convert a :class:`Circle` to an ``IfcCircleProfileDef``.

    Parameters
    ----------
    model : :class:`Model`
    circle : :class:`Circle`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    return model.create(
        "IfcCircleProfileDef",
        ProfileType="AREA",
        Radius=float(circle.radius),
    )


def _profile_with_voids_to_ifc(model: Model, outer: Polygon, inners: list):
    """Convert a profile with voids to an ``IfcArbitraryProfileDefWithVoids``.

    Parameters
    ----------
    model : :class:`Model`
    outer : :class:`Polygon`
    inners : list[:class:`Polygon`]

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
    """
    # Outer curve
    outer_points = []
    for p in outer.points:
        outer_points.append(model.create("IfcCartesianPoint", Coordinates=(float(p[0]), float(p[1]), float(p[2]))))
    outer_points.append(outer_points[0])
    outer_polyline = model.create("IfcPolyline", Points=outer_points)

    # Inner curves
    inner_curves = []
    for inner_polygon in inners:
        inner_points = []
        for p in inner_polygon.points:
            inner_points.append(model.create("IfcCartesianPoint", Coordinates=(float(p[0]), float(p[1]), float(p[2]))))
        inner_points.append(inner_points[0])
        inner_polyline = model.create("IfcPolyline", Points=inner_points)
        inner_curves.append(inner_polyline)

    return model.create(
        "IfcArbitraryProfileDefWithVoids",
        ProfileType="AREA",
        OuterCurve=outer_polyline,
        InnerCurves=inner_curves,
    )


if __name__ == "__main__":
    import compas
    from compas.geometry import Frame

    model = Model.template(schema="IFC2X3", unit="m")

    # geometry = Box.from_width_height_depth(1, 1, 1)
    geometry = Mesh.from_ply(compas.get("bunny.ply"))
    # geometry = Mesh.from_meshgrid(5, 2, 5, 2)

    product = model.create(geometry=geometry, parent=model.building_storeys[0], name="test", frame=Frame.worldXY())

    model.show()

    model.save("temp/representations/test.ifc")
