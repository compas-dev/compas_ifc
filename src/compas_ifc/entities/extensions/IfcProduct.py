from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcProduct
else:
    IfcProduct = object


class IfcProduct(IfcProduct):
    @property
    def geometries(self):
        from compas_ifc.resources import IfcShape_to_brep
        from compas_ifc.resources import IfcIndexedPolyCurve_to_lines

        geometries = {}
        representation = self.Representation
        if representation:
            for repr in representation.Representations:
                identifier = repr.RepresentationIdentifier
                context = repr.ContextOfItems.ContextType
                _type = repr.RepresentationType
                if identifier == "Body":
                    geometries["body"] = [IfcShape_to_brep(item.entity) for item in repr.Items]
                if identifier == "Axis":
                    # items = [IfcIndexedPolyCurve_to_lines(item.entity) for item in repr.Items]
                    geometries["axis"] = "Not implemented"

        geometries["opening"] = "Not implemented"
        geometries["body_without_opening"] = "Not implemented"

        return geometries

    @property
    def transformation(self):
        # TODO: handle scale at Project level
        from compas_ifc.resources import IfcLocalPlacement_to_transformation

        return IfcLocalPlacement_to_transformation(self.ObjectPlacement.entity)
