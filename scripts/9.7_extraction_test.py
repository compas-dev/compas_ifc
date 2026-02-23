"""Test granular export: extract elements with all linked information preserved."""

import os

from compas_ifc.bim import BuildingInformationModel

os.makedirs("temp", exist_ok=True)

# ========================================
# Load Duplex model
# ========================================
print("Loading Duplex model...")
model = BuildingInformationModel(filepath="data/Duplex_A_20110907.ifc")
print(f"Total elements: {len(list(model.elements()))}")
model.print_hierarchy(max_depth=2)

# ========================================
# 1. Extract a single storey
# ========================================
print("\n=== 1. Extract single storey ===")
storey = model.storeys[0]
print(f"Extracting: {storey.ifc_type} '{storey.name}'")
storey_children = list(storey.children)
print(f"Children in source: {len(storey_children)}")

extracted = model.extract(storey, path="temp/extracted_storey.ifc")
extracted.print_hierarchy(max_depth=2)
extracted_elements = list(extracted.elements())
print(f"Extracted elements: {len(extracted_elements)}")

# Verify spatial hierarchy is present
print(f"Sites: {len(extracted.sites)}")
print(f"Buildings: {len(extracted.buildings)}")
print(f"Storeys: {len(extracted.storeys)}")

# Verify geometry preservation
geom_count = sum(1 for e in extracted_elements if e.geometry is not None)
print(f"Elements with geometry: {geom_count}")

# Verify properties preservation
props_count = sum(1 for e in extracted_elements if e.properties)
print(f"Elements with properties: {props_count}")

# Verify styles preservation
style_count = sum(1 for e in extracted_elements if e.style)
print(f"Elements with styles: {style_count}")

# ========================================
# 2. Extract a single element (wall)
# ========================================
print("\n=== 2. Extract single wall ===")
walls = model.get_elements_by_type("IfcWall")
wall = walls[0] if walls else None

if wall:
    print(f"Extracting: {wall.ifc_type} '{wall.name}'")
    print(f"  Geometry: {wall.geometry is not None}")
    print(f"  Properties: {bool(wall.properties)}")
    print(f"  Style: {bool(wall.style)}")

    extracted_wall_model = model.extract(wall, path="temp/extracted_wall.ifc")
    extracted_wall_model.print_hierarchy()

    # Verify the wall's ancestors are present
    ex_walls = extracted_wall_model.get_elements_by_type("IfcWall")
    print(f"Walls in extracted: {len(ex_walls)}")
    for w in ex_walls:
        print(f"  {w.name}")
        print(f"    Geometry: {w.geometry is not None}")
        print(f"    Properties: {bool(w.properties)}")
        print(f"    Style: {bool(w.style)}")

# ========================================
# 3. Extract multiple elements
# ========================================
print("\n=== 3. Extract multiple elements ===")
doors = model.get_elements_by_type("IfcDoor")
windows = model.get_elements_by_type("IfcWindow")
print(f"Doors in source: {len(doors)}")
print(f"Windows in source: {len(windows)}")

selection = doors[:2] + windows[:2]
print(f"Extracting {len(selection)} elements...")
extracted_multi = model.extract(selection, path="temp/extracted_multi.ifc")
extracted_multi.print_hierarchy(max_depth=2)

ex_doors = extracted_multi.get_elements_by_type("IfcDoor")
ex_windows = extracted_multi.get_elements_by_type("IfcWindow")
print(f"Doors in extracted: {len(ex_doors)}")
print(f"Windows in extracted: {len(ex_windows)}")

# ========================================
# 4. Self-containment: reload extracted file
# ========================================
print("\n=== 4. Self-containment (reload extracted storey) ===")
reloaded = BuildingInformationModel(filepath="temp/extracted_storey.ifc")
reloaded_elements = list(reloaded.elements())
print(f"Reloaded elements: {len(reloaded_elements)}")
reloaded_geom = sum(1 for e in reloaded_elements if e.geometry is not None)
print(f"Elements with geometry after reload: {reloaded_geom}")
print(f"Geometry preserved: {reloaded_geom == geom_count}")

# ========================================
# 5. Extract without geometries (lightweight)
# ========================================
print("\n=== 5. Lightweight extraction (no geometry loading) ===")
extracted_light = model.extract(storey, load_geometries=False)
light_elements = list(extracted_light.elements())
print(f"Extracted elements (light): {len(light_elements)}")

print("\nDone!")
