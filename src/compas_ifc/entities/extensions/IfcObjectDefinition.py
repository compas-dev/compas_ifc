from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcObjectDefinition
else:
    IfcObjectDefinition = object


class IfcObjectDefinition(IfcObjectDefinition):

    def __repr__(self):
        return "<#{} {} \"{}\">".format(self.entity.id(), self.__class__.__name__, self.Name)

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
    def descendants(self):
        descendants = []

        for child in self.children:
            descendants.append(child)
            descendants.extend(child.descendants)

        return descendants

    @property
    def material(self):
        from ifcopenshell.util.element import get_material

        return get_material(self.entity)

    def children_by_type(self, type_name, recursive=False):
        if not recursive:
            return [child for child in self.children if child.is_a(type_name)]
        else:
            return [child for child in self.descendants if child.is_a(type_name)]
