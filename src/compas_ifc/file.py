import difflib
import importlib
import multiprocessing
import os
import time
from typing import Any
from typing import Dict
from typing import Type
from typing import Union

import ifcopenshell
import numpy as np
from compas.geometry import Transformation
from ifcopenshell.api import run

import compas_ifc
from compas_ifc.brep import TessellatedBrep
from compas_ifc.entities.base import Base


class IFCFile(object):
    """The IFCFile class is a wrapper around an ifcopenshell file object. It provides low-level access to the IFC data.

    Attributes
    ----------
    filepath : str, optional
        The path to the IFC file.
    model : :class:`compas_ifc.model.Model`
        The model object.
    use_occ : bool
        Whether to use OCC for geometry processing.
    load_geometries : bool
        Whether to load the geometries of the IFC file.
    verbose : bool
        Whether to print verbose output.
    extensions : dict, optional
        A dictionary of custom extensions to be used with the IFC file.
    schema : :class:`ifcopenshell.schema.Schema`
        The IFC schema object.
    schema_name : str
        The name of the IFC schema.
    classes : list[:class:`compas_ifc.entities.base.Base`]
        A list of all the classes for this schema version.
    default_project : :class:`compas_ifc.entities.generated.IFC4.IfcProject`
        The default project in this file. Will be created if it does not exist.
    default_units : :class:`compas_ifc.entities.generated.IFC4.IfcUnitAssignment`
        The default units in this file. Will be created if it does not exist.
    default_owner_history : :class:`compas_ifc.entities.generated.IFC4.IfcOwnerHistory`
        The default owner history in this file. Will be created if it does not exist.
    default_context : :class:`compas_ifc.entities.generated.IFC4.IfcContext`
        The default context in this file. Will be created if it does not exist.
    default_body_context : :class:`compas_ifc.entities.generated.IFC4.IfcContext`
        The default body context in this file. Will be created if it does not exist.

    """

    def __init__(
        self, model, filepath: str = None, schema: str = "IFC4", use_occ: bool = False, load_geometries: bool = True, verbose: bool = True, extensions: Dict[str, Type] = None
    ):
        """
        Construct the IFCFile object.

        Parameters
        ----------
        model : :class:`compas_ifc.model.Model`
            The model object.
        filepath : str, optional
            The path to the IFC file. If not provided, a new IFC file is created.
        schema : str, optional
            The IFC schema to use. Default is "IFC4".
        use_occ : bool, optional
            Whether to use OCC for geometry processing. Default is False.
        load_geometries : bool, optional
            Whether to load the geometries of the IFC file. Default is True.
        verbose : bool, optional
            Whether to print verbose output. Default is True.
        extensions : Dict[str, Type]
            A dictionary of extensions to use, with the key being the IFC class name and the value being the extension class.

        """

        self.extensions = extensions
        self.verbose = verbose
        self.ensure_classes_generated()
        self._entitymap = {}
        self._geometrymap = {}  # entity_id → visual geometry (TessellatedBrep or OCCBrep)
        self._stylemap = {}  # entity_id → visual style dict (facecolors or shellcolors)
        self._relationmap_aggregates = {}  # map of IfcRelAggregates
        self._relationmap_contains = {}  # map of IfcRelContainedInSpatialStructure
        self._default_context = None
        self._default_body_context = None
        self._default_axis_context = None
        self._default_units = None
        self._default_owner_history = None
        self._default_project = None
        self._classes = None

        self.filepath = filepath
        self.model = model
        self.use_occ = use_occ
        if filepath is None:
            self._file = ifcopenshell.file(schema=schema)
            file_name = self._file.wrapped_data.header().file_name_py()
            file_name.author = ["Unknown Author"]
            file_name.organization = ["Unknown Organization"]
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
    def schema(self) -> ifcopenshell.ifcopenshell_wrapper.schema_definition:
        return self._schema

    @property
    def schema_name(self) -> str:
        return self.schema.name()

    @property
    def classes(self) -> list[Base]:
        if not self._classes:
            module = importlib.import_module(f"compas_ifc.entities.generated.{self.schema_name}")
            classes = [x for x in dir(module) if x.startswith("Ifc") and x != "IfcRoot"]
            self._classes = classes
        return self._classes

    def ensure_classes_generated(self):
        """Check if the IFC classes are generated and generate them if not."""
        try:
            from compas_ifc.entities.generated import IFC2X3  # noqa: F401
            from compas_ifc.entities.generated import IFC4  # noqa: F401
            from compas_ifc.entities.generated import IFC4X3  # noqa: F401
        except ImportError:
            if self.verbose:
                print("IFC classes not found. Generating classes...")
            from compas_ifc.entities.generator import Generator

            generator = Generator(schema="IFC2X3")
            generator.generate()

            generator = Generator(schema="IFC4")
            generator.generate()

            generator = Generator(schema="IFC4X3")
            generator.generate()
            if self.verbose:
                print("IFC classes generated.\n\n")

    def file_size(self) -> float:
        """Get the size of the IFC file in MB."""
        file_stats = os.stat(self.filepath)
        size_in_mb = file_stats.st_size / (1024 * 1024)
        size_in_mb = round(size_in_mb, 2)
        return size_in_mb

    def from_entity(self, entity: ifcopenshell.entity_instance) -> Base:
        """
        Convert an ifcopenshell entity to a compas_ifc entity. Will return an existing entity if it has already been converted.

        Parameters
        ----------
        entity : :class:`ifcopenshell.entity_instance`
            The ifcopenshell entity to convert.

        Returns
        -------
        :class:`compas_ifc.entities.base.Base`
            The converted compas_ifc entity.

        """
        if not isinstance(entity, ifcopenshell.entity_instance):
            raise TypeError("Input is not an ifcopenshell.entity_instance")

        _id = entity.id()

        if _id in self._entitymap and _id != 0:
            return self._entitymap[_id]
        else:
            entity = Base(entity, file=self, extensions=self.extensions)
            if _id != 0:
                self._entitymap[_id] = entity
            return entity

    def get_entities_by_type(self, type_name: str) -> list[Base]:
        """
        Get all entities of a given type.

        Parameters
        ----------
        type_name : str
            The name of the type to get entities of.

        Returns
        -------
        list[:class:`compas_ifc.entities.base.Base`]
            A list of all entities of the given type.

        """
        entities = self._file.by_type(type_name)
        return [self.from_entity(entity) for entity in entities]

    def get_entities_by_name(self, name: str) -> list[Base]:
        """
        Get all entities with a given name.

        Parameters
        ----------
        name : str
            The name to search for.

        Returns
        -------
        list[:class:`compas_ifc.entities.base.Base`]
            A list of all entities with the given name.
        """
        return [entity for entity in self.get_entities_by_type("IfcRoot") if entity.Name == name]

    def get_entity_by_global_id(self, global_id: str) -> Base:
        """
        Get an entity by its global ID.

        Parameters
        ----------
        global_id : str
            The global ID to search for.

        Returns
        -------
        :class:`compas_ifc.entities.base.Base`
            The entity with the given global ID.
        """
        return self.from_entity(self._file.by_guid(global_id))

    def get_entity_by_id(self, id: int) -> Base:
        """
        Get an entity by its file ID.

        Parameters
        ----------
        id : int
            The ID to search for.

        Returns
        -------
        :class:`compas_ifc.entities.base.Base`
            The entity with the given ID.
        """
        return self.from_entity(self._file.by_id(id))

    def get_preloaded_geometry(self, entity: Base) -> "TessellatedBrep":
        """
        Get the preloaded visual geometry of an entity.

        Returns the evaluated (tessellated or B-Rep) geometry produced by
        ``ifcopenshell.geom.iterator`` during ``load_geometries()``.
        Parametric information (extrusion profiles, boolean trees, etc.)
        is NOT preserved.

        Parameters
        ----------
        entity : :class:`compas_ifc.entities.base.Base`
            The entity to get the visual geometry of.

        Returns
        -------
        :class:`compas_ifc.brep.TessellatedBrep` or :class:`compas_occ.brep.OCCBrep` or None
            The preloaded visual geometry, or None if not available.
        """
        return self._geometrymap.get(entity.entity.id())

    def get_preloaded_style(self, entity: Base) -> dict:
        """
        Get the preloaded style of an entity.
        """
        return self._stylemap.get(entity.entity.id(), {})

    def load_geometries(self, include=None, exclude=None):
        """
        Load all the geometries of the IFC file using a fast multithreaded iterator.

        Parameters
        ----------
        include : list[str], optional
            A list of entity types to include.
        exclude : list[str], optional
            A list of entity types to exclude.

        """
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

                    faces = shape.geometry.faces
                    edges = shape.geometry.edges
                    verts = shape.geometry.verts

                    facecolors = []
                    for m_id in shape.geometry.material_ids:
                        if m_id == -1:
                            facecolors.append([0.5, 0.5, 0.5, 1])
                            facecolors.append([0.5, 0.5, 0.5, 1])
                            facecolors.append([0.5, 0.5, 0.5, 1])
                            continue
                        material = shape.geometry.materials[m_id]
                        color = (*material.diffuse.components, 1 - material.transparency)
                        facecolors.append(color)
                        facecolors.append(color)
                        facecolors.append(color)

                    brep = TessellatedBrep(vertices=verts, edges=edges, faces=faces)

                    self._geometrymap[shape.id] = brep
                    self._stylemap[shape.id] = {"facecolors": facecolors}

                if not iterator.next():
                    break

        if self.verbose:
            print(f"Time to load all {len(self._geometrymap)} visual geometries {(time.time() - start):.3f}s")

    def save(self, path: str):
        """
        Save the IFC file to a given path.
        """
        self._file.write(path)

    def export(self, path: str, entities: list[Base] = [], as_snippet: bool = False, export_materials: bool = True, export_properties: bool = True, export_styles: bool = True, export_types: bool = True, export_relationships: bool = True):
        """
        Export a subset of the IFC file to a new IFC file.

        Parameters
        ----------
        path : str
            The path to save the exported IFC file to.
        entities : list[:class:`compas_ifc.entities.base.Base`]
            The entities to export.
        as_snippet : bool
            Whether to export as a snippet, without the full spatial hierarchy. Default is False.
        export_materials : bool
            Whether to export materials. Default is True.
        export_properties : bool
            Whether to export properties. Default is True.
        export_styles : bool
            Whether to export styles. Default is True.
        export_types : bool
            Whether to export type definitions (IfcRelDefinesByType). Default is True.
        export_relationships : bool
            Whether to export non-spatial relationships (connections, voids, fills,
            space boundaries) where both endpoints are in the exported set.
            Default is True.

        """
        new_file = IFCFile(None, schema=self.schema_name)

        exported = {}

        def export_entity(entity: Union[Base, Any], file: IFCFile):
            if isinstance(entity, (list, tuple)):
                return [export_entity(a, file) for a in entity]
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

            if export_properties and hasattr(entity, "property_sets"):
                new_entity.property_sets = entity.property_sets

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

            if export_types and hasattr(entity, "IsTypedBy"):
                for rel in entity.IsTypedBy():
                    new_type = export_entity(rel.RelatingType, file)
                    file._create_entity("IfcRelDefinesByType", RelatingType=new_type, RelatedObjects=[new_entity])

            return new_entity

        for entity in entities:
            export_entity(entity, new_file)

        # Export non-spatial relationships where both endpoints are in the exported set
        if export_relationships:
            self._export_mutual_relationships(new_file, exported)

        new_file.save(path)

    def _export_mutual_relationships(self, new_file, exported):
        """Export non-spatial IFC relationships where both endpoints are already exported.

        Covers all relationship types that ``BuildingInformationModel`` loads
        into its interaction graph: topology (voids, fills, connections, space
        boundaries, coverings, interference, projections), structural, and MEP.

        For each relationship in the source file, if all referenced entities
        are present in the ``exported`` dict, a corresponding relationship
        entity is created in ``new_file``.

        Parameters
        ----------
        new_file : IFCFile
            The target file to create relationship entities in.
        exported : dict
            Mapping from source ``Base`` wrappers to their counterparts in
            ``new_file``.

        Returns
        -------
        int
            The number of relationship entities created.

        """
        count = 0
        oh = new_file.default_owner_history

        def _by_type(type_name):
            """Query entities by type, returning [] for types missing in the schema."""
            try:
                return self.get_entities_by_type(type_name)
            except RuntimeError:
                return []

        def _all_exported(*entities):
            """Return True if all entities are non-None and in the exported dict."""
            return all(e is not None and e in exported for e in entities)

        def _exported_list(entities):
            """Return exported counterparts for entities that are in the exported dict."""
            return [exported[e] for e in entities if e in exported]

        # ==================================================================
        # Topology
        # ==================================================================

        # A. IfcRelVoidsElement (wall/slab -> opening)
        for rel in _by_type("IfcRelVoidsElement"):
            host = rel.RelatingBuildingElement
            opening = rel.RelatedOpeningElement
            if _all_exported(host, opening):
                new_file._create_entity(
                    "IfcRelVoidsElement",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingBuildingElement=exported[host],
                    RelatedOpeningElement=exported[opening],
                )
                count += 1

        # B. IfcRelFillsElement (opening -> door/window)
        for rel in _by_type("IfcRelFillsElement"):
            opening = rel.RelatingOpeningElement
            filler = rel.RelatedBuildingElement
            if _all_exported(opening, filler):
                new_file._create_entity(
                    "IfcRelFillsElement",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingOpeningElement=exported[opening],
                    RelatedBuildingElement=exported[filler],
                )
                count += 1

        # C. IfcRelConnectsPathElements (wall-to-wall path connections)
        for rel in _by_type("IfcRelConnectsPathElements"):
            relating = rel.RelatingElement
            related = rel.RelatedElement
            if _all_exported(relating, related):
                new_file._create_entity(
                    "IfcRelConnectsPathElements",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingElement=exported[relating],
                    RelatedElement=exported[related],
                    RelatingPriorities=list(rel.RelatingPriorities or []),
                    RelatedPriorities=list(rel.RelatedPriorities or []),
                    RelatedConnectionType=rel.RelatedConnectionType or "NOTDEFINED",
                    RelatingConnectionType=rel.RelatingConnectionType or "NOTDEFINED",
                )
                count += 1

        # C2. IfcRelConnectsElements (generic, excluding subtypes)
        for rel in _by_type("IfcRelConnectsElements"):
            exact_type = rel.is_a()
            if exact_type in ("IfcRelConnectsPathElements", "IfcRelConnectsWithRealizingElements"):
                continue
            relating = rel.RelatingElement
            related = rel.RelatedElement
            if _all_exported(relating, related):
                new_file._create_entity(
                    "IfcRelConnectsElements",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingElement=exported[relating],
                    RelatedElement=exported[related],
                )
                count += 1

        # C3. IfcRelConnectsWithRealizingElements
        for rel in _by_type("IfcRelConnectsWithRealizingElements"):
            relating = rel.RelatingElement
            related = rel.RelatedElement
            if _all_exported(relating, related):
                realizing = _exported_list(rel.RealizingElements or [])
                new_file._create_entity(
                    "IfcRelConnectsWithRealizingElements",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingElement=exported[relating],
                    RelatedElement=exported[related],
                    RealizingElements=realizing or None,
                )
                count += 1

        # D. IfcRelSpaceBoundary (space <-> element)
        for rel in _by_type("IfcRelSpaceBoundary"):
            space = rel.RelatingSpace
            related = rel.RelatedBuildingElement
            if _all_exported(space, related):
                new_file._create_entity(
                    "IfcRelSpaceBoundary",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingSpace=exported[space],
                    RelatedBuildingElement=exported[related],
                    PhysicalOrVirtualBoundary=rel.PhysicalOrVirtualBoundary or "NOTDEFINED",
                    InternalOrExternalBoundary=rel.InternalOrExternalBoundary or "NOTDEFINED",
                )
                count += 1

        # E. IfcRelCoversBldgElements (host -> coverings)
        for rel in _by_type("IfcRelCoversBldgElements"):
            host = rel.RelatingBuildingElement
            coverings = _exported_list(rel.RelatedCoverings or [])
            if host in exported and coverings:
                new_file._create_entity(
                    "IfcRelCoversBldgElements",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingBuildingElement=exported[host],
                    RelatedCoverings=coverings,
                )
                count += 1

        # E2. IfcRelCoversSpaces (space -> coverings)
        for rel in _by_type("IfcRelCoversSpaces"):
            space = rel.RelatingSpace
            coverings = _exported_list(rel.RelatedCoverings or [])
            if space in exported and coverings:
                new_file._create_entity(
                    "IfcRelCoversSpaces",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingSpace=exported[space],
                    RelatedCoverings=coverings,
                )
                count += 1

        # F. IfcRelInterferesElements (IFC4+ only)
        for rel in _by_type("IfcRelInterferesElements"):
            relating = rel.RelatingElement
            related = rel.RelatedElement
            if _all_exported(relating, related):
                kwargs = {
                    "GlobalId": ifcopenshell.guid.new(),
                    "OwnerHistory": oh,
                    "RelatingElement": exported[relating],
                    "RelatedElement": exported[related],
                }
                interference_type = getattr(rel, "InterferenceType", None)
                if interference_type is not None:
                    kwargs["InterferenceType"] = interference_type
                new_file._create_entity("IfcRelInterferesElements", **kwargs)
                count += 1

        # G. IfcRelProjectsElement
        for rel in _by_type("IfcRelProjectsElement"):
            host = rel.RelatingElement
            feature = rel.RelatedFeatureElement
            if _all_exported(host, feature):
                new_file._create_entity(
                    "IfcRelProjectsElement",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingElement=exported[host],
                    RelatedFeatureElement=exported[feature],
                )
                count += 1

        # ==================================================================
        # Structural
        # ==================================================================

        # H. IfcRelConnectsStructuralMember / IfcRelConnectsWithEccentricity
        for rel in _by_type("IfcRelConnectsStructuralMember"):
            exact_type = rel.is_a()
            member = rel.RelatingStructuralMember
            connection = rel.RelatedStructuralConnection
            if _all_exported(member, connection):
                new_file._create_entity(
                    exact_type,
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingStructuralMember=exported[member],
                    RelatedStructuralConnection=exported[connection],
                )
                count += 1

        # I. IfcRelConnectsStructuralActivity
        for rel in _by_type("IfcRelConnectsStructuralActivity"):
            relating = rel.RelatingElement
            activity = rel.RelatedStructuralActivity
            if _all_exported(relating, activity):
                new_file._create_entity(
                    "IfcRelConnectsStructuralActivity",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingElement=exported[relating],
                    RelatedStructuralActivity=exported[activity],
                )
                count += 1

        # ==================================================================
        # MEP
        # ==================================================================

        # J. IfcRelConnectsPorts
        for rel in _by_type("IfcRelConnectsPorts"):
            port_a = rel.RelatingPort
            port_b = rel.RelatedPort
            if _all_exported(port_a, port_b):
                new_file._create_entity(
                    "IfcRelConnectsPorts",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingPort=exported[port_a],
                    RelatedPort=exported[port_b],
                )
                count += 1

        # K. IfcRelConnectsPortToElement
        for rel in _by_type("IfcRelConnectsPortToElement"):
            port = rel.RelatingPort
            element = rel.RelatedElement
            if _all_exported(port, element):
                new_file._create_entity(
                    "IfcRelConnectsPortToElement",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingPort=exported[port],
                    RelatedElement=exported[element],
                )
                count += 1

        # L. IfcRelFlowControlElements (flow element -> control elements)
        for rel in _by_type("IfcRelFlowControlElements"):
            flow = rel.RelatingFlowElement
            controls = _exported_list(rel.RelatedControlElements or [])
            if flow in exported and controls:
                new_file._create_entity(
                    "IfcRelFlowControlElements",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingFlowElement=exported[flow],
                    RelatedControlElements=controls,
                )
                count += 1

        # M. IfcRelServicesBuildings (system -> buildings)
        for rel in _by_type("IfcRelServicesBuildings"):
            system = rel.RelatingSystem
            buildings = _exported_list(rel.RelatedBuildings or [])
            if system in exported and buildings:
                new_file._create_entity(
                    "IfcRelServicesBuildings",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingSystem=exported[system],
                    RelatedBuildings=buildings,
                )
                count += 1

        # N. IfcRelReferencedInSpatialStructure (spatial -> elements)
        for rel in _by_type("IfcRelReferencedInSpatialStructure"):
            structure = rel.RelatingStructure
            elements = _exported_list(rel.RelatedElements or [])
            if structure in exported and elements:
                new_file._create_entity(
                    "IfcRelReferencedInSpatialStructure",
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=oh,
                    RelatingStructure=exported[structure],
                    RelatedElements=elements,
                )
                count += 1

        return count

    def create(self, cls=None, parent=None, geometry=None, frame=None, properties=None, **kwargs) -> Base:
        """
        Create an entity in this model.

        Parameters
        ----------
        cls : str
            The class of the entity to create. Defaults to an `IfcBuildingElementProxy`.
        parent : :class:`compas_ifc.entities.base.Base`
            The parent entity of the new entity.
        geometry : :class:`compas.geometry.Geometry` or :class:`compas.datastructures.Datastructure`
            The geometry of the new entity.
        frame : :class:`compas.geometry.Frame`
            The placement frame of the new entity.
        properties : dict
            The custom property sets to be added to the new entity.
        **kwargs
            Additional keyword arguments to be added to the new entity.

        Returns
        -------
        :class:`compas_ifc.entities.base.Base`
            The newly created entity.

        """
        if isinstance(cls, type):
            cls_name = cls.__name__
        else:
            cls_name = cls

        if cls_name is None:
            cls_name = "IfcBuildingElementProxy"

        if cls_name not in self.classes:
            matched_classes = self.search_ifc_classes(cls_name)
            if not matched_classes:
                raise ValueError(f"Class {cls_name} not found.")
            else:
                cls_name = matched_classes[0]

        entity = self._create_entity(cls_name, **kwargs)

        if parent:
            self.create_relationship(parent, entity)

        if geometry:
            # Instancing is handled automatically by assign_body_representation:
            # when the same geometry object is assigned to multiple entities,
            # it creates IfcRepresentationMap + IfcMappedItem for the 2nd+ use.
            entity.geometry = geometry

        if frame:
            entity.frame = frame

        if properties:
            entity.property_sets = properties

        if entity.is_a("IfcRoot"):
            entity.GlobalId = ifcopenshell.guid.new()

        return entity

    def create_relationship(self, parent: Base, child: Base) -> Base:
        """
        Create the correct relationship between two entities based on their types.

        Parameters
        ----------
        parent : :class:`compas_ifc.entities.base.Base`
            The parent entity.
        child : :class:`compas_ifc.entities.base.Base`
            The child entity.

        Returns
        -------
        :class:`compas_ifc.entities.base.Base`
            The created relationship.

        """

        guid = ifcopenshell.guid.new()
        if parent.is_a("IfcSpatialStructureElement"):
            if child.is_a("IfcSpatialStructureElement"):
                return self._create_entity("IfcRelAggregates", GlobalId=guid, RelatingObject=parent, RelatedObjects=[child])
            return self._create_entity("IfcRelContainedInSpatialStructure", GlobalId=guid, RelatingStructure=parent, RelatedElements=[child])

        if parent.is_a("IfcElementAssembly") or child.is_a("IfcBuildingElementPart"):
            return self._create_entity("IfcRelAggregates", GlobalId=guid, RelatingObject=parent, RelatedObjects=[child])

        if parent.is_a("IfcPort"):
            if not child.is_a("IfcPort"):
                return self._create_entity("IfcRelConnectsPortToElement", GlobalId=guid, RelatingPort=parent, RelatedElement=child)
            return self._create_entity("IfcRelConnectsPorts", GlobalId=guid, RelatingPort=parent, RelatedPort=child)

        if parent.is_a("IfcElement") and child.is_a("IfcElement"):
            return self._create_entity("IfcRelConnectsElements", GlobalId=guid, RelatingElement=parent, RelatedElement=child)

        if parent.is_a("IfcGroup"):
            return self._create_entity("IfcRelAssignsToGroup", GlobalId=guid, RelatingGroup=parent, RelatedObjects=[child])

        # Default case
        return self._create_entity("IfcRelAggregates", GlobalId=guid, RelatingObject=parent, RelatedObjects=[child])

    def search_ifc_classes(self, name: str, n: int = 5) -> list[Type["Base"]]:
        """
        Search for IFC classes by name

        Parameters
        ----------
        name : str
            The name of the IFC class to search for.
        n : int
            The number of results to return. Default is 5.

        Returns
        -------
        list[Type[:class:`compas_ifc.entities.base.Base`]]
            A list of IFC classes that match the search query.

        """
        classes_dict = {c.lower(): c for c in self.classes}
        classes_lower = list(classes_dict.keys())
        closest_matches_lower = difflib.get_close_matches(name.lower(), classes_lower, n=n)
        closest_matches = [classes_dict[match] for match in closest_matches_lower]
        return closest_matches

    def remove(self, entity: Union[Base, list[Base]]):
        """
        Remove an entity from this model.

        Parameters
        ----------
        entity : :class:`compas_ifc.entities.base.Base` or list[:class:`compas_ifc.entities.base.Base`]
            The entity or entities to remove.

        """
        if isinstance(entity, Base):
            entity = [entity]

        print(f"Removing {len(entity)} entities...")
        ifcopenshell.util.element.batch_remove_deep2(self._file)
        for e in entity:
            ifcopenshell.util.element.remove_deep2(self._file, e.entity)
        self._file = ifcopenshell.util.element.unbatch_remove_deep2(self._file)
        print("Removal done.")

    def _create_entity(self, cls_name, **kwargs) -> Base:
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

    def create_value(self, value):
        """
        Create corresponding IfcValue from a Python value.
        """

        PRIMARY_MEASURE_TYPES = {
            str: "IfcLabel",
            float: "IfcReal",
            bool: "IfcBoolean",
            int: "IfcInteger",
        }

        primary_measure_type = PRIMARY_MEASURE_TYPES[type(value)]
        ifc_value = self._file.create_entity(primary_measure_type, value)
        return ifc_value

    @property
    def default_project(self) -> Base:
        projects = self._file.by_type("IfcProject")
        if projects:
            self._default_project = self.from_entity(projects[0])
        else:
            self._default_project = self._create_entity("IfcProject", GlobalId=ifcopenshell.guid.new(), Name="Default Project")
            self.default_units
            self.default_body_context
            self.default_owner_history
            return self._default_project

        return self._default_project

    @property
    def default_units(self) -> Base:
        if not self._default_units:
            if self.default_project.UnitsInContext:
                self._default_units = self.default_project.UnitsInContext
            else:
                length_unit = self.create("IfcUnit", UnitType="LENGTHUNIT", Prefix="MILLI", Name="METRE")
                area_unit = self.create("IfcUnit", UnitType="AREAUNIT", Prefix="MILLI", Name="SQUARE_METRE")
                volume_unit = self.create("IfcUnit", UnitType="VOLUMEUNIT", Prefix="MILLI", Name="CUBIC_METRE")
                plane_angle_unit = self.create("IfcUnit", UnitType="PLANEANGLEUNIT", Name="RADIAN")
                unit_assignment = self.create("IfcUnitAssignment", Units=[length_unit, area_unit, volume_unit, plane_angle_unit])
                self.default_project.UnitsInContext = unit_assignment
                self._default_units = unit_assignment
        return self._default_units

    @property
    def default_context(self) -> Base:
        if not self._default_context:
            contexts = self.get_entities_by_type("IfcGeometricRepresentationContext")
            for context in contexts:
                if context.ContextType == "Model":
                    self._default_context = context
                    return self._default_context

            self._default_context = self.from_entity(run("context.add_context", self._file, context_type="Model"))
        return self._default_context

    @property
    def default_body_context(self) -> Base:
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
    def default_axis_context(self) -> Base:
        if not self._default_axis_context:
            contexts = self.get_entities_by_type("IfcGeometricRepresentationSubContext")
            for context in contexts:
                if context.ContextIdentifier == "Axis":
                    self._default_axis_context = context
                    return self._default_axis_context

            self._default_axis_context = self.from_entity(
                run(
                    "context.add_context",
                    self._file,
                    context_type="Model",
                    context_identifier="Axis",
                    target_view="GRAPH_VIEW",
                    parent=self.default_context.entity,
                )
            )

        return self._default_axis_context

    @property
    def default_owner_history(self) -> Base:
        # We will create a new owner history since we are updating the file
        if not self._default_owner_history:
            person = self._create_entity("IfcPerson", FamilyName="Unknown Author")
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
                CreationDate=int(time.time()),
            )

            self._default_owner_history = owner_history
        return self._default_owner_history
