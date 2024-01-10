"""
IFC entities always have these three aspects:
- attributes
- properties
- relationships
- (geometry)
"""


model = IfcModel("...")

wall = model.get_by_type("IfcWall")[0]
wall.summary()

wall.attributes.print(max_depth=2)

wall.properties.print()

wall.hierarchy.print(include_acestors=True, include_descendants=True)
