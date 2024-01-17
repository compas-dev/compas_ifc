from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcObjectDefinition
else:
    IfcObjectDefinition = object

from compas.datastructures import Tree, TreeNode


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
