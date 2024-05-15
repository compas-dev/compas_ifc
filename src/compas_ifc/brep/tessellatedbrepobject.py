import numpy as np
from compas.colors import Color
from compas.datastructures import Mesh
from compas_viewer.scene import ViewerSceneObject

from .tessellatedbrep import TessellatedBrep


class TessellatedBrepObject(ViewerSceneObject):
    def __init__(self, tessellatedbrep: TessellatedBrep, facecolors=None, **kwargs):
        super().__init__(item=tessellatedbrep, **kwargs)
        self.tessellatedbrep = tessellatedbrep
        self.facecolors = facecolors

        # TODO: it is not facecolors, it is verexcolor
        if not self.facecolors:
            self.facecolors = [Color(0.9, 0.9, 0.9) for _ in range(len(self.tessellatedbrep.faces) * 3)]

    def _read_points_data(self):
        pass

    def _read_lines_data(self):
        positions = self.tessellatedbrep.vertices.tolist()
        elements = self.tessellatedbrep.edges.tolist()
        colors = [Color(0.1, 0.1, 0.1)] * len(elements)
        return positions, colors, elements

    def _read_frontfaces_data(self):
        positions = self.tessellatedbrep.vertices[self.tessellatedbrep.faces].reshape(-1, 3).tolist()
        elements = np.arange(len(positions) * 3).reshape(-1, 3).tolist()
        colors = [Color(*color) for color in self.facecolors]
        return positions, colors, elements

    def _read_backfaces_data(self):
        positions = self.tessellatedbrep.vertices[self.tessellatedbrep.faces].reshape(-1, 3).tolist()
        elements = np.arange(len(positions) * 3).reshape(-1, 3)
        elements = elements[:, ::-1].tolist()
        colors = [Color(*color) for color in self.facecolors]
        return positions, colors, elements

    def to_mesh(self):
        return Mesh.from_vertices_and_faces(self.tessellatedbrep.vertices, self.tessellatedbrep.faces)
