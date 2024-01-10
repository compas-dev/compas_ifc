"""
- Representation
- Placement
"""


model = IfcModel("...")
project = model.project
building = model.buildins[0]
wall = building.walls[0]
window = building.windows[0]
...