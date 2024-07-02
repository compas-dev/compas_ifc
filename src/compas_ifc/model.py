from compas.data import Data
from compas_ifc.file import IFCFile

from typing import TYPE_CHECKING
from typing import Generator

if TYPE_CHECKING:
    from compas_ifc.entities.base import Base
    from compas_ifc.entities.generated.IFC4 import IfcProject
    from compas_ifc.entities.generated.IFC4 import IfcSite
    from compas_ifc.entities.generated.IFC4 import IfcBuilding
    from compas_ifc.entities.generated.IFC4 import IfcBuildingElement


class Model(Data):
    def __init__(self, path, use_occ=False, load_geometries=True):
        self.file = IFCFile(path, self, use_occ=use_occ, load_geometries=load_geometries)

    @property
    def entities(self) -> Generator["Base", None, None]:
        for entity in self.file._file:
            yield self.file.from_entity(entity)

    @property
    def project(self) -> "IfcProject":
        return self.file.get_entities_by_type("IfcProject")[0]

    @property
    def sites(self) -> list["IfcSite"]:
        return self.file.get_entities_by_type("IfcSite")

    @property
    def buildings(self) -> list["IfcBuilding"]:
        return self.file.get_entities_by_type("IfcBuilding")

    @property
    def building_elements(self) -> list["IfcBuildingElement"]:
        return self.file.get_entities_by_type("IfcBuildingElement")

    def get_entities_by_type(self, type_name) -> list["Base"]:
        return self.file.get_entities_by_type(type_name)

    def get_entities_by_name(self, name) -> list["Base"]:
        return self.file.get_entities_by_name(name)

    def get_entity_by_global_id(self, global_id) -> "Base":
        return self.file.get_entity_by_global_id(global_id)

    def get_entity_by_id(self, id) -> "Base":
        return self.file.get_entity_by_id(id)

    def print_summary(self):
        """
        Overview of IFC file

        Number of entities
        Size of file
        Project info
        number of key type entities
        Plot of spatial hierarchy"""

        print("=" * 80)
        print("File: {}".format(self.file.filepath))
        print("Size: {} MB".format(self.file.file_size()))
        print("Project: {}".format(self.project.Name))
        print("Description: {}".format(self.project.Description))
        print("Number of sites: {}".format(len(self.sites)))
        print("Number of buildings: {}".format(len(self.buildings)))
        print("Number of building elements: {}".format(len(self.building_elements)))
        print("=" * 80)

    def print_spatial_hierarchy(self, max_depth=3):
        self.project.print_spatial_hierarchy(max_depth=max_depth)

    def show(self, entity=None):
        try:
            from compas_viewer import Viewer

        except ImportError:
            raise ImportError("The show method requires compas_viewer to be installed.")

        viewer = Viewer()

        entity_map = {}

        def parse_entity(entity, parent=None):
            obj = None
            name = f"[{entity.__class__.__name__}]{entity.Name}"
            if getattr(entity, "geometry", None):
                if not entity.is_a("IfcSpace"):
                    obj = viewer.scene.add(entity.geometry, name=name, parent=parent, **entity.style)
            if entity.children:
                obj = viewer.scene.add([], name=name, parent=parent)
                for child in entity.children:
                    parse_entity(child, parent=obj)

            if obj:
                entity_map[id(obj)] = entity

        parse_entity(entity or self.project)

        viewer.show()

if __name__ == "__main__":
    model = Model("data/wall-with-opening-and-window.ifc")
    model.summary()
