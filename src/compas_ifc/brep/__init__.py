from .tessellatedbrep import TessellatedBrep

try:
    from .tessellatedbrepobject import TessellatedBrepObject
except ImportError:
    pass

from compas.plugins import plugin
from compas.scene import register
from .buildingelementobject import BuildingElementObject
from compas_ifc.entities.buildingelements import BuildingElement

@plugin(category="factories", requires=["compas_viewer"], trylast=True)
def register_scene_objects():
    register(TessellatedBrep, TessellatedBrepObject, context="Viewer")
    register(BuildingElement, BuildingElementObject, context="Viewer")


    try:
        from compas_occ.brep import OCCBrep
        from .ifcbrepobject import IFCBrepObject

        register(OCCBrep, IFCBrepObject, context="Viewer")

    except ImportError:
        pass


__all__ = ["TessellatedBrep", "TessellatedBrepObject"]
