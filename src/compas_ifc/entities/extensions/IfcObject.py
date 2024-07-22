from typing import TYPE_CHECKING

import ifcopenshell.guid
from ifcopenshell.api import run
from ifcopenshell.util.element import get_psets
from ifcopenshell.util.element import get_quantities

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcObject
else:
    IfcObject = object


class IfcObject(IfcObject):
    _psetsmap = {}

    @property
    def properties(self):
        psets = get_psets(self.entity, psets_only=True)
        for pset in psets.values():
            del pset["id"]
        return psets

    @properties.setter
    def properties(self, psets):
        if id(self.file) not in self._psetsmap:
            self._psetsmap[id(self.file)] = {}

        psetsmap = self._psetsmap[id(self.file)]

        for name, properties in psets.items():
            if id(properties) in psetsmap:
                pset = psetsmap[id(properties)]
                # TODO: Check if relation already exists
                self.file._create_entity(
                    "IfcRelDefinesByProperties",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=self.file.default_owner_history,
                    RelatingPropertyDefinition=pset,
                    RelatedObjects=[self.entity],
                )

            else:
                pset = run("pset.add_pset", self.file._file, product=self.entity, name=name)
                psetsmap[id(properties)] = pset
                for key, value in properties.items():
                    if not isinstance(value, (str, int, float)):
                        properties[key] = str(value)
                run("pset.edit_pset", self.file._file, pset=pset, properties=properties)
                # TODO: remove unused psets

    @property
    def quantities(self):
        qtos = get_psets(self.entity, qtos_only=True)
        return get_quantities(qtos)
