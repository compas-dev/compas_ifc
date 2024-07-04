from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcSpatialElement
else:
    IfcSpatialElement = object


class IfcSpatialElement(IfcSpatialElement):
    @property
    def children(self):
        children = super().children
        children += sum([relation.RelatedElements for relation in self.ContainsElements()], [])
        # NOTE: in IFC2X3 this is in IfcSpatialStructureElement
        return list(set(children))
