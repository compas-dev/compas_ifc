from compas_ifc.entities.generated.IFC4 import IfcBuildingElement
from compas_ifc.model import Model


class ExtendedIfcBuildingElement(IfcBuildingElement):
    @property
    def volume(self):
        return self.geometry.volume


model = Model("data/Duplex_A_20110907.ifc", use_occ=True, extensions={"IfcBuildingElement": ExtendedIfcBuildingElement})

total_wall_volume = 0
for wall in model.get_entities_by_type("IfcWall"):
    total_wall_volume += wall.volume

print("Total wall volume:", total_wall_volume, f"{model.unit}³")

total_slab_volume = 0
for slab in model.get_entities_by_type("IfcSlab"):
    total_slab_volume += slab.volume

print("Total slab volume:", total_slab_volume, f"{model.unit}³")
