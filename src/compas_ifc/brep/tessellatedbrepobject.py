from compas_viewer.scene import ViewerSceneObject
from .tessellatedbrep import TessellatedBrep
from compas.datastructures import Mesh
import numpy as np

class TessellatedBrepObject(ViewerSceneObject):
    def __init__(self, tessellatedbrep: TessellatedBrep, facecolors=None, **kwargs):
        super().__init__(item=tessellatedbrep, **kwargs)
        self.tessellatedbrep = tessellatedbrep
        self.facecolors = facecolors

    def _read_lines_data(self):
        positions = self.tessellatedbrep.vertices
        elements = self.tessellatedbrep.edges
        colors = []
        default_color = self.linescolor["_default"]
        colors = np.full(shape=(len(elements), 3), fill_value=default_color)
        return positions.tolist(), colors.tolist(), elements.tolist()
    
    def _read_frontfaces_data(self):
        positions = self.tessellatedbrep.vertices[self.tessellatedbrep.faces].reshape(-1, 3)
        elements = np.arange(len(positions)*3).reshape(-1, 3)
        return positions.tolist(), self.facecolors, elements.tolist()

    def to_mesh(self):
        return Mesh.from_vertices_and_faces(self.tessellatedbrep.vertices, self.tessellatedbrep.faces)
