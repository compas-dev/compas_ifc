"""
- Representation
- Placement
"""


model = IfcModel("...")

wall = model.get_by_type("IfcWall")[0]
wall.summary()

wall.representations