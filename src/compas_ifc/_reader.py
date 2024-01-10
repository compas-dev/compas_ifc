import ifcopenshell
from compas_ifc.entities.base import Base


class IFCReader(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self._file = ifcopenshell.open(filepath)
        self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(self._file.schema)
        self._entitymap = {}
        # self.get_all_entities()
        # print("Opened file: {}".format(filepath))

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


if __name__ == "__main__":
    reader = IFCReader("data/wall-with-opening-and-window.ifc")
    # print(len(reader._file))
    entities = reader.get_by_type("IfcWall")    
    attributes = entities[0].attributes
                  
    print()

