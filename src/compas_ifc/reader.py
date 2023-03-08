import ifcopenshell
from compas_ifc.entities.entity import Entity
from typing import List


class IFCReader(object):
    """A class for reading IFC files.

    Parameters
    ----------
    model : :class:`compas_ifc.model.Model`
        The model to which the reader belongs.
    entity_types : dict
        A dictionary mapping IFC entity types to corresponding compas_ifc.entities classes.
        This can be used to customize the classes used to represent IFC entities.

    Attributes
    ----------
    model : :class:`compas_ifc.model.Model`
        The model to which the reader belongs.
    entity_types : dict
        A dictionary mapping IFC entity types to corresponding compas_ifc.entities classes.
    projects : List[:class:`Project`]
        The projects contained in the model.
        Typically there is exactly one.
    project : :class:`Project`
        The project of the model.
    sites : List[:class:`Site`]
        The sites contained in the model.
        In a correctly formed hierarchical model, sites are part of a project.
        If that is not the case, they are also accessible here.
    buildings : List[:class:`Building`]
        The buildings contained in the model.
        In a correctly formed hierarchical model, buildings are part of a site.
        If that is not the case, they are also accessible here.
    building_storeys : List[:class:`BuildingStorey`]
        The building storeys contained in the model.
    elements : List[:class:`BuildingElement`]
        All the building elements contained in the model.
        In a correctly formed hierarchical model, building elements are part of a building, building storey, or space.
        If that is not the case, they are also accessible here.

    """

    def __init__(self, model, entity_types: dict = None):
        self.filepath = None
        self.model = model
        self.entity_types = entity_types
        self._file = ifcopenshell.file()
        self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(self._file.schema)
        self._entitymap = {}

    def open(self, filepath: str):
        self.filepath = filepath
        self._file = ifcopenshell.open(filepath)
        self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(self._file.schema)
        self._entitymap = {}
        self.get_all_entities()
        print("Opened file: {}".format(filepath))

    def get_entity(self, entity: ifcopenshell.entity_instance):
        """
        Returns the compas_ifc entity corresponding to the given ifcopenshell entity.

        Parameters
        ----------
        entity : ifcopenshell.entity_instance
            The ifcopenshell entity.

        Returns
        -------
        :class:`compas_ifc.entities.entity.Entity`
            The compas_ifc entity.
        """
        return self._entitymap.setdefault(entity.id(), Entity.factory(entity, self.model, self.entity_types))

    def get_entities_by_type(self, entity_type, accept_subtypes=True):
        """
        Returns all the entities of the given type.

        Parameters
        ----------
        entity_type : str
            The type of the entities to return.
        accept_subtypes : bool, optional
            Whether to include subtypes of the given type.
            Defaults to True.

        Returns
        -------
        List[:class:`compas_ifc.entities.entity.Entity`]
            The entities of the given type.
        """
        entities = []
        for entity in self._entitymap.values():
            if accept_subtypes:
                if entity._entity.is_a(entity_type):
                    entities.append(entity)
            else:
                if entity.ifc_type == entity_type:
                    entities.append(entity)

        return entities

    def get_entities_by_name(self, entity_name) -> List[Entity]:
        """Returns all the entities with the given name."""
        entities = self.get_entities_by_type("IfcRoot")
        return [entity for entity in entities if entity.name == entity_name]

    def get_entity_by_global_id(self, global_id) -> Entity:
        """Returns the entity with the given global id."""
        ifc_entity = self._file.by_guid(global_id)
        if ifc_entity:
            return self.get_entity(ifc_entity)

    def get_entity_by_id(self, id) -> Entity:
        """Returns the entity with the given id."""
        ifc_entity = self._file.by_id(id)
        if ifc_entity:
            return self.get_entity(ifc_entity)

    def get_all_entities(self) -> List[Entity]:
        """Returns all the entities in the model."""
        return [self.get_entity(_entity) for _entity in self._file]
