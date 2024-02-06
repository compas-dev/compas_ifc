from typing import Dict
from typing import List

from compas_ifc.entities.objectdefinition import ObjectDefinition
from compas_ifc.helpers import public_attributes


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

    """

    def __init__(self, entity, model) -> None:
        super().__init__(entity, model)
        self._axis = None
        self._box = None
        self._body = None
        self._opening = None
        self._body_with_opening = None
        self._transformation = None

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
            self._body = entity_body_geometry(self)
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def opening(self):
        from compas_ifc.representation import entity_opening_geometry

        if not self._opening:
            self._opening = entity_opening_geometry(self)
        return self._opening

    @opening.setter
    def opening(self, value):
        self._opening = value

    @property
    def body_with_opening(self):
        from compas_ifc.representation import entity_body_with_opening_geometry

        if not self._body_with_opening:
            self._body_with_opening = self.model.reader.get(self._entity.id()) or entity_body_with_opening_geometry(self)
        return self._body_with_opening

    @body_with_opening.setter
    def body_with_opening(self, value):
        self._body_with_opening = value

    @property
    def transformation(self):
        from compas_ifc.representation import entity_transformation

        if not self._transformation:
            self._transformation = entity_transformation(self)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value
