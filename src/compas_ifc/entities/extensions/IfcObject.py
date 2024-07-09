from typing import TYPE_CHECKING

from ifcopenshell.api import run
from ifcopenshell.util.element import get_psets

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcObject
else:
    IfcObject = object


class IfcObject(IfcObject):
    _psetsmap = {}

    @property
    def properties(self):
        return get_psets(self.entity)

    @properties.setter
    def properties(self, psets):
        for name, properties in psets.items():
            if id(properties) in self._psetsmap:
                pset = self._psetsmap[id(properties)]
                # TODO: Check if relation already exists
                self.file.create_entity("IfcRelDefinesByProperties", GlobalId=self.create_guid(), RelatingPropertyDefinition=pset, RelatedObjects=[self.entity])
            else:
                pset = run("pset.add_pset", self.file._file, product=self.entity, name=name)
                self._psetsmap[id(properties)] = pset
                for key, value in properties.items():
                    if not isinstance(value, (str, int, float)):
                        properties[key] = str(value)
                run("pset.edit_pset", self.file._file, pset=pset, properties=properties)
                # TODO: remove unused psets
