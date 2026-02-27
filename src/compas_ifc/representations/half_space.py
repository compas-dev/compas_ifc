"""
HalfSpace geometry type for parametric IFC representation.

Maps to ``IfcHalfSpaceSolid`` — an infinite solid on one side of
a plane, used as a boolean operand for clipping or difference
operations.
"""

from compas.geometry import Geometry


class HalfSpace(Geometry):
    """An infinite half-space solid defined by a plane and agreement flag.

    Directly corresponds to ``IfcHalfSpaceSolid``.  Used as an operand
    inside :class:`BooleanResult` (or :class:`ClippedExtrusion`) to
    represent infinite clipping cuts.

    Parameters
    ----------
    plane : :class:`Plane`
        The dividing plane surface.
    agreement_flag : bool
        ``True`` means the solid is on the same side as the plane
        normal; ``False`` means the opposite side.
    name : str, optional
        Optional name for the geometry.

    Attributes
    ----------
    plane : :class:`Plane`
        The dividing plane.
    agreement_flag : bool
        Which side of the plane is solid.
    name : str or None
        Optional name.
    """

    def __init__(self, plane, agreement_flag, name=None):
        super().__init__()
        self.plane = plane
        self.agreement_flag = agreement_flag
        self.name = name

    def __repr__(self):
        return f"<HalfSpace point={self.plane.point}, normal={self.plane.normal}, agree={self.agreement_flag}>"

    # ------------------------------------------------------------------
    # Geometry interface
    # ------------------------------------------------------------------

    def transform(self, transformation):
        """Transform the half-space by transforming its plane.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.
        """
        self.plane.transform(transformation)

    def copy(self):
        """Return a deep copy of this half-space.

        Returns
        -------
        :class:`HalfSpace`
        """
        return HalfSpace(
            plane=self.plane.copy(),
            agreement_flag=self.agreement_flag,
            name=self.name,
        )
