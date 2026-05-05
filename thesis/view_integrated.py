"""View the integrated workflow IFC model with colored element types."""

from compas.colors import Color
from compas_viewer import Viewer
from compas_viewer.components import Treeform

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.brep import TessellatedBrep

TYPE_COLORS = {
    "IfcSlab": [0.76, 0.70, 0.60, 1.0],    # warm sand
    "IfcColumn": [0.65, 0.74, 0.78, 1.0],   # cool blue-gray
    "IfcBeam": [0.70, 0.78, 0.65, 1.0],     # soft sage
}
DEFAULT_COLOR = [0.8, 0.8, 0.8, 1.0]

model = BuildingInformationModel("temp/thesis_integrated_workflow.ifc")

viewer = Viewer()
viewer.ui.sidebar.show_objectsetting = False
if model.unit:
    viewer.unit = model.unit


def add_element(elem, parent=None):
    label = f"[{elem.ifc_type}] {elem.name}"
    visual = elem._visual_geometry
    skip = elem.ifc_type in ("IfcSpace", "IfcOpeningElement")

    if visual is not None and not skip:
        rgba = TYPE_COLORS.get(elem.ifc_type, DEFAULT_COLOR)
        style = elem._resolve_style() or {}
        if isinstance(visual, TessellatedBrep):
            style["facecolors"] = [rgba] * (len(visual.faces) * 3)
        else:
            style["surfacecolor"] = Color(*rgba[:3])
        obj = viewer.scene.add(
            visual,
            name=label,
            parent=parent,
            hide_coplanaredges=True,
            **style,
        )
    else:
        obj = viewer.scene.add_group(name=label, parent=parent)

    obj.transformation = elem.transformation
    for child in elem.children:
        add_element(child, parent=obj)


for node in model.tree.root.children:
    add_element(node.element)

treeform = Treeform()
viewer.ui.sidebar.add(treeform)
viewer.show()
