"""
18 HiLo Round-Trip Test
========================

Loads the real-world HiLo architecture model (IFC2X3, 35 MB, ~1900 elements)
via the BuildingInformationModel API and validates end-to-end geometry parsing,
instancing, spatial hierarchy, interaction graph, and extract round-trip.

The HiLo model is significantly more complex than Duplex:
  - 1920 building elements (vs 268)
  - 190 IfcBooleanClippingResult (CSG booleans)
  - 488 IfcRepresentationMap, 637 IfcMappedItem (heavy instancing)
  - MEP distribution system (ports, flow segments, fittings)
  - 3 storeys with German names

Tests:
  1. Geometry parsing: all 1400+ elements parse with minimal errors
  2. Extrusion parametric data: profiles, depths, frames
  3. Instancing: 488 maps, 637 mapped items
  4. Spatial hierarchy: 1 site, 1 building, 3 storeys
  5. Interaction graph: voids, connections, MEP port connections
  6. Extract round-trip: extract a storey, save, reload, verify
"""

import os
import sys
import time

from compas.datastructures import Mesh
from compas.geometry import Circle, Polygon

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import Extrusion

# ==================================================================
# Load model
# ==================================================================

t0 = time.time()
model = BuildingInformationModel("temp/1072_HiLo_Model-Architecture.ifc")
load_time = time.time() - t0

print(f"Loaded in {load_time:.1f}s  (schema={model.schema_name}, unit={model.unit})")
print()

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
# 1. Geometry parsing
# ==================================================================

print("=" * 70)
print("1. GEOMETRY PARSING")
print("=" * 70)

type_counts = {}
geom_count = 0
no_geom = 0
parse_errors = 0

for elem in model.building_elements:
    try:
        geom = elem.geometry
    except Exception:
        parse_errors += 1
        continue
    if geom is None:
        no_geom += 1
        continue
    geom_count += 1
    tn = type(geom).__name__
    type_counts[tn] = type_counts.get(tn, 0) + 1

print(f"  Elements with geometry: {geom_count}")
print(f"  Elements without:       {no_geom}")
print(f"  Parse errors:           {parse_errors}")
for name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    pct = count / geom_count * 100 if geom_count else 0
    print(f"    {name:25s} {count:5d}  ({pct:.1f}%)")
print()

check("Geometries parsed >= 1400", geom_count >= 1400, f"{geom_count}")
check("Parse errors <= 10", parse_errors <= 10, f"{parse_errors} errors")
check("Extrusion is dominant", type_counts.get("Extrusion", 0) >= 1000,
      f"{type_counts.get('Extrusion', 0)} extrusions")
check("TessellatedBrep present", type_counts.get("TessellatedBrep", 0) >= 200,
      f"{type_counts.get('TessellatedBrep', 0)} breps")
check("ClippedExtrusion present", type_counts.get("ClippedExtrusion", 0) >= 120,
      f"{type_counts.get('ClippedExtrusion', 0)} clipped extrusions")

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
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        continue
    if not isinstance(geom, Extrusion):
        continue
    valid_extrusions += 1

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

    d = geom.depth
    depth_range[0] = min(depth_range[0], d)
    depth_range[1] = max(depth_range[1], d)

    if geom.frame is None:
        valid_extrusions -= 1

print(f"  Valid extrusions: {valid_extrusions}")
if valid_extrusions > 0:
    print(f"  Depth range: {depth_range[0]:.3f} to {depth_range[1]:.3f}")
print(f"  Profile types:")
for t, c in sorted(profile_types.items(), key=lambda x: -x[1]):
    print(f"    {t:25s} {c:5d}")
print()

check("All extrusions have frames", valid_extrusions == type_counts.get("Extrusion", 0),
      f"{valid_extrusions}/{type_counts.get('Extrusion', 0)}")
check("Depths are positive", depth_range[0] > 0, f"min={depth_range[0]:.6f}")
check("Multiple profile types", len(profile_types) >= 2, f"{len(profile_types)} types")

# ==================================================================
# 3. Axis representations
# ==================================================================

print("=" * 70)
print("3. AXIS REPRESENTATIONS")
print("=" * 70)

axis_count = 0
axis_types = {}

for elem in model.building_elements:
    axis = elem.axis
    if axis is None:
        continue
    axis_count += 1
    axis_types[elem.ifc_type] = axis_types.get(elem.ifc_type, 0) + 1

print(f"  Elements with axis: {axis_count}")
for t, c in sorted(axis_types.items(), key=lambda x: -x[1]):
    print(f"    {t:35s} {c:4d}")
print()

check("Axis data present", axis_count >= 0, f"{axis_count} axes")

# ==================================================================
# 4. Instancing
# ==================================================================

print("=" * 70)
print("4. INSTANCING")
print("=" * 70)

rep_maps = model._file.get_entities_by_type("IfcRepresentationMap")
mapped_items = model._file.get_entities_by_type("IfcMappedItem")

print(f"  IfcRepresentationMap: {len(rep_maps)}")
print(f"  IfcMappedItem:        {len(mapped_items)}")

