"""Mixin providing element creation convenience methods for BuildingInformationModel."""

from __future__ import annotations

from compas.geometry import Transformation

from compas_ifc.element import GenericElement


class ElementFactoryMixin:
    """Mixin that adds element creation shortcuts to a Model subclass.

    Expects the host class to provide:
    - ``self.add_element(element, parent=...)`` — from compas_model.Model
    - ``self._file`` — :class:`IFCFile`
    - ``self.unit`` (settable)
    - ``self.name`` (settable)
    """

    def create_element(self, ifc_type="IfcBuildingElementProxy", parent=None, geometry=None, frame=None, transformation=None, properties=None, name=None):
        """Create a building element and add it to the model.

        The ``ifc_type`` argument accepts flexible input. If the value matches
        an IFC class (case-insensitive, with or without the ``Ifc`` prefix —
        ``"IfcWall"``, ``"Wall"``, ``"wall"`` are all equivalent), the element
        is created with that IFC class. If the value matches no known class,
        the element falls back to ``IfcBuildingElementProxy`` and the original
        string is stored as ``ObjectType`` so semantic identity is preserved.

        Parameters
        ----------
        ifc_type : str
            The IFC class name (e.g. ``"IfcWall"``, ``"Wall"``) or any custom
            string for non-standard products.
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

        canonical, custom_object_type = self._normalise_ifc_type(ifc_type)

        element = GenericElement(
            ifc_type=canonical,
            geometry=geometry,
            transformation=transformation,
            name=name,
        )

        merged_properties = dict(properties) if properties else {}
        if custom_object_type is not None:
            merged_properties.setdefault("ObjectType", custom_object_type)
        if merged_properties:
            element._properties = merged_properties

        self.add_element(element, parent=parent)
        return element

    def _normalise_ifc_type(self, ifc_type):
        """Resolve a user-supplied type string against the active IFC schema.

        Returns a tuple ``(canonical, custom_object_type)``. ``canonical`` is
        the matched IFC class name (e.g. ``"IfcWall"``). ``custom_object_type``
        is ``None`` when the match was direct, or the original string when the
        value did not map to any IFC class — in which case ``canonical`` is
        ``"IfcBuildingElementProxy"`` and the original string is preserved as
        ``ObjectType`` on the resulting entity.
        """
        if not isinstance(ifc_type, str) or not ifc_type:
            return "IfcBuildingElementProxy", None

        classes = self._file.classes
        # 1. exact match
        if ifc_type in classes:
            return ifc_type, None
        # 2. case-insensitive match
        lower_to_canonical = {c.lower(): c for c in classes}
        if ifc_type.lower() in lower_to_canonical:
            return lower_to_canonical[ifc_type.lower()], None
        # 3. prefix-stripped variants ("Wall" -> "IfcWall")
        if not ifc_type.lower().startswith("ifc"):
            prefixed = "ifc" + ifc_type.lower()
            if prefixed in lower_to_canonical:
                return lower_to_canonical[prefixed], None
        # 4. unknown -> proxy with the user string preserved as ObjectType
        return "IfcBuildingElementProxy", ifc_type

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
