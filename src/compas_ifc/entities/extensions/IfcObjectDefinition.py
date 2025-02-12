from typing import TYPE_CHECKING

from ifcopenshell.util.element import get_material

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcObjectDefinition
else:
    IfcObjectDefinition = object


class IfcObjectDefinition(IfcObjectDefinition):
    """Extension class for :class:`IfcObjectDefinition`.

    Attributes
    ----------
    parent : :class:`IfcObjectDefinition`
        The parent object definition of the object definition.
    children : list[:class:`IfcObjectDefinition`]
        The children object definitions of the object definition.
    material : :class:`IfcMaterial`
        The material of the object definition.
    """

    def __repr__(self):
        return '<#{} {} "{}">'.format(self.entity.id(), self.__class__.__name__, self.Name)

    @property
    def parent(self):
        relations = self.Decomposes()
        if relations:
            return relations[0].RelatingObject
        else:
            return None

    @property
    def children(self):
        return sum([relation.RelatedObjects for relation in self.IsDecomposedBy()], [])

    @property
    def descendants(self):
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.descendants)
        return descendants

    @property
    def material(self):
        material = get_material(self.entity)
        if material:
            return self.file.from_entity(material)
        else:
            return None

    def children_by_type(self, type_name, recursive=False):
        if not recursive:
            return [child for child in self.children if child.is_a(type_name)]
        else:
            return [child for child in self.descendants if child.is_a(type_name)]
