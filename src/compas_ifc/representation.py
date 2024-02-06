"""
********************************************************************************
representation
********************************************************************************

.. currentmodule:: compas_ifc.representation

Other Functions
===============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    entity_annotation_geometry
    entity_axis_geometry
    entity_body_geometry
    entity_box_geometry
    entity_clearance_geometry
    entity_lighting_geometry
    entity_mapped_geometry
    entity_reference_geometry
    entity_profile_geometry
    entity_surface_geometry
    entity_survey_geometry


Other Functions
===============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    tessellation_to_brep
    tessellation_to_mesh

"""

from functools import reduce
from operator import mul
from typing import List

from compas_occ.brep import OCCBrep
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound

from compas.geometry import Box
from compas.geometry import Scale
from compas.geometry import Transformation
from compas_ifc.entities.entity import Entity
from compas_ifc.brep import TessellatedBrep
from compas_ifc.resources import IfcAxis2Placement3D_to_frame
from compas_ifc.resources import IfcBoundingBox_to_box
from compas_ifc.resources import IfcCartesianTransformationOperator3D_to_frame
from compas_ifc.resources import IfcIndexedPolyCurve_to_lines
from compas_ifc.resources import IfcLocalPlacement_to_transformation
from compas_ifc.resources import IfcShape_to_brep
from compas_ifc.resources import IfcShape_to_tessellatedbrep


# this does not belong here
# but rather in the representations module
def IfcMappedItem_to_transformation(item) -> Transformation:
    """
    Convert an IFC MappedItem to a COMPAS transformation.

    """
    stack = []

    source_frame = IfcAxis2Placement3D_to_frame(item.MappingSource.MappingOrigin)
    target_frame = IfcCartesianTransformationOperator3D_to_frame(item.MappingTarget)

    stack.append(source_frame)
    stack.append(target_frame)

    matrices = [Transformation.from_frame(f) for f in stack]
    return reduce(mul, matrices[::-1])


def entity_transformation(entity: Entity):
    """
    Construct the transformation of an entity.
    """
    return _entity_transformation(entity._entity, scale=entity.model.project.length_scale)


def _entity_transformation(_entity, scale=1.0):

    if _entity.ObjectPlacement:
        scaled_placement = IfcLocalPlacement_to_transformation(_entity.ObjectPlacement, scale=scale)
    else:
        scaled_placement = Scale.from_factors([scale, scale, scale])

    return scaled_placement


def entity_body_geometry(entity: Entity, context="Model", use_occ=True, apply_transformation=True):
    """
    Construct the body geometry representations of an entity.

    References
    ----------
    .. [1] :ifc:`body-geometry`

    """
    bodies = []

    representation = None
    if getattr(entity._entity, "Representation", None):
        for temp in entity._entity.Representation.Representations:
            if temp.RepresentationIdentifier == "Body":
                representation = temp
                break

    if not representation:
        return bodies

    if representation.ContextOfItems.ContextType == context:
        for item in representation.Items:
            if use_occ:
                brep = IfcShape_to_brep(item)
                bodies.append(brep)
            else:
                tessellatedbrep = IfcShape_to_tessellatedbrep(item)
                bodies.append(tessellatedbrep)

    if apply_transformation:
        transformation = entity_transformation(entity)
        for body in bodies:
            body.transform(transformation)

    return bodies


def entity_opening_geometry(entity: Entity, use_occ=True, apply_transformation=True):
    """
    Construct the opening geometry representations of an entity.
    """

    voids = []
    if hasattr(entity._entity, "HasOpenings"):
        for opening in entity._entity.HasOpenings:
            element = opening.RelatedOpeningElement

            if apply_transformation:
                transformation = _entity_transformation(element, entity.model.project.length_scale)

            for representation in element.Representation.Representations:
                for item in representation.Items:
                    if use_occ:
                        brep = IfcShape_to_brep(item)
                        if apply_transformation:
                            brep.transform(transformation)
                        voids.append(brep)
                    else:
                        tessellatedbrep = IfcShape_to_tessellatedbrep(item)
                        if apply_transformation:
                            tessellatedbrep.transform(transformation)
                        voids.append(tessellatedbrep)

    return voids


