import numpy as np
from compas.colors import Color
from compas.datastructures import Mesh
from compas_viewer.scene import ViewerSceneObject

from .tessellatedbrep import TessellatedBrep


class TessellatedBrepObject(ViewerSceneObject):
    def __init__(self, facecolors=None, **kwargs):
        super().__init__(**kwargs)

        # NOTE: it is not facecolors, it is verexcolor
        if not facecolors:
            self.facecolors = [Color(0.9, 0.9, 0.9) for _ in range(len(self.tessellatedbrep.faces) * 3)]
        else:
            facecolors = np.array(facecolors)
            self.facecolors = facecolors
            if np.mean(facecolors[:, 3]) < 1:
                # If mean alpha is less than 1, means the object has transparency
                self.opacity = 0.999  # Trigger the render order sorting of object

    @property
    def tessellatedbrep(self) -> TessellatedBrep:
        return self.item

    @property
    def bounding_box_center(self):
        if self._bounding_box_center is None:
            self._bounding_box_center = self.tessellatedbrep.vertices.mean(axis=0)
        return self._bounding_box_center

    def _read_points_data(self):
        pass

    def _read_lines_data(self):
        positions = self.tessellatedbrep.vertices.tolist()
        elements = self.tessellatedbrep.edges.tolist()
        colors = [Color(0.1, 0.1, 0.1)] * len(positions)
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