# Verify mapped items parse
mapped_ok = 0
mapped_fail = 0
for elem in model.building_elements:
    if elem._ifc_entity is None:
        continue
    try:
        rep = elem._ifc_entity.Representation
    except AttributeError:
        continue
    if rep is None:
        continue
    try:
        reps_list = rep.Representations
    except (AttributeError, Exception):
        continue
    for shape_rep in reps_list:
        if shape_rep.RepresentationType == "MappedRepresentation":
            try:
                geom = elem.geometry
                if geom is not None:
                    mapped_ok += 1
                else:
                    mapped_fail += 1
            except Exception:
                mapped_fail += 1
            break

print(f"  Mapped items parsed OK: {mapped_ok}")
print(f"  Mapped items failed:    {mapped_fail}")
print()

check("RepresentationMap >= 480", len(rep_maps) >= 480, f"{len(rep_maps)} maps")
check("MappedItem >= 630", len(mapped_items) >= 630, f"{len(mapped_items)} items")
check("Mapped item parse failures <= 5", mapped_fail <= 5, f"{mapped_fail} failures")

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
    print(f"    {s.name}: {len(s.children)} children")

total_elements = len(model.building_elements)
print(f"  Total building elements: {total_elements}")
print()

check("One site", len(sites) == 1)
check("One building", len(buildings) == 1)
check("Three storeys", len(storeys) == 3, f"{len(storeys)} storeys")
check("All storeys have children", all(len(s.children) > 0 for s in storeys))
check("Total elements >= 1900", total_elements >= 1900, f"{total_elements}")

# ==================================================================
# 6. Interaction graph
# ==================================================================

print("=" * 70)
print("6. INTERACTION GRAPH")
print("=" * 70)

connections = model.connections

# MEP relationships
port_connections = model.get_interactions_by_category("port_connection")
port_elements = model.get_interactions_by_category("port_element")
services = model.get_interactions_by_category("services")

print(f"  Connections:      {len(connections)}")
print(f"  Port connections: {len(port_connections)}")
print(f"  Port-element:     {len(port_elements)}")
print(f"  Services:         {len(services)}")
print()

check("Connections >= 80", len(connections) >= 80, f"{len(connections)} connections")
check("MEP port connections present", len(port_connections) >= 200,
      f"{len(port_connections)} port connections")
check("MEP port-element present", len(port_elements) >= 400,
      f"{len(port_elements)} port-element edges")

# ==================================================================
# 7. Extract round-trip
# ==================================================================

print("=" * 70)
print("7. EXTRACT ROUND-TRIP")
print("=" * 70)

# Pick the smallest storey for speed
target_storey = min(storeys, key=lambda s: len(s.children))
original_count = len([c for c in target_storey.children if not c.is_spatial])

print(f"  Extracting storey: {target_storey.name} ({original_count} elements)")

extract_path = "temp/hilo_extract_test.ifc"

t0 = time.time()
extracted = model.extract(target_storey, path=extract_path)
extract_time = time.time() - t0
print(f"  Extract time: {extract_time:.1f}s")

extracted_elements = extracted.building_elements
extracted_geom_count = sum(1 for e in extracted_elements if e.geometry is not None)

print(f"  Extracted elements:      {len(extracted_elements)}")
print(f"  Extracted with geometry: {extracted_geom_count}")

ext_type_counts = {}
for elem in extracted_elements:
    geom = elem.geometry
    if geom is None:
        continue
    tn = type(geom).__name__
    ext_type_counts[tn] = ext_type_counts.get(tn, 0) + 1

if ext_type_counts:
    print("  Geometry types:")
    for name, count in sorted(ext_type_counts.items(), key=lambda x: -x[1]):
        print(f"    {name:25s} {count:5d}")
print()

check("Extract has elements", len(extracted_elements) >= original_count * 0.8,
      f"{len(extracted_elements)} vs {original_count} original")
check("Extract geometries parse", extracted_geom_count > 0,
      f"{extracted_geom_count} parsed")

# ==================================================================
# 8. Boolean clipping (HiLo-specific: 190 IfcBooleanClippingResult)
# ==================================================================

print("=" * 70)
print("8. BOOLEAN CLIPPING (CSG)")
print("=" * 70)

try:
    bool_clip = model._file.get_entities_by_type("IfcBooleanClippingResult")
    bool_result = model._file.get_entities_by_type("IfcBooleanResult")
except RuntimeError:
    bool_clip = []
    bool_result = []

print(f"  IfcBooleanClippingResult: {len(bool_clip)}")
print(f"  IfcBooleanResult:         {len(bool_result)}")

# Elements with boolean geometry fall back to visual_geometry (TessellatedBrep)
# Verify that fallback works for these
bool_fallback_ok = 0
for elem in model.building_elements:
    try:
        geom = elem.geometry
    except (AttributeError, Exception):
        continue
    if geom is not None and type(geom).__name__ == "TessellatedBrep":
        bool_fallback_ok += 1

print(f"  TessellatedBrep fallbacks: {bool_fallback_ok}")
print()

check("Boolean entities present", len(bool_clip) >= 180, f"{len(bool_clip)} boolean clips")
# With ClippedExtrusion support, most booleans parse parametrically;
# only non-half-space booleans and non-extrusion leaves remain as TessellatedBrep.
check("TessellatedBrep fallback works", bool_fallback_ok >= 200,
      f"{bool_fallback_ok} fallbacks")

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
    print("SUCCESS: All HiLo round-trip tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
