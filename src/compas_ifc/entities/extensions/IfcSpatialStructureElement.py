from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC2X3 import IfcSpatialStructureElement
else:
    IfcSpatialStructureElement = object


class IfcSpatialStructureElement(IfcSpatialStructureElement):
    """Extension class for :class:`IfcSpatialStructureElement`.

    Attributes
    ----------
    children : list[:class:`IfcSpatialElement`]
        The children spatial elements of the spatial structure element.
    """

    @property
    def children(self):
        children = super().children
        children += sum([relation.RelatedElements for relation in self.ContainsElements()], [])
        # NOTE: in IFC4 this is in IfcSpatialElement
        return list(set(children))
