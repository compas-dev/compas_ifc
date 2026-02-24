from typing import TYPE_CHECKING

from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation
from compas_ifc.conversions.frame import assign_entity_frame
from compas_ifc.conversions.representation import assign_body_representation
from compas.geometry import Frame

if TYPE_CHECKING:
    from compas_ifc.entities.generated.IFC4 import IfcProduct
else:
    IfcProduct = object


class IfcProduct(IfcProduct):
    """Extension class for :class:`IfcProduct`.

    Attributes
    ----------
    style : dict
        The style of the product.
    visual_geometry : :class:`compas_ifc.brep.TessellatedBrep` or :class:`compas_occ.brep.OCCBrep`
        The evaluated visual geometry of the product, produced by ifcopenshell.geom.iterator.
        Suitable for display but does NOT preserve parametric information.
    geometry : :class:`~compas.geometry.Geometry` or :class:`~compas.datastructures.Mesh` or None
        Parsed COMPAS geometry from the IFC body representation.
        Returns Box, Sphere, Cone, Cylinder, Extrusion, Mesh, etc.
        Falls back to visual_geometry if parsing is not available.
        Setter writes COMPAS geometry to the IFC file as a body representation.
    axis : :class:`~compas.geometry.Polyline` or None
        The axis (centerline) representation of the product, parsed from the
        ``"Axis"`` representation.  Common for walls, beams, and columns.
    frame : :class:`compas.geometry.Frame`
        The frame of the product.
    """

    @property
    def style(self):
        return self.file.get_preloaded_style(self)

    @property
    def visual_geometry(self):
        """The evaluated visual geometry of the product.

        Produced by ifcopenshell.geom.iterator during ``load_geometries()``.
        Suitable for display but does NOT preserve parametric information
        (extrusion profiles, boolean trees, instancing relationships, etc.).

        Returns
        -------
        :class:`compas_ifc.brep.TessellatedBrep` or :class:`compas_occ.brep.OCCBrep` or None
        """
        if not getattr(self, "_visual_geometry", None):
            self._visual_geometry = self.file.get_preloaded_geometry(self)
            if self._visual_geometry:
                self._visual_geometry.name = self.Name
                if self.file.use_occ:
                    # NOTE: When using OCC, the geometry is pre-transformed to the frame of the entity.
                    # We need to re-transform the geometry back to its original location.
                    # This is not necessary when using TessellatedBrep.
                    T = self.frame.to_transformation()
                    self._visual_geometry.transform(T.inverse())
        return self._visual_geometry

    @visual_geometry.setter
    def visual_geometry(self, value):
        self._visual_geometry = value

    @property
    def geometry(self):
        """Parsed COMPAS geometry from the IFC body representation.

        Attempts to parse the IFC representation graph into native COMPAS
        geometry (Box, Sphere, Cone, Cylinder, Mesh, Extrusion).
        Falls back to the evaluated ``visual_geometry`` if the representation
        type is not yet supported by the parser.

        Returns
        -------
        :class:`~compas.geometry.Geometry` | :class:`~compas.datastructures.Mesh` | None
        """
        if not getattr(self, "_parsed_geometry", None):
            from compas_ifc.conversions.reading import read_body_representation

            try:
                parsed = read_body_representation(self)
            except Exception:
                parsed = None

            if parsed is not None:
                self._parsed_geometry = parsed
            else:
                self._parsed_geometry = self.visual_geometry

        return self._parsed_geometry

    @geometry.setter
    def geometry(self, geometry):
        self._parsed_geometry = geometry
        self._visual_geometry = None  # clear visual cache
        assign_body_representation(self, geometry)
        # TODO: delete existing representation

    @property
    def volume(self):
        """Volume of this element's geometry.

        Tries the parametric geometry's ``volume()`` method first.
        Falls back to ``visual_geometry.volume`` for types that
        cannot compute volume parametrically (e.g. ClippedExtrusion,
        BooleanResult).

        Returns
        -------
        float or None
        """
        geom = self.geometry
        if geom is not None:
            v = getattr(geom, "volume", None)
            if v is not None:
                if callable(v):
                    v = v()
                if v is not None:
                    return v
        # Fallback to tessellated geometry
        vg = self.visual_geometry
        if vg is not None:
            v = getattr(vg, "volume", None)
            if v is not None:
                return v
        return None

    @property
    def surface_area(self):
        """Surface area of this element's geometry.

        Tries the parametric geometry's ``surface_area()`` method first.
        Falls back to ``visual_geometry.surface_area`` for types that
        cannot compute surface area parametrically.

        Returns
        -------
        float or None
        """
        geom = self.geometry
        if geom is not None:
            sa = getattr(geom, "surface_area", None)
            if sa is None:
                # COMPAS shapes use `.area` instead of `.surface_area`
                sa = getattr(geom, "area", None)
            if sa is not None:
                if callable(sa):
                    sa = sa()
                if sa is not None:
                    return sa
        # Fallback to tessellated geometry
        vg = self.visual_geometry
        if vg is not None:
            sa = getattr(vg, "surface_area", None)
            if sa is not None:
                return sa
        return None

    @property
    def axis(self):
        """The axis (centerline) representation of the product.

        Parses the ``"Axis"`` representation into a :class:`~compas.geometry.Polyline`.
        Common for linear elements such as walls, beams, and columns.

        Returns
        -------
        :class:`~compas.geometry.Polyline` | None
        """
        if not getattr(self, "_axis", None):
            from compas_ifc.conversions.reading import read_axis_representation

            try:
                self._axis = read_axis_representation(self)
            except Exception:
                self._axis = None

        return self._axis

    @axis.setter
    def axis(self, polyline):
        self._axis = polyline
        from compas_ifc.conversions.representation import assign_axis_representation

        assign_axis_representation(self, polyline)

    @property
    def frame(self):
        if not getattr(self, "_frame", None):
            if self.ObjectPlacement:
                transformation = IfcLocalPlacement_to_transformation(self.ObjectPlacement)
                self._frame = Frame.from_transformation(transformation)
            else:
                self._frame = None
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame
        # TODO: consider parent frame
        assign_entity_frame(self, frame)
