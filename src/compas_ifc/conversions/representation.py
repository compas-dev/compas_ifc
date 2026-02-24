"""
This module contains functions for converting geometry representations between COMPAS and IFC.
"""

from typing import Union

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Shape
from compas.geometry import Sphere

from compas.geometry import Circle
from compas.geometry import Polygon

from compas_ifc.conversions.brep import brep_to_IfcAdvancedBrep
from compas_ifc.conversions.mesh import mesh_to_IfcFaceBasedSurfaceModel
from compas_ifc.conversions.shapes import box_to_IfcBlock
from compas_ifc.conversions.shapes import cone_to_IfcRightCircularCone
from compas_ifc.conversions.shapes import cylinder_to_IfcRightCircularCylinder
from compas_ifc.conversions.shapes import sphere_to_IfcSphere
from compas_ifc.entities.extensions import IfcProduct
from compas_ifc.model import Model
from compas_ifc.representations import Extrusion

REPRESENTATION_CACHE = {}


def assign_body_representation(entity: IfcProduct, representation: Union[Shape, Mesh, Brep]):
    """
    Assign a representation to an entity.
    """

    model: Model = entity.model

    if id(representation) in REPRESENTATION_CACHE:
        entity.Representation = REPRESENTATION_CACHE[id(representation)]
        return

    # Convert COMPAS geometries to IFC corresponding representation
    if isinstance(representation, Extrusion):
        ifc_extruded = extrusion_to_IfcExtrudedAreaSolid(model, representation)
        items = [ifc_extruded]
        representation_type = "SweptSolid"

    elif isinstance(representation, Shape):
        if isinstance(representation, Box):
            ifc_csg_primitive3d = box_to_IfcBlock(model, representation)
        elif isinstance(representation, Sphere):
            ifc_csg_primitive3d = sphere_to_IfcSphere(model, representation)
        elif isinstance(representation, Cone):
            ifc_csg_primitive3d = cone_to_IfcRightCircularCone(model, representation)
        elif isinstance(representation, Cylinder):
            ifc_csg_primitive3d = cylinder_to_IfcRightCircularCylinder(model, representation)
        else:
            raise NotImplementedError(f"Conversion of {type(representation)} to IFC not implemented.")

        ifc_csg_solid = model.create("IfcCsgSolid", TreeRootExpression=ifc_csg_primitive3d)

        items = [ifc_csg_solid]
        representation_type = "CSG"

    elif isinstance(representation, Mesh):
        ifc_representation = mesh_to_IfcFaceBasedSurfaceModel(model, representation)
        representation_type = "SurfaceModel"
        items = [ifc_representation]

    elif isinstance(representation, Brep):
        if model.file.use_occ:
            items = brep_to_IfcAdvancedBrep(model, representation)
            representation_type = "SolidModel"
        else:
            mesh, _ = representation.to_tesselation()
            ifc_representation = mesh_to_IfcFaceBasedSurfaceModel(model, mesh)
            representation_type = "SurfaceModel"
            items = [ifc_representation]

    else:
        raise NotImplementedError(f"Conversion of {type(representation)} to IFC not implemented.")

    # QUESTION: When using OCCBrep from Extrusion, can we still keep the extrusion data?

    ifc_shape_representation = model.create(
        "IfcShapeRepresentation",
        ContextOfItems=model.file.default_body_context,
        RepresentationIdentifier="Body",
        RepresentationType=representation_type,
        Items=items,
    )

    ifc_product_definition_shape = model.create(
        "IfcProductDefinitionShape",
        Representations=[ifc_shape_representation],
    )

    entity.Representation = ifc_product_definition_shape
    REPRESENTATION_CACHE[id(representation)] = ifc_product_definition_shape

    # TODO: should not overwrite all property sets here
    # TODO: alternative 1: restructure the metadata, remove duplicated info like vertices
    # TODO: alternative 2: save data as compact json string
    # entity.property_sets = {
    #     "Pset_COMPAS": {
    #         "representation_id": ifc_product_definition_shape.id(),
    #         "compas_data": json.loads(representation.to_jsonstring()),
    #     }
    # }


def read_representation(model: Model, entity: IfcProduct):
    """Read the body representation of an entity into COMPAS geometry.

    See :func:`compas_ifc.conversions.reading.read_body_representation`
    for the full implementation.
    """
    from compas_ifc.conversions.reading import read_body_representation

    return read_body_representation(entity)


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
    profile = extrusion.profile
    if isinstance(profile, tuple):
        outer, inners = profile
        swept_area = _profile_with_voids_to_ifc(model, outer, inners)
    elif isinstance(profile, Circle):
        swept_area = _circle_to_IfcCircleProfileDef(model, profile)
    elif isinstance(profile, Polygon):
        swept_area = _polygon_to_IfcArbitraryClosedProfileDef(model, profile)
    else:
        raise NotImplementedError(f"Unsupported profile type: {type(profile)}")

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
