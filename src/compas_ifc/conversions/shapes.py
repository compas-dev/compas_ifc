import ifcopenshell
from compas_ifc.model import Model
from compas.geometry import Box
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Sphere
from compas.geometry import Point
from compas.geometry import Vector
from compas_ifc.entities.base import Base

def frame_to_ifc_axis2_placement_3d(file, frame):
    return create_IfcAxis2Placement3D(file, point=frame.point, dir1=frame.zaxis, dir2=frame.xaxis)


def create_IfcAxis2Placement3D(model: Model, point: Point = None, dir1: Vector = None, dir2: Vector = None) -> Base:
    """
    Create an IFC Axis2Placement3D from a point, a direction and a second direction.
    """
    point = model.create("IfcCartesianPoint", Coordinates=point or [0.0, 0.0, 0.0])
    dir1 = model.create("IfcDirection", DirectionRatios=dir1 or [0.0, 0.0, 1.0])
    dir2 = model.create("IfcDirection", DirectionRatios=dir2 or [1.0, 0.0, 0.0])
    axis2placement = model.create("IfcAxis2Placement3D", Location=point, Axis=dir1, RefDirection=dir2)
    return axis2placement


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
    return model.create(
        "IfcBlock",
        Position=create_IfcAxis2Placement3D(model, pt, box.frame.zaxis, box.frame.xaxis),
        XLength=box.xsize,
        YLength=box.ysize,
        ZLength=box.zsize,
    )


def sphere_to_IfcSphere(file: ifcopenshell.file, sphere: Sphere) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS sphere to an IFC Sphere.
    """
    return file.create_entity(
        "IfcSphere",
        Position=create_IfcAxis2Placement3D(file, sphere.base),
        Radius=sphere.radius,
    )


def cone_to_IfcRightCircularCone(file: ifcopenshell.file, cone: Cone) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS cone to an IFC Cone.
    """
    plane = cone.circle.plane
    return file.create_entity(
        "IfcRightCircularCone",
        Position=create_IfcAxis2Placement3D(file, plane.point, plane.normal),
        Height=cone.height,
        BottomRadius=cone.circle.radius,
    )


def cylinder_to_IfcRightCircularCylinder(file: ifcopenshell.file, cylinder: Cylinder) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS cylinder to an IFC Cylinder.
    """
    plane = cylinder.circle.plane
    return file.create_entity(
        "IfcRightCircularCylinder",
        Position=create_IfcAxis2Placement3D(file, plane.point, plane.normal),
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