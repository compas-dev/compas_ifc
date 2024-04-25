from .tessellatedbrep import TessellatedBrep

try:
    from .tessellatedbrepobject import TessellatedBrepObject
except ImportError:
    pass

from compas.plugins import plugin
from compas.scene import register


@plugin(category="factories", requires=["compas_viewer"])
def register_scene_objects():
    register(TessellatedBrep, TessellatedBrepObject, context="Viewer")


__all__ = ["TessellatedBrep", "TessellatedBrepObject"]
