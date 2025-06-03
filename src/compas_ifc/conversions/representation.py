"""
This module contains functions for converting geometry representations between COMPAS and IFC.
"""

from typing import Union

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Shape
from compas.geometry import Sphere

from compas_ifc.conversions.brep import brep_to_IfcAdvancedBrep
from compas_ifc.conversions.mesh import mesh_to_IfcFaceBasedSurfaceModel
from compas_ifc.conversions.shapes import box_to_IfcBlock
from compas_ifc.conversions.shapes import cone_to_IfcRightCircularCone
from compas_ifc.conversions.shapes import cylinder_to_IfcRightCircularCylinder
from compas_ifc.conversions.shapes import sphere_to_IfcSphere
from compas_ifc.entities.extensions import IfcProduct
from compas_ifc.model import Model

REPRESENTATION_CACHE = {}


def assign_body_representation(entity: IfcProduct, representation: Union[Shape, Mesh, Brep]):
    """
    Assign a representation to an entity.
    """

    model: Model = entity.model

    if id(representation) in REPRESENTATION_CACHE:
        entity.Representation = REPRESENTATION_CACHE[id(representation)]
        return

    # Convert COMPAS geometries to IFC corresponding representation
    if isinstance(representation, Shape):
        if isinstance(representation, Box):
            ifc_csg_primitive3d = box_to_IfcBlock(model, representation)
        elif isinstance(representation, Sphere):
            ifc_csg_primitive3d = sphere_to_IfcSphere(model, representation)
        elif isinstance(representation, Cone):
            ifc_csg_primitive3d = cone_to_IfcRightCircularCone(model, representation)
        elif isinstance(representation, Cylinder):
            ifc_csg_primitive3d = cylinder_to_IfcRightCircularCylinder(model, representation)
        else:
            raise NotImplementedError(f"Conversion of {type(representation)} to IFC not implemented.")

        ifc_csg_solid = model.create("IfcCsgSolid", TreeRootExpression=ifc_csg_primitive3d)

        items = [ifc_csg_solid]
        representation_type = "CSG"

    elif isinstance(representation, Mesh):
        ifc_representation = mesh_to_IfcFaceBasedSurfaceModel(model, representation)
        representation_type = "SurfaceModel"
        items = [ifc_representation]

    elif isinstance(representation, Brep):
        if model.file.use_occ:
            try:
                items = brep_to_IfcAdvancedBrep(model, representation)
                representation_type = "SolidModel"
            except Exception as e:
                print(f"WARNING BREP conversion failed: {e}")
                items = []
                representation_type = "SurfaceModel"

        else:
            mesh, _ = representation.to_tesselation()
            ifc_representation = mesh_to_IfcFaceBasedSurfaceModel(model, mesh)
            representation_type = "SurfaceModel"
            items = [ifc_representation]

    else:
        raise NotImplementedError(f"Conversion of {type(representation)} to IFC not implemented.")

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
    REPRESENTATION_CACHE[id(representation)] = ifc_product_definition_shape

    # TODO: should not overwrite all property sets here
    # TODO: alternative 1: restructure the metadata, remove duplicated info like vertices
    # TODO: alternative 2: save data as compact json string
    # entity.property_sets = {
    #     "Pset_COMPAS": {
    #         "representation_id": ifc_product_definition_shape.id(),
    #         "compas_data": json.loads(representation.to_jsonstring()),
    #     }
    # }


def read_representation(model: Model, entity: IfcProduct):
    pass


if __name__ == "__main__":
    import compas
    from compas.geometry import Frame

    model = Model.template(schema="IFC2X3", unit="m")

    # geometry = Box.from_width_height_depth(1, 1, 1)
    geometry = Mesh.from_ply(compas.get("bunny.ply"))
    # geometry = Mesh.from_meshgrid(5, 2, 5, 2)

    product = model.create(geometry=geometry, parent=model.building_storeys[0], name="test", frame=Frame.worldXY())

    model.show()

    model.save("temp/representations/test.ifc")
