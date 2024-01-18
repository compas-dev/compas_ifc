from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcObject
else:
    IfcObject = object


class IfcObject(IfcObject):
    @property
    def properties(self):
        from ifcopenshell.util.element import get_psets

        return get_psets(self.entity)
