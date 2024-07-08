from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcProduct
else:
    IfcProduct = object


class IfcProduct(IfcProduct):
    @property
    def style(self):
        return self.file.get_preloaded_style(self)

    @property
    def geometry(self):
        if not getattr(self, "_geometry", None):
            self._geometry = self.file.get_preloaded_geometry(self)
            if self.frame:
                # NOTE: preloaded geometry is pre-transformed because of boolean.
                # The pre-transformation is not necessarily the same as the frame of entity.
                # Therefore, we need to re-transform the geometry back to its original location.
                T = self.frame.to_transformation()
                self._geometry.transform(T.inverse())
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        from compas_ifc.resources.representation import write_body_representation

        self._geometry = geometry
        # Update the representation in the IFC file
        # TODO: delete existing representation
        # TODO: make this function more transparent
        write_body_representation(self.file._file, geometry, self.entity, self.file.default_body_context.entity)

    @property
    def frame(self):
        from compas_ifc.representation import IfcLocalPlacement_to_frame

        if not getattr(self, "_frame", None):
            if self.ObjectPlacement:
                self._frame = IfcLocalPlacement_to_frame(self.ObjectPlacement)
            else:
                self._frame = None

        # print(self._frame)
        return self._frame

    @frame.setter
    def frame(self, frame):
        from compas_ifc.resources.shapes import frame_to_ifc_axis2_placement_3d

        self._frame = frame
        # Update the placement in the IFC file
        # TODO: consider parent frame
        # TODO: make this function more transparent
        loacal_placement = frame_to_ifc_axis2_placement_3d(self.file._file, frame)
        placement = self.file._create_entity("IfcLocalPlacement", RelativePlacement=loacal_placement)
        self.ObjectPlacement = placement
