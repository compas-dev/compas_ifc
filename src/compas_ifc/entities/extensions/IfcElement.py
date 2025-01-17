from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcElement
else:
    IfcElement = object


class IfcElement(IfcElement):
    """Extension class for :class:`IfcElement`.

    Attributes
    ----------
    parent : :class:`IfcElement`
        The parent element of the element.
    """

    @property
    def parent(self):
        relations = self.ContainedInStructure()
        if relations:
            return relations[0].RelatingStructure
        else:
            return super().parent
