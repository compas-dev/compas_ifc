from compas_viewer import Viewer
from compas_viewer.layout import Treeform
from compas_ifc.model import Model
from compas_ifc.entities import Entity
from compas.datastructures import Tree, TreeNode

model = Model("data/wall-with-opening-and-window.ifc")


wall = model.get_entities_by_type("IfcWall")[0]


attribute_tree = Tree()
root = TreeNode(name="root")
attribute_tree.add(root)

max_level = 5


def add_attribute_to_tree(entity, parent_node, level=0):
    if level > max_level:
        return

    for key in entity.attributes:
        node = TreeNode(name=key)
        value = entity.attributes[key]
        node.attributes["value"] = str(value)
        parent_node.add(node)

        if isinstance(value, (list, tuple)):
            if isinstance(value[0], Entity):
                for item in value:
                    add_attribute_to_tree(item, node, level=level + 1)
        elif isinstance(value, Entity):
            add_attribute_to_tree(value, node, level=level + 1)


add_attribute_to_tree(wall, root)

viewer = Viewer()
viewer.add(wall.body_with_opening, name=wall.name)
viewer.layout.sidedock.add_element(Treeform(attribute_tree, {"Name": ".name", "Value": ".attributes['value']"}))

viewer.show()
