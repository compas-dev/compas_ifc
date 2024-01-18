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

entity = model.building_elements[0]
entity.print_attributes(max_depth=2)
entity.print_spatial_hierarchy()
entity.print_properties()
