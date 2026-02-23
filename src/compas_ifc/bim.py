from typing import Optional
from typing import Union

from compas.geometry import Frame
from compas.geometry import Transformation
from compas_model.models import Model

from compas_ifc.element import GenericElement
from compas_ifc.file import IFCFile


class BuildingInformationModel(Model):
    """A building information model backed by an IFC file.

    Extends ``compas_model.Model`` to provide IFC-specific functionality
    including reading/writing IFC files, spatial hierarchy management,
    and IFC entity creation. The model's ``tree`` holds the spatial hierarchy
    and the ``graph`` holds non-hierarchical relationships (interactions).

    This class acts as a **bi-directional front-end**: every mutation
    (adding elements, changing geometry/properties/transforms) immediately
    updates the underlying IFC file. Calling ``save()`` writes the file.

    IfcProject-level information (units, schema, metadata) is managed
    directly by this class rather than as a separate element.

    Parameters
    ----------
    filepath : str, optional
        Path to an IFC file to load.
    schema : str, optional
        IFC schema to use when creating a new file. Default is "IFC4".
    use_occ : bool, optional
        Whether to use OpenCascade for geometry. Default is False.
    load_geometries : bool, optional
        Whether to pre-load geometries during import. Default is True.
    rectify_placements : bool, optional
        Whether to rewrite IFC placements during import so that each
        element's ``IfcLocalPlacement.PlacementRelTo`` points to its
        spatial parent's placement and ``RelativePlacement`` holds the
        local transform. Default is True.
    rectify_verbose : bool, optional
        If True and ``rectify_placements`` is True, print a line for each
        rectified placement showing what ``PlacementRelTo`` changed from
        and to (e.g. "IfcWall 'Wall A': PlacementRelTo IfcBuilding 'B1'
        -> IfcBuildingStorey 'S1'"). Default is False.
    name : str, optional
        Name of the model.

    """

    RELATIONSHIP_GROUPS = {
        "topology": {"void", "fill", "connection", "space_boundary", "covering", "interference", "projection"},
        "structural": {"structural"},
        "mep": {"port_connection", "port_element", "flow_control", "services", "spatial_reference"},
    }

    def __init__(
        self,
        filepath: str = None,
        schema: str = "IFC4",
        use_occ: bool = False,
        load_geometries: bool = True,
        rectify_placements: bool = True,
        rectify_verbose: bool = False,
        name: str = None,
        **kwargs,
    ) -> None:
        super().__init__(name=name, **kwargs)

        # IFC file wrapper — pass self so Base.model resolves to this instance
        self._file = IFCFile(
            self,
            filepath=filepath,
            schema=schema,
            use_occ=use_occ,
            load_geometries=load_geometries,
            verbose=False,
        )

        # Element lookup by IFC GlobalId
        self._elements_by_global_id: dict[str, GenericElement] = {}

        # Load spatial hierarchy if opening an existing file
        if filepath:
            self._load_from_ifc(rectify_placements=rectify_placements, rectify_verbose=rectify_verbose)

    # ==========================================================================
    # IFCFile compatibility — conversion functions call entity.model.create()
    # ==========================================================================

    @property
    def file(self):
        """The underlying IFCFile, needed by conversion functions."""
        return self._file

    def create(self, cls=None, parent=None, geometry=None, frame=None, properties=None, **kwargs):
        """Create an IFC entity. Delegates to IFCFile.create().

        This method satisfies the protocol expected by all conversion functions
        (representation.py, frame.py, pset.py, mesh.py, shapes.py, brep.py).
        """
        return self._file.create(cls=cls, parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_value(self, value):
        """Create an IfcValue from a Python scalar. Delegates to IFCFile."""
        return self._file.create_value(value)

    # ==========================================================================
    # User-facing properties
    # ==========================================================================

    @property
    def schema_name(self) -> str:
        return self._file.schema_name

    @property
    def unit(self) -> Optional[str]:
        projects = self._file.get_entities_by_type("IfcProject")
        if not projects:
            return None
        project = projects[0]
        length_unit = project.length_unit
        if length_unit.Name == "METRE" and length_unit.Prefix == "MILLI":
            return "mm"
        elif length_unit.Name == "METRE" and length_unit.Prefix == "CENTI":
            return "cm"
        elif length_unit.Name == "METRE" and not length_unit.Prefix:
            return "m"
        return None

    @unit.setter
    def unit(self, value: str):
        projects = self._file.get_entities_by_type("IfcProject")
        if not projects:
            return
        project = projects[0]
        if value == "mm":
            project.length_unit.Prefix = "MILLI"
        elif value == "cm":
            project.length_unit.Prefix = "CENTI"
        elif value == "m":
            project.length_unit.Prefix = None
        else:
            raise ValueError("Invalid unit. Use 'mm', 'cm', or 'm'.")

    # ==========================================================================
    # Element queries
    # ==========================================================================

    def get_element_by_global_id(self, global_id: str) -> Optional[GenericElement]:
        """Find an element by its IFC GlobalId."""
        return self._elements_by_global_id.get(global_id)

    def get_elements_by_type(self, ifc_type: str) -> list[GenericElement]:
        """Find all elements of a given IFC type (e.g. "IfcWall")."""
        return [e for e in self.elements() if e.ifc_type == ifc_type]

    def get_elements_by_name(self, name: str) -> list[GenericElement]:
        """Find all elements with a given name."""
        return [e for e in self.elements() if e.name == name]

    @property
    def sites(self) -> list[GenericElement]:
        """All IfcSite elements."""
        return self.get_elements_by_type("IfcSite")

    @property
    def buildings(self) -> list[GenericElement]:
        """All IfcBuilding elements."""
        return self.get_elements_by_type("IfcBuilding")

    @property
    def storeys(self) -> list[GenericElement]:
        """All IfcBuildingStorey elements."""
        return self.get_elements_by_type("IfcBuildingStorey")

    @property
    def building_elements(self) -> list[GenericElement]:
        """All non-spatial building elements (walls, slabs, beams, etc.)."""
        return [e for e in self.elements() if not e.is_spatial]

    # ==========================================================================
    # Element add / remove (bi-directional sync)
    # ==========================================================================

    def add_element(self, element, parent=None, material=None):
        """Add a GenericElement to the model tree and create its IFC entity.

        For elements loaded from IFC (with an existing ``_ifc_entity``), only
        the compas_model bookkeeping is performed. For programmatically created
        elements, the IFC entity, relationship, geometry representation, and
        placement are all created in the underlying IFC file.

        Parameters
        ----------
        element : GenericElement
            The element to add.
        parent : GenericElement, optional
            Parent element in the spatial hierarchy.
        material : optional
            Material to assign (from compas_model).

        Returns
        -------
        GenericElement

        """
        # Let compas_model do tree/graph bookkeeping
        result = super().add_element(element, parent=parent, material=material)

        if element._ifc_entity is not None:
            # Import case: element already has an IFC entity, just index it
            if element.global_id:
                self._elements_by_global_id[element.global_id] = element
            return result

        # Programmatic creation: create IFC entity in the file
        ifc_parent = self._resolve_ifc_parent(parent)
        kwargs = {}
        if element.name:
            kwargs["Name"] = element.name

        ifc_entity = self._file.create(cls=element.ifc_type, parent=ifc_parent, **kwargs)
        element._ifc_entity = ifc_entity
        element._global_id = ifc_entity.GlobalId
        self._elements_by_global_id[ifc_entity.GlobalId] = element

        # Sync geometry → IFC representation
        if element._geometry is not None:
            ifc_entity.geometry = element._geometry

        # Sync transformation → IFC placement (with PlacementRelTo for hierarchy)
        if element.transformation:
            self._assign_ifc_placement(element, parent)

        # Sync properties → IFC property sets
        if element._properties:
            ifc_entity.property_sets = element._properties

        return result

    def remove_element(self, element):
        """Remove a GenericElement from the model and the IFC file.

        Parameters
        ----------
        element : GenericElement
            The element to remove.

        """
        if element._ifc_entity is not None:
            self._file.remove(element._ifc_entity)
            element._ifc_entity = None

        if element.global_id and element.global_id in self._elements_by_global_id:
            del self._elements_by_global_id[element.global_id]

        super().remove_element(element)

    def _resolve_ifc_parent(self, parent_element):
        """Return the IFC Base entity for a parent GenericElement.

        If parent is None, defaults to the IfcProject.
        """
        if parent_element is None:
            return self._file.default_project

        if parent_element._ifc_entity is not None:
            return parent_element._ifc_entity

        raise ValueError(
            f"Parent element '{parent_element.name}' has no IFC entity. "
            "Add spatial parents before their children."
        )

    def _assign_ifc_placement(self, element, parent_element):
        """Create an IfcLocalPlacement with PlacementRelTo for correct hierarchy."""
        from compas_ifc.conversions.frame import frame_to_ifc_axis2_placement_3d

        local_frame = Frame.from_transformation(element.transformation)
        local_placement = frame_to_ifc_axis2_placement_3d(self, local_frame)

        parent_placement = None
        if parent_element and parent_element._ifc_entity:
            parent_placement = getattr(parent_element._ifc_entity, "ObjectPlacement", None)

        placement = self._file._create_entity(
            "IfcLocalPlacement",
            PlacementRelTo=parent_placement,
            RelativePlacement=local_placement,
        )
        element._ifc_entity.ObjectPlacement = placement

    # ==========================================================================
    # Convenience creation methods
    # ==========================================================================

    def create_element(self, ifc_type="IfcBuildingElementProxy", parent=None, geometry=None, frame=None, transformation=None, properties=None, name=None):
        """Create a building element and add it to the model.

        Parameters
        ----------
        ifc_type : str
            The IFC class name (e.g. "IfcWall").
        parent : GenericElement, optional
            Parent in the spatial hierarchy.
        geometry : Brep | Mesh | Shape, optional
            Element geometry.
        frame : Frame, optional
            Placement frame (converted to Transformation).
        transformation : Transformation, optional
            Local transformation. Overrides frame if both provided.
        properties : dict, optional
            Property sets.
        name : str, optional
            Element name.

        Returns
        -------
        GenericElement

        """
        if transformation is None and frame is not None:
            transformation = Transformation.from_frame(frame)

        element = GenericElement(
            ifc_type=ifc_type,
            geometry=geometry,
            transformation=transformation,
            name=name,
        )
        if properties:
            element._properties = properties

        self.add_element(element, parent=parent)
        return element

    def create_wall(self, **kwargs):
        """Create an IfcWall and add it to the model."""
        return self.create_element(ifc_type="IfcWall", **kwargs)

    def create_slab(self, **kwargs):
        """Create an IfcSlab and add it to the model."""
        return self.create_element(ifc_type="IfcSlab", **kwargs)

    def create_beam(self, **kwargs):
        """Create an IfcBeam and add it to the model."""
        return self.create_element(ifc_type="IfcBeam", **kwargs)

    def create_column(self, **kwargs):
        """Create an IfcColumn and add it to the model."""
        return self.create_element(ifc_type="IfcColumn", **kwargs)

    def create_window(self, **kwargs):
        """Create an IfcWindow and add it to the model."""
        return self.create_element(ifc_type="IfcWindow", **kwargs)

    def create_door(self, **kwargs):
        """Create an IfcDoor and add it to the model."""
        return self.create_element(ifc_type="IfcDoor", **kwargs)

    def create_roof(self, **kwargs):
        """Create an IfcRoof and add it to the model."""
        return self.create_element(ifc_type="IfcRoof", **kwargs)

    @classmethod
    def template(cls, schema="IFC4", building_count=1, storey_count=1, unit="mm", use_occ=False, name=None):
        """Create a template BIM model with default spatial hierarchy.

        Creates IfcProject → IfcSite → IfcBuilding(s) → IfcBuildingStorey(s).

        Parameters
        ----------
        schema : str
            IFC schema version. Default is "IFC4".
        building_count : int
            Number of buildings. Default is 1.
        storey_count : int
            Number of storeys per building. Default is 1.
        unit : str
            Length unit ("mm", "cm", or "m"). Default is "mm".
        use_occ : bool
            Use OpenCascade for geometry. Default is False.
        name : str, optional
            Model name.

        Returns
        -------
        BuildingInformationModel

        """
        model = cls(schema=schema, use_occ=use_occ, name=name or "Default Project")

        # Ensure default project exists in IFC file
        project = model._file.default_project
        model.name = project.Name or "Default Project"

        site = GenericElement(ifc_type="IfcSite", name="Default Site")
        model.add_element(site)

        for i in range(building_count):
            building = GenericElement(ifc_type="IfcBuilding", name=f"Default Building {i + 1}")
            model.add_element(building, parent=site)

            for j in range(storey_count):
                storey = GenericElement(ifc_type="IfcBuildingStorey", name=f"Default Storey {j + 1}")
                model.add_element(storey, parent=building)

        model.unit = unit
        return model

    # ==========================================================================
    # IFC Import
    # ==========================================================================

    def _load_from_ifc(self, rectify_placements=True, rectify_verbose=False):
        """Load the IFC file into the model tree with rectified transformations.

        Walks the IFC spatial hierarchy (IfcProject → IfcSite → IfcBuilding →
        IfcBuildingStorey → elements), creates GenericElement instances, and adds
        them to the model tree. IfcProject is absorbed into the BuildingModel.

        Transformations are rectified: each element's local transform is computed
        relative to its spatial parent.

        Parameters
        ----------
        rectify_placements : bool
            If True, rewrite each element's ``IfcLocalPlacement`` in the IFC file
            so that ``PlacementRelTo`` points to the spatial parent's placement
            and ``RelativePlacement`` holds the local (relative) transform.
        rectify_verbose : bool
            If True, print detailed information about each rectified placement,
            showing what ``PlacementRelTo`` changed from and to.

        """
        projects = self._file.get_entities_by_type("IfcProject")
        if not projects:
            return

        ifc_project = projects[0]

        # Store project-level info on the model
        self.name = getattr(ifc_project, "Name", None) or self.name

        # Track rectification stats
        self._rectified_count = 0
        self._rectify_verbose = rectify_verbose

        # Recursively load children of the project
        self._load_children(
            ifc_project,
            parent_element=None,
            parent_global_transform=Transformation(),
            rectify_placements=rectify_placements,
        )

        if rectify_placements and self._rectified_count > 0:
            print(f"Rectified {self._rectified_count} IFC placements to align with spatial hierarchy.")

        del self._rectified_count
        del self._rectify_verbose

        # Populate interaction graph with non-spatial relationships
        self._load_relationships_into_graph()

    def _load_children(self, ifc_entity, parent_element, parent_global_transform, rectify_placements=True):
        """Recursively load IFC children into the model tree.

        Parameters
        ----------
        ifc_entity : Base
            The IFC entity whose children to load.
        parent_element : GenericElement or None
            The parent element in the model tree (None for top-level under root).
        parent_global_transform : Transformation
            The global transformation of the parent, used for rectification.
        rectify_placements : bool
            Whether to rewrite IFC placements in the file.

        """
        for child_entity in ifc_entity.children:
            element = GenericElement.from_ifc_entity(child_entity, file=self._file)

            # Rectify: compute local transform relative to spatial parent
            global_transform = getattr(element, "_global_transform", Transformation())
            local_transform = parent_global_transform.inverse() * global_transform
            element.transformation = local_transform

            # Rewrite IFC placement if requested
            if rectify_placements and element._ifc_entity is not None:
                if hasattr(element._ifc_entity, "ObjectPlacement") and element._ifc_entity.ObjectPlacement:
                    self._rectify_ifc_placement(element, parent_element, local_transform)

            # Clean up temporary attribute
            if hasattr(element, "_global_transform"):
                del element._global_transform

            # Add to model — add_element override handles GlobalId indexing
            self.add_element(element, parent=parent_element)

            # Recurse into children
            self._load_children(child_entity, element, global_transform, rectify_placements)

    def _rectify_ifc_placement(self, element, parent_element, local_transform):
        """Rewrite an element's IfcLocalPlacement to use the spatial parent's placement.

        Checks whether the existing ``PlacementRelTo`` already points to the
        spatial parent. If not, rewrites the placement with the correct
        ``PlacementRelTo`` and the rectified ``RelativePlacement``.

        Parameters
        ----------
        element : GenericElement
            The element whose placement to rectify.
        parent_element : GenericElement or None
            The spatial parent element.
        local_transform : Transformation
            The rectified local transform (relative to spatial parent).

        """
        from compas_ifc.conversions.frame import frame_to_ifc_axis2_placement_3d

        ifc_entity = element._ifc_entity
        current_placement = ifc_entity.ObjectPlacement

        # Determine what PlacementRelTo should be
        expected_parent_placement = None
        if parent_element and parent_element._ifc_entity:
            expected_parent_placement = getattr(parent_element._ifc_entity, "ObjectPlacement", None)

        # Check if already correct
        current_parent_placement = current_placement.PlacementRelTo
        if current_parent_placement is expected_parent_placement:
            return

        # Log verbose detail before rewriting
        if getattr(self, "_rectify_verbose", False):
            old_label = self._placement_owner_label(current_parent_placement)
            new_label = self._placement_owner_label(expected_parent_placement)
            elem_label = f"{element.ifc_type} '{element.name}'"
            print(f"  {elem_label}: PlacementRelTo {old_label} -> {new_label}")

        # Rewrite: set RelativePlacement to the rectified local frame
        local_frame = Frame.from_transformation(local_transform)
        new_relative_placement = frame_to_ifc_axis2_placement_3d(self, local_frame)

        current_placement.RelativePlacement = new_relative_placement
        current_placement.PlacementRelTo = expected_parent_placement

        self._rectified_count += 1

    @staticmethod
    def _placement_owner_label(placement):
        """Return a human-readable label for the owner of an IfcLocalPlacement.

        Uses the raw ifcopenshell ``PlacesObject`` inverse attribute to find the
        IFC product that owns the placement. Falls back to the placement entity
        id if the owner cannot be determined.

        Parameters
        ----------
        placement : Base or None
            An ``IfcLocalPlacement`` entity.

        Returns
        -------
        str

        """
        if placement is None:
            return "<None / World>"

        # Access the raw ifcopenshell entity for reliable inverse attribute access
        raw = getattr(placement, "entity", None) or getattr(placement, "_entity", placement)

        try:
            places_object = raw.PlacesObject if hasattr(raw, "PlacesObject") else None
            if places_object:
                owners = list(places_object) if hasattr(places_object, "__iter__") else [places_object]
                if owners:
                    owner = owners[0]
                    owner_type = owner.is_a()
                    owner_name = getattr(owner, "Name", None) or ""
                    return f"{owner_type} '{owner_name}' (#{owner.id()})"
        except Exception:
            pass

        # Fallback: just show the placement entity id
        try:
            eid = raw.id()
        except Exception:
            eid = "?"
        return f"IfcLocalPlacement (#{eid})"

    # ==========================================================================
    # Interaction Graph (non-spatial IFC relationships)
    # ==========================================================================

    def _add_graph_only_element(self, element):
        """Add an element to the graph and element registry, but NOT the tree.

        Used for IFC entities that participate in relationships (graph edges)
        but are not part of the spatial hierarchy (e.g. ``IfcOpeningElement``).

        Parameters
        ----------
        element : GenericElement
            The element to register.

        """
        guid = str(element.guid)
        self._elements[guid] = element
        self.graph.add_element(element)
        element.model = self
        if element.global_id:
            self._elements_by_global_id[element.global_id] = element

    def _build_entity_lookup(self):
        """Build a mapping from raw IFC entity id to GenericElement.

        Returns
        -------
        dict[int, GenericElement]

        """
        lookup = {}
        for element in self._elements.values():
            if hasattr(element, "_ifc_entity") and element._ifc_entity is not None:
                lookup[element._ifc_entity.entity.id()] = element
        return lookup

    def _load_relationships_into_graph(self):
        """Populate the interaction graph with spatial relationships.

        Loads non-hierarchical spatial relationships between building elements
        as graph edges. Only topological relationships that describe physical
        spatial interactions are included — the spatial hierarchy (containment,
        spatial decomposition) is already expressed by the model tree.

        **Topology** (element-to-element physical connections):

            ``void`` — IfcRelVoidsElement (wall/slab → opening)
            ``fill`` — IfcRelFillsElement (opening → door/window)
            ``connection`` — IfcRelConnectsPathElements, IfcRelConnectsElements
            ``space_boundary`` — IfcRelSpaceBoundary (space → bounding element)
            ``covering`` — IfcRelCoversBldgElements, IfcRelCoversSpaces
            ``interference`` — IfcRelInterferesElements (clash)
            ``projection`` — IfcRelProjectsElement

        **Structural** (analytical model connections):

            ``structural`` — IfcRelConnectsStructuralMember / Activity / Eccentricity

        **MEP** (distribution systems):

            ``port_connection`` — IfcRelConnectsPorts
            ``port_element`` — IfcRelConnectsPortToElement
            ``flow_control`` — IfcRelFlowControlElements
            ``services`` — IfcRelServicesBuildings
            ``spatial_reference`` — IfcRelReferencedInSpatialStructure

        Non-spatial relationships (type definitions, material associations,
        group assignments, external references, decomposition, etc.) are
        intentionally excluded — they are accessible via the underlying
        ``_ifc_entity``.

        Entities not already in the spatial tree (e.g. ``IfcOpeningElement``)
        are added as graph-only nodes.
        """
        entity_lookup = self._build_entity_lookup()
        stats = {}

        def _stat(category):
            stats[category] = stats.get(category, 0) + 1

        def _by_type(type_name):
            """Query entities by type, returning [] for types missing in the schema."""
            try:
                return self._file.get_entities_by_type(type_name)
            except RuntimeError:
                return []

        def _ensure_element(ifc_entity):
            """Return GenericElement for ifc_entity, creating graph-only node if needed."""
            if ifc_entity is None:
                return None
            eid = ifc_entity.entity.id()
            elem = entity_lookup.get(eid)
            if elem is None:
                elem = GenericElement.from_ifc_entity(ifc_entity, file=self._file)
                if hasattr(elem, "_global_transform"):
                    del elem._global_transform
                self._add_graph_only_element(elem)
                entity_lookup[eid] = elem
            return elem

        def _add_edge(elem_a, elem_b, category, **attrs):
            """Add an interaction edge with category and optional extra attributes.

            Categories are stored as a set so that parallel IFC relationships
            between the same element pair accumulate rather than overwrite.
            """
            if elem_a is None or elem_b is None:
                return None
            edge = self.add_interaction(elem_a, elem_b)
            existing = self.graph.edge_attribute(edge, "categories")
            if existing is None:
                existing = set()
            existing.add(category)
            self.graph.edge_attribute(edge, "categories", existing)
            for k, v in attrs.items():
                self.graph.edge_attribute(edge, k, v)
            _stat(category)
            return edge

        # ==================================================================
        # GROUP 1: Topology
        # ==================================================================

        # --- A. IfcRelVoidsElement → "void" ---
        for rel in _by_type("IfcRelVoidsElement"):
            host = rel.RelatingBuildingElement
            opening = rel.RelatedOpeningElement

            host_elem = entity_lookup.get(host.entity.id())
            if host_elem is None:
                continue

            # Create graph-only element for the opening
            opening_id = opening.entity.id()
            opening_elem = entity_lookup.get(opening_id)
            if opening_elem is None:
                opening_elem = GenericElement.from_ifc_entity(opening, file=self._file)
                host_global = getattr(host_elem, "_global_transform", None)
                if host_global is None and host_elem.transformation is not None:
                    host_global = host_elem.modeltransformation
                if host_global is None:
                    host_global = Transformation()
                opening_global = getattr(opening_elem, "_global_transform", Transformation())
                opening_elem.transformation = host_global.inverse() * opening_global
                if hasattr(opening_elem, "_global_transform"):
                    del opening_elem._global_transform
                self._add_graph_only_element(opening_elem)
                entity_lookup[opening_id] = opening_elem

            _add_edge(host_elem, opening_elem, "void")

        # --- B. IfcRelFillsElement → "fill" ---
        for rel in _by_type("IfcRelFillsElement"):
            opening_elem = entity_lookup.get(rel.RelatingOpeningElement.entity.id())
            filler_elem = entity_lookup.get(rel.RelatedBuildingElement.entity.id())
            _add_edge(opening_elem, filler_elem, "fill")

        # --- C. IfcRelConnectsPathElements → "connection" ---
        for rel in _by_type("IfcRelConnectsPathElements"):
            elem_a = entity_lookup.get(rel.RelatingElement.entity.id())
            elem_b = entity_lookup.get(rel.RelatedElement.entity.id())
            _add_edge(elem_a, elem_b, "connection")

        # --- C2. IfcRelConnectsElements (base class, excluding subtypes) ---
        for rel in _by_type("IfcRelConnectsElements"):
            # Skip subtypes that are handled explicitly
            exact_type = rel.is_a()
            if exact_type in ("IfcRelConnectsPathElements", "IfcRelConnectsWithRealizingElements"):
                continue
            elem_a = entity_lookup.get(rel.RelatingElement.entity.id())
            elem_b = entity_lookup.get(rel.RelatedElement.entity.id())
            _add_edge(elem_a, elem_b, "connection")

        # --- C3. IfcRelConnectsWithRealizingElements → "connection" ---
        for rel in _by_type("IfcRelConnectsWithRealizingElements"):
            elem_a = entity_lookup.get(rel.RelatingElement.entity.id())
            elem_b = entity_lookup.get(rel.RelatedElement.entity.id())
            _add_edge(elem_a, elem_b, "connection")

        # --- D. IfcRelSpaceBoundary → "space_boundary" ---
        for rel in _by_type("IfcRelSpaceBoundary"):
            related = rel.RelatedBuildingElement
            if related is None:
                continue
            space_elem = entity_lookup.get(rel.RelatingSpace.entity.id())
            related_elem = entity_lookup.get(related.entity.id())
            _add_edge(space_elem, related_elem, "space_boundary")

        # --- E. IfcRelCoversBldgElements → "covering" ---
        for rel in _by_type("IfcRelCoversBldgElements"):
            host_elem = entity_lookup.get(rel.RelatingBuildingElement.entity.id())
            for covering in rel.RelatedCoverings:
                covering_elem = _ensure_element(covering)
                _add_edge(host_elem, covering_elem, "covering")

        # --- E2. IfcRelCoversSpaces → "covering" ---
        for rel in _by_type("IfcRelCoversSpaces"):
            space_elem = entity_lookup.get(rel.RelatingSpace.entity.id())
            for covering in rel.RelatedCoverings:
                covering_elem = _ensure_element(covering)
                _add_edge(space_elem, covering_elem, "covering")

        # --- F. IfcRelInterferesElements → "interference" ---
        for rel in _by_type("IfcRelInterferesElements"):
            elem_a = entity_lookup.get(rel.RelatingElement.entity.id())
            elem_b = entity_lookup.get(rel.RelatedElement.entity.id())
            interference_type = getattr(rel, "InterferenceType", None)
            _add_edge(elem_a, elem_b, "interference", interference_type=interference_type)

        # --- G. IfcRelProjectsElement → "projection" ---
        for rel in _by_type("IfcRelProjectsElement"):
            host_elem = entity_lookup.get(rel.RelatingElement.entity.id())
            feature_elem = _ensure_element(rel.RelatedFeatureElement)
            _add_edge(host_elem, feature_elem, "projection")

        # ==================================================================
        # Structural (analytical model connections)
        # ==================================================================

        # --- H. IfcRelConnectsStructuralMember → "structural" ---
        for rel_type in ("IfcRelConnectsStructuralMember", "IfcRelConnectsWithEccentricity"):
            for rel in _by_type(rel_type):
                member_elem = _ensure_element(rel.RelatingStructuralMember)
                conn_elem = _ensure_element(rel.RelatedStructuralConnection)
                _add_edge(member_elem, conn_elem, "structural")

        # --- I. IfcRelConnectsStructuralActivity → "structural" ---
        for rel in _by_type("IfcRelConnectsStructuralActivity"):
            element_elem = _ensure_element(rel.RelatingElement)
            activity_elem = _ensure_element(rel.RelatedStructuralActivity)
            _add_edge(element_elem, activity_elem, "structural")

        # ==================================================================
        # MEP (distribution systems)
        # ==================================================================

        # --- J. IfcRelConnectsPorts → "port_connection" ---
        for rel in _by_type("IfcRelConnectsPorts"):
            port_a = _ensure_element(rel.RelatingPort)
            port_b = _ensure_element(rel.RelatedPort)
            _add_edge(port_a, port_b, "port_connection")

        # --- K. IfcRelConnectsPortToElement → "port_element" ---
        for rel in _by_type("IfcRelConnectsPortToElement"):
            port_elem = _ensure_element(rel.RelatingPort)
            host_elem = entity_lookup.get(rel.RelatedElement.entity.id())
            if host_elem is None:
                host_elem = _ensure_element(rel.RelatedElement)
            _add_edge(port_elem, host_elem, "port_element")

        # --- L. IfcRelFlowControlElements → "flow_control" ---
        for rel in _by_type("IfcRelFlowControlElements"):
            flow_elem = entity_lookup.get(rel.RelatingFlowElement.entity.id())
            if flow_elem is None:
                flow_elem = _ensure_element(rel.RelatingFlowElement)
            for ctrl in rel.RelatedControlElements:
                ctrl_elem = _ensure_element(ctrl)
                _add_edge(flow_elem, ctrl_elem, "flow_control")

        # --- M. IfcRelServicesBuildings → "services" ---
        for rel in _by_type("IfcRelServicesBuildings"):
            system_elem = _ensure_element(rel.RelatingSystem)
            for bldg in rel.RelatedBuildings:
                bldg_elem = entity_lookup.get(bldg.entity.id())
                _add_edge(system_elem, bldg_elem, "services")

        # --- N. IfcRelReferencedInSpatialStructure → "spatial_reference" ---
        for rel in _by_type("IfcRelReferencedInSpatialStructure"):
            space_elem = entity_lookup.get(rel.RelatingStructure.entity.id())
            for obj in rel.RelatedElements:
                obj_elem = entity_lookup.get(obj.entity.id())
                if obj_elem is None:
                    obj_elem = _ensure_element(obj)
                _add_edge(space_elem, obj_elem, "spatial_reference")

        # ==================================================================
        # Summary
        # ==================================================================
        total = sum(stats.values())
        if total > 0:
            parts = [f"{v} {k}" for k, v in stats.items() if v > 0]
            print(f"Loaded {total} graph edges: {', '.join(parts)}.")

    # ---------- Graph queries ----------

    def get_interactions_by_category(self, category: str) -> list:
        """Get all graph edges that include a specific category.

        An edge may carry multiple categories (e.g. both ``"connection"`` and
        ``"space_boundary"`` if the same element pair has both relationship
        types in the IFC file).

        Parameters
        ----------
        category : str
            The category string (e.g. ``"connection"``, ``"void"``, ``"fill"``,
            ``"space_boundary"``).

        Returns
        -------
        list[tuple[int, int]]
            Graph edges that include the category.

        """
        return [edge for edge in self.graph.edges() if category in (self.graph.edge_attribute(edge, "categories") or set())]

    def get_interactions_by_group(self, group: str) -> list:
        """Get all graph edges belonging to a relationship group.

        Returns edges that have at least one category in the group.

        Parameters
        ----------
        group : str
            One of ``"topology"``, ``"structural"``, or ``"mep"``.

        Returns
        -------
        list[tuple[int, int]]
            Graph edges in the group.

        Raises
        ------
        ValueError
            If the group name is not recognised.

        """
        group_categories = self.RELATIONSHIP_GROUPS.get(group)
        if group_categories is None:
            raise ValueError(f"Unknown group '{group}'. Choose from: {', '.join(self.RELATIONSHIP_GROUPS)}")
        return [edge for edge in self.graph.edges() if (self.graph.edge_attribute(edge, "categories") or set()) & group_categories]

    @property
    def connections(self) -> list:
        """All wall-to-wall connection edges (from ``IfcRelConnectsPathElements``)."""
        return self.get_interactions_by_category("connection")

    @property
    def voids(self) -> list:
        """All void/opening edges (from ``IfcRelVoidsElement``)."""
        return self.get_interactions_by_category("void")

    @property
    def fills(self) -> list:
        """All fill edges (from ``IfcRelFillsElement``)."""
        return self.get_interactions_by_category("fill")

    @property
    def space_boundaries(self) -> list:
        """All space boundary edges (from ``IfcRelSpaceBoundary``)."""
        return self.get_interactions_by_category("space_boundary")

    def edge_elements(self, edge) -> tuple:
        """Return the two GenericElements connected by a graph edge.

        Parameters
        ----------
        edge : tuple[int, int]
            A graph edge.

        Returns
        -------
        tuple[GenericElement, GenericElement]

        """
        u, v = edge
        return self.graph.node_element(u), self.graph.node_element(v)

    # ==========================================================================
    # IFC Export
    # ==========================================================================

    def save(self, path: str):
        """Save the IFC file to disk.

        Since the model is a bi-directional front-end, the IFC file is always
        in sync with the model tree. This simply writes the file.
        """
        self._file.save(path)

    def to_ifc(self, path: str, schema: str = None):
        """Export the model to an IFC file.

        Since the IFC file is always kept in sync, this is equivalent to ``save()``.
        """
        self.save(path)

    def extract(
        self,
        elements,
        path: str = None,
        load_geometries: bool = True,
        export_materials: bool = True,
        export_properties: bool = True,
        export_styles: bool = True,
        export_types: bool = True,
        export_relationships: bool = True,
    ) -> "BuildingInformationModel":
        """Extract elements into a new standalone BuildingInformationModel.

        Collects the given elements and all their descendants, exports them to
        a new IFC file preserving all linked information (geometry, placements,
        properties, materials, styles, type definitions), then loads the result
        as a new model.

        Ancestor spatial containers (IfcProject, IfcSite, IfcBuilding,
        IfcBuildingStorey) are included automatically so the extracted file is
        a valid, self-contained IFC file.

        Non-spatial IFC relationships (connections, voids, fills, space
        boundaries) are preserved when both endpoints of the relationship are
        in the exported set. This ensures the interaction graph is maintained
        in the extracted model.

        Parameters
        ----------
        elements : GenericElement or list[GenericElement]
            Element(s) to extract. All descendants are included automatically.
        path : str, optional
            If given, the extracted IFC file is saved to this path.
            If None, a temporary file is used and cleaned up after loading.
        load_geometries : bool, optional
            Whether to pre-load geometries in the extracted model. Default True.
        export_materials : bool, optional
            Whether to export material associations. Default True.
        export_properties : bool, optional
            Whether to export property sets. Default True.
        export_styles : bool, optional
            Whether to export visual styles. Default True.
        export_types : bool, optional
            Whether to export type definitions (IfcRelDefinesByType). Default True.
        export_relationships : bool, optional
            Whether to export non-spatial relationships (connections, voids,
            fills, space boundaries) where both endpoints are in the exported
            set. Default True.

        Returns
        -------
        BuildingInformationModel
            A new standalone model containing only the extracted elements.

        """
        import os
        import tempfile

        # Normalize input
        if isinstance(elements, GenericElement):
            elements = [elements]

        # Collect all IFC entities: given elements + all their descendants
        ifc_entities = []
        seen = set()

        def _collect(element):
            eid = id(element)
            if eid in seen:
                return
            seen.add(eid)
            if element._ifc_entity is not None:
                ifc_entities.append(element._ifc_entity)
            for child in element.children:
                _collect(child)

        for element in elements:
            _collect(element)

        if not ifc_entities:
            raise ValueError("No IFC entities found in the given elements.")

        # Export to file (IFCFile.export handles spatial ancestors, deduplication,
        # and all linked info: properties, materials, styles, types)
        use_temp = path is None
        if use_temp:
            fd, temp_path = tempfile.mkstemp(suffix=".ifc")
            os.close(fd)
            export_path = temp_path
        else:
            export_path = path

        self._file.export(
            export_path,
            entities=ifc_entities,
            export_materials=export_materials,
            export_properties=export_properties,
            export_styles=export_styles,
            export_types=export_types,
            export_relationships=export_relationships,
        )

        # Load extracted IFC into a new model
        new_model = BuildingInformationModel(
            filepath=export_path,
            schema=self.schema_name,
            load_geometries=load_geometries,
        )

        # If user specified a path, file is already there.
        # If temp file, clean up.
        if use_temp:
            os.remove(temp_path)

        return new_model

    # ==========================================================================
    # Display
    # ==========================================================================

    def print_hierarchy(self, max_depth: int = 10):
        """Print the spatial hierarchy of the model."""

        def _print_node(element, depth, max_depth):
            if depth > max_depth:
                return
            indent = "  " * depth
            geom_marker = "*" if element.geometry is not None else ""
            print(f"{indent}{element.ifc_type}: {element.name} {geom_marker}")
            for child in element.children:
                _print_node(child, depth + 1, max_depth)

        print(f"BuildingInformationModel: {self.name}")
        # Top-level elements are direct children of tree root
        for node in self.tree.root.children:
            _print_node(node.element, 1, max_depth)

    def show(self):
        """Show the model in compas_viewer.

        Directly adds element geometries to the viewer scene, bypassing the
        compas_model scene object pipeline to avoid unnecessary data copies.
        """
        try:
            from compas_viewer import Viewer
            from compas_viewer.components import Treeform
        except ImportError:
            raise ImportError("The show method requires compas_viewer to be installed.")

        viewer = Viewer()
        viewer.ui.sidebar.show_objectsetting = False

        if self.unit:
            viewer.unit = self.unit

        def _add_element(element, parent=None):
            label = f"[{element.ifc_type}] {element.name}"
            obj = None

            if element.geometry is not None and element.ifc_type != "IfcSpace":
                style_kwargs = element.style or {}
                obj = viewer.scene.add(
                    element.geometry,
                    name=label,
                    parent=parent,
                    hide_coplanaredges=True,
                    **style_kwargs,
                )
                obj.transformation = element.modeltransformation
            else:
                obj = viewer.scene.add_group(name=label, parent=parent)

            obj.attributes["element"] = element

            for child in element.children:
                _add_element(child, parent=obj)

        for node in self.tree.root.children:
            _add_element(node.element)

        treeform = Treeform()
        viewer.ui.sidebar.add(treeform)

        def update_treeform(form, node):
            element = node.attributes.get("element")
            if element:
                info = {
                    "Type": element.ifc_type,
                    "Name": element.name,
                    "GlobalId": element.global_id or "",
                }
                info.update(element.properties)
                treeform.update_from_dict(info)

        viewer.ui.sidebar.sceneform.action = update_treeform
        viewer.show()
