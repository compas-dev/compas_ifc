import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Geometry
from compas.geometry import bounding_box
from compas.geometry import transform_points_numpy


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
