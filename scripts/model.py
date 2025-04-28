from compas_ifc.entities.buildingelements import BuildingModel

model = BuildingModel(filepath="data/Duplex_A_20110907.ifc")
# print(model.tree.get_hierarchy_string(max_depth=10))

model.show()

