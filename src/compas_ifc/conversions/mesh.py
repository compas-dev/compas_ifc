from compas.datastructures import Mesh

from compas_ifc.entities.base import Base
from compas_ifc.model import Model


def mesh_to_IfcPolygonalFaceSet(model: Model, mesh: Mesh) -> Base:
    """
    Convert a COMPAS mesh to an IFC PolygonalFaceSet.
    """
    keys = sorted(mesh.vertices())
    vertices = []
    for key in keys:
        coords = mesh.vertex_coordinates(key)
        vertices.append((float(coords[0]), float(coords[1]), float(coords[2])))

    faces = []
    for fkey in mesh.faces():
        indexes = [keys.index(i) + 1 for i in mesh.face_vertices(fkey)]
        faces.append(model.create("IfcIndexedPolygonalFace", CoordIndex=indexes))

    return model.create(
        "IfcPolygonalFaceSet",
        Closed=mesh.is_closed(),
        Coordinates=model.create("IfcCartesianPointList3D", CoordList=vertices),
        Faces=faces,
    )


def mesh_to_IfcFaceBasedSurfaceModel(model: Model, mesh: Mesh) -> Base:
    """
    Convert a COMPAS mesh to an IFC FaceBasedSurfaceModel.
    """
    vertices = {}
    for key in mesh.vertices():
        coords = mesh.vertex_coordinates(key)
        vertex = model.create("IfcCartesianPoint", Coordinates=(float(coords[0]), float(coords[1]), float(coords[2])))
        vertices[key] = vertex

    faces = []
    for fkey in mesh.faces():
        indexes = [vertices[key] for key in mesh.face_vertices(fkey)]
        polyloop = model.create("IfcPolyLoop", Polygon=indexes)
        bound = model.create("IfcFaceOuterBound", Bound=polyloop, Orientation=True)
        face = model.create("IfcFace", Bounds=[bound])
        faces.append(face)

    face_set = model.create("IfcConnectedFaceSet", CfsFaces=faces)
    ifc_face_based_surface_model = model.create("IfcFaceBasedSurfaceModel", FbsmFaces=[face_set])

    return ifc_face_based_surface_model
