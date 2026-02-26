from typing import Optional
from typing import Type
from typing import Union

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation
from compas_model.elements import Element
from compas_model.elements import reset_computed
from compas_model.interactions import Contact

from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation


class GenericElement(Element):
    """A unified element representing any building component in an IFC model.

    This class extends ``compas_model.Element`` to bridge IFC entity data
    with the compas_model infrastructure. It provides a clean, minimal API
    for accessing element properties while keeping a reference to the
    underlying IFC entity for advanced access.

    All IFC product subclasses (IfcWall, IfcSlab, IfcBeam, etc.) as well as
    spatial containers (IfcSite, IfcBuilding, IfcBuildingStorey) are represented
    uniformly as ``GenericElement`` instances with different ``ifc_type`` values.

    Property setters are **bi-directional**: setting geometry, name, properties,
    or transformation on the element also updates the underlying IFC entity.

    Parameters
    ----------
    ifc_type : str, optional
        The IFC class name (e.g. "IfcWall", "IfcSlab", "IfcBuildingStorey").
    geometry : Brep | Mesh, optional
        The geometry of the element.
    transformation : Transformation, optional
        The local transformation relative to the parent element.
    name : str, optional
        The name of the element.

    """

    @property
    def __data__(self) -> dict:
        data = super().__data__
        data["ifc_type"] = self.ifc_type
        data["global_id"] = self._global_id
        data["properties"] = self._properties
        return data

    def __init__(
        self,
        ifc_type: str = "IfcGenericElementProxy",
        geometry: Optional[Union[Brep, Mesh]] = None,
        transformation: Optional[Transformation] = None,
        name: Optional[str] = None,
        **kwargs,
    ) -> None:
        # Must initialize before super().__init__ because Data.__init__
        # calls self.name = name which triggers the name setter.
        self._ifc_entity = None
        self._global_id = None
        self._properties = None
        self._style = None

        super().__init__(
            geometry=geometry,
            transformation=transformation,
            name=name,
            **kwargs,
        )
        self.ifc_type = ifc_type

    def __repr__(self) -> str:
        return f"<GenericElement {self.ifc_type} '{self.name}'>"

    def __str__(self) -> str:
        return f"<GenericElement {self.ifc_type} '{self.name}'>"

    # ==========================================================================
    # User-facing API (bi-directional: reads from IFC, writes back to IFC)
    # ==========================================================================

    @property
    def ifc_entity(self):
        """The underlying raw IFC entity (read-only escape hatch).

        Returns ``None`` for elements created programmatically without an IFC source.
        """
        return self._ifc_entity

    @property
    def global_id(self) -> Optional[str]:
        """The IFC GlobalId of the element."""
        if self._global_id is None and self._ifc_entity is not None:
            self._global_id = self._ifc_entity.GlobalId
        return self._global_id

    @global_id.setter
    def global_id(self, value: str) -> None:
        self._global_id = value

    @property
    def name(self):
        return super().name

    @name.setter
    def name(self, value):
        self._name = value
        # Sync to IFC
        if self._ifc_entity is not None and getattr(self, "model", None) is not None:
            self._ifc_entity.Name = value

    @property
    def properties(self) -> dict:
        """Unified properties of the element.

        Merges IFC schema attributes (Name, Description, ObjectType, etc.)
        and property sets (Pset_WallCommon, etc.) into a single flat dict.
        Lazy-loaded from the IFC entity on first access.
        """
        if self._properties is None:
            if self._ifc_entity is not None:
                self._properties = self._load_properties()
            else:
                self._properties = {}
        return self._properties

    @properties.setter
    def properties(self, value: dict) -> None:
        self._properties = value
        # Sync to IFC
        if self._ifc_entity is not None and getattr(self, "model", None) is not None and value:
            schema_attrs = {"Description", "ObjectType", "Tag", "PredefinedType"}
            psets = {k: v for k, v in value.items() if k not in schema_attrs and isinstance(v, dict)}
            if psets:
                self._ifc_entity.property_sets = psets
            for attr in schema_attrs:
                if attr in value:
                    setattr(self._ifc_entity, attr, value[attr])

    @property
    def style(self) -> dict:
        """Visual style attributes (color, transparency) from the IFC entity."""
        if self._style is None:
            if self._ifc_entity is not None:
                self._style = self._ifc_entity.style
            else:
                self._style = {}
        return self._style

    @style.setter
    def style(self, value: dict) -> None:
        self._style = value

    @property
    def is_spatial(self) -> bool:
        """Whether this element is a spatial container (site, building, storey, space)."""
        spatial_types = {"IfcSite", "IfcBuilding", "IfcBuildingStorey", "IfcSpace", "IfcFacility", "IfcFacilityPart"}
        return self.ifc_type in spatial_types

    @property
    def geometry(self):
        """The geometry of the element.

        Lazy-loaded from the underlying IFC entity on first access.
        Setting geometry also updates the IFC representation.
        """
        if self._geometry is None and self._ifc_entity is not None:
            try:
                geom = self._ifc_entity.geometry
            except AttributeError:
                # Not all IFC types have geometry (e.g. IfcSystem, IfcGroup)
                geom = None
            if geom is not None:
                self._geometry = geom
        return self._geometry

    @geometry.setter
    @reset_computed
    def geometry(self, geometry) -> None:
        self._geometry = geometry
        # Sync to IFC
        if self._ifc_entity is not None and getattr(self, "model", None) is not None and geometry is not None:
            self._ifc_entity.geometry = geometry

    @property
    def visual_geometry(self):
        """The tessellated visual geometry of the element.

        Produced by ifcopenshell's geometry iterator, suitable for display.
        Unlike ``geometry``, this always returns a viewer-compatible type
        (``TessellatedBrep`` or ``OCCBrep``), never a parametric shape.
        """
        if self._ifc_entity is not None:
            try:
                return self._ifc_entity.visual_geometry
            except AttributeError:
                return None
        return None

    @property
    def volume(self):
        """Volume of this element's geometry.

        Delegates to the underlying IFC entity's ``volume`` property,
        which tries the parametric geometry's ``volume()`` method first,
        then falls back to ``visual_geometry.volume`` (tessellated brep).

        Returns
        -------
        float or None
        """
        if self._ifc_entity is not None:
            return self._ifc_entity.volume
        return None

    @property
    def surface_area(self):
        """Surface area of this element's geometry.

        Delegates to the underlying IFC entity's ``surface_area`` property,
        which tries the parametric geometry first, then falls back to
        ``visual_geometry.surface_area`` (tessellated brep).

        Returns
        -------
        float or None
        """
        if self._ifc_entity is not None:
            return self._ifc_entity.surface_area
        return None

    @property
    def transformation(self):
        return self._transformation

    @transformation.setter
    @reset_computed
    def transformation(self, transformation) -> None:
        self._transformation = transformation
        # Sync to IFC
        if self._ifc_entity is not None and getattr(self, "model", None) is not None and transformation is not None:
            frame = Frame.from_transformation(transformation)
            self._ifc_entity.frame = frame

    # ==========================================================================
    # Internal helpers
    # ==========================================================================

    def _load_properties(self) -> dict:
        """Merge IFC schema attributes and property sets into a unified dict."""
        props = {}

        # IFC schema attributes (Name, Description, ObjectType, Tag, etc.)
        entity = self._ifc_entity
        for attr_name in ("Description", "ObjectType", "Tag", "PredefinedType"):
            val = getattr(entity, attr_name, None)
            if val is not None:
                props[attr_name] = val

        # Property sets (Pset_WallCommon, PSet_Revit_*, etc.)
        psets = entity.property_sets
        if psets:
            props.update(psets)

        return props

    # ==========================================================================
    # compas_model.Element abstract method implementations
    # ==========================================================================

    def compute_elementgeometry(self, include_features: bool = False):
        return self.geometry

    def compute_aabb(self, inflate: float = 1.0) -> Optional[Box]:
        geom = self.elementgeometry
        if geom is None:
            return None
        if hasattr(geom, "aabb"):
            return geom.aabb
        if isinstance(geom, Mesh):
            from compas.geometry import bounding_box

            pts = geom.vertices_attributes("xyz")
            bb = bounding_box(pts)
            return Box.from_bounding_box(bb)
        return None

    def compute_obb(self, inflate: float = 1.0) -> Optional[Box]:
        geom = self.elementgeometry
        if geom is None:
            return None
        if hasattr(geom, "obb"):
            return geom.obb
        return self.compute_aabb(inflate)

    def compute_collision_mesh(self, inflate: float = 1.0) -> Optional[Mesh]:
        geom = self.elementgeometry
        if geom is None:
            return None
        if isinstance(geom, Mesh):
            return geom
        if hasattr(geom, "to_tesselation") or hasattr(geom, "to_mesh"):
            try:
                return geom.to_tesselation()
            except Exception:
                pass
            try:
                return geom.to_mesh()
            except Exception:
                pass
        return None

    def compute_point(self) -> Optional[Point]:
        geom = self.elementgeometry
        if geom is None:
            return None
        if hasattr(geom, "centroid"):
            c = geom.centroid
            if isinstance(c, Point):
                return c
            return Point(*c)
        return None

    def compute_surface_mesh(self, meshsize_min=None, meshsize_max=None) -> Optional[Mesh]:
        return self.compute_collision_mesh()

    def compute_volumetric_mesh(self, meshsize_min=None, meshsize_max=None):
        return None

    def compute_contacts(
        self,
        other: "GenericElement",
        tolerance: float = 1e-6,
        minimum_area: float = 1e-2,
        contacttype: Type[Contact] = Contact,
    ) -> list:
        """Compute contacts between this element and another element.

        Extends the base implementation to handle ``TessellatedBrep`` geometry
        by converting it to ``Mesh`` before computing contacts.

        Parameters
        ----------
        other : GenericElement
            The other element.
        tolerance : float, optional
            Distance tolerance for coplanarity check.
        minimum_area : float, optional
            Minimum area of a valid contact polygon.
        contacttype : type, optional
            Contact class to instantiate.

        Returns
        -------
        list[Contact]

        """
        from compas_ifc.algorithms.contacts import fast_mesh_mesh_contacts
        from compas_ifc.brep.tessellatedbrep import TessellatedBrep
        from compas_model.algorithms.contacts import brep_brep_contacts

        a = self.modelgeometry
        b = other.modelgeometry
        if a is None or b is None:
            return []

        # Convert TessellatedBrep to Mesh for contact detection
        if isinstance(a, TessellatedBrep):
            a = a.to_mesh()
        if isinstance(b, TessellatedBrep):
            b = b.to_mesh()

        if isinstance(a, Mesh) and isinstance(b, Mesh):
            return fast_mesh_mesh_contacts(a, b, tolerance=tolerance, minimum_area=minimum_area, contacttype=contacttype)
        elif isinstance(a, Brep) and isinstance(b, Brep):
            return brep_brep_contacts(a, b, tolerance=tolerance, minimum_area=minimum_area, contacttype=contacttype)

        return []

    def compute_collisions(
        self,
        other: "GenericElement",
        tolerance: float = 1e-6,
    ) -> list:
        """Detect volumetric collision between this element and another.

        Uses ray-casting to find vertices of one mesh that lie inside the
        other.  Handles ``TessellatedBrep`` geometry by converting to
        ``Mesh`` first.

        Parameters
        ----------
        other : GenericElement
            The other element.
        tolerance : float, optional
            Numerical tolerance for the ray-triangle intersection test.

        Returns
        -------
        list[Point]
            Penetrating vertices (empty if no collision).

        """
        from compas_ifc.algorithms.collisions import fast_mesh_mesh_collision
        from compas_ifc.brep.tessellatedbrep import TessellatedBrep

        a = self.modelgeometry
        b = other.modelgeometry
        if a is None or b is None:
            return []

        # Convert TessellatedBrep to Mesh for collision detection
        if isinstance(a, TessellatedBrep):
            a = a.to_mesh()
        if isinstance(b, TessellatedBrep):
            b = b.to_mesh()

        if isinstance(a, Mesh) and isinstance(b, Mesh):
            return fast_mesh_mesh_collision(a, b, tolerance=tolerance)

        return []

    # ==========================================================================
    # Construction
    # ==========================================================================

    @classmethod
    def from_ifc_entity(cls, ifc_entity, file=None) -> "GenericElement":
        """Create a GenericElement from a raw IFC entity.

        This computes the **global** transformation from the IFC placement chain.
        The caller is responsible for converting it to a local (relative-to-parent)
        transformation when adding to the model tree.

        Parameters
        ----------
        ifc_entity : :class:`compas_ifc.entities.base.Base`
            The wrapped IFC entity.
        file : :class:`compas_ifc.file.IFCFile`, optional
            The IFC file (for geometry pre-loading).

        Returns
        -------
        GenericElement

        """
        element = cls(
            ifc_type=ifc_entity.is_a(),
            name=getattr(ifc_entity, "Name", None) or "",
        )
        element._ifc_entity = ifc_entity
        element._global_id = getattr(ifc_entity, "GlobalId", None)

        # Compute global transformation from IFC placement chain
        if hasattr(ifc_entity, "ObjectPlacement") and ifc_entity.ObjectPlacement:
            global_transform = IfcLocalPlacement_to_transformation(ifc_entity.ObjectPlacement)
            element._global_transform = global_transform
        else:
            element._global_transform = Transformation()

        return element
