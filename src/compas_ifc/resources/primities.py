import ifcopenshell
from compas.geometry import Frame
from compas.geometry import Point

from .shapes import create_IfcAxis2Placement3D


def point_to_ifc_cartesian_point(file: ifcopenshell.file, point: Point) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS point to an IFC Cartesian Point.
    """
    point = [float(i) for i in point]
    return file.create_entity("IFCCARTESIANPOINT", (*point,))


def occ_plane_to_frame(occ_plane) -> Frame:
    """
    Convert an OCC plane to a COMPAS frame.
    """
    location = occ_plane.Location().Coord()
    xdir = occ_plane.XAxis().Direction().Coord()
    ydir = occ_plane.YAxis().Direction().Coord()
    return Frame(location, xdir, ydir)


def frame_to_ifc_plane(file: ifcopenshell.file, frame: Frame) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS frame to an IFC Plane.
    """
    IfcAxis2Placement3D = create_IfcAxis2Placement3D(file, frame.point, frame.zaxis, frame.xaxis)
    return file.create_entity("IfcPlane", IfcAxis2Placement3D)
