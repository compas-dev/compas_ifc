"""Mixin providing IFC import/export tree-building functionality for BuildingInformationModel.

Groups all spatial hierarchy code: loading the IFC tree structure, rectifying
placements, and extracting/exporting subsets of the model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from compas.geometry import Frame
from compas.geometry import Transformation

from compas_ifc.element import GenericElement

if TYPE_CHECKING:
    from compas_ifc.bim import BuildingInformationModel


class TreeMixin:
    """Mixin that adds IFC import/export capabilities to a Model subclass.

    Expects the host class to provide:
    - ``self._file`` — :class:`IFCFile`
    - ``self._elements_by_global_id`` — dict of IFC GlobalId → GenericElement
    - ``self.add_element(element, parent=...)`` — from compas_model.Model
    - ``self._load_relationships_into_graph()`` — from InteractionMixin
    """

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

        # Pre-scan void/fill relationships for tree nesting
        self._void_map = {}  # host entity id -> list of opening entities
        self._fill_map = {}  # opening entity id -> list of filler entities
        self._fillers_to_skip = set()  # entity ids of fillers with void/fill path

        try:
            for rel in self._file.get_entities_by_type("IfcRelVoidsElement"):
                host_id = rel.RelatingBuildingElement.entity.id()
                opening = rel.RelatedOpeningElement
                self._void_map.setdefault(host_id, []).append(opening)
        except RuntimeError:
            pass

        try:
            for rel in self._file.get_entities_by_type("IfcRelFillsElement"):
                opening_id = rel.RelatingOpeningElement.entity.id()
                filler = rel.RelatedBuildingElement
                self._fill_map.setdefault(opening_id, []).append(filler)
                self._fillers_to_skip.add(filler.entity.id())
        except RuntimeError:
            pass

        # Track rectification stats and verbose logs
        self._rectified_count = 0
        self._rectify_verbose = rectify_verbose
        self._void_fill_log = []  # buffered void/fill chain messages
        self._rectify_log = []  # buffered rectification messages
        self._rectify_patterns = {}  # (elem_type, old_parent_type, new_parent_type) -> {"count": int, "example": str}

        # Recursively load children of the project
        self._load_children(
            ifc_project,
            parent_element=None,
            parent_global_transform=Transformation(),
            rectify_placements=rectify_placements,
        )

        if rectify_verbose and self._void_fill_log:
            print(f"Nested {len(self._void_fill_log)} void/fill chains into the spatial tree:")
            for msg in self._void_fill_log:
                print(f"  {msg}")

        if rectify_verbose and self._rectify_log:
            print(f"Rectified {self._rectified_count} IFC placements to align with spatial hierarchy:")
            for msg in self._rectify_log:
                print(f"  {msg}")
        elif rectify_placements and self._rectified_count > 0:
            print(f"Rectified {self._rectified_count} IFC placements to align with spatial hierarchy.")

        # Store public rectification stats: pattern frequencies and void/fill chain info
        self.rectification_stats = {
            "rectified_count": self._rectified_count,
            "void_fill_chains": len(self._void_fill_log),
            "patterns": {k: v for k, v in self._rectify_patterns.items()},
        }

        del self._rectified_count
        del self._rectify_verbose
        del self._void_fill_log
        del self._rectify_log
        del self._rectify_patterns
        del self._void_map
        del self._fill_map
        del self._fillers_to_skip

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
            # Skip fillers that will be injected under their opening
            if child_entity.entity.id() in self._fillers_to_skip:
                elem = GenericElement._from_ifc_entity(child_entity)
                if hasattr(elem, "_global_transform"):
                    del elem._global_transform
                continue

            element = GenericElement._from_ifc_entity(child_entity)

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

            # Inject void/fill children (opening -> filler) under this element
            self._inject_void_fill_children(element, global_transform, rectify_placements)

    def _inject_void_fill_children(self, host_element, host_global_transform, rectify_placements):
        """Inject opening and filler elements as tree children of their host.

        For each ``IfcRelVoidsElement`` that references the host, the opening
        element is added as a child of the host.  For each
        ``IfcRelFillsElement`` that references the opening, the filler
        (door/window) is added as a child of the opening.

        Parameters
        ----------
        host_element : GenericElement
            The element that may be voided (e.g. a wall).
        host_global_transform : Transformation
            The global transformation of the host element.
        rectify_placements : bool
            Whether to rewrite IFC placements in the file.

        """
        if not hasattr(host_element, "_ifc_entity") or host_element._ifc_entity is None:
            return

        host_id = host_element._ifc_entity.entity.id()
        openings = self._void_map.get(host_id)
        if not openings:
            return

        host_label = f"{host_element.ifc_type} '{host_element.name}'"

        for opening_entity in openings:
            opening_elem = GenericElement._from_ifc_entity(opening_entity)

            opening_global = getattr(opening_elem, "_global_transform", Transformation())
            opening_local = host_global_transform.inverse() * opening_global
            opening_elem.transformation = opening_local

            if rectify_placements and opening_elem._ifc_entity is not None:
                if hasattr(opening_elem._ifc_entity, "ObjectPlacement") and opening_elem._ifc_entity.ObjectPlacement:
                    self._rectify_ifc_placement(opening_elem, host_element, opening_local)

            if hasattr(opening_elem, "_global_transform"):
                del opening_elem._global_transform

            self.add_element(opening_elem, parent=host_element)

            # Add fillers (doors/windows) under this opening
            filler_labels = []
            fillers = self._fill_map.get(opening_entity.entity.id(), [])
            for filler_entity in fillers:
                filler_elem = GenericElement._from_ifc_entity(filler_entity)

                filler_global = getattr(filler_elem, "_global_transform", Transformation())
                filler_local = opening_global.inverse() * filler_global
                filler_elem.transformation = filler_local

                if rectify_placements and filler_elem._ifc_entity is not None:
                    if hasattr(filler_elem._ifc_entity, "ObjectPlacement") and filler_elem._ifc_entity.ObjectPlacement:
                        self._rectify_ifc_placement(filler_elem, opening_elem, filler_local)

                if hasattr(filler_elem, "_global_transform"):
                    del filler_elem._global_transform

                self.add_element(filler_elem, parent=opening_elem)
                filler_labels.append(f"{filler_elem.ifc_type} '{filler_elem.name}'")

            # Log the full chain: host -> opening [-> filler ...]
            opening_label = f"{opening_elem.ifc_type} '{opening_elem.name}'"
            chain = f"{host_label} -> {opening_label}"
            for fl in filler_labels:
                chain += f" -> {fl}"
            self._void_fill_log.append(chain)

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

        # Collect structured pattern data
        old_parent_type = self._placement_owner_type(current_parent_placement)
        new_parent_type = self._placement_owner_type(expected_parent_placement)
        pattern_key = (element.ifc_type, old_parent_type, new_parent_type)
        if hasattr(self, "_rectify_patterns"):
            entry = self._rectify_patterns.get(pattern_key)
            if entry is None:
                self._rectify_patterns[pattern_key] = {
                    "count": 1,
                    "example": f"{element.ifc_type} '{element.name}'",
                }
            else:
                entry["count"] += 1

        # Buffer verbose detail before rewriting
        if getattr(self, "_rectify_verbose", False):
            old_label = self._placement_owner_label(current_parent_placement)
            new_label = self._placement_owner_label(expected_parent_placement)
            elem_label = f"{element.ifc_type} '{element.name}'"
            self._rectify_log.append(f"{elem_label}: PlacementRelTo {old_label} -> {new_label}")

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

    @staticmethod
    def _placement_owner_type(placement):
        """Return the IFC type of the product that owns an IfcLocalPlacement.

        Parameters
        ----------
        placement : Base or None
            An ``IfcLocalPlacement`` entity.

        Returns
        -------
        str

        """
        if placement is None:
            return "<World>"

        raw = getattr(placement, "entity", None) or getattr(placement, "_entity", placement)
        try:
            places_object = raw.PlacesObject if hasattr(raw, "PlacesObject") else None
            if places_object:
                owners = list(places_object) if hasattr(places_object, "__iter__") else [places_object]
                if owners:
                    return owners[0].is_a()
        except Exception:
            pass
        return "<Unknown>"

    # ==========================================================================
    # IFC Export
    # ==========================================================================

    def export(self, path: str, elements):
        """Export selected elements to a new IFC file.

        Wraps :meth:`IFCFile.export` for convenience. The exported file
        includes spatial ancestor containers automatically.

        Parameters
        ----------
        path : str
            Output IFC file path.
        elements : list[GenericElement]
            Elements to export. Their underlying IFC entities are collected.

        """
        ifc_entities = []
        for e in elements if isinstance(elements, (list, tuple)) else [elements]:
            if hasattr(e, "_ifc_entity") and e._ifc_entity is not None:
                ifc_entities.append(e._ifc_entity)
            elif hasattr(e, "entity"):
                ifc_entities.append(e)
        self._file.export(path, ifc_entities)

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

        Non-spatial IFC relationships (connections, space boundaries) are
        preserved when both endpoints of the relationship are in the exported
        set. This ensures the interaction graph is maintained in the extracted
        model.

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
            Whether to export non-spatial relationships (connections, space
            boundaries) where both endpoints are in the exported
            set. Default True.

        Returns
        -------
        BuildingInformationModel
            A new standalone model containing only the extracted elements.

        """
        import os
        import tempfile

        from compas_ifc.bim import BuildingInformationModel

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
