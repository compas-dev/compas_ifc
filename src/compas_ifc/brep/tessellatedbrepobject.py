from compas_viewer.scene import ViewerSceneObject
from .tessellatedbrep import TessellatedBrep
from compas.datastructures import Mesh
import numpy as np


class TessellatedBrepObject(ViewerSceneObject):
    def __init__(self, tessellatedbrep: TessellatedBrep, facecolors=None, **kwargs):
        super().__init__(item=tessellatedbrep, **kwargs)
        self.tessellatedbrep = tessellatedbrep
        self.facecolors = facecolors
        self.use_rgba = True

        # TODO: it is not facecolors, it is verexcolor
        if not self.facecolors:
            self.facecolors = [[0.5, 0.5, 0.5, 1.0] for _ in range(len(self.tessellatedbrep.faces) * 3)]

    def _read_lines_data(self):
        positions = self.tessellatedbrep.vertices
        elements = self.tessellatedbrep.edges
        colors = []
        default_color = self.linescolor["_default"]
        colors = np.full(shape=(len(elements), 3), fill_value=default_color)
        return positions.tolist(), colors.tolist(), elements.tolist()

    def _read_frontfaces_data(self):
        positions = self.tessellatedbrep.vertices[self.tessellatedbrep.faces].reshape(-1, 3).tolist()
        elements = np.arange(len(positions) * 3).reshape(-1, 3).tolist()
        colors = [color[:3] for color in self.facecolors]
        opacities = [color[3] for color in self.facecolors]
        return positions, colors, opacities, elements

    def _read_backfaces_data(self):
        positions = self.tessellatedbrep.vertices[self.tessellatedbrep.faces].reshape(-1, 3).tolist()
        elements = np.arange(len(positions) * 3).reshape(-1, 3)
        elements = elements[:, ::-1].tolist()
        colors = [color[:3] for color in self.facecolors]
        opacities = [color[3] for color in self.facecolors]
        return positions, colors, opacities, elements

    def to_mesh(self):
        return Mesh.from_vertices_and_faces(self.tessellatedbrep.vertices, self.tessellatedbrep.faces)
