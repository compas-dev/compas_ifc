from typing import TYPE_CHECKING

from ifcopenshell.util.element import get_psets

from compas_ifc.conversions.pset import from_dict_to_pset
from compas_ifc.conversions.pset import from_psets_to_dict

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcObject
else:
    IfcObject = object


class IfcObject(IfcObject):
    """Extension class for :class:`IfcObject`.

    Attributes
    ----------
    properties : dict
        The property sets of the object.
    quantities : dict
        The quantity sets of the object.
    """

    _psetsmap = {}

    @property
    def psetsmap(self):
        if id(self.file) not in self._psetsmap:
            self._psetsmap[id(self.file)] = {}
        return self._psetsmap[id(self.file)]

    @property
    def property_sets(self):
        return from_psets_to_dict(self)

    @property_sets.setter
    def property_sets(self, psets):
        for name, pset in psets.items():
            if id(pset) in self.psetsmap:
                ifc_property_set = self.psetsmap[id(pset)]
            else:
                ifc_property_set = from_dict_to_pset(self.file, pset, name)
                self.psetsmap[id(pset)] = ifc_property_set
                # TODO: remove unused psets

            self.file.create(
                "IfcRelDefinesByProperties",
                OwnerHistory=self.file.default_owner_history,
                RelatingPropertyDefinition=ifc_property_set,
                RelatedObjects=[self],
            )

    @property
    def quantity_sets(self):
        qtos = get_psets(self.entity, qtos_only=True)
        for qto in qtos.values():
            del qto["id"]
        return qtos
