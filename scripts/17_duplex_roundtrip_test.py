"""
17 Duplex Round-Trip Test
==========================

Loads the real-world Duplex model (IFC2X3) via the BuildingInformationModel
API, verifies geometry parsing for all elements, then exports a subset and
validates the round-trip.

Tests:
  1. Load & parse: all 265 elements with geometry should parse correctly
  2. Geometry type distribution: Extrusion majority, Mesh, TessellatedBrep
  3. Extrusion parametric data: profile types, depth, direction, frame
  4. Axis representations: 65 elements should have axis polylines
  5. Instancing: 60 IfcRepresentationMap, 167 IfcMappedItem — all parse
  6. Spatial hierarchy: 4 storeys with correct parent structure
  7. Interaction graph: voids, fills, connections, space boundaries
  8. Export round-trip: extract a storey, save, reload, verify
"""

import os
import sys

from compas.datastructures import Mesh
from compas.geometry import Circle, Polygon

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import Extrusion

# ==================================================================
# Load model
# ==================================================================

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

pass_count = 0
fail_count = 0
results = []


def check(label, condition, detail=""):
    global pass_count, fail_count
    status = "PASS" if condition else "FAIL"
    if condition:
        pass_count += 1
    else:
        fail_count += 1
    results.append((status, label, detail))
    return condition


# ==================================================================
# 1. Geometry parsing — all elements
# ==================================================================

print("=" * 70)
print("1. GEOMETRY PARSING")
print("=" * 70)

type_counts = {}
geom_count = 0
parse_errors = 0

for elem in model.building_elements:
    try:
        geom = elem.geometry
    except Exception as e:
        parse_errors += 1
        continue
    if geom is None:
        continue
    geom_count += 1
    tn = type(geom).__name__
    type_counts[tn] = type_counts.get(tn, 0) + 1

print(f"  Elements with geometry: {geom_count}")
print(f"  Parse errors: {parse_errors}")
for name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    pct = count / geom_count * 100 if geom_count else 0
    print(f"    {name:25s} {count:4d}  ({pct:.1f}%)")
print()

check("Total geometries parsed", geom_count >= 260, f"{geom_count} elements")
check("No parse errors", parse_errors == 0, f"{parse_errors} errors")
check("Extrusion is dominant type", type_counts.get("Extrusion", 0) >= 190,
      f"{type_counts.get('Extrusion', 0)} extrusions")
check("Mesh elements present", type_counts.get("Mesh", 0) >= 60,
      f"{type_counts.get('Mesh', 0)} meshes")

# ==================================================================
# 2. Extrusion parametric data
# ==================================================================

print("=" * 70)
print("2. EXTRUSION PARAMETRIC DATA")
print("=" * 70)

profile_types = {}
depth_range = [float("inf"), 0]
valid_extrusions = 0

for elem in model.building_elements:
    geom = elem.geometry
    if not isinstance(geom, Extrusion):
        continue
    valid_extrusions += 1

    # Profile classification
    p = geom.profile
    if isinstance(p, Circle):
        ptype = "Circle"
    elif isinstance(p, Polygon):
        ptype = f"Polygon({len(p.points)}pts)"
    elif isinstance(p, tuple):
        ptype = f"WithVoids({len(p[1])})"
    else:
        ptype = type(p).__name__
    profile_types[ptype] = profile_types.get(ptype, 0) + 1

    # Depth range
    d = geom.depth
    depth_range[0] = min(depth_range[0], d)
    depth_range[1] = max(depth_range[1], d)

    # Validate frame is not None
    if geom.frame is None:
        valid_extrusions -= 1

print(f"  Valid extrusions: {valid_extrusions}")
print(f"  Depth range: {depth_range[0]:.3f} to {depth_range[1]:.3f}")
print(f"  Profile types:")
for t, c in sorted(profile_types.items(), key=lambda x: -x[1]):
    print(f"    {t:25s} {c:4d}")
print()

check("All extrusions have valid frame", valid_extrusions == type_counts.get("Extrusion", 0),
      f"{valid_extrusions}/{type_counts.get('Extrusion', 0)}")
check("Polygon(4pts) is most common", profile_types.get("Polygon(4pts)", 0) >= 140,
      f"{profile_types.get('Polygon(4pts)', 0)} rectangular")
check("All depths are positive", depth_range[0] > 0, f"min depth={depth_range[0]:.6f}")

# ==================================================================
# 3. Axis representations
# ==================================================================

print("=" * 70)
print("3. AXIS REPRESENTATIONS")
print("=" * 70)

axis_count = 0
axis_types = {}

for elem in model.building_elements:
    if elem.ifc_entity is None:
        continue
    axis = elem.ifc_entity.axis
    if axis is None:
        continue
    axis_count += 1
    axis_types[elem.ifc_type] = axis_types.get(elem.ifc_type, 0) + 1

    # Validate axis has at least 2 points
    if len(axis.points) < 2:
        axis_count -= 1

print(f"  Elements with axis: {axis_count}")
for t, c in sorted(axis_types.items(), key=lambda x: -x[1]):
    print(f"    {t:35s} {c:4d}")
print()

check("Axis count matches expected", axis_count >= 60, f"{axis_count} axes")
check("Walls have most axes", axis_types.get("IfcWallStandardCase", 0) >= 50,
      f"{axis_types.get('IfcWallStandardCase', 0)} wall axes")

