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


def mesh_to_IfcTriangulatedFaceSet(model: Model, mesh: Mesh) -> Base:
    """Convert a COMPAS mesh to an IFC TriangulatedFaceSet.

    All non-triangular faces are fan-triangulated (vertex 0 to each pair of
    consecutive vertices).  The resulting face set uses IFC4 indexed storage
    with shared coordinates.

    Parameters
    ----------
    model : :class:`Model`
    mesh : :class:`Mesh`

    Returns
    -------
    :class:`~compas_ifc.entities.base.Base`
        An ``IfcTriangulatedFaceSet`` entity.
    """
    keys = sorted(mesh.vertices())
    key_index = {k: i for i, k in enumerate(keys)}

    vertices = []
    for key in keys:
        coords = mesh.vertex_coordinates(key)
        vertices.append((float(coords[0]), float(coords[1]), float(coords[2])))

    triangles = []
    for fkey in mesh.faces():
        face_verts = [key_index[v] + 1 for v in mesh.face_vertices(fkey)]
        # Fan triangulation for n-gons
        for i in range(1, len(face_verts) - 1):
            triangles.append((face_verts[0], face_verts[i], face_verts[i + 1]))

    return model.create(
        "IfcTriangulatedFaceSet",
        Coordinates=model.create("IfcCartesianPointList3D", CoordList=vertices),
        CoordIndex=triangles,
        Closed=mesh.is_closed(),
    )
