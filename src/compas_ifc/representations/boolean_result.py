"""
BooleanResult geometry type for parametric IFC representation.

Maps to ``IfcBooleanResult`` — a CSG boolean operation on two geometry
operands.  Supports ``UNION``, ``INTERSECTION``, and ``DIFFERENCE``
operators with arbitrary operand types (extrusions, CSG primitives,
half-spaces, or nested boolean results).
"""

from compas.geometry import Geometry


class BooleanResult(Geometry):
    """A CSG boolean operation on two geometry operands.

    Directly corresponds to ``IfcBooleanResult``.  Each operand can be
    any COMPAS geometry type — an :class:`Extrusion`, a shape primitive
    (``Box``, ``Sphere``, etc.), a :class:`HalfSpace`, another
    :class:`BooleanResult`, or any other geometry that the reading
    pipeline produces.

    This is a recursive structure: complex CSG trees are represented
    as nested ``BooleanResult`` instances.

    Parameters
    ----------
    operator : str
        The boolean operator: ``"UNION"``, ``"INTERSECTION"``, or
        ``"DIFFERENCE"``.
    first_operand : :class:`~compas.geometry.Geometry`
        The first operand.
    second_operand : :class:`~compas.geometry.Geometry`
        The second operand.
    name : str, optional
        Optional name for the geometry.

    Attributes
    ----------
    operator : str
        The boolean operator.
    first_operand : :class:`~compas.geometry.Geometry`
        The first operand.
    second_operand : :class:`~compas.geometry.Geometry`
        The second operand.
    name : str or None
        Optional name.
    """

    VALID_OPERATORS = ("UNION", "INTERSECTION", "DIFFERENCE")

    def __init__(self, operator, first_operand, second_operand, name=None):
        super().__init__()
        if operator not in self.VALID_OPERATORS:
            raise ValueError(f"Invalid boolean operator: {operator!r}. Must be one of {self.VALID_OPERATORS}")
        self.operator = operator
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.name = name

    def __repr__(self):
        return f"<BooleanResult {self.operator} first={type(self.first_operand).__name__} second={type(self.second_operand).__name__}>"

    # ------------------------------------------------------------------
    # Geometry interface
    # ------------------------------------------------------------------

    def transform(self, transformation):
        """Transform the boolean result by transforming both operands.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.
        """
        self.first_operand.transform(transformation)
        self.second_operand.transform(transformation)

    def copy(self):
        """Return a deep copy of this boolean result.

        Returns
        -------
        :class:`BooleanResult`
        """
        return BooleanResult(
            operator=self.operator,
            first_operand=self.first_operand.copy(),
            second_operand=self.second_operand.copy(),
            name=self.name,
        )

    # ------------------------------------------------------------------
    # Geometric properties
    # ------------------------------------------------------------------

    def volume(self):
        """Volume of the boolean result.

        .. note::

            Returns ``None`` because exact volume requires CSG boolean
            operations that cannot be computed parametrically.
            Use ``element.visual_geometry.volume`` for accurate results
            via the ifcopenshell tessellated geometry, or use the
            element-level ``element.volume`` property which falls back
            to the tessellated geometry automatically.
        """
        return None

    def surface_area(self):
        """Surface area of the boolean result.

        .. note::

            Returns ``None`` because exact surface area requires CSG
            boolean operations.  See :meth:`volume` for how to obtain
            accurate results.
        """
        return None

    # ------------------------------------------------------------------
    # Tree traversal helpers
    # ------------------------------------------------------------------

    def leaf_operands(self):
        """Yield all leaf (non-BooleanResult) operands in the CSG tree.

        Traverses the tree depth-first and yields every operand that
        is not itself a :class:`BooleanResult`.

        Yields
        ------
        :class:`~compas.geometry.Geometry`
        """
        for operand in (self.first_operand, self.second_operand):
            if isinstance(operand, BooleanResult):
                yield from operand.leaf_operands()
            else:
                yield operand

    def depth(self):
        """Return the depth of the CSG tree rooted at this node.

        Returns
        -------
        int
            Depth of 1 means no nested boolean results.
        """
        d1 = self.first_operand.depth() if isinstance(self.first_operand, BooleanResult) else 0
        d2 = self.second_operand.depth() if isinstance(self.second_operand, BooleanResult) else 0
        return 1 + max(d1, d2)

    # ------------------------------------------------------------------
    # Mesh generation
    # ------------------------------------------------------------------

    def to_vertices_and_faces(self, n=16):
        """Discretise the boolean result into vertices and faces.

        .. note::

            This is an **approximate** discretisation that returns the
            first operand only.  Exact boolean geometry would require
            boolean operations via OpenCascade.

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
        if hasattr(self.first_operand, "to_vertices_and_faces"):
            return self.first_operand.to_vertices_and_faces(n=n)
        return [], []

    def to_mesh(self, n=16):
        """Convert the boolean result to a :class:`compas.datastructures.Mesh`.

        .. note::

            Returns the first operand mesh only.  See
            :meth:`to_vertices_and_faces` for details.

        Parameters
        ----------
        n : int
            Number of sample points for circular profiles.

        Returns
        -------
        :class:`compas.datastructures.Mesh` | None
        """
        if hasattr(self.first_operand, "to_mesh"):
            return self.first_operand.to_mesh(n=n)
        return None
