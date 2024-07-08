import multiprocessing
import os
import time

import ifcopenshell
import numpy as np
from compas.geometry import Transformation
from ifcopenshell.api import run

from compas_ifc.entities.base import Base


class IFCFile(object):
    def __init__(self, model, filepath=None, schema="IFC4", use_occ=False, load_geometries=True):
        self._entitymap = {}
        self._geometrymap = {}
        self._stylemap = {}
        self._relationmap_aggregates = {}  # map of IfcRelAggregates
        self._relationmap_contains = {}  # map of IfcRelContainedInSpatialStructure
        self._default_context = None
        self._default_body_context = None

        self.filepath = filepath
        self.model = model
        self.use_occ = use_occ
        if filepath is None:
            self._file = ifcopenshell.file(schema=schema)
            print("IFC file created in schema: {}".format(schema))
        else:
            self._file = ifcopenshell.open(filepath)
            print("IFC file loaded: {}".format(filepath))

        self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(self._file.schema)

        if load_geometries and filepath is not None:
            self.load_geometries()

    def file_size(self):
        file_stats = os.stat(self.filepath)
        size_in_mb = file_stats.st_size / (1024 * 1024)
        size_in_mb = round(size_in_mb, 2)
        return size_in_mb

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

    def get_entities_by_type(self, type_name) -> list[Base]:
        entities = self._file.by_type(type_name)
        return [self.from_entity(entity) for entity in entities]

    def get_entities_by_name(self, name) -> list[Base]:
        return [entity for entity in self.get_entities_by_type("IfcRoot") if entity.Name == name]

    def get_entity_by_global_id(self, global_id) -> Base:
        return self.from_entity(self._file.by_guid(global_id))

    def get_entity_by_id(self, id) -> Base:
        return self.from_entity(self._file.by_id(id))

    def get_preloaded_geometry(self, entity):
        return self._geometrymap.get(entity.entity.id())

    def get_preloaded_style(self, entity):
        return self._stylemap.get(entity.entity.id(), {})

    def load_geometries(self, include=None, exclude=None):
        """Load all the geometries of the IFC file using a fast multithreaded iterator."""
        print("Loading geometries...")
        import ifcopenshell.geom

        settings = ifcopenshell.geom.settings()
        if self.use_occ:
            settings.set(settings.USE_PYTHON_OPENCASCADE, True)

        iterator = ifcopenshell.geom.iterator(settings, self._file, multiprocessing.cpu_count(), include=include, exclude=exclude)
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

        print(f"Time to load all {len(self._geometrymap)} geometries {(time.time() - start):.3f}s")

    def save(self, path):
        self._file.write(path)

    def create(self, cls="IfcBuildingElementProxy", parent=None, geometry=None, frame=None, psets=None, **kwargs):
        if isinstance(cls, type):
            cls_name = cls.__name__
        else:
            cls_name = cls

        entity = self._create_entity(cls_name, **kwargs)

        if parent:
            if hasattr(entity, "ContainedInStructure"):
                self._create_entity("IfcRelContainedInSpatialStructure", RelatingStructure=parent, RelatedElements=[entity])
            else:
                self._create_entity("IfcRelAggregates", RelatingObject=parent, RelatedObjects=[entity])

        if geometry:
            # TODO: Deal with instancing
            entity.geometry = geometry

        if frame:
            entity.frame = frame

        return entity

    def _create_entity(self, cls_name, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, Base):
                kwargs[key] = value.entity
            elif isinstance(value, (list, tuple)):
                kwargs[key] = [v.entity if isinstance(v, Base) else v for v in value]
        entity = self._file.create_entity(cls_name, **kwargs)
        return self.from_entity(entity)

    @property
    def default_body_context(self):
        contexts = self._file.by_type("IfcGeometricRepresentationSubContext")
        for context in contexts:
            if context.ContextIdentifier == "Body":
                self._default_body_context = context
                break
        if not self._default_body_context:
            self._default_body_context = run(
                "context.add_context",
                self._file,
                context_type="Model",
                context_identifier="Body",
                target_view="MODEL_VIEW",
                parent=self.default_context,
            )
        return self._default_body_context

    @property
    def default_context(self):
        contexts = self._file.by_type("IfcGeometricRepresentationContext")
        for context in contexts:
            if context.ContextType == "Model":
                self._default_context = context
                break
        if not self._default_context:
            self._default_context = run("context.add_context", self._file, context_type="Model")
        return self._default_context
