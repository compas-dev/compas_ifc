from typing import List

import ifcopenshell
import os
import multiprocessing
import numpy as np
from compas.geometry import Transformation
import time

from compas_ifc.entities.entity import Entity


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

    def __init__(self, model, entity_types: dict = None, use_occ=True):
        self.filepath = None
        self.model = model
        self.entity_types = entity_types
        self.use_occ = use_occ
        self._file = ifcopenshell.file()
        self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(self._file.schema)
        self._entitymap = {}
        self._geometrymap = {}
        self._stylemap = {}

    def open(self, filepath: str):
        self.filepath = filepath
        self._file = ifcopenshell.open(filepath)
        self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(self._file.schema)
        self._entitymap = {}
        print("Opened file: {}".format(filepath))
        self.load_geometries()

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
        _entities = self._file.by_type(entity_type, include_subtypes=accept_subtypes)
        return [self.get_entity(_entity) for _entity in _entities]

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

    def file_size(self):
        """Returns the size of the IFC file in bytes."""
        file_stats = os.stat(self.filepath)
        size_in_mb = file_stats.st_size / (1024 * 1024)
        size_in_mb = round(size_in_mb, 2)
        return size_in_mb

    def get_preloaded_geometry(self, entity):
        return self._geometrymap.get(entity._entity.id())

    def get_preloaded_style(self, entity):
        return self._stylemap.get(entity._entity.id(), {})

    def load_geometries(self, include=None, exclude=None):
        """Load all the geometries of the IFC file using a fast multithreaded iterator."""
        print("Loading geometries...")
        import ifcopenshell.geom

        settings = ifcopenshell.geom.settings()
        if self.use_occ:
            settings.set(settings.USE_PYTHON_OPENCASCADE, True)

        iterator = ifcopenshell.geom.iterator(
            settings, self._file, multiprocessing.cpu_count(), include=include, exclude=exclude
        )
        start = time.time()
        if iterator.initialize():
            while True:
                shape = iterator.get()
                if self.use_occ:
                    from compas_occ.brep import OCCBrep

                    brep = OCCBrep.from_shape(shape.geometry)

                    shellcolors = []
                    for style_id, style in zip(shape.style_ids, shape.styles):
                        if style_id == -1:
                            shellcolors.append((0.5, 0.5, 0.5, 1.0))
                        else:
                            shellcolors.append(style)

                    self._geometrymap[shape.data.id] = brep
                    self._stylemap[shape.data.id] = {"shellcolors": shellcolors, "use_rgba": True}

                else:
                    from .brep import TessellatedBrep

                    matrix = shape.transformation.matrix.data
                    faces = shape.geometry.faces
                    edges = shape.geometry.edges
                    verts = shape.geometry.verts

                    matrix = np.array(matrix).reshape((4, 3))
                    matrix = np.hstack([matrix, np.array([[0], [0], [0], [1]])])
                    matrix = matrix.transpose()
                    transformation = Transformation.from_matrix(matrix.tolist())

                    facecolors = []
                    for m_id in shape.geometry.material_ids:
                        if m_id == -1:
                            facecolors.append([0.5, 0.5, 0.5, 1])
                            facecolors.append([0.5, 0.5, 0.5, 1])
                            facecolors.append([0.5, 0.5, 0.5, 1])
                            continue
                        material = shape.geometry.materials[m_id]
                        color = (*material.diffuse, 1 - material.transparency)
                        facecolors.append(color)
                        facecolors.append(color)
                        facecolors.append(color)

                    brep = TessellatedBrep(vertices=verts, edges=edges, faces=faces)

                    brep.transform(transformation)
                    self._geometrymap[shape.id] = brep
                    self._stylemap[shape.id] = {"facecolors": facecolors}

                if not iterator.next():
                    break

        print("Time to load all geometries ", time.time() - start)
