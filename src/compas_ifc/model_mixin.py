"""Mixin providing compas_model lifecycle overrides for BuildingInformationModel.

Groups the add_element / remove_element overrides that keep the compas_model
tree/graph in sync with the underlying IFC file, together with the IFC
placement helpers they depend on.
"""

from __future__ import annotations

from compas.geometry import Frame

from compas_ifc.element import GenericElement


class ModelMixin:
    """Mixin that overrides compas_model element lifecycle for IFC sync.

    Expects the host class to provide:
    - ``self._file`` — :class:`IFCFile`
    - ``self._elements_by_global_id`` — dict of IFC GlobalId → GenericElement
    - ``self.specifications`` — list of active validation specs
    - ``self._enforce_specifications(element)`` — from BuildingInformationModel
    """

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
    # IFC placement helpers
    # ==========================================================================

    def _resolve_ifc_parent(self, parent_element):
        """Return the IFC Base entity for a parent GenericElement.

        If parent is None, defaults to the IfcProject.
        """
        if parent_element is None:
            return self._file.default_project

        if parent_element._ifc_entity is not None:
            return parent_element._ifc_entity

        raise ValueError(f"Parent element '{parent_element.name}' has no IFC entity. Add spatial parents before their children.")

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
