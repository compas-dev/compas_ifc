from ifcopenshell.api import run

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Sphere
from compas_occ.brep import OCCBrep

from .brep import brep_to_ifc_advanced_brep
from .mesh import mesh_to_IfcPolygonalFaceSet
from .shapes import box_to_IfcBlock
from .shapes import cone_to_IfcRightCircularCone
from .shapes import cylinder_to_IfcRightCircularCylinder
from .shapes import sphere_to_IfcSphere


def write_body_representation(file, body, ifc_entity, context):
    def _body_to_shape(body):
        if isinstance(body, Box):
            shape = box_to_IfcBlock(file, body)
        elif isinstance(body, Sphere):
            shape = sphere_to_IfcSphere(file, body)
        elif isinstance(body, Cone):
            shape = cone_to_IfcRightCircularCone(file, body)
        elif isinstance(body, Cylinder):
            shape = cylinder_to_IfcRightCircularCylinder(file, body)
        elif isinstance(body, Mesh):
            shape = mesh_to_IfcPolygonalFaceSet(file, body)
        elif isinstance(body, OCCBrep):
            shape = brep_to_ifc_advanced_brep(file, body)
        else:
            raise Exception("Unsupported body type.")
        return shape

    if isinstance(body, list):
        shape = []
        for b in body:
            s = _body_to_shape(b)
            if not isinstance(s, list):
                shape.append(s)
            else:
                shape.extend(s)
    else:
        shape = _body_to_shape(body)
        if not isinstance(shape, list):
            shape = [shape]

    representation = file.create_entity(
        "IfcShapeRepresentation",
        ContextOfItems=context,
        RepresentationIdentifier="Body",
        RepresentationType="SolidModel",
        Items=shape,
    )

    run("geometry.assign_representation", file, product=ifc_entity, representation=representation)
