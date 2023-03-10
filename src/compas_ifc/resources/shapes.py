import ifcopenshell

from compas.geometry import Box
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Sphere


def create_IfcAxis2Placement3D(file, point=None, dir1=None, dir2=None):
    """
    Create an IFC Axis2Placement3D from a point, a direction and a second direction.
    """
    point = file.createIfcCartesianPoint(point or (0.0, 0.0, 0.0))
    dir1 = file.createIfcDirection(dir1 or (0.0, 0.0, 1.0))
    dir2 = file.createIfcDirection(dir2 or (1.0, 0.0, 0.0))
    axis2placement = file.createIfcAxis2Placement3D(point, dir1, dir2)
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


def box_to_IfcBlock(file: ifcopenshell.file, box: Box) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS box to an IFC Block.
    """
    pt = box.frame.point
    pt -= [box.xsize / 2, box.ysize / 2, box.zsize / 2]
    return file.create_entity(
        "IfcBlock",
        Position=create_IfcAxis2Placement3D(file, pt, box.frame.zaxis, box.frame.xaxis),
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
        Position=create_IfcAxis2Placement3D(file, sphere.point),
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
