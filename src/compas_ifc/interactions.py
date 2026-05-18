"""Mixin providing interaction-graph functionality for BuildingInformationModel.

Groups all graph-related code: loading IFC relationships, querying edges,
computing connections (contacts) and collisions (interferences).
"""

from __future__ import annotations

import ifcopenshell.guid

from compas_ifc.element import GenericElement


def _matches_any_type(element, ifc_types) -> bool:
    """Return True if ``element`` is an instance of any class in ``ifc_types``.

    Uses ifcopenshell's ``is_a()`` so subclass matching works — passing
    ``"IfcWall"`` matches ``IfcWallStandardCase``. Mirrors what
    ``raw_file.by_type(name)`` does for the rest of the selection grammar.
    """
    return any(element._ifc_entity.is_a(t) for t in ifc_types)


class InteractionMixin:
    """Mixin that adds interaction-graph capabilities to a Model subclass.

    Expects the host class to provide:
    - ``self._file`` — :class:`IFCFile`
    - ``self._elements`` — dict of guid → GenericElement
    - ``self._elements_by_global_id`` — dict of IFC GlobalId → GenericElement
    - ``self.graph`` — :class:`compas_model.models.InteractionGraph`
    - ``self.add_interaction(a, b)`` — from compas_model.Model
    - ``self.elements()`` — iterator over all GenericElement
    """

    # Category → group mapping for relationship queries.
    RELATIONSHIP_GROUPS = {
        "topology": {"connection", "space_boundary", "covering", "interference", "projection"},
        "structural": {"structural"},
        "mep": {"port_connection", "port_element", "flow_control", "services", "spatial_reference"},
    }

    # ==========================================================================
    # Graph loading (private)
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

        Entities not already in the spatial tree are added as graph-only nodes.

        Void (``IfcRelVoidsElement``) and fill (``IfcRelFillsElement``)
        relationships are expressed in the spatial tree (host -> opening ->
        filler) and are therefore not duplicated as graph edges.
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
                elem = GenericElement._from_ifc_entity(ifc_entity)
                if hasattr(elem, "_global_transform"):
                    del elem._global_transform
                self._add_graph_only_element(elem)
                entity_lookup[eid] = elem
            return elem

        def _add_edge(elem_a, elem_b, category, **attrs):
            """Add a relationship record to the interaction edge between two elements.

            Each IFC relationship instance is stored as a separate record in the
            edge's ``relationships`` list, preserving multiplicity (e.g. multiple
            space boundaries between the same space and wall).
            """
            if elem_a is None or elem_b is None:
                return None
            edge = self.add_interaction(elem_a, elem_b)
            rels = self.graph.edge_attribute(edge, "relationships")
            if rels is None:
                rels = []
            record = {"category": category}
            record.update(attrs)
            rels.append(record)
            self.graph.edge_attribute(edge, "relationships", rels)
            _stat(category)
            return edge

        # ==================================================================
        # GROUP 1: Topology
        # ==================================================================
        # Note: void (IfcRelVoidsElement) and fill (IfcRelFillsElement)
        # are captured in the spatial tree, not as graph edges.

        # --- A. IfcRelConnectsPathElements → "connection" ---
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

    # ==========================================================================
    # Graph queries (public)
    # ==========================================================================

    def _edge_relationships(self, edge) -> list:
        """Return the list of relationship records stored on a graph edge.

        Each record is a dict with at least a ``"category"`` key. Additional
        keys depend on the relationship type (e.g. ``"interference_type"``).

        Parameters
        ----------
        edge : tuple[int, int]
            A graph edge.

        Returns
        -------
        list[dict]

        """
        return self.graph.edge_attribute(edge, "relationships") or []

    def get_interactions_by_category(self, category: str) -> list:
        """Get all graph edges that have at least one relationship of a given category.

        Parameters
        ----------
        category : str
            The category string (e.g. ``"connection"``, ``"space_boundary"``).

        Returns
        -------
        list[tuple[int, int]]
            Graph edges that include the category.

        """
        return [edge for edge in self.graph.edges() if any(r["category"] == category for r in self._edge_relationships(edge))]

    def get_interactions_by_group(self, group: str) -> list:
        """Get all graph edges belonging to a relationship group.

        Returns edges that have at least one relationship whose category
        belongs to the group.

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
        return [edge for edge in self.graph.edges() if any(r["category"] in group_categories for r in self._edge_relationships(edge))]

    @property
    def connections(self) -> list:
        """All wall-to-wall connection edges (from ``IfcRelConnectsPathElements``)."""
        return self.get_interactions_by_category("connection")

    @property
    def space_boundaries(self) -> list:
        """All space boundary edges (from ``IfcRelSpaceBoundary``)."""
        return self.get_interactions_by_category("space_boundary")

    @property
    def interferences(self) -> list:
        """All interference/collision edges (from ``IfcRelInterferesElements`` or computed)."""
        return self.get_interactions_by_category("interference")

    def _edge_elements(self, edge) -> tuple:
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
    # Automatic connection detection
    # ==========================================================================

    def compute_connections(
        self,
        tolerance: float = 1e-3,
        minimum_area: float = 1e-2,
        element_types: list = None,
        create_ifc_relations: bool = True,
    ):
        """Detect geometric contacts between building elements and add them as connection edges.

        Uses a two-stage broadphase filter:

        1. BVH spatial search with inflated AABBs to find rough neighbours.
        2. Tight world-space AABB overlap test to discard false positives.

        Then performs face-level contact detection on remaining pairs.
        Discovered contacts are stored as ``"connection"`` relationship records
        on the interaction graph, alongside any existing relationships.

        Parameters
        ----------
        tolerance : float, optional
            Distance tolerance for the coplanarity check (metres). Default ``1e-3``.
        minimum_area : float, optional
            Minimum area of a valid contact polygon (m²). Default ``1e-2``.
        element_types : list[str], optional
            IFC type names to include (e.g. ``["IfcWall", "IfcSlab"]``). Subclass
            matching applies, so ``"IfcWall"`` includes ``IfcWallStandardCase``.
            If ``None``, all non-spatial elements with geometry are considered.
        create_ifc_relations : bool, optional
            If ``True`` (default), also create ``IfcRelConnectsElements`` entities
            in the IFC file so that discovered connections persist on save/reload.

        Returns
        -------
        int
            Number of new connection edges created.

        """
        from compas_model.models.bvh import ElementBVH

        # ---- collect candidates ------------------------------------------------
        candidates = []
        for e in self.elements():
            if e._is_spatial or e.geometry is None or e.treenode is None:
                continue
            if element_types is not None and not _matches_any_type(e, element_types):
                continue
            candidates.append(e)

        if not candidates:
            return 0

        # ---- broadphase 1: BVH -------------------------------------------------
        bvh = ElementBVH.from_elements(candidates)

        # ---- pre-compute world AABBs for tight filter ---------------------------
        world_aabbs = {id(e): e.aabb for e in candidates}

        def _aabb_overlap(box_a, box_b, tol=0.01):
            """Return True if two AABBs overlap within tolerance."""
            if box_a is None or box_b is None:
                return False
            a_pts = box_a.points
            b_pts = box_b.points
            for i in range(3):
                a_lo = min(p[i] for p in a_pts)
                a_hi = max(p[i] for p in a_pts)
                b_lo = min(p[i] for p in b_pts)
                b_hi = max(p[i] for p in b_pts)
                if a_lo > b_hi + tol or b_lo > a_hi + tol:
                    return False
            return True

        # ---- narrowphase -------------------------------------------------------
        new_connections = 0
        seen_pairs = set()

        for element in candidates:
            neighbours = bvh.nearest_neighbors(element)
            for neighbour in neighbours:
                pair = frozenset((id(element), id(neighbour)))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                # broadphase 2: tight AABB overlap
                if not _aabb_overlap(world_aabbs[id(element)], world_aabbs[id(neighbour)], tol=tolerance):
                    continue

                # narrowphase: face-level contact detection
                contacts = element.compute_contacts(neighbour, tolerance=tolerance, minimum_area=minimum_area)
                if not contacts:
                    continue

                # store on graph
                node_a = element.graphnode
                node_b = neighbour.graphnode
                record = {"category": "connection", "source": "computed"}

                if self.graph.has_edge((node_a, node_b)):
                    edge = (node_a, node_b)
                    rels = self.graph.edge_attribute(edge, "relationships") or []
                    rels.append(record)
                    self.graph.edge_attribute(edge, "relationships", rels)
                    self.graph.edge_attribute(edge, "contacts", contacts)
                elif self.graph.has_edge((node_b, node_a)):
                    edge = (node_b, node_a)
                    rels = self.graph.edge_attribute(edge, "relationships") or []
                    rels.append(record)
                    self.graph.edge_attribute(edge, "relationships", rels)
                    self.graph.edge_attribute(edge, "contacts", contacts)
                else:
                    self.graph.add_edge(node_a, node_b, relationships=[record], contacts=contacts)

                new_connections += 1

                if create_ifc_relations and element._ifc_entity and neighbour._ifc_entity:
                    self._file._file.create_entity(
                        "IfcRelConnectsElements",
                        GlobalId=ifcopenshell.guid.new(),
                        RelatingElement=element._ifc_entity.entity,
                        RelatedElement=neighbour._ifc_entity.entity,
                    )

        return new_connections

    # ==========================================================================
    # Automatic collision (interference) detection
    # ==========================================================================

    def compute_collisions(
        self,
        tolerance: float = 1e-6,
        min_depth: float = 1e-4,
        element_types: list = None,
        create_ifc_relations: bool = True,
        skip_related: bool = True,
    ):
        """Detect volumetric collisions (interferences) between building elements.

        Uses the same two-stage broadphase as :meth:`compute_connections`:

        1. BVH spatial search with inflated AABBs to find rough neighbours.
        2. Tight world-space AABB overlap test to discard false positives.

        Then performs ray-casting collision detection on remaining pairs.
        Discovered collisions are stored as ``"interference"`` relationship
        records on the interaction graph.

        Parameters
        ----------
        tolerance : float, optional
            Numerical tolerance for the ray-triangle intersection test.
            Default ``1e-6``.
        min_depth : float, optional
            Minimum penetration depth to count as a collision (excludes
            touching pairs). Default ``1e-4``.
        element_types : list[str], optional
            IFC type names to include (e.g. ``["IfcWall", "IfcColumn"]``).
            Subclass matching applies, so ``"IfcWall"`` includes
            ``IfcWallStandardCase``. If ``None``, all non-spatial elements with
            geometry are considered.
        create_ifc_relations : bool, optional
            If ``True`` (default), also create ``IfcRelInterferesElements`` entities
            in the IFC file so that discovered interferences persist on save/reload.
        skip_related : bool, optional
            If ``True`` (default), skip pairs where one element is an ancestor
            of the other in the spatial tree. This filters out expected
            overlaps such as ``wall → opening → window/door`` (the void/fill
            chain), where the opening and its filler share the same volume
            by construction.

        Returns
        -------
        int
            Number of new interference edges created.

        """
        from compas_model.models.bvh import ElementBVH

        # ---- collect candidates ------------------------------------------------
        candidates = []
        for e in self.elements():
            if e._is_spatial or e.geometry is None or e.treenode is None:
                continue
            if element_types is not None and not _matches_any_type(e, element_types):
                continue
            candidates.append(e)

        if not candidates:
            return 0

        # ---- broadphase 1: BVH -------------------------------------------------
        bvh = ElementBVH.from_elements(candidates)

        # ---- pre-compute world AABBs for tight filter ---------------------------
        world_aabbs = {id(e): e.aabb for e in candidates}

        # ---- pre-compute ancestor id-sets so the narrowphase relatedness check
        # ---- is O(1) instead of two parent-chain walks per pair ----------------
        ancestors = {}
        if skip_related:
            for e in candidates:
                chain = set()
                cur = e.parent
                while cur is not None:
                    chain.add(id(cur))
                    cur = cur.parent
                ancestors[id(e)] = chain

        def _aabb_overlap(box_a, box_b, tol=0.01):
            """Return True if two AABBs overlap within tolerance."""
            if box_a is None or box_b is None:
                return False
            a_pts = box_a.points
            b_pts = box_b.points
            for i in range(3):
                a_lo = min(p[i] for p in a_pts)
                a_hi = max(p[i] for p in a_pts)
                b_lo = min(p[i] for p in b_pts)
                b_hi = max(p[i] for p in b_pts)
                if a_lo > b_hi + tol or b_lo > a_hi + tol:
                    return False
            return True

        # ---- narrowphase -------------------------------------------------------
        new_collisions = 0
        seen_pairs = set()

        for element in candidates:
            neighbours = bvh.nearest_neighbors(element)
            for neighbour in neighbours:
                pair = frozenset((id(element), id(neighbour)))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                # broadphase 2: tight AABB overlap
                if not _aabb_overlap(world_aabbs[id(element)], world_aabbs[id(neighbour)], tol=tolerance):
                    continue

                if skip_related and (id(neighbour) in ancestors[id(element)] or id(element) in ancestors[id(neighbour)]):
                    continue

                # narrowphase: ray-casting collision detection
                penetrating = element.compute_collisions(neighbour, tolerance=tolerance, min_depth=min_depth)
                if not penetrating:
                    continue

                # store on graph
                node_a = element.graphnode
                node_b = neighbour.graphnode
                record = {"category": "interference", "source": "computed"}

                if self.graph.has_edge((node_a, node_b)):
                    edge = (node_a, node_b)
                    rels = self.graph.edge_attribute(edge, "relationships") or []
                    rels.append(record)
                    self.graph.edge_attribute(edge, "relationships", rels)
                    self.graph.edge_attribute(edge, "penetrating_points", penetrating)
                elif self.graph.has_edge((node_b, node_a)):
                    edge = (node_b, node_a)
                    rels = self.graph.edge_attribute(edge, "relationships") or []
                    rels.append(record)
                    self.graph.edge_attribute(edge, "relationships", rels)
                    self.graph.edge_attribute(edge, "penetrating_points", penetrating)
                else:
                    self.graph.add_edge(node_a, node_b, relationships=[record], penetrating_points=penetrating)

                new_collisions += 1

                # IfcRelInterferesElements is IFC4+
                if create_ifc_relations and element._ifc_entity and neighbour._ifc_entity and "IfcRelInterferesElements" in self._file.classes:
                    self._file._file.create_entity(
                        "IfcRelInterferesElements",
                        GlobalId=ifcopenshell.guid.new(),
                        RelatingElement=element._ifc_entity.entity,
                        RelatedElement=neighbour._ifc_entity.entity,
                    )

        return new_collisions

    # ==========================================================================
    # Collision visualisation
    # ==========================================================================

    def show_collisions(
        self,
        tolerance: float = 1e-6,
        min_depth: float = 1e-4,
        element_types: list = None,
    ):
        """Show the model with an interactive collision list in compas_viewer.

        Runs collision detection (if not already done), then opens a viewer
        with all building elements and a sidebar panel listing every collision
        pair.  Selecting a pair highlights the two colliding elements in red
        and dims everything else.

        Parameters
        ----------
        tolerance : float, optional
            Tolerance for the collision detection.
        min_depth : float, optional
            Minimum penetration depth.
        element_types : list[str], optional
            IFC type names to include in collision detection.

        """
        try:
            from compas_viewer import Viewer
            from compas_viewer.components import Treeform
        except ImportError:
            raise ImportError("The show_collisions method requires compas_viewer to be installed.")

        from compas.colors import Color

        # ---- run collision detection if needed --------------------------------
        if not self.interferences:
            print("Running collision detection...")
            n = self.compute_collisions(tolerance=tolerance, element_types=element_types)
            print(f"Found {n} collisions.")

        if not self.interferences:
            print("No collisions to display.")

        # ---- set up viewer ----------------------------------------------------
        viewer = Viewer()
        viewer.ui.sidebar.show_objectsetting = False

        if self.unit:
            viewer.unit = self.unit

        # Map global_id → scene object for fast lookup
        gid_to_obj = {}
        original_colors = {}  # gid → facecolor or facecolors (depending on object type)
        geometry_gids = set()  # gids that have actual geometry (not groups)

        def _add_element(element, parent=None):
            label = f"[{element.ifc_type}] {element.name}"
            obj = None
            visual = element._visual_geometry
            skip_visual = element.ifc_type in ("IfcSpace", "IfcOpeningElement")
            has_geometry = visual is not None and not skip_visual

            if has_geometry:
                style_kwargs = element._resolve_style() or {}
                obj = viewer.scene.add(
                    visual,
                    name=label,
                    parent=parent,
                    hide_coplanaredges=True,
                    **style_kwargs,
                )
            else:
                obj = viewer.scene.add_group(name=label, parent=parent)

            obj.transformation = element.transformation
            obj.attributes["element"] = element
            if element.global_id:
                gid_to_obj[element.global_id] = obj
                if has_geometry:
                    geometry_gids.add(element.global_id)
                    # TessellatedBrepObject uses facecolors (list), others use facecolor
                    if hasattr(obj, "facecolors"):
                        original_colors[element.global_id] = list(obj.facecolors)
                    else:
                        original_colors[element.global_id] = obj.facecolor

            for child in element.children:
                _add_element(child, parent=obj)

        for node in self.tree.root.children:
            _add_element(node.element)

        # ---- build collision list data ----------------------------------------
        collision_data = []
        for edge in self.interferences:
            a, b = self._edge_elements(edge)
            pts = self.graph.edge_attribute(edge, "penetrating_points") or []
            collision_data.append(
                {
                    "a_gid": a.global_id,
                    "b_gid": b.global_id,
                    "a_label": f"[{a.ifc_type}] {a.name}",
                    "b_label": f"[{b.ifc_type}] {b.name}",
                    "count": len(pts),
                }
            )

        # ---- property treeform (top) ------------------------------------------
        info_treeform = Treeform()
        viewer.ui.sidebar.add(info_treeform)

        # ---- collision list treeform (bottom) ---------------------------------
        collision_tree_data = {}
        for i, c in enumerate(collision_data):
            collision_tree_data[f"Collision {i + 1}"] = {
                "Element A": c["a_label"],
                "Element B": c["b_label"],
                "Penetrating points": str(c["count"]),
            }

        if not collision_tree_data:
            collision_tree_data["No collisions detected"] = ""

        collision_treeform = Treeform()
        collision_treeform.update_from_dict(collision_tree_data)
        viewer.ui.sidebar.add(collision_treeform)

        # ---- highlight state --------------------------------------------------
        COLOR_A = Color(1.0, 0.15, 0.15)  # red
        COLOR_B = Color(0.15, 0.8, 0.15)  # green

        active_pair = [None]  # mutable container for closure
        dirty_gids = set()  # gids whose colors have been modified

        def _set_color(obj, color):
            """Set face color on any scene object type."""
            if hasattr(obj, "facecolors"):
                obj.facecolors = [color] * len(obj.facecolors)
            else:
                obj.facecolor = color

        def _restore_color(gid):
            """Restore original color for a geometry object."""
            obj = gid_to_obj[gid]
            orig = original_colors[gid]
            if hasattr(obj, "facecolors"):
                obj.facecolors = list(orig)
            else:
                obj.facecolor = orig

        def _show_all():
            """Show all geometry objects and restore original colours."""
            for gid in geometry_gids:
                obj = gid_to_obj[gid]
                obj.show = True
                if gid in dirty_gids:
                    _restore_color(gid)
                    obj.update(update_data=True)
            dirty_gids.clear()

        def _isolate_pair(gid_a, gid_b):
            """Show colliding pair (red + green); hide all other geometry objects."""
            # Restore any previously colored objects before coloring new ones
            for gid in list(dirty_gids):
                if gid != gid_a and gid != gid_b:
                    _restore_color(gid)
                    gid_to_obj[gid].update(update_data=True)
                    dirty_gids.discard(gid)

            for gid in geometry_gids:
                obj = gid_to_obj[gid]
                if gid == gid_a:
                    obj.show = True
                    _set_color(obj, COLOR_A)
                    obj.update(update_data=True)
                    dirty_gids.add(gid)
                elif gid == gid_b:
                    obj.show = True
                    _set_color(obj, COLOR_B)
                    obj.update(update_data=True)
                    dirty_gids.add(gid)
                else:
                    obj.show = False

        def on_collision_selected(node):
            """Handle collision list item selection."""
            # Walk up to the top-level node (e.g. "Collision 3").
            top = node
            while top.parent and not top.parent.is_root:
                top = top.parent

            name = top.name
            if not name.startswith("Collision "):
                if active_pair[0] is not None:
                    _show_all()
                    active_pair[0] = None
                    viewer.renderer.update()
                return

            idx = int(name.split()[-1]) - 1
            if idx < 0 or idx >= len(collision_data):
                return

            c = collision_data[idx]

            # Toggle: clicking same pair again restores the view
            if active_pair[0] == idx:
                _show_all()
                active_pair[0] = None
                info_treeform.update_from_dict({})
            else:
                _isolate_pair(c["a_gid"], c["b_gid"])
                active_pair[0] = idx

                info_treeform.update_from_dict(
                    {
                        "Collision": {
                            "Element A": c["a_label"],
                            "Element B": c["b_label"],
                            "Penetrating points": str(c["count"]),
                        },
                    }
                )

            viewer.renderer.update()

        collision_treeform.action = on_collision_selected

        # ---- scene tree click: also update info panel -------------------------
        def on_scene_selected(form, node):
            element = node.attributes.get("element")
            if element:
                info = {
                    "Type": element.ifc_type,
                    "Name": element.name,
                    "GlobalId": element.global_id or "",
                }
                info.update(element.properties)
                info_treeform.update_from_dict(info)

            # Restore view when clicking the scene tree
            if active_pair[0] is not None:
                _show_all()
                active_pair[0] = None
                viewer.renderer.update()

        viewer.ui.sidebar.sceneform.action = on_scene_selected

        print(f"Showing {len(collision_data)} collision(s) in viewer.")
        viewer.show()

    def show_collision_pairs(
        self,
        tolerance: float = 1e-6,
        min_depth: float = 1e-4,
        element_types: list = None,
        skip_related: bool = True,
        show_points: bool = True,
        pointsize: int = 20,
    ):
        """Visualize all collision pairs at once, each pair in its own colour.

        Runs collision detection (if not already done), then opens
        compas_viewer with every colliding element coloured by its pair.
        Non-colliding subtrees are hidden. Penetration points are shown
        as a Pointcloud per pair in the matching colour.

        Elements appearing in multiple pairs take the colour of the first
        pair they appear in.

        Parameters
        ----------
        tolerance, min_depth, element_types, skip_related
            See :meth:`compute_collisions`.
        show_points : bool, optional
            If ``True`` (default), draw a Pointcloud per pair for the
            penetration samples.
        pointsize : int, optional
            Pixel size for penetration-point markers.
        """
        try:
            from compas_viewer import Viewer
        except ImportError:
            raise ImportError("The show_collision_pairs method requires compas_viewer to be installed.")

        import colorsys

        from compas.colors import Color
        from compas.geometry import Pointcloud

        if not self.interferences:
            print("Running collision detection...")
            n = self.compute_collisions(
                tolerance=tolerance,
                min_depth=min_depth,
                element_types=element_types,
                skip_related=skip_related,
            )
            print(f"Found {n} collisions.")

        edges = self.interferences
        if not edges:
            print("No collisions to visualize.")
            return

        # Distinct hues via golden-ratio rotation — neighbouring pair indices
        # land on far-apart hues so legend overlap is rare.
        GOLDEN = 0.6180339887498949
        pair_colors = []
        for i in range(len(edges)):
            r, g, b = colorsys.hsv_to_rgb((i * GOLDEN) % 1.0, 0.85, 0.95)
            pair_colors.append(Color(r, g, b))

        elem_color = {}  # global_id → first-pair color
        pair_points = []  # list of (Color, list[Point])
        for i, edge in enumerate(edges):
            a, b = self._edge_elements(edge)
            color = pair_colors[i]
            if a.global_id and a.global_id not in elem_color:
                elem_color[a.global_id] = color
            if b.global_id and b.global_id not in elem_color:
                elem_color[b.global_id] = color
            pts = self.graph.edge_attribute(edge, "penetrating_points") or []
            if pts:
                pair_points.append((color, pts))

        viewer = Viewer()
        viewer.ui.sidebar.show_objectsetting = False
        if self.unit:
            viewer.unit = self.unit

        # Mark ancestors of every colliding element — non-colliding subtrees
        # are skipped entirely; non-colliding ancestors remain as groups so
        # the parent-relative transformation chain stays intact.
        needed = set()

        def _mark(element):
            has_collision = element.global_id in elem_color
            for child in element.children:
                if _mark(child):
                    has_collision = True
            if has_collision and element.global_id:
                needed.add(element.global_id)
            return has_collision

        for node in self.tree.root.children:
            _mark(node.element)

        def _add_element(element, parent=None):
            if element.global_id not in needed:
                return
            label = f"[{element.ifc_type}] {element.name}"
            visual = element._visual_geometry
            color = elem_color.get(element.global_id)
            has_geometry = visual is not None and color is not None

            if has_geometry:
                style_kwargs = element._resolve_style() or {}
                obj = viewer.scene.add(
                    visual,
                    name=label,
                    parent=parent,
                    hide_coplanaredges=True,
                    **style_kwargs,
                )
                if hasattr(obj, "facecolors"):
                    obj.facecolors = [color] * len(obj.facecolors)
                else:
                    obj.facecolor = color
            else:
                obj = viewer.scene.add_group(name=label, parent=parent)

            obj.transformation = element.transformation
            obj.attributes["element"] = element

            for child in element.children:
                _add_element(child, parent=obj)

        for node in self.tree.root.children:
            _add_element(node.element)

        if show_points:
            for color, pts in pair_points:
                viewer.scene.add(Pointcloud(pts), pointcolor=color, pointsize=pointsize)

        print(f"Showing {len(edges)} collision pair(s) in viewer.")
        viewer.show()
