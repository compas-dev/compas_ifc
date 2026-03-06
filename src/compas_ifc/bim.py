from typing import Optional

from compas_model.models import Model

from compas_ifc.element import GenericElement
from compas_ifc.factory import ElementFactoryMixin
from compas_ifc.file import IFCFile
from compas_ifc.interactions import InteractionMixin
from compas_ifc.tree import TreeMixin


class BuildingInformationModel(ElementFactoryMixin, InteractionMixin, TreeMixin, Model):
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

        # Validation specifications (opt-in enforcement)
        self.specifications = []

        # Load spatial hierarchy if opening an existing file
        if filepath:
            self._load_from_ifc(rectify_placements=rectify_placements, rectify_verbose=rectify_verbose)

    # ==========================================================================
    # IFC entity creation — conversion functions call model._create()
    # ==========================================================================

    def _create(self, cls=None, parent=None, geometry=None, frame=None, properties=None, **kwargs):
        """Create an IFC entity. Delegates to IFCFile.create().

        This method satisfies the protocol expected by all conversion functions
        (representation.py, frame.py, pset.py, mesh.py, shapes.py, brep.py).
        """
        return self._file._create(cls=cls, parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def _create_value(self, value):
        """Create an IfcValue from a Python scalar. Delegates to IFCFile."""
        return self._file._create_value(value)

    # ==========================================================================
    # User-facing properties
    # ==========================================================================

    @property
    def project(self):
        """The underlying IfcProject entity (read-only escape hatch).

        Returns the Base-wrapped ``IfcProject`` entity, providing access to
        project-level attributes (``Name``, ``Description``, ``sites``,
        ``buildings``, ``contexts``, ``units``, ``north``, ``frame``, etc.).

        Returns ``None`` if no IfcProject exists in the file.
        """
        projects = self._file.get_entities_by_type("IfcProject")
        return projects[0] if projects else None

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
        """Find all elements of a given IFC type (e.g. "IfcWall").

        Supports IFC class hierarchy matching: querying ``"IfcProduct"`` will
        match ``IfcWall``, ``IfcBeam``, ``IfcColumn``, etc.
        """
        results = []
        for e in self.elements():
            if e.ifc_type == ifc_type:
                results.append(e)
            elif e._ifc_entity is not None and e._ifc_entity.is_a(ifc_type):
                results.append(e)
        return results

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
        return [e for e in self.elements() if not e._is_spatial]

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

        ifc_entity = self._file._create(cls=element.ifc_type, parent=ifc_parent, **kwargs)
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

        # Enforce validation specifications if any are active
        if self.specifications:
            self._enforce_specifications(element)

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

    # ==========================================================================
    # Validation
    # ==========================================================================

    def validate(self, specifications=None):
        """Validate all elements against information requirements.

        Parameters
        ----------
        specifications : list[:class:`~compas_ifc.validation.Specification`], optional
            Specifications to check. If ``None``, uses ``self.specifications``.

        Returns
        -------
        list[:class:`~compas_ifc.validation.ValidationResult`]
            One result per (element, applicable specification) pair.

        """
        from compas_ifc.validation import validate_model

        specs = specifications if specifications is not None else self.specifications
        return validate_model(self, specs)

    def _enforce_specifications(self, element):
        """Check an element against active specifications, raise on failure.

        Called automatically from ``add_element`` when ``self.specifications``
        is non-empty.

        Raises
        ------
        ValueError
            If the element fails any applicable specification.

        """
        from compas_ifc.validation import validate_element

        results = validate_element(element, self.specifications)
        failures = [r for r in results if r.status == "fail"]
        if failures:
            msgs = []
            for f in failures:
                parts = []
                if f.missing_psets:
                    parts.append(f"missing psets: {f.missing_psets}")
                if f.property_errors:
                    parts.append(f"property errors: {f.property_errors}")
                msgs.append(f"[{f.specification}] {'; '.join(parts)}")
            raise ValueError(f"Element '{element.name}' ({element.ifc_type}) failed validation: {' | '.join(msgs)}")

    # ==========================================================================
    # IFC Export
    # ==========================================================================

    def save(self, path: str):
        """Save the IFC file to disk.

        Since the model is a bi-directional front-end, the IFC file is always
        in sync with the model tree. This simply writes the file.
        """
        self._file.save(path)

    # ==========================================================================
    # Display
    # ==========================================================================

    def show(self, elements=None):
        """Show the model (or specific elements and their children) in compas_viewer.

        Parameters
        ----------
        elements : :class:`GenericElement` or list[:class:`GenericElement`], optional
            One or more elements to show. Each element and its children are
            included. If ``None``, the entire model is shown.

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

        def _add_element(elem, parent=None):
            label = f"[{elem.ifc_type}] {elem.name}"
            obj = None

            visual = elem._visual_geometry
            skip_visual = elem.ifc_type in ("IfcSpace", "IfcOpeningElement")
            if visual is not None and not skip_visual:
                style_kwargs = elem._resolve_style() or {}
                obj = viewer.scene.add(
                    visual,
                    name=label,
                    parent=parent,
                    hide_coplanaredges=True,
                    **style_kwargs,
                )
            else:
                obj = viewer.scene.add_group(name=label, parent=parent)

            obj.transformation = elem.transformation
            obj.attributes["element"] = elem

            for child in elem.children:
                _add_element(child, parent=obj)

        if elements is not None:
            if not isinstance(elements, (list, tuple)):
                elements = [elements]
            for elem in elements:
                _add_element(elem)
        else:
            for node in self.tree.root.children:
                _add_element(node.element)

        treeform = Treeform()
        viewer.ui.sidebar.add(treeform)

        def update_treeform(form, node):
            elem = node.attributes.get("element")
            if elem:
                info = {
                    "Type": elem.ifc_type,
                    "Name": elem.name,
                    "GlobalId": elem.global_id or "",
                }
                info.update(elem.properties)
                treeform.update_from_dict(info)

        viewer.ui.sidebar.sceneform.action = update_treeform
        viewer.show()

