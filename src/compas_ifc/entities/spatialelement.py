from typing import List
from compas_ifc.entities.product import Product


class SpatialElement(Product):
    """
    Class representing an IFC spatial element. A spatial element is a product that is used to spatially organize other products.
    """

    def is_containment_hierarchical(self) -> bool:
        """Return True if the spatial element is hierarchical, which means it can have only one decomposition parent."""
        if len(self._entity.Decomposes) > 1:
            return False
        return True

    def contains_elements(self) -> List["SpatialElement"]:
        """Returen contained elements of a spatial element."""
        return [self.model.reader.get_entity(rel) for rel in self._entity.ContainsElements]
