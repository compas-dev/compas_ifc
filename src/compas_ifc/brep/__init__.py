from .tessellatedbrep import TessellatedBrep

try:
    from .tessellatedbrepobject import TessellatedBrepObject
except ImportError:
    pass

from compas.plugins import plugin
from compas.scene import register


@plugin(category="factories", requires=["compas_viewer"], trylast=True)
def register_scene_objects():
    register(TessellatedBrep, TessellatedBrepObject, context="Viewer")

    try:
        from compas_occ.brep import OCCBrep
        from .ifcbrepobject import IFCBrepObject

        register(OCCBrep, IFCBrepObject, context="Viewer")

    except ImportError:
        pass


__all__ = ["TessellatedBrep", "TessellatedBrepObject"]
