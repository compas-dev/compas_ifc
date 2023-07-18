from typing import List

from compas_ifc.entities.element import Element
from compas_ifc.entities.building import Building
from compas_ifc.entities.buildingelements import BuildingElement
from compas_ifc.entities.geographicelement import GeographicElement
from compas_ifc.entities.buildingelements import BuildingElementProxy
from compas_ifc.entities.buildingstorey import BuildingStorey
from compas_ifc.entities.objectdefinition import ObjectDefinition
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
        self._new_entities = set()
        self._projects = None
        self._sites = None
        self._buildings = None
        self._building_storeys = None
        self._elements = None
        self._building_elements = None
        self._geographic_elements = None
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
        return self.reader.get_all_entities() + list(self._new_entities)

    def get_entities_by_type(self, ifc_type: str, include_subtypes: bool = True) -> List[Entity]:
        """Get all entities of a specific ifc type in the model. If include_subtypes is True, also return entities of subtypes of the given type."""
        entities = self.reader.get_entities_by_type(ifc_type, include_subtypes)
        for entity in self._new_entities:
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
        if self._projects is None:
            self._projects = self.get_entities_by_type("IfcProject")
        return self._projects

    @property
    def sites(self) -> List[Site]:
        if self._sites is None:
            self._sites = self.get_entities_by_type("IfcSite")
        return self._sites

    @property
    def buildings(self) -> List[Building]:
        if self._buildings is None:
            self._buildings = self.get_entities_by_type("IfcBuilding")
        return self._buildings

    @property
    def building_storeys(self) -> List[BuildingStorey]:
        if self._building_storeys is None:
            self._building_storeys = self.get_entities_by_type("IfcBuildingStorey")
        return self._building_storeys

    @property
    def elements(self) -> List[Element]:
        if self._elements is None:
            self._elements = self.get_entities_by_type("IfcElement")
        return self._elements

    @property
    def building_elements(self) -> List[BuildingElement]:
        if self._building_elements is None:
            self._building_elements = self.get_entities_by_type("IfcBuildingElement")
        return self._building_elements

    @property
    def geographic_elements(self) -> List[GeographicElement]:
        if self._geographic_elements is None:
            self._geographic_elements = self.get_entities_by_type("IfcGeographicElement")
        return self._geographic_elements

    def create(self, cls, attributes, parent=None):
        """Create an entity and add it to the model.

        Parameters
        ----------
        cls : :class:`compas_ifc.entities.Entity`
            The type of entity to create.
        attributes : dict
            The attributes of the entity.
        parent : :class:`compas_ifc.entities.Entity`
            The parent entity of the entity.

        Returns
        -------
        :class:`compas_ifc.entities.Entity`
            The created entity.
        """
        entity = cls(None, self)
        entity.set_attributes(attributes)
        if parent:
            if isinstance(entity, ObjectDefinition):
                entity.parent = parent
            else:
                print(hasattr(entity, "parent"))
                raise ValueError(f"{entity} cannot be assigned a parent.")
        self._new_entities.add(entity)

        if cls == Project:
            self._projects = [entity]

        return entity

    def insert(self, geometry, parent=None, name=None, description=None, cls=None) -> BuildingElementProxy:
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
        if cls is None:
            cls = BuildingElementProxy
        element = cls(None, self)
        element.body = geometry
        element.parent = parent
        element["Name"] = name
        element["Description"] = description
        self._new_entities.add(element)
        return element
