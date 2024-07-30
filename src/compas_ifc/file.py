import multiprocessing
import os
import time
from typing import Any
from typing import Union

import ifcopenshell
import numpy as np
from compas.geometry import Transformation
from ifcopenshell.api import run

import compas_ifc
from compas_ifc.entities.base import Base


class IFCFile(object):
    def __init__(self, model, filepath=None, schema="IFC4", use_occ=False, load_geometries=True, verbose=True):

        self.verbose = verbose
        self.ensure_classes_generated()
        self._entitymap = {}
        self._geometrymap = {}
        self._stylemap = {}
        self._relationmap_aggregates = {}  # map of IfcRelAggregates
        self._relationmap_contains = {}  # map of IfcRelContainedInSpatialStructure
        self._default_context = None
        self._default_body_context = None
        self._default_units = None
        self._default_owner_history = None
        self._default_project = None

        self.filepath = filepath
        self.model = model
        self.use_occ = use_occ
        if filepath is None:
            self._file = ifcopenshell.file(schema=schema)
            if self.verbose:
                print("IFC file created in schema: {}".format(schema))
        else:
            self._file = ifcopenshell.open(filepath)
            if self.verbose:
                print("IFC file loaded: {}".format(filepath))

        self._schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name(self._file.schema)

        if load_geometries and filepath is not None:
            self.load_geometries()

    @property
    def schema(self):
        return self._schema

    @property
    def schema_name(self):
        return self.schema.name()

    def ensure_classes_generated(self):
        try:
            from compas_ifc.entities.generated import IFC2X3  # noqa: F401
            from compas_ifc.entities.generated import IFC4  # noqa: F401
        except ImportError:
            if self.verbose:
                print("IFC classes not found. Generating classes...")
            from compas_ifc.entities.generator import Generator

            generator = Generator(schema="IFC2X3")
            generator.generate()

            generator = Generator(schema="IFC4")
            generator.generate()
            if self.verbose:
                print("IFC classes generated.\n\n")

    def file_size(self):
        file_stats = os.stat(self.filepath)
        size_in_mb = file_stats.st_size / (1024 * 1024)
        size_in_mb = round(size_in_mb, 2)
        return size_in_mb

    def from_entity(self, entity):
        if not isinstance(entity, ifcopenshell.entity_instance):
            raise TypeError("Input is not an ifcopenshell.entity_instance")

        _id = entity.id()

        if _id in self._entitymap and _id != 0:
            return self._entitymap[_id]
        else:
            entity = Base(entity, self)
            if _id != 0:
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
        if self.verbose:
            print("Loading geometries...")
        import ifcopenshell.geom

        settings = ifcopenshell.geom.settings()
        settings.set(settings.CONVERT_BACK_UNITS, True)
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
                    self._stylemap[shape.data.id] = {"shellcolors": shellcolors}

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

        if self.verbose:
            print(f"Time to load all {len(self._geometrymap)} geometries {(time.time() - start):.3f}s")

    def save(self, path):
        self._file.write(path)

    def export(self, path: str, entities: list[Base] = [], as_snippet: bool = False, export_materials: bool = True, export_properties: bool = True, export_styles: bool = True):
        new_file = IFCFile(None, schema=self.schema_name)

        exported = {}

        def export_entity(entity: Union[Base, Any], file: IFCFile):
            if not isinstance(entity, Base):
                return entity

            if entity.is_a("IfcOwnerHistory"):
                return file.default_owner_history

            if entity in exported:
                return exported[entity]

            parent = getattr(entity, "parent", None)
            if parent and not as_snippet:
                new_parent_entity = export_entity(parent, file)

            new_entity = file._create_entity(entity.is_a())
            exported[entity] = new_entity

            if parent and not as_snippet:
                if hasattr(entity, "ContainedInStructure") and entity.ContainedInStructure():
                    file._create_entity("IfcRelContainedInSpatialStructure", RelatingStructure=new_parent_entity, RelatedElements=[new_entity])
                else:
                    file._create_entity("IfcRelAggregates", RelatingObject=new_parent_entity, RelatedObjects=[new_entity])

            for key, attr in entity.attributes.items():
                # Skip Representation and ObjectPlacement if not in the list of entities to export
                if key in ["Representation", "ObjectPlacement"] and entity not in entities:
                    continue

                if isinstance(attr, Base):
                    attr = export_entity(attr, file)
                elif isinstance(attr, (list, tuple)):
                    attr = [export_entity(a, file) for a in attr]

                setattr(new_entity, key, attr)

            if export_properties and hasattr(entity, "properties"):
                new_entity.properties = entity.properties

            if export_materials and hasattr(entity, "HasAssociations"):
                # TODO: create material settor on class extension.
                for relation in entity.HasAssociations():
                    if relation.is_a("IfcRelAssociatesMaterial"):
                        new_material_entity = export_entity(relation.RelatingMaterial, file)
                        file._create_entity("IfcRelAssociatesMaterial", RelatingMaterial=new_material_entity, RelatedObjects=[new_entity])

            if export_styles and hasattr(entity, "StyledByItem") and entity.entity.id():
                # TODO: create style settor on class extension.
                for style_item in entity.StyledByItem():
                    styles = [export_entity(s, file) for s in style_item.Styles]
                    file._create_entity("IfcStyledItem", Styles=styles, Item=new_entity)

            return new_entity

        for entity in entities:
            export_entity(entity, new_file)

        new_file.save(path)

    def create(self, cls="IfcBuildingElementProxy", parent=None, geometry=None, frame=None, properties=None, **kwargs):
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

        if properties:
            entity.properties = properties

        return entity

    def remove(self, entity):
        if isinstance(entity, Base):
            entity = [entity]

        print(f"Removing {len(entity)} entities...")
        ifcopenshell.util.element.batch_remove_deep2(self._file)
        for e in entity:
            ifcopenshell.util.element.remove_deep2(self._file, e.entity)
        self._file = ifcopenshell.util.element.unbatch_remove_deep2(self._file)
        print("Removal done.")

    def _create_entity(self, cls_name, **kwargs):
        camel_case_kwargs = {}

        for key, value in kwargs.items():
            if isinstance(value, Base):
                kwargs[key] = value.entity
            elif isinstance(value, (list, tuple)):
                kwargs[key] = [v.entity if isinstance(v, Base) else v for v in value]

            # if key is a snake_case key, convert it to camelCase
            if key[0].isupper():
                camel_case_kwargs[key] = kwargs[key]
            else:
                camel_case_key = "".join([word.capitalize() for word in key.split("_")])
                camel_case_kwargs[camel_case_key] = kwargs[key]

        entity = self._file.create_entity(cls_name, **camel_case_kwargs)
        return self.from_entity(entity)

    @property
    def default_project(self):
        projects = self._file.by_type("IfcProject")
        if projects:
            self._default_project = self.from_entity(projects[0])
        else:
            self._default_project = self._create_entity("IfcProject", Name="Default Project")
            self.default_units
            self.default_body_context
            self.default_owner_history
            return self._default_project

        return self._default_project

    @property
    def default_units(self):
        if not self._default_units:
            if self.default_project.UnitsInContext:
                self._default_units = self.default_project.UnitsInContext
            else:
                self._default_units = self.from_entity(run("unit.assign_unit", self._file))
        return self._default_units

    @property
    def default_context(self):
        if not self._default_context:
            contexts = self.get_entities_by_type("IfcGeometricRepresentationContext")
            for context in contexts:
                if context.ContextType == "Model":
                    self._default_context = context
                    return self._default_context

            self._default_context = self.from_entity(run("context.add_context", self._file, context_type="Model"))
        return self._default_context

    @property
    def default_body_context(self):
        if not self._default_body_context:
            contexts = self.get_entities_by_type("IfcGeometricRepresentationSubContext")
            for context in contexts:
                if context.ContextIdentifier == "Body":
                    self._default_body_context = context
                    return self._default_body_context

            self._default_body_context = self.from_entity(
                run(
                    "context.add_context",
                    self._file,
                    context_type="Model",
                    context_identifier="Body",
                    target_view="MODEL_VIEW",
                    parent=self.default_context.entity,
                )
            )

        return self._default_body_context

    @property
    def default_owner_history(self):
        # We will create a new owner history since we are updating the file
        if not self._default_owner_history:
            person = self._create_entity("IfcPerson")
            organization = self._create_entity("IfcOrganization", Name="compas.dev")
            person_and_org = self._create_entity("IfcPersonAndOrganization", ThePerson=person, TheOrganization=organization)
            application = self._create_entity(
                "IfcApplication",
                ApplicationDeveloper=organization,
                Version=compas_ifc.__version__,
                ApplicationFullName="compas_ifc",
                ApplicationIdentifier="compas_ifc v" + compas_ifc.__version__,
            )

            owner_history = self._create_entity(
                "IfcOwnerHistory",
                OwningUser=person_and_org,
                OwningApplication=application,
                ChangeAction="ADDED",
                CreationDate=int(time.time()),
            )

            self._default_owner_history = owner_history
        return self._default_owner_history
