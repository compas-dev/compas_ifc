"""
********************************************************************************
model
********************************************************************************

.. currentmodule:: compas_ifc.model

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Model

"""

from typing import List

from compas_ifc.entities.building import Building
from compas_ifc.entities.buildingelements import BuildingElementProxy
from compas_ifc.entities.buildingstorey import BuildingStorey
from compas_ifc.entities.entity import Entity
from compas_ifc.entities.project import Project
from compas_ifc.entities.site import Site

from .reader import IFCReader
from .writer import IFCWriter


class Model:
    """
    Class representing an entire IFC model.

    Parameters
    ----------
    filepath : str
        The path to the IFC file.
    entity_types : dict
        A dictionary mapping IFC entity types to corresponding compas_ifc.entities classes.
        This can be used to customize the classes used to represent IFC entities.

    Attributes
    ----------
    reader : :class:`IFCReader`
        The reader used to read the content of an IFC file.
    writer : :class:`IFCWriter`
        The writer used to write the content of an IFC file.
    schema : str
        The schema of the IFC file.
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

    def __init__(self, filepath: str = None, entity_types: dict = None) -> None:
        self.reader = IFCReader(model=self, entity_types=entity_types)
        self.writer = IFCWriter(model=self)
        self._inserted_entities = set()
        if filepath:
            self.open(filepath)

    def open(self, filepath: str) -> None:
        self.reader.open(filepath)

    def save(self, filepath: str) -> None:
        self.writer.save(filepath)

    def export(self, entities, filepath: str) -> None:
        self.writer.export(entities, filepath)

    def get_all_entities(self) -> List[Entity]:
        """Get all entities in the model."""
        return self.reader.get_all_entities() + list(self._inserted_entities)

    def get_entities_by_type(self, ifc_type: str, include_subtypes: bool = True) -> List[Entity]:
        """Get all entities of a specific ifc type in the model. If include_subtypes is True, also return entities of subtypes of the given type."""
        entities = self.reader.get_entities_by_type(ifc_type, include_subtypes)
        for entity in self._inserted_entities:
            if entity.ifc_type == ifc_type:
                entities.append(entity)
        return entities

    def get_entity_by_global_id(self, global_id) -> Entity:
        """Get an entity by its global id."""
        return self.reader.get_entity_by_global_id(global_id)

    def get_entity_by_id(self, name) -> Entity:
        """Get an entity by its id in the IFC file."""
        return self.reader.get_entity_by_id(name)

    def get_entities_by_name(self, entity_name) -> List[Entity]:
        """Get all entities with a specific name."""
        return self.reader.get_entities_by_name(entity_name)

    def print_spatial_hierarchy(self, max_level: int = 4) -> None:
        """Print the spatial hierarchy of the model."""
        self.project.print_spatial_hierarchy(max_level)

    @property
    def schema(self) -> str:
        return self.reader._schema

    @property
    def project(self) -> Project:
        if self.projects:
            return self.projects[0]

    @property
    def projects(self) -> List[Project]:
        return self.get_entities_by_type("IfcProject")

    @property
    def sites(self) -> List[Site]:
        return self.get_entities_by_type("IfcSite")

    @property
    def buildings(self) -> List[Building]:
        return self.get_entities_by_type("IfcBuilding")

    @property
    def building_storeys(self) -> List[BuildingStorey]:
        return self.get_entities_by_type("IfcBuildingStorey")

    @property
    def elements(self) -> List[Building]:
        return self.get_entities_by_type("IfcElement")

    def insert(self, geometry, parent=None, name=None, description=None) -> BuildingElementProxy:
        """Insert a geometry into the model. The geometry will be wrapped in a building element proxy.

        Parameters
        ----------
        geometry : :class:`compas.geometry.Geometry` or :class:`compas.datastructures.Mesh`
            The geometry to be inserted.
        parent : :class:`compas_ifc.entities.Entity`
            The parent entity of the geometry.
        name : str
            The name of the element.
        description : str
            The description of the element.

        Returns
        -------
        :class:`compas_ifc.entities.buildingelements.BuildingElementProxy`
            The building element proxy wrapping the geometry.
        """
        element = BuildingElementProxy(None, self)
        element.body = geometry
        element.parent = parent
        element["Name"] = name
        element["Description"] = description
        self._inserted_entities.add(element)
        return element
