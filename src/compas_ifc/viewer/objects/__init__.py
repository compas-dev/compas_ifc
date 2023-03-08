from compas_view2.objects import Object
from compas_ifc.entities.entity import Entity
from compas_ifc.entities.project import Project

from .entityobject import EntityObject
from .projectobject import ProjectObject


Object.register(Entity, EntityObject)
Object.register(Project, ProjectObject)
