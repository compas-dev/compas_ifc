from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcSpatialElement
else:
    IfcSpatialElement = object


class IfcSpatialElement(IfcSpatialElement):
    @property
    def children(self):
        children = super().children
        relations = self.ContainsElements()
        # NOTE: in IFC2X3 this is in IfcSpatialStructureElement
        if relations:
            children += relations[0].RelatedElements

        return list(set(children))