# ==================================================================
# 4. Instancing (IfcRepresentationMap + IfcMappedItem)
# ==================================================================

print("=" * 70)
print("4. INSTANCING")
print("=" * 70)

rep_maps = model.file.get_entities_by_type("IfcRepresentationMap")
mapped_items = model.file.get_entities_by_type("IfcMappedItem")

print(f"  IfcRepresentationMap: {len(rep_maps)}")
print(f"  IfcMappedItem:        {len(mapped_items)}")

# Verify mapped items parse correctly
mapped_parse_ok = 0
mapped_parse_fail = 0
for elem in model.building_elements:
    if elem.ifc_entity is None:
        continue
    rep = elem.ifc_entity.Representation
    if rep is None:
        continue
    for shape_rep in rep.Representations:
        if shape_rep.RepresentationType == "MappedRepresentation":
            try:
                geom = elem.geometry
                if geom is not None:
                    mapped_parse_ok += 1
                else:
                    mapped_parse_fail += 1
            except Exception:
                mapped_parse_fail += 1
            break

print(f"  Mapped items parsed OK: {mapped_parse_ok}")
print(f"  Mapped items failed:    {mapped_parse_fail}")
print()

check("RepresentationMap count", len(rep_maps) >= 55, f"{len(rep_maps)} maps")
check("MappedItem count", len(mapped_items) >= 160, f"{len(mapped_items)} items")
check("All mapped items parse", mapped_parse_fail == 0, f"{mapped_parse_fail} failures")

# ==================================================================
# 5. Spatial hierarchy
# ==================================================================

print("=" * 70)
print("5. SPATIAL HIERARCHY")
print("=" * 70)

sites = model.sites
buildings = model.buildings
storeys = model.storeys

print(f"  Sites:     {len(sites)}")
print(f"  Buildings: {len(buildings)}")
print(f"  Storeys:   {len(storeys)}")
for s in storeys:
    children_count = len(s.children)
    print(f"    {s.name}: {children_count} children")
print()

check("One site", len(sites) == 1)
check("One building", len(buildings) == 1)
check("Four storeys", len(storeys) == 4, f"{len(storeys)} storeys")
check("All storeys have children", all(len(s.children) > 0 for s in storeys))

# ==================================================================
# 6. Interaction graph
# ==================================================================

print("=" * 70)
print("6. INTERACTION GRAPH")
print("=" * 70)

voids = model.voids
fills = model.fills
connections = model.connections
space_boundaries = model.space_boundaries

print(f"  Voids:            {len(voids)}")
print(f"  Fills:            {len(fills)}")
print(f"  Connections:      {len(connections)}")
print(f"  Space boundaries: {len(space_boundaries)}")
print()

check("Voids present (openings)", len(voids) >= 40, f"{len(voids)} voids")
check("Fills present (doors/windows)", len(fills) >= 30, f"{len(fills)} fills")
check("Connections present", len(connections) >= 70, f"{len(connections)} connections")
check("Space boundaries present", len(space_boundaries) >= 180, f"{len(space_boundaries)} boundaries")

# ==================================================================
# 7. Extract round-trip
# ==================================================================

print("=" * 70)
print("7. EXTRACT ROUND-TRIP")
print("=" * 70)

# Pick the first storey with the most building elements
target_storey = max(storeys, key=lambda s: len(s.children))
original_count = len([c for c in target_storey.children if not c.is_spatial])

print(f"  Extracting storey: {target_storey.name} ({original_count} elements)")

os.makedirs("temp", exist_ok=True)
extract_path = "temp/duplex_extract_test.ifc"

extracted = model.extract(target_storey, path=extract_path)

# Count elements in extracted model
extracted_elements = extracted.building_elements
extracted_geom_count = sum(1 for e in extracted_elements if e.geometry is not None)

print(f"  Extracted elements:           {len(extracted_elements)}")
print(f"  Extracted with geometry:      {extracted_geom_count}")
print()

check("Extract has elements", len(extracted_elements) >= original_count * 0.8,
      f"{len(extracted_elements)} vs {original_count} original")
check("Extract geometries parse", extracted_geom_count > 0,
      f"{extracted_geom_count} parsed")

# Verify geometry types preserved
ext_type_counts = {}
for elem in extracted_elements:
    geom = elem.geometry
    if geom is None:
        continue
    tn = type(geom).__name__
    ext_type_counts[tn] = ext_type_counts.get(tn, 0) + 1

if ext_type_counts:
    print("  Extracted geometry types:")
    for name, count in sorted(ext_type_counts.items(), key=lambda x: -x[1]):
        print(f"    {name:25s} {count:4d}")
    print()

    check("Extrusions in extract", ext_type_counts.get("Extrusion", 0) > 0,
          f"{ext_type_counts.get('Extrusion', 0)} extrusions")

# ==================================================================
# Summary
# ==================================================================

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print()

for status, label, detail in results:
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status:<6} {label}{suffix}")

print()
print(f"  {pass_count} PASS / {fail_count} FAIL  (of {pass_count + fail_count} checks)")
print()

if fail_count == 0:
    print("SUCCESS: All Duplex round-trip tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
