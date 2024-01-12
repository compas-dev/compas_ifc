import ifcopenshell

from compas.datastructures import Mesh


def mesh_to_IfcPolygonalFaceSet(file: ifcopenshell.file, mesh: Mesh) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS mesh to an IFC PolygonalFaceSet.
    """
    _vertices = []
    for key, attr in mesh.vertices(True):
        _vertices.append((key, (float(attr["x"]), float(attr["y"]), float(attr["z"]))))
    _vertices = sorted(_vertices, key=lambda x: x[0])
    vertices = [v[1] for v in _vertices]

    keys = [v[0] for v in _vertices]

    faces = []
    for fkey in mesh.faces():
        indexes = [keys.index(i) + 1 for i in mesh.face_vertices(fkey)]
        faces.append(file.createIfcIndexedPolygonalFace(indexes))

    return file.create_entity(
        "IfcPolygonalFaceSet",
        Coordinates=file.createIfcCartesianPointList3D(vertices),
        Faces=faces,
    )
