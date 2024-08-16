try:
    import numpy as np
    from compas.colors import Color
    from compas.tolerance import TOL
    from compas_occ.brep import OCCBrep
    from compas_viewer.scene.brepobject import BRepObject

    class IFCBrepObject(BRepObject):
        def __init__(self, shellcolors=None, **kwargs):
            brep = kwargs["item"]
            brep.simplify()
            brep.heal()

            super().__init__(**kwargs)
            self.shells = [shell.to_tesselation(TOL.lineardeflection)[0] for shell in self.brep.shells]
            self.shellcolors = shellcolors or [self.facecolor.rgba for _ in self.shells]
            self._bounding_box_center = None

        @property
        def brep(self) -> OCCBrep:
            return self.item

        @property
        def bounding_box_center(self):
            if not self._bounding_box_center:
                self._bounding_box_center = np.mean(self.points, axis=0)
            return self._bounding_box_center

        def _read_frontfaces_data(self):
            positions = []
            elements = np.array([], dtype=int).reshape(0, 3)
            colors = []

            for shell, color in zip(self.shells, self.shellcolors):
                shell_positions, shell_elements = shell.to_vertices_and_faces()
                shell_elements = np.array(shell_elements) + len(positions)
                positions += shell_positions
                elements = np.vstack((elements, shell_elements))
                colors += [Color(*color)] * len(shell_positions)  # TODO: this is terrible
                if color[3] < 1:
                    self.opacity = 0.999  # NOTE: this is to trigger the object order sorting

            return positions, colors, elements

        def _read_backfaces_data(self):
            positions = []
            elements = np.array([], dtype=int).reshape(0, 3)
            colors = []

            for shell, color in zip(self.shells, self.shellcolors):
                shell_positions, shell_elements = shell.to_vertices_and_faces()
                for element in shell_elements:
                    element.reverse()
                shell_elements = np.array(shell_elements) + len(positions)
                positions += shell_positions
                elements = np.vstack((elements, shell_elements))
                colors += [Color(*color)] * len(shell_positions)

            return positions, colors, elements

except ImportError:
    pass
