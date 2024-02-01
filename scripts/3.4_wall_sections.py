from compas_viewer import Viewer
from compas.geometry import Plane
from compas_ifc.model import Model


model = Model("data/wall-with-opening-and-window.ifc")
viewer = Viewer()

sectionPlane = Plane([0, 0, 1], [0, 0, 1])

for wall in model.get_entities_by_type("IfcWall"):
    print("Converting brep:", wall)
    viewer.add(wall.body_with_opening, name="{}.Body".format(wall.name), opacity=0.5)

    print("creating section...")
    sections = []
    for shape in wall.body_with_opening:
        brep = shape.slice(sectionPlane)
        sections.append(shape.slice(sectionPlane))

    viewer.add(sections, name="{}.Sections".format(wall.name), linecolor=(1, 0, 0), linewidth=5, show_lines=True)

print("Finished")
viewer.show()
