import ifcopenshell

from compas.datastructures import Mesh


def mesh_to_IfcPolygonalFaceSet(file: ifcopenshell.file, mesh: Mesh) -> ifcopenshell.entity_instance:
    """
    Convert a COMPAS mesh to an IFC PolygonalFaceSet.
    """
    vertices = []
    for _, attr in mesh.vertices(True):
        vertices.append((float(attr["x"]), float(attr["y"]), float(attr["z"])))
    faces = []
    for fkey in mesh.faces():
        indexes = [i + 1 for i in mesh.face_vertices(fkey)]
        faces.append(file.createIfcIndexedPolygonalFace(indexes))

    return file.create_entity(
        "IfcPolygonalFaceSet",
        Coordinates=file.createIfcCartesianPointList3D(vertices),
        Faces=faces,
    )
