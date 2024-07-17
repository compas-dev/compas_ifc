from typing import TYPE_CHECKING
from typing import Generator

from compas.data import Data
from compas.geometry import Transformation
from compas.tolerance import TOL

from compas_ifc.file import IFCFile

if TYPE_CHECKING:
    from compas_ifc.entities.base import Base
    from compas_ifc.entities.generated.IFC4 import IfcBuilding
    from compas_ifc.entities.generated.IFC4 import IfcBuildingElement
    from compas_ifc.entities.generated.IFC4 import IfcBuildingStorey
    from compas_ifc.entities.generated.IFC4 import IfcProject
    from compas_ifc.entities.generated.IFC4 import IfcSite


class Model(Data):
    def __init__(self, filepath=None, schema=None, use_occ=False, load_geometries=True):
        self.file = IFCFile(self, filepath=filepath, schema=schema, use_occ=use_occ, load_geometries=load_geometries)
        if filepath:
            self.update_linear_deflection()

    @property
    def schema(self):
        return self.file.schema

    @property
    def schema_name(self):
        return self.file.schema_name

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
    def building_storeys(self) -> list["IfcBuildingStorey"]:
        return self.file.get_entities_by_type("IfcBuildingStorey")

    @property
    def building_elements(self) -> list["IfcBuildingElement"]:
        return self.file.get_entities_by_type("IfcBuildingElement")

    @property
    def unit(self):
        length_unit = self.project.length_unit
        if length_unit.Name == "METRE" and length_unit.Prefix == "MILLI":
            return "mm"
        elif length_unit.Name == "METRE" and length_unit.Prefix == "CENTI":
            return "cm"
        elif length_unit.Name == "METRE" and not length_unit.Prefix:
            return "m"

    @unit.setter
    def unit(self, value):
        if value == "mm":
            self.project.length_unit.Prefix = "MILLI"
        elif value == "cm":
            self.project.length_unit.Prefix = "CENTI"
        elif value == "m":
            self.project.length_unit.Prefix = None
        else:
            raise ValueError("Invalid unit. Use 'mm', 'cm', or 'm'.")

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

    def save(self, path: str):
        self.file.save(path)

    def export(self, path: str, entities: list["Base"] = [], as_snippet: bool = False, export_materials: bool = True, export_properties: bool = True):
        self.file.export(path, entities=entities, as_snippet=as_snippet, export_materials=export_materials, export_properties=export_properties)

    def show(self, entity=None):
        try:
            from compas_viewer import Viewer
            from compas_viewer.components import Treeform

        except ImportError:
            raise ImportError("The show method requires compas_viewer to be installed.")

        viewer = Viewer()
        print(f"Unit: {self.unit}")
        viewer.unit = self.unit

        entity_map = {}

        def parse_entity(entity, parent=None):
            obj = None
            name = f"[{entity.__class__.__name__}]{entity.Name}"
            transformation = Transformation.from_frame(entity.frame) if entity.frame else None
            if getattr(entity, "geometry", None) and not entity.is_a("IfcSpace"):
                obj = viewer.scene.add(entity.geometry, name=name, parent=parent, **entity.style)
                obj.transformation = transformation
            else:
                obj = viewer.scene.add([], name=name, parent=parent)

            obj.attributes["entity"] = entity

            for child in entity.children:
                parse_entity(child, parent=obj)

            if obj:
                entity_map[id(obj)] = entity

        parse_entity(entity or self.project)

        treeform = Treeform()
        viewer.ui.sidebar.widget.addWidget(treeform)

        def update_treeform(form, node):
            entity = node.attributes["entity"]
            treeform.update_from_dict({"Attributes": entity.attributes, "Properties": getattr(entity, "properties", {})})

        viewer.ui.sidebar.sceneform.callback = update_treeform

        viewer.show()

    def create(self, cls="IfcBuildingElementProxy", parent=None, geometry=None, frame=None, properties=None, **kwargs):
        return self.file.create(cls=cls, parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def update_linear_deflection(self):
        if self.unit == "mm":
            TOL.lineardeflection = 1
        elif self.unit == "cm":
            TOL.lineardeflection = 1e-1
        elif self.unit == "m":
            TOL.lineardeflection = 1e-3

    @classmethod
    def template(cls, schema="IFC4", building_count=1, storey_count=1, unit="mm"):
        model = cls(schema=schema)
        project = model.file.default_project
        site = model.create("IfcSite", parent=project, Name="Default Site")
        for i in range(building_count):
            building = model.create("IfcBuilding", parent=site, Name=f"Default Building {i+1}")
            for j in range(storey_count):
                model.create("IfcBuildingStorey", parent=building, Name=f"Default Storey {j+1}")

        model.unit = unit
        model.update_linear_deflection()
        return model


if __name__ == "__main__":
    model = Model("data/wall-with-opening-and-window.ifc")
    model.summary()
