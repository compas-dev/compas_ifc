from .tessellatedbrep import TessellatedBrep
from compas_model.viewer import ElementObject
from compas_model.elements import Group
from .tessellatedbrepobject import TessellatedBrepObject


class BuildingElementObject(ElementObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.element.ifc_type == "IfcSpace":
            self.opacity = 0

    def create_visualization_object(self, **kwargs):
        if isinstance(self.element, Group):
            self.visualization_object = None
        elif isinstance(self.element.geometry, TessellatedBrep):
            brep_kwargs = kwargs.copy()
            brep_kwargs["item"] = self.element.geometry
            self.visualization_object = TessellatedBrepObject(**brep_kwargs, **self.element.ifc_entity.style)
        else:
            self.visualization_object = None

        
        global_transformation = self.element.transformation

        if self.element.parent:
            parent_global_transformation = self.element.parent.transformation
            local_transformation = global_transformation * parent_global_transformation.inverse()
        else:
            local_transformation = global_transformation

        self.transformation = local_transformation

