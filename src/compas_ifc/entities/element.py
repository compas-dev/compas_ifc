from .product import Product


class Element(Product):
    """
    Class representing an IFC element. An element is a product that is intended to be physically constructed or installed.

    Attributes
    ----------
    parent : :class:`compas_ifc.entities.SpatialElement`
        The spatial element containing this element.

    """

    def contained_in_structure(self):
        """Return the spatial structure containing this element."""
        if self not in self.model._inserted_entities:
            for rel in self._entity.ContainedInStructure:
                return self.model.reader.get_entity(rel)

    @property
    def parent(self):
        if not self._parent:
            relation = self.contained_in_structure()
            if relation:
                self._parent = relation["RelatingStructure"]
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
