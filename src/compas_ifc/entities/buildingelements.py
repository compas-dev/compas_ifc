from compas_model.models import Model
from compas_model.elements import Element


class BuildingModel(Model):
    # This class will maintain and update a IFC file underneath.

    def __init__(self, filepath=None, **kwargs):

        from compas_ifc.file import IFCFile

        # The model will start an empty IFC file if not provided.
        super().__init__(**kwargs)
        self.file = IFCFile(None, filepath=filepath)
        self.load_hierarchy()

    def load_hierarchy(self):

        self.project = self.file.get_entities_by_type("IfcProject")[0]

        def load_recursively(entity, parent=None):
            for child in entity.children:
                name = f"{child.Name}[{child.is_a()}]"
                element = BuildingElement(ifc_entity=child, name=name, model=self)
                self.add_element(element, parent=parent)
                load_recursively(child, element)

        load_recursively(self.project)

    def show(self):
        from compas_viewer import Viewer
        from compas_viewer.components import Treeform

        viewer = Viewer()
        viewer.ui.sidebar.show_objectsetting = False

        viewer.scene.add(self)

        treeform = Treeform()
        viewer.ui.sidebar.widget.addWidget(treeform)

        def update_treeform(form, obj):
            treeform.update_from_dict({"Attributes": obj.element.ifc_attributes, "PSets": obj.element.ifc_psets})

        viewer.ui.sidebar.sceneform.callback = update_treeform

        viewer.show()


class BuildingElement(Element):
    def __init__(self, ifc_entity=None, model=None, **kwargs):
        super().__init__(**kwargs)

        self.model = model
        self.ifc_entity = ifc_entity  # Read-only, underlying IFC entity.

        # self.material = None # There needs to be some mapping mechanism between the material class and Qtos in IFC.

        # links to parents
        # self.storey = None
        # self.building = None

    @property
    def ifc_attributes(self):
        return self.ifc_entity.attributes

    @property
    def ifc_psets(self):
        return self.ifc_entity.property_sets

    @property
    def ifc_type(self):
        return self.ifc_entity.is_a()

    @property
    def geometry(self):
        return self.ifc_entity.geometry

    @property
    def transformation(self):
        # TODO: this is not 100% correct
        return self.ifc_entity.frame.to_transformation()



# TODO: Transparent way to work with grid and storeys etc.
