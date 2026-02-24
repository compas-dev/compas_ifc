from typing import TYPE_CHECKING

from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation
from compas_ifc.conversions.frame import assign_entity_frame
from compas_ifc.conversions.representation import assign_body_representation
from compas.geometry import Frame

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcProduct
else:
    IfcProduct = object


class IfcProduct(IfcProduct):
    """Extension class for :class:`IfcProduct`.

    Attributes
    ----------
    style : dict
        The style of the product.
    visual_geometry : :class:`compas_ifc.brep.TessellatedBrep` or :class:`compas_occ.brep.OCCBrep`
        The evaluated visual geometry of the product, produced by ifcopenshell.geom.iterator.
        Suitable for display but does NOT preserve parametric information.
    geometry : :class:`compas_ifc.brep.TessellatedBrep` or :class:`compas_occ.brep.OCCBrep`
        Backward-compatible access. Getter returns visual_geometry.
        Setter writes COMPAS geometry to the IFC file as a body representation.
    frame : :class:`compas.geometry.Frame`
        The frame of the product.
    """

    @property
    def style(self):
        return self.file.get_preloaded_style(self)

    @property
    def visual_geometry(self):
        """The evaluated visual geometry of the product.

        Produced by ifcopenshell.geom.iterator during ``load_geometries()``.
        Suitable for display but does NOT preserve parametric information
        (extrusion profiles, boolean trees, instancing relationships, etc.).

        Returns
        -------
        :class:`compas_ifc.brep.TessellatedBrep` or :class:`compas_occ.brep.OCCBrep` or None
        """
        if not getattr(self, "_visual_geometry", None):
            self._visual_geometry = self.file.get_preloaded_geometry(self)
            if self._visual_geometry:
                self._visual_geometry.name = self.Name
                if self.file.use_occ:
                    # NOTE: When using OCC, the geometry is pre-transformed to the frame of the entity.
                    # We need to re-transform the geometry back to its original location.
                    # This is not necessary when using TessellatedBrep.
                    T = self.frame.to_transformation()
                    self._visual_geometry.transform(T.inverse())
        return self._visual_geometry

    @visual_geometry.setter
    def visual_geometry(self, value):
        self._visual_geometry = value

    @property
    def geometry(self):
        """Backward-compatible geometry access.

        Getter returns the evaluated visual geometry (same as ``visual_geometry``).
        Setter writes a COMPAS geometry object to the IFC file as a body
        representation (IfcShapeRepresentation).

        Returns
        -------
        :class:`compas_ifc.brep.TessellatedBrep` or :class:`compas_occ.brep.OCCBrep` or None
        """
        return self.visual_geometry

    @geometry.setter
    def geometry(self, geometry):
        self._visual_geometry = geometry
        assign_body_representation(self, geometry)
        # TODO: delete existing representation

    @property
    def frame(self):
        if not getattr(self, "_frame", None):
            if self.ObjectPlacement:
                transformation = IfcLocalPlacement_to_transformation(self.ObjectPlacement)
                self._frame = Frame.from_transformation(transformation)
            else:
                self._frame = None
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame
        # TODO: consider parent frame
        assign_entity_frame(self, frame)
