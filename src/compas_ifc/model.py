from compas.data import Data
from compas_ifc.reader import IFCReader

from typing import TYPE_CHECKING
from typing import Generator

if TYPE_CHECKING:
    from compas_ifc.entities.base import Base
    from compas_ifc.entities.generated.IFC4 import IfcProject
    from compas_ifc.entities.generated.IFC4 import IfcSite
    from compas_ifc.entities.generated.IFC4 import IfcBuilding
    from compas_ifc.entities.generated.IFC4 import IfcBuildingElement


class Model(Data):
    def __init__(self, path, use_occ=False):
        self.reader = IFCReader(path, self, use_occ=use_occ)

    @property
    def entities(self) -> Generator["Base", None, None]:
        for entity in self.reader._file:
            yield self.reader.from_entity(entity)

    @property
    def project(self) -> "IfcProject":
        return self.reader.get_entities_by_type("IfcProject")[0]

    @property
    def sites(self) -> list["IfcSite"]:
        return self.reader.get_entities_by_type("IfcSite")

    @property
    def buildings(self) -> list["IfcBuilding"]:
        return self.reader.get_entities_by_type("IfcBuilding")

    @property
    def building_elements(self) -> list["IfcBuildingElement"]:
        return self.reader.get_entities_by_type("IfcBuildingElement")

    def get_entities_by_type(self, type_name) -> list["Base"]:
        return self.reader.get_entities_by_type(type_name)

    def get_entities_by_name(self, name) -> list["Base"]:
        return self.reader.get_entities_by_name(name)

    def get_entity_by_global_id(self, global_id) -> "Base":
        return self.reader.get_entity_by_global_id(global_id)

    def get_entity_by_id(self, id) -> "Base":
        return self.reader.get_entity_by_id(id)

    def print_summary(self):
        """
        Overview of IFC file

        Number of entities
        Size of file
        Project info
        number of key type entities
        Plot of spatial hierarchy"""

        print("=" * 80)
        print("File: {}".format(self.reader.filepath))
        print("Size: {} MB".format(self.reader.file_size()))
        print("Project: {}".format(self.project.Name))
        print("Description: {}".format(self.project.Description))
        print("Number of sites: {}".format(len(self.sites)))
        print("Number of buildings: {}".format(len(self.buildings)))
        print("Number of building elements: {}".format(len(self.building_elements)))
        print("=" * 80)

    def print_spatial_hierarchy(self):
        self.project.print_spatial_hierarchy()

    def show(self):
        raise NotImplementedError


if __name__ == "__main__":
    model = Model("data/wall-with-opening-and-window.ifc")
    model.summary()