def entity_body_with_opening_geometry(entity: Entity = None, bodies=None, voids=None, context="Model", use_occ=False):
    """
    Construct the body geometry representations of an entity.

    References
    ----------
    .. [1] :ifc:`body-geometry`

    """
    bodies = bodies or entity_body_geometry(entity, context=context, use_occ=use_occ, apply_transformation=True)
    voids = voids or entity_opening_geometry(entity, use_occ=use_occ, apply_transformation=True)

    if not voids:
        return bodies

    if use_occ:
        print("Using OCC for boolean operations.")
        compound = TopoDS_Compound()
        builder = BRep_Builder()
        builder.MakeCompound(compound)
        for brep in voids:
            builder.Add(compound, brep.occ_shape)
        B = OCCBrep.from_shape(compound)

        shapes = []
        for A in bodies:
            try:
                C: OCCBrep = A - B
                C.make_solid()
                shapes.append(C)
            except Exception:
                shapes.append(A)
                print("Warning: Failed to subtract voids from body.")
    else:
        print("Using CGAL for boolean operations.")
        from compas_cgal.booleans import boolean_difference

        shapes = []
        for A in bodies:
            C = A
            for B in voids:
                vertices, faces = boolean_difference(C.to_vertices_and_faces(), B.to_vertices_and_faces())
                C = TessellatedBrep(vertices=vertices, faces=faces)
            shapes.append(C)

    return shapes


def entity_box_geometry(entity, context="Model") -> List[Box]:
    """
    Construct the box geometry representations of an entity.

    References
    ----------
    .. [1] :ifc:`box-geometry`

    """
    boxes = []

    representation = None

    if getattr(entity._entity, "Representation", None):
        for temp in entity._entity.Representation.Representations:
            if temp.RepresentationIdentifier == "Box":
                representation = temp
                break

    if not representation:
        return boxes

    placement = IfcLocalPlacement_to_transformation(entity._entity.ObjectPlacement)
    scale = entity.model.project.length_scale
    scale = Scale.from_factors([scale, scale, scale])

    if representation.ContextOfItems.ContextType == context:
        if representation.RepresentationType == "BoundingBox":
            for item in representation.Items:
                box = IfcBoundingBox_to_box(item)
                box.transform(placement)
                box.transform(scale)
                boxes.append(box)

    return boxes


def entity_annotation_geometry(entity):
    raise NotImplementedError


def entity_axis_geometry(entity, context="Model"):
    """
    Construct the axis geometry representations of an entity.

    References
    ----------
    .. [1] :ifc:`axis-geometry`

    """
    axes = []
    representation = None

    if getattr(entity._entity, "Representation", None):
        for temp in entity._entity.Representation.Representations:
            if temp.RepresentationIdentifier == "Axis":
                representation = temp
                break

    if not representation:
        return axes

    placement = IfcLocalPlacement_to_transformation(entity._entity.ObjectPlacement)
    scale = entity.model.project.length_scale
    scale = Scale.from_factors([scale, scale, scale])

    if representation.ContextOfItems.ContextType == context:
        if representation.RepresentationType == "Curve2D":
            for item in representation.Items:
                # TODO: deal with other types of curves
                if item.is_a("IfcIndexedPolyCurve"):
                    axis = IfcIndexedPolyCurve_to_lines(item)
                    for line in axis:
                        line.transform(placement)
                        line.transform(scale)
                        axes.append(line)

    return axes


def entity_profile_geometry(entity):
    pass


def entity_surface_geometry(entity):
    pass


def entity_reference_geometry(entity):
    pass


def entity_clearance_geometry(entity):
    pass


def entity_lighting_geometry(entity):
    pass


def entity_survey_geometry(entity):
    pass


def entity_mapped_geometry(entity):
    pass
