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
    style : :class:`IfcStyle`
        The style of the product.
    geometry : :class:`compas_ifc.brep.TessellatedBrep`
        The geometry of the product. (OCCBrep is using COMPAS OCC)
    frame : :class:`compas.geometry.Frame`
        The frame of the product.
    """

    @property
    def style(self):
        return self.file.get_preloaded_style(self)

    @property
    def geometry(self):
        if not getattr(self, "_geometry", None):
            self._geometry = self.file.get_preloaded_geometry(self)
            if self._geometry:
                self._geometry.name = self.Name
                if self.file.use_occ:
                    # NOTE: When using OCC, the geometry is pre-transformed to the frame of the entity.
                    # We need to re-transform the geometry back to its original location.
                    # This is not necessary when using TessellatedBrep.
                    T = self.frame.to_transformation()
                    self._geometry.transform(T.inverse())
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        self._geometry = geometry
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
