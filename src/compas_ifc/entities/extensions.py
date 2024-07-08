class IfcObjectDefinition:
    def test(self):
        print("test")


class IfcBuilding:
    def test2(self):
        print("test2")


EXTENSIONS = {
    "IfcObjectDefinition": IfcObjectDefinition,
    "IfcBuilding": IfcBuilding,
}
