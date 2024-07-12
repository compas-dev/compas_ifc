from compas.datastructures import Tree
from compas.datastructures import TreeNode

from .root import Root


class ObjectDefinition(Root):
    """Base class for all object definitions. An object definition is a definition of a thing that is or may be part of a spatial structure.

    Attributes
    ----------
    parent : :class:`compas_ifc.entities.ObjectDefinition`
        The parent of this element in spatial hierarchy.
    children : List[:class:`compas_ifc.entities.ObjectDefinition`]
        The children of this element in spatial hierarchy.

    """

    def __init__(self, entity, model) -> None:
        super().__init__(entity, model)
        self._parent = None

    def decomposes(self):
        """Return the relation that decomposes this element."""
        if self not in self.model._new_entities:
            for rel in self._entity.Decomposes:
                return self.model.reader.get_entity(rel)

    @property
    def parent(self):
        if not self._parent and self._entity:
            relation = self.decomposes()
            if relation:
                self._parent = relation["RelatingObject"]
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def is_decomposed_by(self):
        """Return the relation that this element is decomposed by."""
        return [self.model.reader.get_entity(rel) for rel in self._entity.IsDecomposedBy]

    @property
    def children(self):
        children = [entity for entity in self.model.get_entities_by_type("IfcObjectDefinition") if entity.parent == self]
        for entity in self.model._new_entities:
            if entity.parent == self and entity not in children:
                children.append(entity)

        # sort children by name
        children.sort(key=lambda x: x.name)
        return children

    def traverse(self, recursive: bool = True):
        """Traverse children of this element.

        Parameters
        ----------
        recursive : bool, optional
            Whether to traverse down the tree recursively, by default True

        Yields
        ------
        :class:`compas_ifc.entities.ObjectDefinition`
            The children of this element.
        """
        for child in self.children:
            yield child
            if recursive:
                yield from child.traverse(recursive)

    def traverse_ancestor(self, recursive: bool = True):
        """Traverse ancestors of this element.

        Parameters
        ----------
        recursive : bool, optional
            Whether to traverse up the tree recursively, by default True

        Yields
        ------
        :class:`compas_ifc.entities.ObjectDefinition`
            The ancestors of this element.
        """
        parent = self.parent
        if parent:
            yield from parent.traverse_ancestor(recursive)
            yield parent

    def traverse_branch(self, recursive: bool = True):
        """Traverse the spatial branch of this element.

        Parameters
        ----------
        recursive : bool, optional
            Whether to traverse up and down the tree recursively, by default True

        Yields
        ------
        :class:`compas_ifc.entities.ObjectDefinition`
            The ancestors, self, and children of this element.
        """
        yield from self.traverse_ancestor(recursive)
        yield self
        yield from self.traverse(recursive)

    def print_spatial_hierarchy(self, max_level: int = 4) -> None:
        """Print the spatial hierarchy of this element.

        Parameters
        ----------
        max_level : int, optional
            The maximum level of the hierarchy to print, by default 4

        Returns
        -------
        None
        """
        print("=" * 80)
        print("SPATIAL HIERARCHY")
        print(self.spatial_hierarchy.get_hierarchy_string(max_depth=max_level))
        print("=" * 80)

    @property
    def spatial_hierarchy(self) -> Tree:
        tree = Tree()

        class Node(TreeNode):
            def __repr__(self):
                return str(self.name)

        root = Node(self)

        tree.add(root)

        def traverse(entity, parent):
            node = Node(entity)
            parent.add(node)
            for child in entity.children:
                traverse(child, node)

        traverse(self, root)
        return tree
