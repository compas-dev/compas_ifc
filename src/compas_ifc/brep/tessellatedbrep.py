import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Geometry
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
