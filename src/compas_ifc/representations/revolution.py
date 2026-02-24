"""
Revolution geometry type for parametric IFC representation.
"""

import math

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Transformation
from compas.geometry import Vector


class Revolution(Geometry):
    """A solid defined by revolving a 2D profile around an axis.

    Directly corresponds to ``IfcRevolvedAreaSolid``.  Preserves the
    parametric data that is lost when ifcopenshell evaluates the shape
    into tessellated or OCC geometry.

    Parameters
    ----------
    profile : :class:`Polygon` | :class:`Circle` | tuple[:class:`Polygon`, list[:class:`Polygon`]]
        The swept 2D profile.  Same conventions as :class:`Extrusion`.
    axis_point : :class:`Point`
        Origin of the revolution axis (in local frame coordinates).
    axis_direction : :class:`Vector`
        Unit direction of the revolution axis (in local frame coordinates).
    angle : float
        Revolution angle **in degrees** (IFC convention).
        Use 360 for a full revolution.
    frame : :class:`Frame`, optional
        Local placement of the solid.
        Corresponds to ``IfcRevolvedAreaSolid.Position``.
    name : str, optional
        Optional name for the revolution.

    Attributes
    ----------
    profile : :class:`Polygon` | :class:`Circle` | tuple[:class:`Polygon`, list[:class:`Polygon`]]
    axis_point : :class:`Point`
    axis_direction : :class:`Vector`
    angle : float
    frame : :class:`Frame`
    name : str or None
    """

    def __init__(self, profile, axis_point, axis_direction, angle, frame=None, name=None):
        super().__init__()
        self.profile = profile
        self.axis_point = Point(*axis_point)
        self.axis_direction = Vector(*axis_direction)
        self.angle = float(angle)
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
        return f"<Revolution profile={ptype} angle={self.angle:.1f}°>"

    # ------------------------------------------------------------------
    # Geometry interface
    # ------------------------------------------------------------------

    def transform(self, transformation):
        """Transform the revolution by transforming its frame.

        The profile geometry stays in local coordinates; only the
        placement frame is transformed.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.
        """
        self.frame.transform(transformation)

    def copy(self):
        """Return a deep copy of this revolution.

        Returns
        -------
        :class:`Revolution`
        """
        if isinstance(self.profile, tuple):
            outer = self.profile[0].copy()
            inners = [p.copy() for p in self.profile[1]]
            profile_copy = (outer, inners)
        elif hasattr(self.profile, "copy"):
            profile_copy = self.profile.copy()
        else:
            profile_copy = self.profile
        return Revolution(
            profile=profile_copy,
            axis_point=self.axis_point.copy(),
            axis_direction=self.axis_direction.copy(),
            angle=self.angle,
            frame=self.frame.copy(),
            name=self.name,
        )

    # ------------------------------------------------------------------
    # Mesh generation
    # ------------------------------------------------------------------

    def _profile_points(self, n=16):
        """Return the profile as a list of 2D/3D points.

        Parameters
        ----------
        n : int
            Number of sample points for circular profiles.

        Returns
        -------
        list[:class:`Point`]
        """
        if isinstance(self.profile, tuple):
            return [Point(*p) for p in self.profile[0].points]
        elif isinstance(self.profile, Circle):
            cx = self.profile.frame.point.x if hasattr(self.profile, "frame") else 0
            cy = self.profile.frame.point.y if hasattr(self.profile, "frame") else 0
            r = self.profile.radius
            return [
                Point(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n), 0)
                for i in range(n)
            ]
        elif isinstance(self.profile, Polygon):
            return [Point(*p) for p in self.profile.points]
        else:
            return []

    def to_vertices_and_faces(self, n_profile=16, n_angle=32):
        """Discretise the revolution into vertices and faces.

        Rotates the profile around the revolution axis at *n_angle*
        evenly spaced steps.

        Parameters
        ----------
        n_profile : int
            Number of sample points for circular profiles.
        n_angle : int
            Number of angular steps around the revolution.

        Returns
        -------
        tuple[list[list[float]], list[list[int]]]
            ``(vertices, faces)`` suitable for
            :meth:`Mesh.from_vertices_and_faces`.
        """
        pts = self._profile_points(n=n_profile)
        if not pts:
            return [], []

        angle_rad = math.radians(self.angle)
        m = len(pts)
        full_rev = abs(self.angle - 360.0) < 1e-6

        # Generate rotated rings
        vertices = []
        for j in range(n_angle + (0 if full_rev else 1)):
            theta = angle_rad * j / n_angle
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)

            # Rotation around axis_direction through axis_point
            ax = self.axis_direction
            ap = self.axis_point
            for p in pts:
                # Translate so axis goes through origin
                dx = p.x - ap.x
                dy = p.y - ap.y
                dz = p.z - ap.z
                # Rodrigues' rotation formula
                dot = ax.x * dx + ax.y * dy + ax.z * dz
                cx = ax.y * dz - ax.z * dy
                cy = ax.z * dx - ax.x * dz
                cz = ax.x * dy - ax.y * dx
                rx = dx * cos_t + cx * sin_t + ax.x * dot * (1 - cos_t)
                ry = dy * cos_t + cy * sin_t + ax.y * dot * (1 - cos_t)
                rz = dz * cos_t + cz * sin_t + ax.z * dot * (1 - cos_t)
                vertices.append([rx + ap.x, ry + ap.y, rz + ap.z])

        # Build faces (quad strips between consecutive rings)
        faces = []
        n_rings = n_angle if full_rev else n_angle + 1
        for j in range(n_angle):
            j_next = (j + 1) % n_rings
            for i in range(m):
                i_next = (i + 1) % m
                faces.append([
                    j * m + i,
                    j * m + i_next,
                    j_next * m + i_next,
                    j_next * m + i,
                ])

        return vertices, faces

    def to_mesh(self, n_profile=16, n_angle=32):
        """Convert the revolution to a :class:`compas.datastructures.Mesh`.

        Parameters
        ----------
        n_profile : int
            Number of sample points for circular profiles.
        n_angle : int
            Number of angular steps around the revolution.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(n_profile=n_profile, n_angle=n_angle)
        if not vertices:
            return None
        return Mesh.from_vertices_and_faces(vertices, faces)
