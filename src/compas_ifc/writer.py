import time

import ifcopenshell
from ifcopenshell.api import run

from .entities.element import Element
from .entities.entity import Entity
from .entities.objectdefinition import ObjectDefinition
from .entities.product import Product
from .entities.project import Project
from .entities.root import Root
from .resources.representation import write_body_representation
from .resources.shapes import frame_to_ifc_axis2_placement_3d


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
        self._relationmap_aggregates = {}
        self._relationmap_contains = {}
        self._representationmap = {}
        self._psetsmap = {}
        self._default_context = None
        self._default_body_context = None
        self._default_project = None
        self._default_site = None
        self._default_building = None
        self._default_building_storey = None
        self._default_owner_history = None

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
                self._default_project = self.file.create_entity("IfcProject", GlobalId=self.create_guid(), Name="Default Project")
                run("unit.assign_unit", self.file)
            else:
                self._default_project = self.write_entity(self.model.projects[0])
        return self._default_project

    @property
    def default_site(self):
        if not self._default_site:
            if not self.model.sites:
                self._default_site = self.file.create_entity("IfcSite", Name="Default Site", GlobalId=self.create_guid())
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
                self._default_building = self.file.create_entity("IfcBuilding", GlobalId=self.create_guid(), Name="Default Building")
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
                self._default_building_storey = self.file.create_entity("IfcBuildingStorey", GlobalId=self.create_guid(), Name="Default Storey")
                self.file.create_entity(
                    "IfcRelAggregates",
                    GlobalId=self.create_guid(),
                    RelatingObject=self.default_building,
                    RelatedObjects=[self._default_building_storey],
                )
            else:
                self._default_building_storey = self.write_entity(self.model.building_storeys[0])
        return self._default_building_storey

    @property
    def default_owner_history(self):
        if not self._default_owner_history:
            import compas_ifc

            person = self.file.create_entity("IfcPerson")
            organization = self.file.create_entity("IfcOrganization", Name="compas.dev")
            person_and_org = self.file.create_entity("IfcPersonAndOrganization", ThePerson=person, TheOrganization=organization)
            application = self.file.create_entity(
                "IfcApplication",
                ApplicationDeveloper=organization,
                Version=compas_ifc.__version__,
                ApplicationFullName="compas_ifc",
                ApplicationIdentifier="compas_ifc v" + compas_ifc.__version__,
            )

            owner_history = self.file.create_entity(
                "IfcOwnerHistory",
                OwningUser=person_and_org,
                OwningApplication=application,
                ChangeAction="ADDED",
                CreationDate=int(time.time()),
            )

            self._default_owner_history = owner_history
        return self._default_owner_history

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
            if self._relationmap_contains.get(parent):
                relation = self._relationmap_contains[parent]
                children = set(relation.RelatedElements)
                children.add(child)
                children = list(children)
                children.sort(key=lambda x: x.Name)
                relation.RelatedElements = tuple(children)
            else:
                relation = self.file.create_entity(
                    "IfcRelContainedInSpatialStructure",
                    GlobalId=self.create_guid(),
                    RelatingStructure=parent,
                    RelatedElements=[child],
                )
                self._relationmap_contains[parent] = relation
        else:
            if self._relationmap_aggregates.get(parent):
                relation = self._relationmap_aggregates[parent]
                children = set(relation.RelatedObjects)
                children.add(child)
                children = list(children)
                children.sort(key=lambda x: x.Name)
                relation.RelatedObjects = tuple(children)
            else:
                relation = self.file.create_entity("IfcRelAggregates", GlobalId=self.create_guid(), RelatingObject=parent, RelatedObjects=[child])
                self._relationmap_aggregates[parent] = relation

    def write_entity(self, entity: Entity) -> None:
        """Writes the given entity recursively with all its referencing attributes to the ifc file."""
        if entity in self._entitymap:
            return self._entitymap[entity]

        attributes = {}
        if isinstance(entity, Root):
            attributes["OwnerHistory"] = self.default_owner_history

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
                setattr(ifc_entity, key, value)

        self._entitymap[entity] = ifc_entity

        if not entity._entity:
            # Entity created in memory
            self.write_entity_representation(entity)
            self.write_entity_placement(entity)
            self.write_entity_pset(entity, ifc_entity)

        if isinstance(entity, Project):
            print("Writing project: " + str(entity))
            run("unit.assign_unit", self.file)

        return ifc_entity

    def write_entity_pset(self, entity: Entity, ifc_entity: ifcopenshell.entity_instance):
        for name, properties in entity.psets.items():
            if id(properties) in self._psetsmap:
                pset = self._psetsmap[id(properties)]
                # TODO: This can be mreged too.
                self.file.create_entity("IfcRelDefinesByProperties", GlobalId=self.create_guid(), RelatingPropertyDefinition=pset, RelatedObjects=[ifc_entity])
            else:
                pset = run("pset.add_pset", self.file, product=ifc_entity, name=name)
                self._psetsmap[id(properties)] = pset
                run("pset.edit_pset", self.file, pset=pset, properties=properties)

    def write_entity_representation(self, entity: Entity):
        """Writes the representations of the given entity to the ifc file."""
        if isinstance(entity, Product):
            if entity.body:
                if id(entity.body) not in self._representationmap:
                    representation = write_body_representation(self.file, entity.body, self._entitymap[entity], self.default_body_context)
                    self._representationmap[id(entity.body)] = representation
                else:
                    representation = self._representationmap[id(entity.body)]
                    run(
                        "geometry.assign_representation",
                        self.file,
                        product=self._entitymap[entity],
                        representation=representation,
                    )

    def write_entity_placement(self, entity: Entity):
        """Writes the placement of the given entity to the ifc file."""
        if isinstance(entity, Product):
            if entity.frame:
                # TODO: consider parent frame
                loacal_placement = frame_to_ifc_axis2_placement_3d(self.file, entity.frame)
                placement = self.file.create_entity("IfcLocalPlacement", RelativePlacement=loacal_placement)
                self._entitymap[entity].ObjectPlacement = placement
