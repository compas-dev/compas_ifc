from typing import List

# from compas.geometry import Polyline
from compas.geometry import Box
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Transformation

# from compas.datastructures import Mesh
from compas_ifc.resources.geometry import IfcAxis2Placement3D_to_frame
from compas_ifc.resources.geometry import IfcDirection_to_vector
from compas_ifc.resources.geometry import IfcProfileDef_to_curve
from compas_ifc.brep import TessellatedBrep

from ifcopenshell import geom


def IfcAdvancedBrep_to_brep(advanced_brep):
    """
    Convert an IFC AdvancedBrep [advancedbrep]_ to a COMPAS brep.

    """
    pass


def IfcAdvancedBrepWithVoids_to_brep(advanced_brep_with_voids):
    """
    Convert an IFC AdvancedBrepWithVoids [advancedbrepwithvoids]_ to a COMPAS brep.

    """
    pass


def IfcBlock_to_box(block) -> Box:
    """
    Convert an IFC Block [block]_ to a COMPAS box.

    """
    pass


def IfcBooleanClippingResult_to_brep(boolean_clipping_result):
    """
    Convert an IFC BooleanClippingResult [booleanclippingresult]_ to a COMPAS brep.

    """
    return IfcBooleanResult_to_brep(boolean_clipping_result)


def IfcBooleanResult_to_brep(boolean_result):
    """
    Convert an IFC BooleanResult [booleanresult]_ to a COMPAS brep.

    """
    from compas_occ.brep import OCCBrep

    br = boolean_result

    # First Operand
    if br.FirstOperand.is_a("IfcBooleanResult"):
        A = IfcBooleanResult_to_brep(br.FirstOperand)
    elif br.FirstOperand.is_a("IfcExtrudedAreaSolid"):
        A = IfcExtrudedAreaSolid_to_brep(br.FirstOperand)
    else:
        raise NotImplementedError

    # Second Operand
    if br.SecondOperand.is_a("IfcBoxedHalfSpace"):
        B = IfcBoxedHalfSpace(br.SecondOperand)
    elif br.SecondOperand.is_a("IfcPolygonalBoundedHalfSpace"):
        B = IfcPolygonalBoundedHalfSpace_to_brep(br.SecondOperand)
    elif br.SecondOperand.is_a("IfcPolygonalFaceSet"):
        B = IfcPolygonalFaceSet_to_brep(br.SecondOperand)
    else:
        raise NotImplementedError(br.SecondOperand)

    # Operator
    if br.Operator == "UNION":
        C: OCCBrep = A + B
    elif br.Operator == "INTERSECTION":
        C: OCCBrep = A & B
    elif br.Operator == "DIFFERENCE":
        C: OCCBrep = A - B
    else:
        raise NotImplementedError(br.Operator)

    C.sew()
    C.fix()
    C.make_solid()
    return C


def IfcIndexedPolyCurve_to_lines(axis) -> List[Line]:
    """
    Convert an IFC Axis [axis]_ to a COMPAS polyline.

    """
    lines = []
    points = IfcCartesianPointList(axis.Points)
    for segment in axis.Segments:
        start, end = segment.wrappedValue
        start -= 1
        end -= 1
        lines.append(Line(points[start], points[end]))
    return lines


def IfcBoundingBox_to_box(bounding_box) -> Box:
    """
    Convert an IFC BoundingBox [boundingbox]_ to a COMPAS box.

    """
    a = Point(*bounding_box.Corner.Coordinates)
    b = a + [bounding_box.XDim, bounding_box.YDim, 0]
    box = Box.from_corner_corner_height(a, b, bounding_box.ZDim)
    return box


def IfcBoxedHalfSpace(boxed_half_space):
    bhs = boxed_half_space
    print(bhs.BaseSurface)
    print(bhs.Enclosure)
    print(bhs.AgreementFlag)


def IfcCartesianPointList(cartesian_point_list) -> List[Point]:
    return [Point(*p) for p in cartesian_point_list.CoordList]


