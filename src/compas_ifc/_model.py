from compas.data import Data
from compas_ifc._reader import IFCReader
from compas_ifc.entities.generated import IfcProject
from compas_ifc.entities.generated import IfcSite
from compas_ifc.entities.generated import IfcBuilding
from compas_ifc.entities.generated import IfcBuildingElement

class IfcModel(Data):
    def __init__(self, path):
        self.reader = IFCReader(path)

    @property
    def project(self) -> IfcProject:
        return self.reader.get_by_type("IfcProject")[0]

    @property
    def sites(self) -> IfcSite:
        return self.reader.get_by_type("IfcSite")

    @property
    def buildings(self) -> IfcBuilding:
        return self.reader.get_by_type("IfcBuilding")
    
    @property
    def building_elements(self) -> IfcBuildingElement:
        return self.reader.get_by_type("IfcBuildingElement")

    def get_by_type(self, type_name):
        return self.reader.get_by_type(type_name)

    def summary(self):
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

    def show(self):
        raise NotImplementedError

if __name__ == "__main__":
    model = IfcModel("data/wall-with-opening-and-window.ifc")
    model.summary()