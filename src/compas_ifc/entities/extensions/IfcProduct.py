from typing import TYPE_CHECKING

from compas_ifc.conversions.frame import IfcLocalPlacement_to_frame
from compas_ifc.conversions.frame import assign_entity_frame
from compas_ifc.conversions.representation import assign_body_representation

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
            if self.frame and self._geometry:
                # NOTE: preloaded geometry is pre-transformed because of boolean.
                # The pre-transformation is not necessarily the same as the frame of entity.
                # Therefore, we need to re-transform the geometry back to its original location.
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
                self._frame = IfcLocalPlacement_to_frame(self.ObjectPlacement)
            else:
                self._frame = None

        # print(self._frame)
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame
        # TODO: consider parent frame
        assign_entity_frame(self, frame)
