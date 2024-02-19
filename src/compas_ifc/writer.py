import ifcopenshell
from ifcopenshell.api import run

from .entities.objectdefinition import ObjectDefinition
from .entities.element import Element
from .entities.entity import Entity
from .entities.product import Product
from .entities.project import Project
from .resources.representation import write_body_representation


class IFCWriter(object):
    """
    A class for writing IFC files.

    Parameters
    ----------
    model : :class:`compas_ifc.model.Model`
        The model to which the writer belongs.

    Attributes
    ----------
    model : :class:`compas_ifc.model.Model`
        The model to which the writer belongs.
    file : :class:`ifcopenshell.file`
        The IFC file to which the model is being written to.
    default_context : :class:`ifcopenshell.entity_instance`
        The default context of the model. Created if it does not exist.
    default_body_context : :class:`ifcopenshell.entity_instance`
        The default body context of the model. Created if it does not exist.
    default_project : :class:`ifcopenshell.entity_instance`
        The default project of the model. Created if it does not exist.
    default_site : :class:`ifcopenshell.entity_instance`
        The default site of the model. Created if it does not exist.
    default_building : :class:`ifcopenshell.entity_instance`
        The default building of the model. Created if it does not exist.
    default_building_storey : :class:`ifcopenshell.entity_instance`
        The default building storey of the model. Created if it does not exist.

    """

    def __init__(self, model):
        self.file = None
        self.model = model
        self._entitymap = {}
        self._default_context = None
        self._default_body_context = None
        self._default_project = None
        self._default_site = None
        self._default_building = None
        self._default_building_storey = None

    @property
    def default_context(self):
        # TODO: allow loading of existing contexts
        if not self._default_context:
            self._default_context = run("context.add_context", self.file, context_type="Model")
        return self._default_context

    @property
    def default_body_context(self):
        # TODO: allow loading of existing contexts
        if not self._default_body_context:
            self._default_body_context = run(
                "context.add_context",
                self.file,
                context_type="Model",
                context_identifier="Body",
                target_view="MODEL_VIEW",
                parent=self.default_context,
            )
        return self._default_body_context

    @property
    def default_project(self):
        if not self._default_project:
            if not self.model.projects:
                self._default_project = self.file.create_entity(
                    "IfcProject", GlobalId=self.create_guid(), Name="Default Project"
                )
                run("unit.assign_unit", self.file)
            else:
                self._default_project = self.write_entity(self.model.projects[0])
        return self._default_project

    @property
    def default_site(self):
        if not self._default_site:
            if not self.model.sites:
                self._default_site = self.file.create_entity(
                    "IfcSite", Name="Default Site", GlobalId=self.create_guid()
                )
                self.file.create_entity(
                    "IfcRelAggregates",
                    GlobalId=self.create_guid(),
                    RelatingObject=self.default_project,
                    RelatedObjects=[self._default_site],
                )
            else:
                self._default_site = self.write_entity(self.model.sites[0])
        return self._default_site

    @property
    def default_building(self):
        if not self._default_building:
            if not self.model.buildings:
                self._default_building = self.file.create_entity(
                    "IfcBuilding", GlobalId=self.create_guid(), Name="Default Building"
                )
                self.file.create_entity(
                    "IfcRelAggregates",
                    GlobalId=self.create_guid(),
                    RelatingObject=self.default_site,
                    RelatedObjects=[self._default_building],
                )
            else:
                self._default_building = self.write_entity(self.model.buildings[0])
        return self._default_building

    @property
    def default_building_storey(self):
        if not self._default_building_storey:
            if not self.model.building_storeys:
                self._default_building_storey = self.file.create_entity(
                    "IfcBuildingStorey", GlobalId=self.create_guid(), Name="Default Storey"
                )
                self.file.create_entity(
                    "IfcRelAggregates",
                    GlobalId=self.create_guid(),
                    RelatingObject=self.default_building,
                    RelatedObjects=[self._default_building_storey],
                )
            else:
                self._default_building_storey = self.write_entity(self.model.building_storeys[0])
        return self._default_building_storey

    def create_guid(self):
        return ifcopenshell.guid.new()

    def reset(self):
        """Resets the writer to start with a new ifc file."""
        self.file = ifcopenshell.file(schema=self.model.schema.name())
        self._entitymap = {}
        self._default_context = None
        self._default_body_context = None
        self._default_project = None
        self._default_site = None
        self._default_building = None
        self._default_building_storey = None

    def export(self, entities, filepath: str) -> None:
        """Exports the given entities to the ifc file."""
        print("Exporting IFC file to: " + filepath)
        self.reset()
        # TODO: make this better
        self.default_project

        # TODO: make this better
        for entity in self.model._new_entities:
            if not entity.parent and self.model.building_storeys:
                entity.parent = self.model.building_storeys[0]

        for entity in entities:
            for node in entity.traverse_branch():
                self.write_entity(node)

        for entity in entities:
            for node in entity.traverse_branch():
                self.write_relation(node)

        self.file.write(filepath)
        print("Done.")

    def save(self, filepath: str) -> None:
        """Writes the model as ifc file to the given filepath."""
        print("Saving IFC file to: " + filepath)
        self.reset()
        # TODO: make this better
        self.default_project

        for entity in self.model.get_all_entities():
            self.write_entity(entity)

        for entity in self.model._new_entities:  # TODO: needs better api
            self.write_relation(entity)

        self.file.write(filepath)
        print("Done.")

    def write_relation(self, entity: Entity):
        """Writes the relation of the given entity to the ifc file."""
        if entity._entity:
            # Entity from ifc file
            self.trim_existing_relation(entity)
        else:
            # Entity created in memory
            if isinstance(entity, ObjectDefinition) and not isinstance(entity, Project):
                # Only ObjectDefinitions can have parental relations, except for Project.
                self.create_new_relation(entity)

    def trim_existing_relation(self, entity: Entity) -> None:
        """writes a existing parental relation to the ifc file, trimming the non existing children."""

        if not entity.parent:
            return

        chilren_to_include = []
        relation = None

        # Modify the relation to only include the children that has been written to the ifc file.
        if hasattr(entity, "contained_in_structure"):
            relation = entity.contained_in_structure()
            for child in relation["RelatedElements"]:
                if child in self._entitymap:
                    chilren_to_include.append(child)
            relation["RelatedElements"] = chilren_to_include
        elif hasattr(entity, "decomposes"):
            relation = entity.decomposes()
            for child in relation["RelatedObjects"]:
                if child in self._entitymap:
                    chilren_to_include.append(child)
            relation["RelatedObjects"] = chilren_to_include
        else:
            raise Exception("Entity has no parent relation.")

        self.write_entity(relation)

    def create_new_relation(self, entity: ObjectDefinition):
        """Writes a new parental relation to the ifc file."""

        if entity.parent:
            parent = self._entitymap[entity.parent]
        else:
            # If no parent is given, use the default building storey.
            parent = self.default_building_storey

        child = self._entitymap[entity]

        if isinstance(entity, Element):
            self.file.create_entity(
                "IfcRelContainedInSpatialStructure",
                GlobalId=self.create_guid(),
                RelatingStructure=parent,
                RelatedElements=[child],
            )
        else:
            self.file.create_entity(
                "IfcRelAggregates", GlobalId=self.create_guid(), RelatingObject=parent, RelatedObjects=[child]
            )

    def write_entity(self, entity: Entity) -> None:
        """Writes the given entity recursively with all its referencing attributes to the ifc file."""
        if entity in self._entitymap:
            return self._entitymap[entity]

        attributes = {}
        for key, value in entity.attributes.items():
            if isinstance(value, Entity):
                attributes[key] = self.write_entity(value)
            elif isinstance(value, list) and value and isinstance(value[0], Entity):
                attributes[key] = [self.write_entity(v) for v in value]
            else:
                attributes[key] = value

        # ifc_entity = self.file.create_entity(entity.ifc_type, **attributes)
        ifc_entity = self.file.create_entity(entity.ifc_type)
        for key, value in attributes.items():
            if value is not None:
                print(key, value)
                setattr(ifc_entity, key, value)

        self._entitymap[entity] = ifc_entity

        if not entity._entity:
            # Entity created in memory
            self.write_entity_representation(entity)

        return ifc_entity

    def write_entity_pset(self, entity: Entity):
        raise NotImplementedError()

    def write_entity_representation(self, entity: Entity):
        """Writes the representations of the given entity to the ifc file."""
        if isinstance(entity, Product):
            try:
                write_body_representation(self.file, entity.body, self._entitymap[entity], self.default_body_context)
            except Exception as e:
                print("Error writing body representation of entity: " + str(entity))
                print(e)
                pass
