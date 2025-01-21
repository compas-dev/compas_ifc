from typing import TYPE_CHECKING
from typing import Dict
from typing import Generator
from typing import Type
from typing import Union

from compas.data import Data
from compas.datastructures import Datastructure
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Transformation
from compas.tolerance import TOL

from compas_ifc.file import IFCFile

if TYPE_CHECKING:
    import ifcopenshell.ifcopenshell_wrapper

    from compas_ifc.entities.base import Base
    from compas_ifc.entities.generated.IFC4 import IfcBuilding
    from compas_ifc.entities.generated.IFC4 import IfcBuildingElement
    from compas_ifc.entities.generated.IFC4 import IfcBuildingStorey
    from compas_ifc.entities.generated.IFC4 import IfcProject
    from compas_ifc.entities.generated.IFC4 import IfcSite


class Model(Data):
    """The Model class is the COMPAS IFC's main entry point.
    It is a intuitive abstraction on top of an IFC file, providing a set of easy-to-use methods for interacting with the IFC data.

    Attributes
    ----------
    file : :class:`compas_ifc.file.IFCFile`
        The IFC file object.
    schema : :class:`ifcopenshell.schema.Schema`
        The IFC schema object.
    schema_name : str
        The name of the IFC schema.
    entities : Generator[:class:`compas_ifc.entities.base.Base`, None, None]
        A generator of all entities in the IFC file.
    project : :class:`compas_ifc.entities.generated.IFC4.IfcProject`
        The project entity.
    sites : list[:class:`compas_ifc.entities.generated.IFC4.IfcSite`]
        A list of all site entities.
    buildings : list[:class:`compas_ifc.entities.generated.IFC4.IfcBuilding`]
        A list of all building entities.
    building_storeys : list[:class:`compas_ifc.entities.generated.IFC4.IfcBuildingStorey`]
        A list of all building storey entities.
    building_elements : list[:class:`compas_ifc.entities.generated.IFC4.IfcBuildingElement`]
        A list of all building element entities.
    unit : str
        The unit of the IFC file. Can be "mm", "cm", or "m".

    """

    def __init__(self, filepath: str = None, schema: str = "IFC4", use_occ: bool = False, load_geometries: bool = True, verbose: bool = True, extensions: Dict[str, Type] = None):
        """
        Construct the Model object.

        Parameters
        ----------
        filepath : str
            The path to the IFC file.
        schema : str
            The IFC schema to use. Default is "IFC4".
        use_occ : bool
            Whether to use OCC for geometry processing. Default is False.
        load_geometries : bool
            Whether to pre-load geometries from the IFC file using multi-threading. Default is True.
        verbose : bool
            Whether to print verbose output. Default is True.
        extensions : Dict[str, Type]
            A dictionary of extensions to use, with the key being the IFC class name and the value being the extension class.

        """
        self.file = IFCFile(self, filepath=filepath, schema=schema, use_occ=use_occ, load_geometries=load_geometries, verbose=verbose, extensions=extensions)
        if filepath:
            self.update_linear_deflection()

    @property
    def schema(self) -> "ifcopenshell.ifcopenshell_wrapper.schema_definition":
        return self.file.schema

    @property
    def schema_name(self) -> str:
        return self.file.schema_name

    @property
    def entities(self) -> Generator["Base", None, None]:
        for entity in self.file._file:
            yield self.file.from_entity(entity)

    @property
    def project(self) -> "IfcProject":
        projects = self.file.get_entities_by_type("IfcProject")
        return projects[0] if projects else None

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
    def unit(self) -> str:
        length_unit = self.project.length_unit
        if length_unit.Name == "METRE" and length_unit.Prefix == "MILLI":
            return "mm"
        elif length_unit.Name == "METRE" and length_unit.Prefix == "CENTI":
            return "cm"
        elif length_unit.Name == "METRE" and not length_unit.Prefix:
            return "m"

    @unit.setter
    def unit(self, value: str):
        if value == "mm":
            self.project.length_unit.Prefix = "MILLI"
        elif value == "cm":
            self.project.length_unit.Prefix = "CENTI"
        elif value == "m":
            self.project.length_unit.Prefix = None
        else:
            raise ValueError("Invalid unit. Use 'mm', 'cm', or 'm'.")

    def get_entities_by_type(self, type_name: str) -> list["Base"]:
        """Get entities by type name

        Parameters
        ----------
        type_name : str
            The name of the type to get entities for.

        Returns
        -------
        list[:class:`compas_ifc.entities.base.Base`]
            A list of entities of the given type.
        """
        return self.file.get_entities_by_type(type_name)

    def get_entities_by_name(self, name: str) -> list["Base"]:
        """Get entities by name

        Parameters
        ----------
        name : str
            The name of the entity to get.

        Returns
        -------
        list[:class:`compas_ifc.entities.base.Base`]
            A list of entities with the given name.
        """
        return self.file.get_entities_by_name(name)

    def get_entity_by_global_id(self, global_id: str) -> "Base":
        """Get an entity by global ID

        Parameters
        ----------
        global_id : str
            The global ID of the entity to get.

        Returns
        -------
        :class:`compas_ifc.entities.base.Base`
            The entity with the given global ID.
        """
        return self.file.get_entity_by_global_id(global_id)

    def get_entity_by_id(self, id: int) -> "Base":
        """Get an entity by ID

        Parameters
        ----------
        id : int
            The ID of the entity to get.

        Returns
        -------
        :class:`compas_ifc.entities.base.Base`
            The entity with the given ID.
        """
        return self.file.get_entity_by_id(id)

    def search_ifc_classes(self, name: str, n: int = 5) -> list[Type["Base"]]:
        """
        Search for IFC classes by name

        Parameters
        ----------
        name : str
            The name of the IFC class to search for.
        n : int
            The number of results to return. Default is 5.

        Returns
        -------
        list[Type[:class:`compas_ifc.entities.base.Base`]]
            A list of IFC classes that match the search query.

        """
        return self.file.search_ifc_classes(name, n)

    def print_summary(self):
        """Print a summary of the IFC file."""

        print("=" * 80)
        print("Schema: {}".format(self.schema_name))
        if self.file.filepath:
            print("File: {}".format(self.file.filepath))
            print("Size: {} MB".format(self.file.file_size()))
        if self.project:
            print("Project: {}".format(self.project.Name))
            print("Description: {}".format(self.project.Description))
        print("Number of sites: {}".format(len(self.sites)))
        print("Number of buildings: {}".format(len(self.buildings)))
        print("Number of building elements: {}".format(len(self.building_elements)))
        print("=" * 80)

    def print_spatial_hierarchy(self, max_depth: int = 3):
        """Print the spatial hierarchy of the IFC file."""
        self.project.print_spatial_hierarchy(max_depth=max_depth)

    def save(self, path: str):
        """Save the IFC file."""
        self.file.save(path)

    def export(self, path: str, entities: list["Base"] = [], as_snippet: bool = False, export_materials: bool = True, export_properties: bool = True, export_styles: bool = True):
        """
        Export a subset of the IFC file to a new IFC file.

        Parameters
        ----------
        path : str
            The path to save the exported IFC file to.
        entities : list[:class:`compas_ifc.entities.base.Base`]
            The entities to export.
        as_snippet : bool
            Whether to export as a snippet, without the full spatial hierarchy. Default is False.
        export_materials : bool
            Whether to export materials. Default is True.
        export_properties : bool
            Whether to export properties. Default is True.
        export_styles : bool
            Whether to export styles. Default is True.

        """
        self.file.export(path, entities=entities, as_snippet=as_snippet, export_materials=export_materials, export_properties=export_properties, export_styles=export_styles)

    def show(self, entity: "Base" = None):
        """Show the IFC file in a viewer, either the entire project or a single entity.

        Parameters
        ----------
        entity : :class:`compas_ifc.entities.base.Base`
            The entity to show. If None, the entire project will be shown.
        """
        try:
            from compas_viewer import Viewer
            from compas_viewer.components import Treeform

        except ImportError:
            raise ImportError("The show method requires compas_viewer to be installed.")

        viewer = Viewer()
        print(f"Unit: {self.unit}")
        viewer.unit = self.unit
        viewer.ui.sidebar.show_objectsetting = False

        entity_map = {}

        def parse_entity(entity, parent=None):
            obj = None
            name = f"[{entity.__class__.__name__}]{entity.Name}"
            transformation = Transformation.from_frame(entity.frame) if entity.frame else None
            if getattr(entity, "geometry", None) and not entity.is_a("IfcSpace"):
                obj = viewer.scene.add(entity.geometry, name=name, parent=parent, hide_coplanaredges=True, **entity.style)
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
            treeform.update_from_dict({"Attributes": entity.attributes, "PSets": getattr(entity, "property_sets", {})})

        viewer.ui.sidebar.sceneform.callback = update_treeform

        viewer.show()

    def create(
        self, cls: str = "IfcBuildingElementProxy", parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs
    ) -> "Base":
        """
        Create an entity in this model.

        Parameters
        ----------
        cls : str
            The class of the entity to create. Defaults to an `IfcBuildingElementProxy`.
        parent : :class:`compas_ifc.entities.base.Base`
            The parent entity of the new entity.
        geometry : :class:`compas.geometry.Geometry` or :class:`compas.datastructures.Datastructure`
            The geometry of the new entity.
        frame : :class:`compas.geometry.Frame`
            The placement frame of the new entity.
        properties : dict
            The custom property sets to be added to the new entity.
        **kwargs
            Additional keyword arguments to be added to the new entity.

        Returns
        -------
        :class:`compas_ifc.entities.base.Base`
            The newly created entity.

        """
        return self.file.create(cls=cls, parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_value(self, value):
        return self.file.create_value(value)

    def create_default_project(self) -> "IfcProject":
        """Create a default project in this model if one does not exist."""
        return self.file.default_project

    def remove(self, entity: Union["Base", list["Base"]]):
        """
        Remove an entity from this model.

        Parameters
        ----------
        entity : :class:`compas_ifc.entities.base.Base` or list[:class:`compas_ifc.entities.base.Base`]
            The entity or entities to remove.

        """
        self.file.remove(entity)

    def update_linear_deflection(self):
        """Update the linear deflection tolerance settings in COMPAS based on the unit of the model."""
        # TODO: deal with conversion based units like "FOOT"
        if self.unit == "mm":
            TOL.lineardeflection = 1
        elif self.unit == "cm":
            TOL.lineardeflection = 1e-1
        elif self.unit == "m":
            TOL.lineardeflection = 1e-3

    @classmethod
    def template(cls, schema: str = "IFC4", building_count: int = 1, storey_count: int = 1, unit: str = "mm") -> "Model":
        """Create a template model with a default project, site, building, and storey.

        Parameters
        ----------
        schema : str
            The IFC schema to use. Defaults to "IFC4".
        building_count : int
            The number of buildings to create. Defaults to 1.
        storey_count : int
            The number of storeys to create. Defaults to 1.
        unit : str
            The unit of the model. Defaults to "mm".

        Returns
        -------
        :class:`compas_ifc.model.Model`
            The newly created model.
        """
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

    # Helper functions to create specific IFC entities

    def create_wall(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a wall in this model."""
        return self.file.create(cls="IfcWall", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_slab(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a slab in this model."""
        return self.file.create(cls="IfcSlab", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_roof(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a roof in this model."""
        return self.file.create(cls="IfcRoof", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_window(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a window in this model."""
        return self.file.create(cls="IfcWindow", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_door(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a door in this model."""
        return self.file.create(cls="IfcDoor", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_column(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a column in this model."""
        return self.file.create(cls="IfcColumn", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_beam(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a beam in this model."""
        return self.file.create(cls="IfcBeam", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_railing(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a railing in this model."""
        return self.file.create(cls="IfcRailing", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def create_stair(self, parent: "Base" = None, geometry: Union[Geometry, Datastructure] = None, frame: Frame = None, properties: dict = None, **kwargs) -> "Base":
        """Create a stair in this model."""
        return self.file.create(cls="IfcStair", parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)
