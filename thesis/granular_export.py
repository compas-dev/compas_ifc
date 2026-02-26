"""
Granular Export Evaluation
==========================

Evaluates the model.extract() method by extracting single-storey subsets
from the Duplex model (IFC2X3, ~295 elements) and verifying that the
exported IFC files are self-contained with correct positioning and valid
hierarchy structure.

  Part 1: Single Storey Extraction — extract each storey, verify hierarchy
  Part 2: Position Preservation — global positions match original model
  Part 3: Discipline Subset — extract only walls, verify subset
  Part 4: Code Conciseness — line count vs direct IfcOpenShell manipulation

Addresses the Collaboration Barrier by enabling granular model sharing:
partners receive only the elements relevant to their scope, in valid IFC
files with auto-generated spatial scaffolding.
"""

import os
import sys

from compas.geometry import Point

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.conversions.frame import IfcLocalPlacement_to_transformation

pass_count = 0
fail_count = 0
results = []

POSITION_TOL = 1e-3  # mm-level tolerance


def check(label, condition, detail=""):
    global pass_count, fail_count
    status = "PASS" if condition else "FAIL"
    if condition:
        pass_count += 1
    else:
        fail_count += 1
    results.append((status, label, detail))
    return condition


def collect_global_positions(element):
    """Collect global_id -> IFC global position for an element and all descendants."""
    positions = {}

    def _walk(elem):
        if elem._ifc_entity is None:
            return
        if not hasattr(elem._ifc_entity, "ObjectPlacement") or not elem._ifc_entity.ObjectPlacement:
            return
        if getattr(elem, "treenode", None) is None:
            return
        T = IfcLocalPlacement_to_transformation(elem._ifc_entity.ObjectPlacement)
        pos = Point(T.matrix[0][3], T.matrix[1][3], T.matrix[2][3])
        positions[elem.global_id] = pos
        for c in elem.children:
            _walk(c)

    _walk(element)
    return positions


def check_positions(extracted_model, original_positions, label_prefix):
    """Check that all elements in extracted model match original global positions."""
    misaligned = 0
    checked = 0
    max_error = 0.0
    for elem in extracted_model.elements():
        if elem._ifc_entity is None:
            continue
        if not hasattr(elem._ifc_entity, "ObjectPlacement") or not elem._ifc_entity.ObjectPlacement:
            continue
        if getattr(elem, "treenode", None) is None:
            continue
        gid = elem.global_id
        if gid not in original_positions:
            continue
        T = IfcLocalPlacement_to_transformation(elem._ifc_entity.ObjectPlacement)
        pos = Point(T.matrix[0][3], T.matrix[1][3], T.matrix[2][3])
        dist = pos.distance_to_point(original_positions[gid])
        checked += 1
        max_error = max(max_error, dist)
        if dist > POSITION_TOL:
            misaligned += 1
    return checked, misaligned, max_error


# ==================================================================
# Load full model
# ==================================================================

print("=" * 70)
print("GRANULAR EXPORT EVALUATION — data/Duplex_A_20110907.ifc")
print("=" * 70)

model = BuildingInformationModel(
    "data/Duplex_A_20110907.ifc",
    load_geometries=False,
)

total_elements = len(list(model.elements()))
storey_count = len(model.storeys)

print(f"\n  Full model: {total_elements} elements, {storey_count} storeys")

# Collect all global positions from original model
all_original_positions = {}
for elem in model.elements():
    if elem._ifc_entity is None:
        continue
    if not hasattr(elem._ifc_entity, "ObjectPlacement") or not elem._ifc_entity.ObjectPlacement:
        continue
    if getattr(elem, "treenode", None) is None:
        continue
    T = IfcLocalPlacement_to_transformation(elem._ifc_entity.ObjectPlacement)
    pos = Point(T.matrix[0][3], T.matrix[1][3], T.matrix[2][3])
    all_original_positions[elem.global_id] = pos

print(f"  Elements with positions: {len(all_original_positions)}")

os.makedirs("temp", exist_ok=True)


# ==================================================================
# PART 1: SINGLE STOREY EXTRACTION
# ==================================================================

print()
print("=" * 70)
print("PART 1: SINGLE STOREY EXTRACTION")
print("=" * 70)


def count_descendants(elem):
    t = 0
    for c in elem.children:
        t += 1 + count_descendants(c)
    return t


print(f"\n  {'Storey':<25s} {'Children':>8s} {'Descendants':>12s}")
print("  " + "-" * 50)
for storey in model.storeys:
    desc = count_descendants(storey)
    print(f"  {storey.name:<25s} {len(storey.children):8d} {desc:12d}")
print()

