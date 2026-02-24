"""
ClippedExtrusion geometry type for parametric IFC representation.

Maps to ``IfcBooleanClippingResult`` chains where the leaf operand
is an ``IfcExtrudedAreaSolid`` and each clipping operand is an
``IfcHalfSpaceSolid``.
"""

from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Plane

from compas_ifc.representations.extrusion import Extrusion


class ClippedExtrusion(Geometry):
    """An extrusion clipped by one or more half-space planes.

    Directly corresponds to a chain of ``IfcBooleanClippingResult``
    entities with ``Operator=DIFFERENCE``.  The leaf ``FirstOperand``
    is an ``IfcExtrudedAreaSolid`` and each ``SecondOperand`` is an
    ``IfcHalfSpaceSolid``.

    Preserves all parametric data: the base extrusion profile,
    direction, depth and frame, plus every clipping plane with its
    agreement flag.

    Parameters
    ----------
    extrusion : :class:`Extrusion`
        The base extrusion being clipped.
    clipping_planes : list[tuple[:class:`Plane`, bool]]
        Each entry is ``(plane, agreement_flag)``.
        *plane* defines the clipping surface.
        *agreement_flag* ``True`` means the solid is on the same
        side as the plane normal; ``False`` means the opposite side.
    name : str, optional
        Optional name for the geometry.

    Attributes
    ----------
    extrusion : :class:`Extrusion`
        The base extrusion.
    clipping_planes : list[tuple[:class:`Plane`, bool]]
        Clipping planes with agreement flags.
    name : str or None
        Optional name.
    """

    def __init__(self, extrusion, clipping_planes, name=None):
        super().__init__()
        self.extrusion = extrusion
        self.clipping_planes = list(clipping_planes)
        self.name = name

    def __repr__(self):
        ext = self.extrusion
        from compas.geometry import Circle, Polygon

        if isinstance(ext.profile, tuple):
            n_voids = len(ext.profile[1])
            ptype = f"ProfileWithVoids({n_voids} voids)"
        elif isinstance(ext.profile, Circle):
            ptype = f"Circle(r={ext.profile.radius:.3f})"
        elif isinstance(ext.profile, Polygon):
            ptype = f"Polygon({len(ext.profile.points)})"
        else:
            ptype = type(ext.profile).__name__
        return f"<ClippedExtrusion profile={ptype} depth={ext.depth:.3f}, {len(self.clipping_planes)} clips>"

    # ------------------------------------------------------------------
    # Geometry interface
    # ------------------------------------------------------------------

    def transform(self, transformation):
        """Transform the clipped extrusion.

        Transforms the base extrusion frame and every clipping plane.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.
        """
        self.extrusion.transform(transformation)
        new_planes = []
        for plane, agreement in self.clipping_planes:
            plane_copy = plane.copy()
            plane_copy.transform(transformation)
            new_planes.append((plane_copy, agreement))
        self.clipping_planes = new_planes

    def copy(self):
        """Return a deep copy of this clipped extrusion.

        Returns
        -------
        :class:`ClippedExtrusion`
        """
        return ClippedExtrusion(
            extrusion=self.extrusion.copy(),
            clipping_planes=[(p.copy(), a) for p, a in self.clipping_planes],
            name=self.name,
        )

    # ------------------------------------------------------------------
    # Mesh generation
    # ------------------------------------------------------------------

    def to_vertices_and_faces(self, n=16):
        """Discretise the clipped extrusion into vertices and faces.

        .. note::

            This is an **approximate** discretisation that returns the
            unclipped base extrusion.  Exact clipped geometry would
            require boolean operations via OpenCascade.

        Parameters
        ----------
        n : int
            Number of sample points for circular profiles.

        Returns
        -------
        tuple[list[list[float]], list[list[int]]]
            ``(vertices, faces)`` suitable for
            :meth:`Mesh.from_vertices_and_faces`.
        """
        return self.extrusion.to_vertices_and_faces(n=n)

    def to_mesh(self, n=16):
        """Convert the clipped extrusion to a :class:`compas.datastructures.Mesh`.

        .. note::

            Returns the unclipped base extrusion mesh.  See
            :meth:`to_vertices_and_faces` for details.

        Parameters
        ----------
        n : int
            Number of sample points for circular profiles.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
        """
        return self.extrusion.to_mesh(n=n)
