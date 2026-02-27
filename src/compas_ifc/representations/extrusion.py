"""
Extrusion geometry type for parametric IFC representation.
"""

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector


class Extrusion(Geometry):
    """A solid defined by sweeping a 2D profile along a direction.

    Directly corresponds to ``IfcExtrudedAreaSolid``.  Preserves the
    parametric data that is lost when ifcopenshell evaluates the shape
    into tessellated or OCC geometry.

    Parameters
    ----------
    profile : :class:`Polygon` | :class:`Circle` | tuple[:class:`Polygon`, list[:class:`Polygon`]]
        The swept 2D profile.  A :class:`Polygon` for simple closed
        profiles, a :class:`Circle` for circular profiles, or a
        ``(outer, [inner, ...])`` tuple for profiles with voids.
    direction : :class:`Vector`
        Unit direction of the extrusion (in local frame coordinates).
    depth : float
        Length of the extrusion along *direction*.
    frame : :class:`Frame`, optional
        Local placement of the extrusion solid.
        Corresponds to ``IfcExtrudedAreaSolid.Position``.
    name : str, optional
        Optional name for the extrusion.

    Attributes
    ----------
    profile : :class:`Polygon` | :class:`Circle` | tuple[:class:`Polygon`, list[:class:`Polygon`]]
        The swept 2D profile.
    direction : :class:`Vector`
        Extrusion direction.
    depth : float
        Extrusion depth.
    frame : :class:`Frame`
        Local coordinate frame.
    name : str or None
        Optional name.
    """

    def __init__(self, profile, direction, depth, frame=None, name=None):
        super().__init__()
        self.profile = profile
        self.direction = Vector(*direction)
        self.depth = float(depth)
        self.frame = frame or Frame.worldXY()
        self.name = name

    def __repr__(self):
        if isinstance(self.profile, tuple):
            n_voids = len(self.profile[1])
            ptype = f"ProfileWithVoids({n_voids} voids)"
        elif isinstance(self.profile, Circle):
            ptype = f"Circle(r={self.profile.radius:.3f})"
        elif isinstance(self.profile, Polygon):
            ptype = f"Polygon({len(self.profile.points)})"
        else:
            ptype = type(self.profile).__name__
        return f"<Extrusion profile={ptype} depth={self.depth:.3f}>"

    # ------------------------------------------------------------------
    # Geometry interface
    # ------------------------------------------------------------------

    def transform(self, transformation):
        """Transform the extrusion by transforming its frame.

        The profile geometry stays in local coordinates; only the
        placement frame is transformed.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.
        """
        self.frame.transform(transformation)

    def copy(self):
        """Return a deep copy of this extrusion.

        Returns
        -------
        :class:`Extrusion`
        """
        if isinstance(self.profile, tuple):
            outer = self.profile[0].copy()
            inners = [p.copy() for p in self.profile[1]]
            profile_copy = (outer, inners)
        elif hasattr(self.profile, "copy"):
            profile_copy = self.profile.copy()
        else:
            profile_copy = self.profile
        return Extrusion(
            profile=profile_copy,
            direction=self.direction.copy(),
            depth=self.depth,
            frame=self.frame.copy(),
            name=self.name,
        )

    # ------------------------------------------------------------------
    # Geometric properties
    # ------------------------------------------------------------------

    def _profile_area(self):
        """Compute the area of the profile cross-section.

        Returns
        -------
        float
            Area of the profile.  For profiles with voids, returns the
            outer area minus the sum of void areas.
        """
        if isinstance(self.profile, Polygon):
            return self.profile.area
        elif isinstance(self.profile, Circle):
            return self.profile.area
        elif isinstance(self.profile, tuple):
            outer_area = self.profile[0].area
            void_area = sum(v.area for v in self.profile[1])
            return outer_area - void_area
        return 0.0

    def _profile_perimeter(self):
        """Compute the perimeter of the profile cross-section.

        Returns
        -------
        float
            Perimeter of the profile.  For profiles with voids, returns
            the outer perimeter plus the sum of void perimeters (all
            boundaries contribute to the side surface).
        """
        if isinstance(self.profile, Polygon):
            return self.profile.length
        elif isinstance(self.profile, Circle):
            return self.profile.circumference
        elif isinstance(self.profile, tuple):
            outer_perimeter = self.profile[0].length
            void_perimeters = sum(v.length for v in self.profile[1])
            return outer_perimeter + void_perimeters
        return 0.0

    def volume(self):
        """Compute the exact volume of the extrusion.

        ``V = profile_area * depth``

        Returns
        -------
        float
        """
        return self._profile_area() * self.depth

    def surface_area(self):
        """Compute the exact surface area of the extrusion.

        ``A = 2 * profile_area + perimeter * depth``

        Returns
        -------
        float
        """
        return 2 * self._profile_area() + self._profile_perimeter() * self.depth

    # ------------------------------------------------------------------
    # Mesh generation
    # ------------------------------------------------------------------

    def _profile_points(self, n=16):
        """Return the profile as a list of 3D points.

        For a :class:`Circle`, sample *n* points.
        For a :class:`Polygon`, return the polygon points.
        For a profile with voids, return only the outer polygon points.

        Parameters
        ----------
        n : int
            Number of sample points for circular profiles.

        Returns
        -------
        list[:class:`Point`]
        """
        import math

        if isinstance(self.profile, tuple):
            return [Point(*p) for p in self.profile[0].points]
        elif isinstance(self.profile, Circle):
            cx = self.profile.frame.point.x if hasattr(self.profile, "frame") else 0
            cy = self.profile.frame.point.y if hasattr(self.profile, "frame") else 0
            r = self.profile.radius
            return [Point(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n), 0) for i in range(n)]
        elif isinstance(self.profile, Polygon):
            return [Point(*p) for p in self.profile.points]
        else:
            return []

    def to_vertices_and_faces(self, n=16):
        """Discretise the extrusion into vertices and faces.

        Constructs a prism from the (possibly sampled) profile polygon
        and the extrusion vector.

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
        pts = self._profile_points(n=n)
        if not pts:
            return [], []

        extrusion_vec = self.direction * self.depth
        m = len(pts)

        # Bottom face vertices (0..m-1) and top face vertices (m..2m-1)
        vertices = [[p.x, p.y, p.z] for p in pts]
        vertices += [[p.x + extrusion_vec.x, p.y + extrusion_vec.y, p.z + extrusion_vec.z] for p in pts]

        faces = []
        # Bottom face (reversed winding for outward normal)
        faces.append(list(range(m - 1, -1, -1)))
        # Top face
        faces.append(list(range(m, 2 * m)))
        # Side faces
        for i in range(m):
            j = (i + 1) % m
            faces.append([i, j, m + j, m + i])

        return vertices, faces

    def to_mesh(self, n=16):
        """Convert the extrusion to a :class:`compas.datastructures.Mesh`.

        Parameters
        ----------
        n : int
            Number of sample points for circular profiles.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(n=n)
        if not vertices:
            return None
        return Mesh.from_vertices_and_faces(vertices, faces)
