import ifcopenshell
from compas_ifc.model import Model
from compas.geometry import Box
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Sphere
from compas_ifc.entities.base import Base
from compas_ifc.conversions.frame import create_IfcAxis2Placement3D


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


def box_to_IfcBlock(model: Model, box: Box) -> Base:
    """
    Convert a COMPAS box to an IFC Block.
    """
    pt = box.frame.point.copy()
    pt -= [box.xsize / 2, box.ysize / 2, box.zsize / 2]
    print(pt)
    return model.create(
        "IfcBlock",
        Position=create_IfcAxis2Placement3D(model, pt, box.frame.zaxis, box.frame.xaxis),
        XLength=box.xsize,
        YLength=box.ysize,
        ZLength=box.zsize,
    )


def sphere_to_IfcSphere(model: Model, sphere: Sphere) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS sphere to an IFC Sphere.
    """
    return model.create(
        "IfcSphere",
        Position=create_IfcAxis2Placement3D(model, sphere.base),
        Radius=sphere.radius,
    )


def cone_to_IfcRightCircularCone(model: Model, cone: Cone) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS cone to an IFC Cone.
    """
    plane = cone.circle.plane
    return model.create(
        "IfcRightCircularCone",
        Position=create_IfcAxis2Placement3D(model, plane.point, plane.normal),
        Height=cone.height,
        BottomRadius=cone.circle.radius,
    )


def cylinder_to_IfcRightCircularCylinder(model: Model, cylinder: Cylinder) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS cylinder to an IFC Cylinder.
    """
    plane = cylinder.circle.plane
    return model.create(
        "IfcRightCircularCylinder",
        Position=create_IfcAxis2Placement3D(model, plane.point, plane.normal),
        Height=cylinder.height,
        Radius=cylinder.circle.radius,
    )


def occ_cylinder_to_ifc_cylindrical_surface(file, occ_cylinder):
    location = occ_cylinder.Location().Coord()
    xdir = occ_cylinder.XAxis().Direction().Coord()
    zdir = occ_cylinder.Axis().Direction().Coord()
    IfcAxis2Placement3D = create_IfcAxis2Placement3D(file, location, zdir, xdir)
    return file.create_entity("IfcCylindricalSurface", IfcAxis2Placement3D, occ_cylinder.Radius())


if __name__ == "__main__":
    model = Model()
    print(create_IfcAxis2Placement3D(model))

    box = Box(10, 10, 10)
    box_to_IfcBlock(model, box).print_attributes(max_depth=5)
