"""
This module contains functions for converting representations between COMPAS and IFC.
"""

from typing import TYPE_CHECKING
from typing import Union
from compas.geometry import Shape
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Cylinder
from compas.geometry import Cone
from compas.geometry import Torus
from compas.datastructures import Mesh
from compas_ifc.entities.extensions import IfcProduct
from compas_ifc.conversions.shapes import box_to_IfcBlock
from compas_ifc.conversions.shapes import sphere_to_IfcSphere
from compas_ifc.conversions.mesh import mesh_to_IfcPolygonalFaceSet
from compas_ifc.conversions.mesh import mesh_to_IfcFaceBasedSurfaceModel
from compas_ifc.conversions.pset import from_dict_to_pset
from compas_ifc.entities.base import Base
from compas_ifc.model import Model
import compas
import json


def assign_body_representation(model: Model, entity: IfcProduct, representation: Union[Shape, Mesh]):
    """
    Assign a representation to an entity.
    """

    # Convert COMPAS geometries to IFC corresponding representation
    if isinstance(representation, Shape):
        if isinstance(representation, Box):
            ifc_csg_primitive3d = box_to_IfcBlock(model, representation)
        elif isinstance(representation, Sphere):
            ifc_csg_primitive3d = sphere_to_IfcSphere(model, representation)
        else:
            raise NotImplementedError(f"Conversion of {type(representation)} to IFC not implemented.")

        ifc_csg_solid = model.create("IfcCsgSolid", TreeRootExpression=ifc_csg_primitive3d)

        items = [ifc_csg_solid]
        representation_type = "CSG"

    elif isinstance(representation, Mesh):
        ifc_representation = mesh_to_IfcFaceBasedSurfaceModel(model, representation)
        representation_type = "SurfaceModel"
        items = [ifc_representation]

    # QUESTION: When using OCCBrep from Extrusion, can we still keep the extrusion data?

    ifc_shape_representation = model.create(
        "IfcShapeRepresentation",
        ContextOfItems=model.file.default_body_context,
        RepresentationIdentifier="Body",
        RepresentationType=representation_type,
        Items=items,
    )

    ifc_product_definition_shape = model.create(
        "IfcProductDefinitionShape",
        Representations=[ifc_shape_representation],
    )

    entity.Representation = ifc_product_definition_shape

    # TODO: should not overwrite all property sets here
    # TODO: alternative 1: restructure the metadata, remove duplicated info like vertices
    # TODO: alternative 2: save data as compact json string
    entity.property_sets = {
        "Pset_COMPAS": {
            "representation_id": ifc_product_definition_shape.id(),
            "compas_data": json.loads(representation.to_jsonstring()),
        }
    }


def read_representation(model: Model, entity: IfcProduct):
    pass


if __name__ == "__main__":

    from compas.geometry import Frame

    model = Model.template(schema="IFC4", unit="m")

    product = model.create(parent=model.building_storeys[0], name="test", frame=Frame.worldXY())

    representation = Box.from_width_height_depth(1, 1, 1)
    # representation = Mesh.from_ply(compas.get("bunny.ply"))
    # representation = Mesh.from_meshgrid(5, 2, 5, 2)

    assign_body_representation(model, product, representation)

    model.save("temp/representations/test.ifc")

    print(product.property_sets)

    # model = Model("temp/representations/test.ifc")

    # model.show()
