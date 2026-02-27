from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel(filepath="data/Duplex_A_20110907.ifc", use_occ=True)

total_wall_volume = sum(e.volume for e in model.get_elements_by_type("IfcWall") if e.volume)
print("Total wall volume:", total_wall_volume, f"{model.unit}³")

total_slab_volume = sum(e.volume for e in model.get_elements_by_type("IfcSlab") if e.volume)
print("Total slab volume:", total_slab_volume, f"{model.unit}³")
