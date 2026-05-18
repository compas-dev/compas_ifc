from typing import Generic
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import numpy as np

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import bounding_box
from compas.geometry import transform_points_numpy
from compas_model.elements import Element
from compas_model.elements import reset_computed
from compas_model.interactions import Contact

from compas_ifc.brep.tessellatedbrep import TessellatedBrep
from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation

# Generic over the underlying IFC entity wrapper type. At runtime ``T`` is
# erased; the parameterisation exists purely so that overloaded query and
# factory methods can return ``GenericElement[IfcWall]`` and have IDEs
# resolve ``element.ifc_entity`` to the precise IFC class. No upper bound
# because the stub-side ``IfcXxx`` classes form their own EXPRESS-schema
# hierarchy that does not include the runtime ``Base`` wrapper.
T = TypeVar("T")


class GenericElement(Generic[T], Element):
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
        self._ifc_entity: Optional[T] = None
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
    def global_id(self) -> Optional[str]:
        """The IFC GlobalId of the element."""
        if self._global_id is None and self._ifc_entity is not None:
            self._global_id = self._ifc_entity.GlobalId
        return self._global_id

    @global_id.setter
    def global_id(self, value: str) -> None:
        self._global_id = value

    @property
    def ifc_entity(self) -> Optional[T]:
        """The underlying IFC entity wrapper.

        Read-only accessor for the typed IFC entity. The parameterisation of
        :class:`GenericElement` flows through here so that, for example,
        ``model.create_wall().ifc_entity`` is statically known to be an
        ``IfcWall`` and exposes schema attributes like ``OverallHeight`` to
        the IDE.
        """
        return self._ifc_entity

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
    def _is_spatial(self) -> bool:
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
    def _visual_geometry(self):
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
    def axis(self):
        """The axis (centerline) representation of the element.

        Returns a ``Polyline`` for elements that have an axis representation
        (typically walls, beams, columns). Returns ``None`` otherwise.
        """
        if self._ifc_entity is not None:
            try:
                return self._ifc_entity.axis
            except AttributeError:
                return None
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

    def _to_dict(self) -> dict:
        """Return a dictionary representation of the underlying IFC entity attributes.

        Delegates to the IFC entity's ``to_dict()`` method which returns
        all IFC schema attributes as a nested dictionary.
        """
        if self._ifc_entity is not None:
            return self._ifc_entity.to_dict()
        return {"ifc_type": self.ifc_type, "name": self.name}

    def show(self):
        """Show this element and its children in compas_viewer."""
        self.model.show(elements=self)

    # ==========================================================================
    # Internal helpers
    # ==========================================================================

    def _resolve_style(self) -> dict:
        """Lazy-load and return visual style attributes (color, transparency) from the IFC entity."""
        if self._style is None:
            if self._ifc_entity is not None:
                self._style = self._ifc_entity.style
            else:
                self._style = {}
        return self._style

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
        # Extrusion.transform leaves profile points local, so go through the
        # tessellated visual_geometry rather than self.elementgeometry.
        verts, _ = self._world_triangles()
        if verts is None or len(verts) == 0:
            return None
        return Box.from_bounding_box(bounding_box(verts))

    def compute_obb(self, inflate: float = 1.0) -> Optional[Box]:
        from compas.geometry import oriented_bounding_box_numpy

        verts, _ = self._world_triangles()
        if verts is None or len(verts) == 0:
            return None
        return Box.from_bounding_box(oriented_bounding_box_numpy(verts))

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

    def _world_triangles(self) -> tuple:
        """Return cached ``(vertices, triangle_indices)`` numpy arrays in world coords.

        ``vertices`` has shape ``(V, 3)``; ``triangle_indices`` has shape ``(F, 3)``.

        Cache keyed on the identity of ``self.modeltransformation``. Invalidated
        because ``reset_computed`` (in ``compas_model``) clears the underlying
        ``_modeltransformation`` to None whenever transformation/geometry change,
        and the next access lazily produces a fresh ``Transformation`` instance
        that fails the ``is``-identity check here.
        """
        xform = self.modeltransformation
        cache = getattr(self, "_world_triangles_cache", None)
        if cache is not None and cache[0] is xform:
            return cache[1], cache[2]

        vg = self._visual_geometry
        if vg is None:
            self._world_triangles_cache = (xform, None, None)
            return None, None

        if isinstance(vg, TessellatedBrep):
            verts_local = np.asarray(vg.vertices, dtype=np.float64)
            tris = np.asarray(vg.faces, dtype=np.int64)
        elif hasattr(vg, "to_mesh"):
            from compas_ifc.algorithms.collisions import _mesh_to_numpy

            verts_local, tris = _mesh_to_numpy(vg.to_mesh())
        else:
            self._world_triangles_cache = (xform, None, None)
            return None, None

        if xform is not None and len(verts_local) > 0:
            verts_world = transform_points_numpy(verts_local, xform)
        else:
            # Copy so the cache doesn't alias the source TessellatedBrep array.
            verts_world = verts_local.copy()

        self._world_triangles_cache = (xform, verts_world, tris)
        self._world_mesh_cache = None
        return verts_world, tris

    def _world_mesh(self) -> Optional[Mesh]:
        """Return a cached world-coord ``Mesh`` for callers that need the compas Mesh API.

        Prefer :meth:`_world_triangles` directly for numerical work.
        """
        verts, tris = self._world_triangles()
        if verts is None:
            return None
        cached = getattr(self, "_world_mesh_cache", None)
        if cached is not None:
            return cached
        mesh = Mesh.from_vertices_and_faces(verts.tolist(), tris.tolist())
        self._world_mesh_cache = mesh
        return mesh

    def compute_contacts(
        self,
        other: "GenericElement",
        tolerance: float = 1e-6,
        minimum_area: float = 1e-2,
        contacttype: Type[Contact] = Contact,
    ) -> list:
        """Compute contacts between this element and another element.

        Operates on world-coord meshes derived from the tessellated
        ``visual_geometry`` (see :meth:`_world_mesh`).

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

        a = self._world_mesh()
        b = other._world_mesh()
        if a is None or b is None:
            return []
        return fast_mesh_mesh_contacts(a, b, tolerance=tolerance, minimum_area=minimum_area, contacttype=contacttype)

    def compute_collisions(
        self,
        other: "GenericElement",
        tolerance: float = 1e-6,
    ) -> list:
        """Detect volumetric collision between this element and another.

        Operates on world-coord meshes derived from the tessellated
        ``visual_geometry`` (see :meth:`_world_mesh`).

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
        from compas_ifc.algorithms.collisions import fast_mesh_mesh_collision_numpy

        verts_a, tris_a = self._world_triangles()
        verts_b, tris_b = other._world_triangles()
        if verts_a is None or verts_b is None:
            return []
        return fast_mesh_mesh_collision_numpy(verts_a, tris_a, verts_b, tris_b, tolerance=tolerance)

    # ==========================================================================
    # Construction
    # ==========================================================================

    @classmethod
    def _from_ifc_entity(cls, ifc_entity) -> "GenericElement":
        """Create a GenericElement from a raw IFC entity.

        This computes the **global** transformation from the IFC placement chain.
        The caller is responsible for converting it to a local (relative-to-parent)
        transformation when adding to the model tree.

        Parameters
        ----------
        ifc_entity : :class:`compas_ifc.entities.base.Base`
            The wrapped IFC entity.

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
