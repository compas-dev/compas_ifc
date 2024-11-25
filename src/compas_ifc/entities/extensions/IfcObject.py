from typing import TYPE_CHECKING

import ifcopenshell.guid
from ifcopenshell.api import run
from ifcopenshell.util.element import get_psets
from compas_ifc.entities.base import Base
from compas_ifc.conversions.pset import from_dict_to_pset

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcObject
else:
    IfcObject = object


class IfcObject(IfcObject):
    _psetsmap = {}

    @property
    def psetsmap(self):
        if id(self.file) not in self._psetsmap:
            self._psetsmap[id(self.file)] = {}
        return self._psetsmap[id(self.file)]

    @property
    def property_sets(self):
        psets = get_psets(self.entity, psets_only=True)
        for pset in psets.values():
            del pset["id"]
        return psets

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
    def quantities(self):
        qtos = get_psets(self.entity, qtos_only=True)
        for qto in qtos.values():
            del qto["id"]
        return qtos