# Extract each storey
storey_extracts = {}
print(f"  {'Storey':<25s} {'Extracted':>9s} {'Sites':>6s} {'Bldgs':>6s} {'Storeys':>8s} {'Rectified':>10s}")
print("  " + "-" * 70)

for storey in model.storeys:
    safe_name = storey.name.replace("/", "_").replace(" ", "_")
    extract_path = f"temp/thesis_extract_{safe_name}.ifc"
    sub = model.extract(storey, path=extract_path, load_geometries=False)

    sub_elements = len(list(sub.elements()))
    sub_sites = len(sub.sites)
    sub_buildings = len(sub.get_elements_by_type("IfcBuilding"))
    sub_storeys = len(sub.storeys)
    sub_rectified = sub.rectification_stats["rectified_count"]

    print(f"  {storey.name:<25s} {sub_elements:9d} {sub_sites:6d} {sub_buildings:6d} {sub_storeys:8d} {sub_rectified:10d}")
    storey_extracts[storey.name] = sub

print()

# Verify hierarchy scaffolding for each extracted model
all_have_scaffolding = True
for name, sub in storey_extracts.items():
    has_site = len(sub.sites) >= 1
    has_building = len(sub.get_elements_by_type("IfcBuilding")) >= 1
    has_storey = len(sub.storeys) >= 1
    has_project = len(sub._file._file.by_type("IfcProject")) >= 1
    ok = has_site and has_building and has_storey and has_project
    if not ok:
        all_have_scaffolding = False
        print(f"  WARNING: {name} missing scaffolding: site={has_site} bldg={has_building} storey={has_storey} proj={has_project}")

check("Extract: all storeys produce valid IFC", all_have_scaffolding)
check("Extract: each has >= 1 storey",
      all(len(sub.storeys) >= 1 for sub in storey_extracts.values()),
      ", ".join(f"{n}:{len(sub.storeys)}" for n, sub in storey_extracts.items()))
check("Extract: each has IfcProject in file",
      all(len(sub._file._file.by_type("IfcProject")) >= 1 for sub in storey_extracts.values()))


# ==================================================================
# PART 2: POSITION PRESERVATION
# ==================================================================

print()
print("=" * 70)
print("PART 2: POSITION PRESERVATION")
print("=" * 70)

print(f"\n  {'Storey':<25s} {'Checked':>8s} {'Misaligned':>10s} {'Max Error':>12s}")
print("  " + "-" * 60)

all_aligned = True
total_checked = 0
total_misaligned = 0

for name, sub in storey_extracts.items():
    checked, misaligned, max_err = check_positions(sub, all_original_positions, name)
    total_checked += checked
    total_misaligned += misaligned
    if misaligned > 0:
        all_aligned = False
    err_str = f"{max_err:.2e}" if max_err > 0 else "0"
    print(f"  {name:<25s} {checked:8d} {misaligned:10d} {err_str:>12s}")

print(f"\n  Total: {total_checked} checked, {total_misaligned} misaligned")
print()

check("Position: all extracts aligned", all_aligned,
      f"{total_misaligned} misaligned of {total_checked}")


# ==================================================================
# PART 3: DISCIPLINE SUBSET (walls only)
# ==================================================================

print()
print("=" * 70)
print("PART 3: DISCIPLINE SUBSET — walls only")
print("=" * 70)

walls = model.get_elements_by_type("IfcWallStandardCase")
print(f"\n  Walls in full model: {len(walls)}")

wall_extract_path = "temp/thesis_extract_walls_only.ifc"
wall_sub = model.extract(walls, path=wall_extract_path, load_geometries=False)

wall_sub_elements = list(wall_sub.elements())
wall_sub_total = len(wall_sub_elements)
wall_sub_walls = len(wall_sub.get_elements_by_type("IfcWallStandardCase"))
wall_sub_types = {}
for e in wall_sub_elements:
    wall_sub_types[e.ifc_type] = wall_sub_types.get(e.ifc_type, 0) + 1

print(f"  Extracted model: {wall_sub_total} elements")
print(f"  Walls in extract: {wall_sub_walls}")
print(f"  Other types (scaffolding):")
for t, c in sorted(wall_sub_types.items(), key=lambda x: -x[1]):
    if t != "IfcWallStandardCase":
        print(f"    {t}: {c}")
print()

# Position check for walls
wall_checked, wall_misaligned, wall_max_err = check_positions(wall_sub, all_original_positions, "walls")
print(f"  Position check: {wall_checked} checked, {wall_misaligned} misaligned")
if wall_max_err > 0:
    print(f"  Max error: {wall_max_err:.2e}")
print()

check("Discipline: walls preserved", wall_sub_walls == len(walls),
      f"{wall_sub_walls} vs {len(walls)}")
