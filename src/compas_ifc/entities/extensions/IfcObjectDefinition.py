from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcObjectDefinition
else:
    IfcObjectDefinition = object


class IfcObjectDefinition(IfcObjectDefinition):
    @property
    def parent(self):
        relations = self.Decomposes()
        if relations:
            return relations[0].RelatingObject
        else:
            return None

    @property
    def children(self):
        relations = self.IsDecomposedBy()
        if relations:
            return relations[0].RelatedObjects
        else:
            return []

    @property
    def material(self):
        from ifcopenshell.util.element import get_material

        return get_material(self.entity)
