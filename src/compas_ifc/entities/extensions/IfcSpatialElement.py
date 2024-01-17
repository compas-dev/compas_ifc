from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcSpatialElement
else:
    IfcSpatialElement = object


class IfcSpatialElement(IfcSpatialElement):
    @property
    def children(self):
        children = super().children
        relations = self.ContainsElements()
        if relations:
            children += relations[0].RelatedElements

        return children