check("Discipline: has hierarchy scaffolding",
      len(wall_sub.sites) >= 1 and len(wall_sub.storeys) >= 1)
check("Discipline: positions aligned", wall_misaligned == 0,
      f"{wall_misaligned} misaligned of {wall_checked}")


# ==================================================================
# PART 4: CODE CONCISENESS
# ==================================================================

print()
print("=" * 70)
print("PART 4: CODE CONCISENESS — compas_ifc vs direct IfcOpenShell")
print("=" * 70)

# compas_ifc approach (granular export)
compas_ifc_code = '''model = BuildingInformationModel("building.ifc")
storey = [s for s in model.storeys if s.name == "Level 2"][0]
subset = model.extract(storey, path="level_2_only.ifc")'''

# Direct IfcOpenShell approach (equivalent functionality)
ifcopenshell_code = '''import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.placement

source = ifcopenshell.open("building.ifc")

# Find storey by name
storey = None
for s in source.by_type("IfcBuildingStorey"):
    if s.Name == "Level 2":
        storey = s
        break

# Collect elements in storey via IfcRelContainedInSpatialStructure
elements = set()
for rel in source.by_type("IfcRelContainedInSpatialStructure"):
    if rel.RelatingStructure == storey:
        for elem in rel.RelatedElements:
            elements.add(elem)

# Collect void/fill children (openings, doors, windows)
extra = set()
for elem in elements:
    for rel in source.by_type("IfcRelVoidsElement"):
        if rel.RelatingBuildingElement == elem:
            opening = rel.RelatedOpeningElement
            extra.add(opening)
            for frel in source.by_type("IfcRelFillsElement"):
                if frel.RelatingOpeningElement == opening:
                    extra.add(frel.RelatedBuildingElement)
elements.update(extra)

# Create new file with spatial hierarchy scaffolding
target = ifcopenshell.file(schema=source.schema)
owner = source.by_type("IfcOwnerHistory")[0]
new_owner = target.add(owner)
project = source.by_type("IfcProject")[0]
new_project = target.add(project)
site = source.by_type("IfcSite")[0]
new_site = target.add(site)
building = source.by_type("IfcBuilding")[0]
new_building = target.add(building)
new_storey = target.add(storey)

# Re-create spatial aggregation relationships
target.create_entity("IfcRelAggregates",
    GlobalId=ifcopenshell.guid.new(),
    OwnerHistory=new_owner,
    RelatingObject=new_project,
    RelatedObjects=[new_site])
target.create_entity("IfcRelAggregates",
    GlobalId=ifcopenshell.guid.new(),
    OwnerHistory=new_owner,
    RelatingObject=new_site,
    RelatedObjects=[new_building])
target.create_entity("IfcRelAggregates",
    GlobalId=ifcopenshell.guid.new(),
    OwnerHistory=new_owner,
    RelatingObject=new_building,
    RelatedObjects=[new_storey])

# Copy elements and fix placement references
new_elements = []
for elem in elements:
    new_elem = target.add(elem)
    new_elements.append(new_elem)

# Re-create containment relationship
target.create_entity("IfcRelContainedInSpatialStructure",
    GlobalId=ifcopenshell.guid.new(),
    OwnerHistory=new_owner,
    RelatedElements=new_elements,
    RelatingStructure=new_storey)

target.write("level_2_only.ifc")'''

compas_lines = len(compas_ifc_code.strip().split("\n"))
ifcos_lines = len(ifcopenshell_code.strip().split("\n"))

print(f"\n  Code comparison (single storey extraction):")
print(f"    {'Approach':<30s} {'Lines':>6s}")
print("    " + "-" * 40)
print(f"    {'compas_ifc (model.extract)':<30s} {compas_lines:6d}")
print(f"    {'Direct IfcOpenShell':<30s} {ifcos_lines:6d}")
print(f"    {'Reduction':<30s} {ifcos_lines - compas_lines:6d} ({100 - 100 * compas_lines / ifcos_lines:.0f}%)")
print()

print(f"  compas_ifc additionally handles:")
print(f"    - Void/fill chain descendants (automatic)")
print(f"    - Material associations and property sets")
print(f"    - Visual styles and type definitions")
print(f"    - Placement chain rewriting (no 'exploding model')")
print(f"    - Graph edge preservation (connections, space boundaries)")
print()

check("Code: compas_ifc < IfcOpenShell lines", compas_lines < ifcos_lines,
      f"{compas_lines} vs {ifcos_lines}")
check("Code: >= 90% reduction", (1 - compas_lines / ifcos_lines) >= 0.90,
      f"{100 - 100 * compas_lines / ifcos_lines:.0f}%")


# ==================================================================
# SUMMARY
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
    print("SUCCESS: All granular export evaluation tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
