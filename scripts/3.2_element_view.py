from compas_ifc.bim import BuildingInformationModel

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")
# model.get_elements_by_type("IfcWindow")[0].show()


# "1hOSvn6df7F8_7GcBWlRrM"

# "1hOSvn6df7F8_7GcBWlRqU"

element1 = model.get_element_by_global_id("1hOSvn6df7F8_7GcBWlRrM")
element2 = model.get_element_by_global_id("1hOSvn6df7F8_7GcBWlRqU")

model.show(elements=[element1, element2])