import ifcopenshell
from compas_ifc.entities.base import Base
import os

class IFCReader(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self._file = ifcopenshell.open(filepath)
        self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(self._file.schema)
        self._entitymap = {}
        print("IFC file loaded: {}".format(filepath))

    def from_entity(self, entity):
        
        if not isinstance(entity, ifcopenshell.entity_instance):
            raise TypeError("Input is not an ifcopenshell.entity_instance")
        
        _id = entity.id()

        if _id in self._entitymap:
            return self._entitymap[_id]
        else:
            entity = Base(entity, self)
            self._entitymap[_id] = entity
            return entity

    def get_by_type(self, type_name):
        entities = self._file.by_type(type_name)
        return [self.from_entity(entity) for entity in entities]

    def file_size(self):
        file_stats = os.stat(self.filepath)
        size_in_mb = file_stats.st_size / (1024 * 1024)
        size_in_mb = round(size_in_mb, 2)
        return size_in_mb


if __name__ == "__main__":
    reader = IFCReader("data/wall-with-opening-and-window.ifc")
    reader.file_size()
    # print(len(reader._file))
    # entities = reader.get_by_type("IfcProject")    
    # entities[0].print_attributes(max_depth=1)
                  
    # for key in entities[0]:
    #     print(key, entities[0][key])
