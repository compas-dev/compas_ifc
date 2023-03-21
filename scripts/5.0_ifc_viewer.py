import os

from compas_ifc.viewer import IFC_viewer

HERE = os.path.dirname(__file__)
FILE = os.path.join(
    HERE,
    "..",
    "data",
    "wall-with-opening-and-window.ifc",
)


viewer = IFC_viewer()
viewer.open(FILE)

viewer.add_all()
viewer.show_forms()
viewer.view.camera.zoom_extents()

viewer.show()
