from compas_view2.collections import Collection
from compas_view2.objects import CollectionObject

from compas_ifc.entities.entity import Entity
from compas_ifc.representation import entity_body_geometry


class EntityObject(CollectionObject):
    def __init__(self, entity: Entity, **kwargs):
        super().__init__(Collection(entity_body_geometry(entity)), **kwargs)
        self._entity = entity

    @property
    def entity(self):
        return self._entity
