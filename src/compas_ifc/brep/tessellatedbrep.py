import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Geometry
from compas.geometry import area_polygon
from compas.geometry import bounding_box
from compas.geometry import transform_points_numpy
from compas.geometry import volume_polyhedron


class TessellatedBrep(Geometry):
    def __init__(self, vertices=None, edges=None, faces=None, **kwargs):
        super().__init__(**kwargs)
        if vertices is None:
            vertices = []
        if edges is None:
            edges = []
        if faces is None:
            faces = []
        self.vertices = np.array(vertices).reshape(-1, 3)
        self.edges = np.array(edges).reshape(-1, 2)
        self.faces = np.array(faces).reshape(-1, 3)

    @property
    def __data__(self):
        return {
            "vertices": self.vertices.tolist(),
            "edges": self.edges.tolist(),
            "faces": self.faces.tolist(),
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            vertices=data["vertices"],
            edges=data["edges"],
            faces=data["faces"],
        )

    def transform(self, transformation):
        self.vertices = transform_points_numpy(self.vertices, transformation)

    def to_vertices_and_faces(self):
        return self.vertices, self.faces

    def to_mesh(self):
        mesh = Mesh.from_vertices_and_faces(self.vertices, self.faces)
        mesh.name = self.name
        return mesh

    @property
    def aabb(self):
        from compas.geometry import Box

        return Box.from_bounding_box(bounding_box(self.vertices))

    @property
    def obb(self):
        from compas.geometry import Box
        from compas.geometry import oriented_bounding_box_numpy

        return Box.from_bounding_box(oriented_bounding_box_numpy(self.vertices))

    @property
    def volume(self):
        """Calculate the volume of the tessellated BREP by converting to mesh.

        Returns
        -------
        float or None
            The volume of the BREP if the mesh is closed, None otherwise.
        """
        # Handle edge case: empty vertices or faces
        if len(self.vertices) == 0 or len(self.faces) == 0:
            return None

        try:
            mesh = self.to_mesh()

            # Check if mesh is closed - volume can only be calculated for closed meshes
            if not mesh.is_closed():
                return None

            # Get vertices and faces for volume calculation
            vertices, faces = mesh.to_vertices_and_faces()

            # Calculate volume using COMPAS geometry function
            return volume_polyhedron((vertices, faces))

        except Exception:
            # Return None if any error occurs during calculation
            return None

    @property
    def surface_area(self):
        """Calculate the surface area of the tessellated BREP by converting to mesh.

        Returns
        -------
        float or None
            The surface area of the BREP, or None if calculation fails.
        """
        # Handle edge case: empty vertices or faces
        if len(self.vertices) == 0 or len(self.faces) == 0:
            return None

        try:
            mesh = self.to_mesh()

            # Calculate total surface area by summing face areas
            total_area = 0.0
            for face_key in mesh.faces():
                # Get face vertices coordinates
                face_vertices = [mesh.vertex_coordinates(vertex) for vertex in mesh.face_vertices(face_key)]

                # Calculate area of this face using COMPAS geometry function
                face_area = area_polygon(face_vertices)
                total_area += face_area

            return total_area

        except Exception:
            # Return None if any error occurs during calculation
            return None
