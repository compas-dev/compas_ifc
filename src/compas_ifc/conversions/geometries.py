from compas_ifc.resources import IfcShape_to_brep  # TODO: move this
from compas_ifc.resources import IfcShape_to_tessellatedbrep  # TODO: move this
from compas_ifc.resources import IfcLocalPlacement_to_transformation  # TODO: move this
from compas.geometry import Scale

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcElement


def entity_transformation(entity: "IfcElement"):
    """
    Construct the transformation of an entity.
    """
    scale = entity.model.project.length_scale

    if entity.ObjectPlacement:
        scaled_placement = IfcLocalPlacement_to_transformation(entity.ObjectPlacement, scale=scale)
    else:
        scaled_placement = Scale.from_factors([scale, scale, scale])

    return scaled_placement


def entity_body_geometry(entity: "IfcElement", context="Model", use_occ=False, apply_transformation=True):
    """
    Construct the body geometry representations of an entity.
    """
    bodies = []

    representation = None
    if entity.Representation:
        for temp in entity.Representation.Representations:
            if temp.RepresentationIdentifier == "Body" and temp.ContextOfItems.ContextType == context:
                representation = temp
                break

    if not representation:
        return bodies

    for item in representation.Items:
        if use_occ:
            brep = IfcShape_to_brep(item.entity) # TODO: improve this, should just give item
            bodies.append(brep)
        else:
            tessellatedbrep = IfcShape_to_tessellatedbrep(item.entity) # TODO: improve this, should just give item
            bodies.append(tessellatedbrep)

    if apply_transformation:
        transformation = entity_transformation(entity)
        for body in bodies:
            body.transform(transformation)

    return bodies


def entity_opening_geometry(entity: "IfcElement", use_occ=False, apply_transformation=True):
    """
    Construct the opening geometry representations of an entity.
    """

    voids = []
    for opening in entity.HasOpenings():
        element = opening.RelatedOpeningElement

        if apply_transformation:
            transformation = entity_transformation(element)

        for representation in element.Representation.Representations:
            for item in representation.Items:
                if use_occ:
                    brep = IfcShape_to_brep(item.entity) # TODO: improve this, should just give item
                    if apply_transformation:
                        brep.transform(transformation)
                    voids.append(brep)
                else:
                    tessellatedbrep = IfcShape_to_tessellatedbrep(item.entity) # TODO: improve this, should just give item
                    if apply_transformation:
                        tessellatedbrep.transform(transformation)
                    voids.append(tessellatedbrep)

    return voids
