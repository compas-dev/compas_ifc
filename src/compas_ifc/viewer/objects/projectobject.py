from compas_ifc.entities.project import Project
from .entityobject import EntityObject


class ProjectObject(EntityObject):
    def get_body_geometry(self, project: Project):
        shapes = [project.frame]
        return shapes
