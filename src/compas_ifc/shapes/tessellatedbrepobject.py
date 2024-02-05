from compas_viewer.scene import ViewerSceneObject
from .tessellatedbrep import TessellatedBrep
import numpy as np

class TessellatedBrepObject(ViewerSceneObject):
    def __init__(self, tessellatedbrep: TessellatedBrep, **kwargs):
        super().__init__(item=tessellatedbrep, **kwargs)
        self.tessellatedbrep = tessellatedbrep

    def _read_lines_data(self):
        positions = self.tessellatedbrep.vertices
        elements = self.tessellatedbrep.edges
        colors = []
        default_color = self.linescolor["_default"]
        colors = np.full(shape=(len(elements), 3), fill_value=default_color)
        return positions.tolist(), colors.tolist(), elements.tolist()
    
    def _read_frontfaces_data(self):
        positions = self.tessellatedbrep.vertices
        elements = self.tessellatedbrep.faces
        colors = []
        default_color = self.facescolor["_default"]
        colors = np.full(shape=(len(elements), 3), fill_value=default_color)
        return positions.tolist(), colors.tolist(), elements.tolist()
