"""Test combined graph + extraction: extract all walls connected to a given wall."""

import os

from compas_ifc.bim import BuildingInformationModel

os.makedirs("temp", exist_ok=True)

# ========================================
# Load Duplex model
# ========================================
print("Loading Duplex model...")
model = BuildingInformationModel(filepath="data/Duplex_A_20110907.ifc", load_geometries=False)

# ========================================
# 1. Pick a seed wall
# ========================================
print("\n=== 1. Pick a seed wall ===")
walls = model.get_elements_by_type("IfcWall") + model.get_elements_by_type("IfcWallStandardCase")
print(f"Total walls: {len(walls)}")

seed = walls[0]
print(f"Seed wall: {seed.ifc_type} '{seed.name}'")

# ========================================
# 2. Find all connected walls via graph
# ========================================
print("\n=== 2. Find connected walls ===")

# Walk the connection graph from the seed wall
visited = set()
frontier = [seed]
connected_walls = []

while frontier:
    current = frontier.pop()
    if id(current) in visited:
        continue
    visited.add(id(current))
    connected_walls.append(current)

    # Find neighbors via connection edges
    node = current.graphnode
    for edge in model.connections:
        u, v = edge
        if u == node:
            neighbor = model.graph.node_element(v)
        elif v == node:
            neighbor = model.graph.node_element(u)
        else:
            continue

        if id(neighbor) not in visited:
            frontier.append(neighbor)

print(f"Connected cluster size: {len(connected_walls)}")
for w in connected_walls:
    print(f"  {w.ifc_type} '{w.name}'")

# ========================================
# 3. Extract connected walls
# ========================================
print("\n=== 3. Extract connected walls ===")
extracted = model.extract(connected_walls, path="temp/connected_walls.ifc", load_geometries=False)
extracted.print_hierarchy(max_depth=3)

ex_walls = extracted.get_elements_by_type("IfcWall") + extracted.get_elements_by_type("IfcWallStandardCase")
print(f"\nExtracted walls: {len(ex_walls)}")
print(f"Expected: {len(connected_walls)}")
print(f"Match: {len(ex_walls) == len(connected_walls)}")

# Verify linked info
print("\nLinked info check:")
for w in ex_walls[:3]:
    print(f"  {w.name}")
    print(f"    Properties: {bool(w.properties)}")
    print(f"    Style: {bool(w._resolve_style())}")

# ========================================
# 4. Verify graph in extracted model
# ========================================
print("\n=== 4. Graph in extracted model ===")
print(f"Connection edges: {len(extracted.connections)}")

print("\nDone!")
