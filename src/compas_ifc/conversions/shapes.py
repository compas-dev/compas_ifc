from __future__ import annotations

from typing import TYPE_CHECKING

import ifcopenshell
from compas.geometry import Box
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Sphere

from compas_ifc.conversions.frame import create_IfcAxis2Placement3D
from compas_ifc.entities.base import Base

if TYPE_CHECKING:
    from compas_ifc.bim import BuildingInformationModel


def create_IfcShapeRepresentation(file: ifcopenshell.file, item: ifcopenshell.entity_instance, context: ifcopenshell.entity_instance) -> ifcopenshell.entity_instance:
    """
    Create an IFC Shape Representation from an IFC item and a context.
    """
    return file.create_entity(
        "IfcShapeRepresentation",
        ContextOfItems=context,
        RepresentationIdentifier="Body",
        RepresentationType="SolidModel",
        Items=[item],
    )


def box_to_IfcBlock(model: BuildingInformationModel, box: Box) -> Base:
    """
    Convert a COMPAS box to an IFC Block.
    """
    pt = box.frame.point.copy()
    pt -= [box.xsize / 2, box.ysize / 2, box.zsize / 2]
    return model._create(
        "IfcBlock",
        Position=create_IfcAxis2Placement3D(model, pt, box.frame.zaxis, box.frame.xaxis),
        XLength=box.xsize,
        YLength=box.ysize,
        ZLength=box.zsize,
    )


def sphere_to_IfcSphere(model: BuildingInformationModel, sphere: Sphere) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS sphere to an IFC Sphere.
    """
    return model._create(
        "IfcSphere",
        Position=create_IfcAxis2Placement3D(model, sphere.base),
        Radius=sphere.radius,
    )


def cone_to_IfcRightCircularCone(model: BuildingInformationModel, cone: Cone) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS cone to an IFC Cone.
    """
    plane = cone.circle.plane
    return model._create(
        "IfcRightCircularCone",
        Position=create_IfcAxis2Placement3D(model, plane.point, plane.normal),
        Height=cone.height,
        BottomRadius=cone.circle.radius,
    )


def cylinder_to_IfcRightCircularCylinder(model: BuildingInformationModel, cylinder: Cylinder) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS cylinder to an IFC Cylinder.
    """
    plane = cylinder.circle.plane
    return model._create(
        "IfcRightCircularCylinder",
        Position=create_IfcAxis2Placement3D(model, plane.point, plane.normal),
        Height=cylinder.height,
        Radius=cylinder.circle.radius,
    )


def occ_cylinder_to_ifc_cylindrical_surface(model: BuildingInformationModel, occ_cylinder):
    location = occ_cylinder.Location().Coord()
    xdir = occ_cylinder.XAxis().Direction().Coord()
    zdir = occ_cylinder.Axis().Direction().Coord()
    IfcAxis2Placement3D = create_IfcAxis2Placement3D(model, location, zdir, xdir)
    return model._create("IfcCylindricalSurface", Position=IfcAxis2Placement3D, Radius=occ_cylinder.Radius())


def occ_sphere_to_ifc_spherical_surface(model: BuildingInformationModel, occ_sphere):
    location = occ_sphere.Location().Coord()
    xdir = occ_sphere.XAxis().Direction().Coord()
    zdir = occ_sphere.Position().Axis().Direction().Coord()
    IfcAxis2Placement3D = create_IfcAxis2Placement3D(model, location, zdir, xdir)
    return model._create("IfcSphericalSurface", Position=IfcAxis2Placement3D, Radius=occ_sphere.Radius())


def occ_torus_to_ifc_toroidal_surface(model: BuildingInformationModel, occ_torus):
    location = occ_torus.Location().Coord()
    xdir = occ_torus.XAxis().Direction().Coord()
    zdir = occ_torus.Axis().Direction().Coord()
    IfcAxis2Placement3D = create_IfcAxis2Placement3D(model, location, zdir, xdir)
    return model._create("IfcToroidalSurface", Position=IfcAxis2Placement3D, MajorRadius=occ_torus.MajorRadius(), MinorRadius=occ_torus.MinorRadius())


if __name__ == "__main__":
    from compas_ifc.bim import BuildingInformationModel

    model = BuildingInformationModel()
    print(create_IfcAxis2Placement3D(model))

    box = Box(10, 10, 10)
    box_to_IfcBlock(model, box).print_attributes(max_depth=5)
