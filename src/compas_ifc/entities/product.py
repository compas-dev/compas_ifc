from typing import Dict
from typing import List

from compas_ifc.entities.objectdefinition import ObjectDefinition
from compas_ifc.helpers import public_attributes
from compas.geometry import Transformation
from compas.geometry import Scale


class Product(ObjectDefinition):
    """
    Class representing an IFC product. A product may be a physical object or a virtual object, that has one or more geometric representations.

    Attributes
    ----------
    axis : List[:class:`compas.geometry.Line`]
        The axis representation of the product. Converted to list of COMPAS lines.
    box : :class:`compas.geometry.Box`
        The box representation of the product. Converted to COMPAS box.
    body : List[:class:`compas_occ.geometry.Shape`]
        The body representation of the product. Converted to list of OCC shapes (BRep).
    body_with_opening : List[:class:`compas_occ.geometry.Shape`]
        The body representation of the product including openings. Converted to list of OCC shapes (BRep).
    opening : List[:class:`compas_occ`]
        The opening representation of the product. Converted to list of OCC shapes (BRep).
    transformation : :class:`compas.geometry.Transformation`
        The transformation of the product, Calculated from the stack of transformations of the product's parent entities. Read-only.
    style : dict
        The style of the product. Converted to dictionary.
    frame : :class:`compas.geometry.Frame`
        The frame of the product. Converted to COMPAS frame.


    """

    def __init__(self, entity, model) -> None:
        super().__init__(entity, model)
        self._axis = None
        self._box = None
        self._body = None
        self._opening = None
        self._body_with_opening = None
        self._transformation = None
        self._style = None
        self._frame = None

    def classifications(self) -> List[Dict[str, str]]:
        """
        External sources of information associated with this product.
        The source of information can be:

        * a classification system;
        * a dictionary server;
        * any external catalogue that classifies the product further;
        * a service that combines the above.

        Returns
        -------
        List[dict[str, str]]

        References
        ----------
        :ifc:`classification`

        """
        classifications = []
        if self._entity.HasAssociations:
            for association in self._entity.HasAssociations:
                if association.is_a("IfcRelAssociatesClassification"):
                    classifications.append(
                        {
                            "name": association.Name,
                            "identification": association.RelatingClassification.Identification,
                            "source": association.RelatingClassification.ReferencedSource.Source,
                        }
                    )
        return classifications

    def materials(self) -> List[Dict]:
        """
        The materials associated with this product.

        Returns
        -------
        List[Dict]

        """
        materials = []

        for association in self._entity.HasAssociations:
            if not association.is_a("IfcRelAssociatesMaterial"):
                continue

            if association.RelatingMaterial.is_a("IfcMaterialLayerSet"):
                print(public_attributes(association.RelatingMaterial))

            elif association.RelatingMaterial.is_a("IfcMaterialLayerSetUsage"):
                print(public_attributes(association.RelatingMaterial))

            elif association.RelatingMaterial.is_a("IfcMaterialConstituentSet"):
                # name = association.RelatingMaterial.Name
                for constituent in association.RelatingMaterial.MaterialConstituents:
                    for pset in constituent.Material.HasProperties:
                        properties = {}
                        for prop in pset.Properties:
                            key = prop.Name
                            value = prop.NominalValue.get_info()["wrappedValue"]
                            properties[key] = value

            else:
                raise NotImplementedError

        return materials

    @property
    def axis(self):
        from compas_ifc.representation import entity_axis_geometry

        if not self._axis:
            self._axis = entity_axis_geometry(self)
        return self._axis

    @property
    def box(self):
        from compas_ifc.representation import entity_box_geometry

        if not self._box:
            self._box = entity_box_geometry(self) or entity_box_geometry(self, context="Plan")
        return self._box

    @property
    def body(self):
        from compas_ifc.representation import entity_body_geometry

        if not self._body:
            self._body = entity_body_geometry(self, use_occ=self.model.reader.use_occ)
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def opening(self):
        from compas_ifc.representation import entity_opening_geometry

        if not self._opening:
            self._opening = entity_opening_geometry(self, use_occ=self.model.reader.use_occ)
        return self._opening

    @opening.setter
    def opening(self, value):
        self._opening = value

    @property
    def body_with_opening(self):

        if self._body_with_opening is None:

            if self._entity:

                from compas_ifc.representation import entity_body_with_opening_geometry

                if not self._body_with_opening:
                    cached_geometry = self.model.reader.get_preloaded_geometry(self)
                    if cached_geometry:
                        self._body_with_opening = cached_geometry
                    else:
                        # TODO: double check if this is still triggered with preloaded geometry
                        # raise
                        self._body_with_opening = entity_body_with_opening_geometry(self, use_occ=self.model.reader.use_occ)

            else:

                scale = self.model.project.length_scale
                T = Transformation.from_frame(self.frame)
                S = Scale.from_factors([scale, scale, scale])
                
                from compas.geometry import Shape
                if isinstance(self.body, Shape):
                    geometry = self.body.transformed(S * T)
                    geometry.scale(scale)
                else:
                    geometry = self.body.transformed(S * T)

                self._body_with_opening = geometry

        return self._body_with_opening

    @body_with_opening.setter
    def body_with_opening(self, value):
        self._body_with_opening = value

    @property
    def geometry(self):
        return self.body_with_opening

    @property
    def transformation(self):
        from compas_ifc.representation import entity_transformation

        if not self._transformation:
            self._transformation = entity_transformation(self)
        return self._transformation

    @property
    def frame(self):
        from compas_ifc.representation import entity_frame

        if not self._frame and self._entity:
            self._frame = entity_frame(self)
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def style(self):
        if not self._style:
            self._style = self.model.reader.get_preloaded_style(self)
        # TODO: handle non-preloaded situation
        return self._style
