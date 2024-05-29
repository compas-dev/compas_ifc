from typing import List

import ifcopenshell

from compas_ifc.entities.building import Building
from compas_ifc.entities.buildingelements import BuildingElement
from compas_ifc.entities.buildingelements import BuildingElementProxy
from compas_ifc.entities.buildingstorey import BuildingStorey
from compas_ifc.entities.element import Element
from compas_ifc.entities.entity import Entity
from compas_ifc.entities.geographicelement import GeographicElement
from compas_ifc.entities.project import Project
from compas_ifc.entities.site import Site
from compas_ifc.entities import DEFAULT_ENTITY_TYPES
from compas.data import json_dump
from compas.data import json_load
from uuid import uuid4

from .reader import IFCReader
from .writer import IFCWriter

import os


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

    def __init__(self, filepath: str = None, entity_types: dict = None, use_occ=False, schema=None, load_geometries=True) -> None:
        self.reader = IFCReader(model=self, entity_types=entity_types, use_occ=use_occ)
        self.writer = IFCWriter(model=self)
        self._new_entities = set()
        self._projects = None
        self._sites = None
        self._buildings = None
        self._building_storeys = None
        self._elements = None
        self._building_elements = None
        self._geographic_elements = None
        self._schema = None
        if schema:
            self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema)

        if filepath:
            self.open(filepath, load_geometries=load_geometries)

    def open(self, filepath: str, load_geometries=True) -> None:
        self.reader.open(filepath, load_geometries=load_geometries)

    def save(self, filepath: str) -> None:
        self.writer.save(filepath)

    def export(self, entities, filepath: str) -> None:
        self.writer.export(entities, filepath)

    def get_all_entities(self) -> List[Entity]:
        """Get all entities in the model."""
        return self.reader.get_all_entities() + list(self._new_entities)

    def get_entities_by_type(self, ifc_type: str, include_subtypes: bool = True, sort_by_name=True) -> List[Entity]:
        """Get all entities of a specific ifc type in the model. If include_subtypes is True, also return entities of subtypes of the given type."""
        entities = self.reader.get_entities_by_type(ifc_type, include_subtypes)
        for entity in self._new_entities:
            if entity.is_a(ifc_type):
                entities.append(entity)

        if sort_by_name:
            entities.sort(key=lambda x: x.name if x.name else "")
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

    def print_summary(self):
        """Print a summary of the model."""

        print("=" * 80)
        print("File: {}".format(self.reader.filepath))
        # print("Size: {} MB".format(self.reader.file_size()))
        print("Project: {}".format(self.project.name))
        print("Description: {}".format(self.project.attributes.get("Description", "")))
        print("Number of sites: {}".format(len(self.sites)))
        print("Number of buildings: {}".format(len(self.buildings)))
        print("Number of building elements: {}".format(len(self.building_elements)))
        print("=" * 80)

    @property
    def schema(self) -> str:
        return self._schema or self.reader._schema

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

    def create(self, cls=None, parent=None, geometry=None, frame=None, psets=None, **kwargs):
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

        def get_type(type_name):

            types = DEFAULT_ENTITY_TYPES.copy()
            if self.reader.entity_types:
                types.update(self.reader.entity_types)

            for key, value in types.items():
                if key == type_name:
                    return value

            return BuildingElementProxy

        if not isinstance(cls, type):
            cls = get_type(cls)

        entity = cls(None, self)
        entity.set_attributes(kwargs)

        if frame:
            if not hasattr(entity, "frame"):
                raise TypeError(f"{cls} cannot be assigned a frame.")
            entity.frame = frame

        if geometry:
            if not hasattr(entity, "body"):
                raise TypeError(f"{cls} cannot be assigned a geometry.")
            entity.body = geometry

        if parent:
            if not hasattr(entity, "parent"):
                raise TypeError(f"{cls} cannot be assigned a parent.")
            entity.parent = parent

        if psets:
            entity.psets = psets

        self._new_entities.add(entity)

        if cls == Project:
            self._projects = [entity]

        return entity

    def insert(self, geometry, parent=None, name=None, description=None, cls=None, frame=None) -> BuildingElementProxy:
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
        element.frame = frame
        element["Name"] = name
        element["Description"] = description
        self._new_entities.add(element)
        return element

    def export_session(self, path, export_geometries=True):

        try:
            from compas_occ.brep import Brep
            from compas.geometry import Box
            from compas.geometry import Sphere
            from compas.geometry import Shape
            from compas.datastructures import Mesh
            import shutil

        except ImportError:
            raise ImportError("The export_session method requires compas_occ to be installed.")

        if os.path.exists(path):
            if input(f"Directory {path} already exists. Do you want to overwrite it? (Y/n): ") != "n":
                shutil.rmtree(path)
            else:
                return

        os.makedirs(path, exist_ok=True)
        os.makedirs(os.path.join(path, "geometries"), exist_ok=True)

        geometry_map = {}

        def export_entity(entity: Entity, geometry_map=geometry_map):

            data = {}
            data["type"] = entity.ifc_type
            data["name"] = entity.name
            data["description"] = entity["Description"]

            if entity.psets:
                data["psets"] = entity.psets

            if entity.children:
                data["children"] = []

                for child in entity.children:
                    data["children"].append(export_entity(child))

            if export_geometries and hasattr(entity, "body_with_opening") and entity.body_with_opening:

                if geometry_map.get(id(entity.body_with_opening)):
                    # TODO: check when reading from existing IFC files.
                    data["geometry"] = geometry_map[id(entity.body_with_opening)]
                else:
                    if isinstance(entity.body_with_opening, Box):
                        brep = Brep.from_box(entity.body_with_opening)
                    elif isinstance(entity.body_with_opening, Sphere):
                        brep = Brep.from_sphere(entity.body_with_opening)
                    elif isinstance(entity.body_with_opening, Mesh):
                        brep = Brep.from_mesh(entity.body_with_opening)
                    elif isinstance(entity.body_with_opening, Shape):
                        brep = Brep.from_mesh(Mesh.from_shape(entity.body_with_opening))
                    elif isinstance(entity.body_with_opening, Brep):
                        brep = entity.body_with_opening
                    else:
                        raise ValueError(f"Geometry type {type(entity.body_with_opening)} not supported.")

                    file_name = f"{uuid4()}.stp"
                    brep.to_step(os.path.join(path, "geometries", file_name))
                    data["geometry"] = file_name
                    geometry_map[id(entity.body_with_opening)] = file_name

            if entity.frame:
                data["frame"] = entity.frame

            return data

        data = export_entity(self.project, geometry_map=geometry_map)
        json_dump(data, os.path.join(path, "session.json"), pretty=False)

    def load_session(self, path):

        try:
            from compas_occ.brep import Brep
            from compas_ifc.entities import DEFAULT_ENTITY_TYPES

        except ImportError:
            raise ImportError("The load_session method requires compas_occ to be installed.")

        session = json_load(os.path.join(path, "session.json"))
        geometry_map = {}

        def get_type(type_name):
            types = DEFAULT_ENTITY_TYPES.copy()
            if self.reader.entity_types:
                types.update(self.reader.entity_types)

            for key, value in types.items():
                if key == type_name:
                    return value

            return BuildingElementProxy

        def load_entity(data, parent=None, geometry_map=geometry_map):

            ifc_type = get_type(data["type"])
            entity = self.create(ifc_type, parent=parent, Name=data["name"], Description=data.get("description", ""))

            if "children" in data:
                for child_data in data["children"]:
                    load_entity(child_data, entity)

            if "geometry" in data:
                if geometry_map.get(data["geometry"]):
                    entity.body = geometry_map.get(data["geometry"])
                else:
                    entity.body = Brep.from_step(os.path.join(path, "geometries", data["geometry"]))
                    geometry_map[data["geometry"]] = entity.body

            if "frame" in data:
                print(entity)
                entity.frame = data["frame"]

            if "psets" in data:
                entity.psets = data["psets"]

        load_entity(session, parent=None, geometry_map=geometry_map)

    @classmethod
    def template(cls, schema="IFC4", building_count=1, storey_count=1):
        model = cls(schema=schema)
        project = model.create(Project, Name="Default Project")
        site = model.create(Site, parent=project, Name="Default Site")
        for i in range(building_count):
            building = model.create(Building, parent=site, Name=f"Default Building {i+1}")
            for j in range(storey_count):
                model.create(BuildingStorey, parent=building, Name=f"Default Storey {j+1}")
        return model

    def show(self, entity=None):
        try:
            from compas_viewer import Viewer
            from compas.datastructures import Tree
            from compas.datastructures import TreeNode
            from compas_viewer.config import Config
            from compas_viewer.components import Treeform
            from compas_viewer.components import Sceneform
        except ImportError:
            raise ImportError("The show method requires compas_viewer to be installed.")

        config = Config()
        config.ui.sidebar.sceneform = False
        config.ui.sidedock.show = False

        viewer = Viewer(config=config)

        entity_map = {}

        def parse_entity(entity, parent=None):
            
            obj = None
            if getattr(entity, "geometry", None):
                if not entity.is_a("IfcSpace"):
                    obj = viewer.scene.add(entity.geometry, name=entity.name, parent=parent, **entity.style)
            if entity.children:
                obj = viewer.scene.add([], name=entity.name, parent=parent)
                for child in entity.children:
                    parse_entity(child, parent=obj)
            
            if obj:
                entity_map[id(obj)] = entity

        parse_entity(entity or self.project)

        propertyform = Treeform(Tree(), {"Name": (lambda o: o.name), "value": (lambda o: o.attributes.get("value", ""))})

        def callback(obj):

            entity = entity_map[id(obj)]
            tree = Tree()
            root = TreeNode("ROOT")
            tree.add(root)
            attribute_node = TreeNode("Attributes")
            root.add(attribute_node)
            for name, value in entity.attributes.items():
                attribute_node.add(TreeNode(name, value=value))

            properties_node = TreeNode("Properties")
            root.add(properties_node)

            
            for pset, properties in entity.psets.items():
                pset_node = TreeNode(pset)
                properties_node.add(pset_node)
                for name, value in properties.items():
                    pset_node.add(TreeNode(name, value=value))

            propertyform.tree = tree
            propertyform.update()

        def get_name(obj):
            entity = entity_map.get(id(obj))
            if entity:
                return f"[{entity.ifc_type}] {entity.name}"
            return ""

        sceneform = Sceneform(viewer.scene, {"Name": get_name}, callback=callback)
        

        viewer.ui.sidebar.widget.addWidget(sceneform)
        viewer.ui.sidebar.widget.addWidget(propertyform)

        viewer.show()
