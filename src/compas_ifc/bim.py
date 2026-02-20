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
    name : str, optional
        Name of the model.

    User-facing attributes
    ----------------------
    schema_name : str
        The name of the IFC schema (e.g. "IFC4", "IFC2X3").
    unit : str
        The length unit of the model ("mm", "cm", or "m").
    sites : list[GenericElement]
        All IfcSite elements.
    buildings : list[GenericElement]
        All IfcBuilding elements.
    storeys : list[GenericElement]
        All IfcBuildingStorey elements.
    building_elements : list[GenericElement]
        All non-spatial elements (walls, slabs, etc.).

    """

    def __init__(
        self,
        filepath: str = None,
        schema: str = "IFC4",
        use_occ: bool = False,
        load_geometries: bool = True,
        name: str = None,
        **kwargs,
    ) -> None:
        super().__init__(name=name, **kwargs)

        # IFC file wrapper — uses the old Model as owner (pass None, we handle it)
        self._file = IFCFile(
            None,
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
            self._load_from_ifc()

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
        """All IfcSite elements at the top level of the tree."""
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
    # IFC Import
    # ==========================================================================

    def _load_from_ifc(self):
        """Load the IFC file into the model tree with rectified transformations.

        This walks the IFC spatial hierarchy (IfcProject → IfcSite → IfcBuilding →
        IfcBuildingStorey → elements), creates GenericElement instances, and adds
        them to the model tree. IfcProject is absorbed into the BuildingModel itself.

        Transformations are rectified: each element's local transform is computed
        relative to its spatial parent, regardless of where the IFC placement chain
        originally pointed.
        """
        projects = self._file.get_entities_by_type("IfcProject")
        if not projects:
            return

        ifc_project = projects[0]

        # Store project-level info on the model
        self.name = getattr(ifc_project, "Name", None) or self.name

        # Recursively load children of the project
        self._load_children(ifc_project, parent_element=None, parent_global_transform=Transformation())

    def _load_children(self, ifc_entity, parent_element, parent_global_transform):
        """Recursively load IFC children into the model tree.

        Parameters
        ----------
        ifc_entity : Base
            The IFC entity whose children to load.
        parent_element : GenericElement or None
            The parent element in the model tree (None for top-level under root).
        parent_global_transform : Transformation
            The global transformation of the parent, used for rectification.

        """
        for child_entity in ifc_entity.children:
            element = GenericElement.from_ifc_entity(child_entity, file=self._file)

            # Rectify: compute local transform relative to spatial parent
            global_transform = getattr(element, "_global_transform", Transformation())
            local_transform = parent_global_transform.inverse() * global_transform
            element.transformation = local_transform

            # Clean up temporary attribute
            if hasattr(element, "_global_transform"):
                del element._global_transform

            # Add to model (tree + graph)
            self.add_element(element, parent=parent_element)

            # Index by GlobalId
            if element.global_id:
                self._elements_by_global_id[element.global_id] = element

            # Recurse into children
            self._load_children(child_entity, element, global_transform)

    # ==========================================================================
    # IFC Export
    # ==========================================================================

    def save(self, path: str):
        """Save the current IFC file to disk.

        For models loaded from IFC, this saves the underlying file directly.
        For models built programmatically, use ``to_ifc()`` instead.
        """
        self._file.save(path)

    def to_ifc(self, path: str, schema: str = None):
        """Export the model tree to a new IFC file.

        TODO: Implement full export pipeline (tree → IFC entities → file).
        For now, delegates to save() for models loaded from IFC.
        """
        # TODO: Full export pipeline
        self.save(path)

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
        Each element's geometry is placed using the transformation from the
        IFC placement chain (already in global coordinates).
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
