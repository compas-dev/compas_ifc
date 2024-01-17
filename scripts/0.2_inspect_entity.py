"""
IFC entities always have these three aspects:
- attributes
- properties
- relationships
- (geometry)
"""

from compas_ifc._model import IfcModel
from compas_ifc.entities.generated import IfcWall


model = IfcModel("data/wall-with-opening-and-window.ifc")

model.building_elements[0].print_spatial_hierarchy()

# entity = model.get_by_type("IfcWall")[0]

# entity.print_attributes(max_depth=2)

# wall.properties.print()

# wall.hierarchy.print(include_acestors=True, include_descendants=True)
