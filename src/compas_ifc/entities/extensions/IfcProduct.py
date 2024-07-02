from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcProduct
else:
    IfcProduct = object


class IfcProduct(IfcProduct):

    @property
    def transformation(self):
        from compas_ifc.conversions.geometries import entity_transformation

        return entity_transformation(self)

    @property
    def body_with_opening(self):
        return self.file.get_preloaded_geometry(self)

    @property
    def style(self):
        return self.file.get_preloaded_style(self)

    @property
    def body(self):
        from compas_ifc.conversions.geometries import entity_body_geometry

        if getattr(self, "_body", None) is None:
            self._body = entity_body_geometry(self, use_occ=self.file.use_occ)
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def opening(self):
        from compas_ifc.conversions.geometries import entity_opening_geometry

        if getattr(self, "_opening", None) is None:
            self._opening = entity_opening_geometry(self, use_occ=self.file.use_occ)
        return self._opening

    @opening.setter
    def opening(self, value):
        self._opening = value


    @property
    def geometry(self):
        return self.body_with_opening