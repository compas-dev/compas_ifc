import os

from compas_view2.app import App
from compas_view2.app import Controller
from qtpy import QtCore
from qtpy import QtWidgets

from compas_ifc.attributes import attribute_enumeration_items
from compas_ifc.attributes import is_attribute_enumeration
from compas_ifc.entities.entity import Entity
from compas_ifc.model import Model

# i guess this import is to trigger registrations?
from compas_ifc.viewer import objects  # noqa: F401

HERE = os.path.dirname(__file__)
CONFIG = os.path.join(HERE, "config.json")


class IFCController(Controller):
    # Model

    def new_model(self):
        self.app.warning("Coming soon...")

    def load_model(self):
        self.app.warning("Coming soon...")

    def save_model(self):
        self.app.warning("Coming soon...")

    def saveas_model(self):
        self.app.warning("Coming soon...")

    def export_model(self):
        self.app.warning("Coming soon...")


class IFC_viewer(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, config=CONFIG, controller_class=IFCController, title="COMPAS IFC", **kwargs)
        self.ifc = None

        # extra = {"density_scale": "-1"}
        # apply_stylesheet(self._app, theme="dark_blue.xml", extra=extra)
        self.on_object_selected += [self.on_entityobj_selected]
        self.create_tabs()

    def create_tabs(self):
        containerwidget = QtWidgets.QWidget()
        tabwidget = QtWidgets.QTabWidget()
        tabwidget.addTab(self.view, "3D")
        tabwidget.addTab(self.IFC_form(), "IFC")
        tabwidget.addTab(QtWidgets.QWidget(), "JSON")
        tabwidget.addTab(QtWidgets.QWidget(), "Data")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabwidget)
        containerwidget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.window.setCentralWidget(containerwidget)

        def on_tab_changed(index):
            if index == 0:
                self.show_forms()
            else:
                self.close_forms()

        tabwidget.currentChanged.connect(on_tab_changed)

    def IFC_form(self):
        scroll = QtWidgets.QScrollArea()
        content = QtWidgets.QLabel()
        content.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        content.setContentsMargins(10, 10, 10, 10)
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        self.ifc_content = content
        return scroll

    def open(self, path, model_cls=Model):
        self.ifc_content.setText(open(path, "r").read())
        self.model = model_cls(path)

    def add_hierachy(self, entity: Entity, **kwargs):
        parent = entity.parent
        chain = []

        while parent:
            chain.append(parent)
            parent = parent.parent

        chain.reverse()
        chain.append(entity)

        parent = self
        for i, entity in enumerate(chain):
            existed = [obj for obj in self.view.objects.values() if obj.entity == entity]
            if existed:
                print(" " * i, "->", entity, "already exists")
                parent = existed[0]
            else:
                print(" " * i, "->", entity)
                parent = parent.add(entity, **kwargs)
                last = parent

        return last

    def add_all(self, **kwargs):
        def add_branch(entity, parent):
            print("Adding", entity)
            obj = parent.add(entity, **kwargs)
            if hasattr(entity, "children"):
                for child in entity.children:
                    add_branch(child, obj)

        for project in self.model.projects:
            add_branch(project, self)

    def on_entityobj_selected(self, selected):
        if selected:
            selected = selected[0]
            while not hasattr(selected, "entity") and selected.parent:
                selected = selected.parent
            if hasattr(selected, "entity"):
                entity = selected.entity
                self.ifc_info_form(entity)
                spatial_treeform = self.dock_slots["spatial"]
                for entry in spatial_treeform.entries:
                    if entry["entity"] == entity:
                        spatial_treeform.select([entry])

    def show_forms(self, entity: Entity = None):
        self.ifc_hierarchy_form()
        self.ifc_info_form(entity)

    def close_forms(self):
        if self.dock_slots.get("spatial"):
            self.dock_slots["spatial"].close()
            del self.dock_slots["spatial"]
        if self.dock_slots.get("info"):
            self.dock_slots["info"].close()
            del self.dock_slots["info"]

    def ifc_hierarchy_form(self):
        def on_item_pressed(form, entry):
            self.ifc_info_form(entry["entity"])
            for obj in self.view.objects.values():
                if getattr(obj, "entity", None) == entry["entity"]:
                    obj.is_selected = True
                    for child in obj.children:
                        child.is_selected = True
                else:
                    obj.is_selected = False
            self.view.update()

        def add_branch(objs):
            branch = []
            for obj in objs:
                if hasattr(obj, "entity"):
                    entity = obj.entity
                    node_item = {
                        "name": f"{entity.name} ({entity.ifc_type})",
                        "entity": entity,
                        "children": add_branch(obj.children),
                        "expanded": True,
                        "on_item_pressed": on_item_pressed,
                    }

                    branch.append(node_item)
            return branch

        root_objs = [obj for obj in self.view.objects if obj.parent is None]
        spatial_structure = add_branch(root_objs)

        return self.treeform(
            "Spatial Structure",
            spatial_structure,
            slot="spatial",
            location="right",
            columns=["name"],
            show_headers=False,
            striped_rows=True,
        )

    def get_enum_options(self, entity: Entity):
        enum_options = {}
        etype = entity._entity.is_a()
        declaration = entity.model.schema.declaration_by_name(etype)
        for a in declaration.attributes():
            if is_attribute_enumeration(a):
                enum_options[a.name()] = list(attribute_enumeration_items(a))
        return enum_options

    def attribute_tab(self, entity: Entity = None):
        attributes = []
        if entity:
            if entity._entity is not None:
                enum_options = self.get_enum_options(entity)

                def expand_dict(dict_entry):
                    attributes = []
                    for name, value in dict_entry.items():

                        def on_item_edited(form, entry, column, value):
                            dict_entry[entry["name"]] = value

                        if isinstance(value, dict):
                            attributes.append({"name": name, "children": expand_dict(value)})
                        else:
                            if name in enum_options:
                                value = {"value": value, "options": enum_options[name]}
                            attributes.append(
                                {
                                    "name": name,
                                    "value": value,
                                    "on_item_edited": on_item_edited,
                                }
                            )
                    return attributes

                attributes = expand_dict(entity.attributes)

            else:
                attributes = [{"name": name, "value": value} for name, value in entity.attributes.items()]

        return {
            "name": "Attributes",
            "data": attributes,
            "columns": [
                {"name": "name", "key": "name"},
                {"name": "value", "key": "value", "editable": True},
            ],
        }

    def property_tab(self, entity: Entity = None):
        properties = []
        if entity:
            for pset_name, pset in entity.psets.items():
                for name, value in pset.items():
                    properties.append({"name": name, "value": value, "source": pset_name})

            properties = sorted(properties, key=lambda x: x["name"])

        return {
            "name": "Properties",
            "data": properties,
            "columns": [
                {"name": "name", "key": "name"},
                {"name": "value", "key": "value", "editable": True},
                {"name": "source", "key": "source"},
            ],
        }

    def ifc_info_tabs(self, entity: Entity = None):
        return [self.attribute_tab(entity), self.property_tab(entity)]

    def ifc_info_form(self, entity: Entity = None):
        return self.tabsform(
            "Info",
            self.ifc_info_tabs(entity),
            slot="info",
            location="right",
            columns=["name", "value", "source"],
            striped_rows=True,
        )
