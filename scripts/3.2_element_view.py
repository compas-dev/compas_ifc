from compas_viewer import Viewer
from compas_ifc.model import Model

# model = Model("data/wall-with-opening-and-window.ifc")
model = Model("temp/Duplex_A_20110907.ifc")
viewer = Viewer(rendermode="lighted")

for entity in model.get_entities_by_type("IfcBuildingElement"):
    print("Converting:", entity)

    # for a in entity.body:
    #     obj = viewer.add(a, name="{}.Body".format(entity.name))
    
    # for a in entity.opening:
    #     obj = viewer.add(a, name="{}.opening".format(entity.name))
    
    for a in entity.body_with_opening:
        obj = viewer.add(a, name="{}.opening".format(entity.name))

viewer.show()