def IfcExtrudedAreaSolid_to_brep(extruded_area_solid):
    from compas_occ.brep import OCCBrep

    eas = extruded_area_solid
    profile = IfcProfileDef_to_curve(eas.SweptArea)

    position = IfcAxis2Placement3D_to_frame(eas.Position)
    transformation = Transformation.from_frame(position)

    def _extrude(profile, eas):
        vector = IfcDirection_to_vector(eas.ExtrudedDirection)
        vector.scale(eas.Depth)
        brep = OCCBrep.from_extrusion(profile, vector)
        brep.sew()
        brep.fix()
        brep.make_solid()
        brep.transform(transformation)
        return brep

    if isinstance(profile, list):
        extrusions = [_extrude(p, eas) for p in profile]
        union = extrusions[0]
        for e in extrusions[1:]:
            union = union + e
        union.sew()
        union.fix()
        union.make_solid()
        return union
    else:
        return _extrude(profile, eas)


def IfcFacetedBrep_to_brep(faceted_brep):
    pass


def IfcFacetedBrepWithVoids_to_brep(faceted_brep_with_voids):
    # fbwv = faceted_brep_with_voids
    pass


def IfcIndexedPolygonalFaceSet_to_brep():
    pass


def IfcPolygonalBoundedHalfSpace_to_brep(polygonal_bounded_half_space):
    pbhs = polygonal_bounded_half_space
    print(pbhs.Position)
    print(pbhs.PolygonalBoundary)
    print(pbhs.BaseSurface)


def IfcPolygonalFaceSet_to_brep(polygonal_face_set):
    from compas_occ.brep import OCCBrep

    pfs = polygonal_face_set

    xyz = pfs.Coordinates.CoordList
    vertices = [[float(x), float(y), float(z)] for x, y, z in xyz]
    faces = [[i - 1 for i in face.CoordIndex] for face in pfs.Faces]
    polygons = [[vertices[index] for index in face] for face in faces]
    brep = OCCBrep.from_polygons(polygons)

    brep.sew()
    brep.fix()
    brep.make_solid()

    return brep


def IfcTessellatedFaceSet_to_brep(tessellated_face_set):
    tfs = tessellated_face_set

    if tfs.is_a("IfcTriangulatedFaceSet"):
        return IfcTriangulatedFaceSet_to_brep(tfs)

    if tfs.is_a("IfcPolygonalFaceSet"):
        return IfcPolygonalFaceSet_to_brep(tfs)

    raise NotImplementedError(tfs.is_a())


def IfcTriangulatedFaceSet_to_brep(triangulated_face_set):
    from compas_occ.brep import OCCBrep

    tfs = triangulated_face_set

    xyz = tfs.Coordinates.CoordList
    vertices = [[float(x), float(y), float(z)] for x, y, z in xyz]
    faces = [[a - 1, b - 1, c - 1] for a, b, c in tfs.CoordIndex]
    triangles = [[vertices[index] for index in face] for face in faces]
    brep = OCCBrep.from_polygons(triangles)

    brep.sew()
    brep.fix()
    brep.make_solid()

    return brep


def IfcShape_to_brep(ifc_shape):
    from compas_occ.brep import OCCBrep

    settings = geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    shape = geom.create_shape(settings, ifc_shape)

    brep = OCCBrep.from_shape(shape)
    brep.sew()
    brep.fix()
    brep.make_solid()

    return brep


def IfcShape_to_tessellatedbrep(ifc_shape):
    settings = geom.settings()
    shape = geom.create_shape(settings, ifc_shape)
    return TessellatedBrep(vertices=shape.verts, edges=shape.edges, faces=shape.faces)


# # IfcTessellationItem_to_mesh
# def tessellation_to_mesh(item) -> Mesh:
#     """
#     Convert a tessellation item to a Mesh.

#     """
#     mesh = Mesh()
#     mesh.update_default_face_attributes(colour=None)

#     face_color = {}

#     if item.HasColours:
#         colourmap = item.HasColours[0]
#         for index, face in zip(
#             colourmap.ColourIndex,
#             colourmap.MappedTo.Faces,
#         ):
#             fid = face.id()
#             colour = colourmap.Colours.ColourList[index - 1]
#             face_color[fid] = Color(*colour)

#     for face in item.Faces:
#         vertices = []
#         for index in face.CoordIndex:
#             x, y, z = item.Coordinates.CoordList[index - 1]
#             vertices.append(mesh.add_vertex(x=x, y=y, z=z))
#         mesh.add_face(vertices, colour=face_color.get(face.id()))
#     return mesh
