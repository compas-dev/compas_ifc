from .entity import Entity
import ifcopenshell


class Root(Entity):
    """Base class for all IFC entities that are derived from IfcRoot.

    Attributes
    ----------
    global_id : str
        The global id of the entity.
    name : str
        The name of the entity.
    """

    def __init__(self, entity, model) -> None:
        super().__init__(entity, model)
        if not entity:
            self["GlobalId"] = ifcopenshell.guid.new()
            self["Name"] = None

    def __repr__(self):
        return "<{}:{} Name: {}, GlobalId: {}>".format(type(self).__name__, self.ifc_type, self.name, self.global_id)

    @property
    def global_id(self):
        return self["GlobalId"]

    @property
    def name(self):
        return self["Name"]
