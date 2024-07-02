from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC2X3 import IfcSpatialStructureElement
else:
    IfcSpatialStructureElement = object


class IfcSpatialStructureElement(IfcSpatialStructureElement):
    @property
    def children(self):
        children = super().children
        relations = self.ContainsElements()
        # NOTE: in IFC4 this is in IfcSpatialElement
        if relations:
            children += relations[0].RelatedElements

        return children
