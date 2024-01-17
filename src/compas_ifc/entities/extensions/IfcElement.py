from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcElement
else:
    IfcElement = object


class IfcElement(IfcElement):
    @property
    def parent(self):
        relations = self.ContainedInStructure()
        if relations:
            return relations[0].RelatingStructure
        else:
            return super().parent
