"""
Custom Validation Evaluation
=============================

Evaluates the Pydantic-based validation system against the Duplex model
(IFC2X3, ~295 elements).  Addresses the Innovation Barrier through schema
definition and enforcement testing.

  Part 1: Standard Pset Validation — 7 standard IFC property-set schemas
  Part 2: Custom Project Schema — stricter project-specific constraints
  Part 3: Enforcement — add_element rejects non-conforming elements
  Part 4: Schema Export & IDS Comparison — JSON Schema export, line counts

The validation module (compas_ifc.validation) provides Pydantic BaseModel
subclasses for each standard IFC property set.  A Specification groups
applicability criteria (IFC types) with required Pset schemas, mirroring
the IDS structure but in far fewer lines.
"""

import json
import sys

from pydantic import BaseModel, Field, ValidationError
from typing import Optional

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.element import GenericElement
from compas_ifc.validation import (
    Pset_BeamCommon,
    Pset_DoorCommon,
    Pset_RoofCommon,
    Pset_SlabCommon,
    Pset_SpaceCommon,
    Pset_WallCommon,
    Pset_WindowCommon,
    Specification,
)

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
# PART 1: STANDARD PSET VALIDATION
# ==================================================================

print("=" * 70)
print("PART 1: STANDARD PSET VALIDATION — data/Duplex_A_20110907.ifc")
print("=" * 70)

model = BuildingInformationModel(
    filepath="data/Duplex_A_20110907.ifc",
    load_geometries=False,
)

total_elements = len(list(model.elements()))
print(f"\n  Total elements: {total_elements}")

# Define all 7 standard specifications
specifications = [
    Specification(
        name="Wall common properties",
        ifc_types=["IfcWall", "IfcWallStandardCase"],
        required_psets={"Pset_WallCommon": Pset_WallCommon},
    ),
    Specification(
        name="Slab common properties",
        ifc_types=["IfcSlab"],
        required_psets={"Pset_SlabCommon": Pset_SlabCommon},
    ),
    Specification(
        name="Door common properties",
        ifc_types=["IfcDoor"],
        required_psets={"Pset_DoorCommon": Pset_DoorCommon},
    ),
    Specification(
        name="Window common properties",
        ifc_types=["IfcWindow"],
        required_psets={"Pset_WindowCommon": Pset_WindowCommon},
    ),
    Specification(
        name="Beam common properties",
        ifc_types=["IfcBeam"],
        required_psets={"Pset_BeamCommon": Pset_BeamCommon},
    ),
    Specification(
        name="Space common properties",
        ifc_types=["IfcSpace"],
        required_psets={"Pset_SpaceCommon": Pset_SpaceCommon},
    ),
    Specification(
        name="Roof common properties",
        ifc_types=["IfcRoof"],
        required_psets={"Pset_RoofCommon": Pset_RoofCommon},
    ),
]

print(f"  Specifications defined: {len(specifications)}")
print()

# Run validation
validation_results = model.validate(specifications)

total_checks = len(validation_results)
passed = sum(1 for r in validation_results if r.status == "pass")
failed = sum(1 for r in validation_results if r.status == "fail")

print(f"  Total element-spec checks: {total_checks}")
print(f"  Passed: {passed}")
print(f"  Failed: {failed}")
print()

# Breakdown by specification
print(f"  {'Specification':<30s} {'Elements':>8s} {'Pass':>6s} {'Fail':>6s}")
print("  " + "-" * 55)
spec_names = sorted(set(r.specification for r in validation_results))
for spec_name in spec_names:
    spec_results = [r for r in validation_results if r.specification == spec_name]
    sp = sum(1 for r in spec_results if r.status == "pass")
    sf = sum(1 for r in spec_results if r.status == "fail")
    print(f"  {spec_name:<30s} {len(spec_results):8d} {sp:6d} {sf:6d}")
print()

# Classify failures
failures = [r for r in validation_results if r.status == "fail"]
n_missing = sum(1 for r in failures if r.missing_psets)
n_property_errors = sum(1 for r in failures if r.property_errors and not r.missing_psets)

print(f"  Failure breakdown:")
print(f"    Missing required psets:  {n_missing}")
print(f"    Property value errors:   {n_property_errors}")
print()

# Show failure details
if failures:
    print("  Failure details:")
    for r in failures:
        if r.missing_psets:
            print(f"    [{r.specification}] {r.element_type} '{r.element_name}':")
            print(f"      missing psets: {r.missing_psets}")
        for err in r.property_errors:
            print(f"    [{r.specification}] {r.element_type} '{r.element_name}':")
            print(f"      {err['pset']}.{err['property']} - {err['error']}")
    print()

# Checks
check("Std: total checks >= 140", total_checks >= 140, f"{total_checks}")
check("Std: pass rate >= 95%", passed / total_checks >= 0.95 if total_checks else False,
      f"{100 * passed / total_checks:.1f}%")
check("Std: all 7 specs tested", len(spec_names) == 7, f"{len(spec_names)}")


# ==================================================================
# PART 2: CUSTOM PROJECT SCHEMA
# ==================================================================

print()
print("=" * 70)
print("PART 2: CUSTOM PROJECT SCHEMA")
print("=" * 70)

# Define a stricter project-specific schema for fire safety compliance.
# This requires FireRating to be present (not optional) and constrains
# ThermalTransmittance to a maximum value.


class FireSafetyWallSchema(BaseModel):
    """Project-specific schema: fire-rated exterior walls."""

    IsExternal: bool
    LoadBearing: bool = False
    FireRating: str  # Required (not optional) — must be specified
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0, le=5.0)


class FireSafetyDoorSchema(BaseModel):
    """Project-specific schema: fire-rated doors."""

    IsExternal: bool
    FireRating: str  # Required — must be specified
    FireExit: Optional[bool] = None
    SelfClosing: Optional[bool] = None


fire_safety_specs = [
    Specification(
        name="Fire-rated walls",
        ifc_types=["IfcWall", "IfcWallStandardCase"],
        required_psets={"Pset_WallCommon": FireSafetyWallSchema},
        description="All walls must have an explicit FireRating value.",
    ),
    Specification(
        name="Fire-rated doors",
        ifc_types=["IfcDoor"],
        required_psets={"Pset_DoorCommon": FireSafetyDoorSchema},
        description="All doors must have an explicit FireRating value.",
    ),
]

print(f"\n  Custom specifications defined: {len(fire_safety_specs)}")
for spec in fire_safety_specs:
    print(f"    {spec.name}: {spec.ifc_types}")
    print(f"      {spec.description}")
print()

# Run custom validation
custom_results = model.validate(fire_safety_specs)

custom_total = len(custom_results)
custom_pass = sum(1 for r in custom_results if r.status == "pass")
custom_fail = sum(1 for r in custom_results if r.status == "fail")

print(f"  Total checks: {custom_total}")
print(f"  Passed: {custom_pass}")
print(f"  Failed: {custom_fail}")
print()

# Breakdown by specification
print(f"  {'Specification':<30s} {'Elements':>8s} {'Pass':>6s} {'Fail':>6s}")
print("  " + "-" * 55)
for spec in fire_safety_specs:
    spec_results = [r for r in custom_results if r.specification == spec.name]
    sp = sum(1 for r in spec_results if r.status == "pass")
    sf = sum(1 for r in spec_results if r.status == "fail")
    print(f"  {spec.name:<30s} {len(spec_results):8d} {sp:6d} {sf:6d}")
print()

# Classify custom failures
custom_failures = [r for r in custom_results if r.status == "fail"]
custom_missing = sum(1 for r in custom_failures if r.missing_psets)
custom_prop_errors = sum(len(r.property_errors) for r in custom_failures if not r.missing_psets)

# Error type breakdown across all failures
error_types = {}  # error type -> count
for r in custom_failures:
    for err in r.property_errors:
        etype = err.get("type", "unknown")
        error_types[etype] = error_types.get(etype, 0) + 1

print(f"  Custom failure breakdown:")
print(f"    Elements with missing psets:    {custom_missing}")
print(f"    Elements with property errors:  {sum(1 for r in custom_failures if r.property_errors and not r.missing_psets)}")
print(f"    Total property errors:          {custom_prop_errors}")
if error_types:
    print(f"    Error types:")
    for etype, count in sorted(error_types.items(), key=lambda x: -x[1]):
        print(f"      {etype}: {count}")
print()

# Sample failure details (first 5)
if custom_failures:
    print("  Sample failure details (first 5):")
    for r in custom_failures[:5]:
        if r.missing_psets:
            print(f"    {r.element_type} '{r.element_name}': missing {r.missing_psets}")
        for err in r.property_errors:
            print(f"    {r.element_type} '{r.element_name}': "
                  f"{err['pset']}.{err['property']} - {err['error']}")
    if len(custom_failures) > 5:
        print(f"    ... and {len(custom_failures) - 5} more")
    print()

# Checks
check("Custom: elements checked >= 60", custom_total >= 60, f"{custom_total}")
check("Custom: stricter schema finds more failures", custom_fail > failed,
      f"{custom_fail} vs {failed} standard")
check("Custom: pass + fail == total", custom_pass + custom_fail == custom_total,
      f"{custom_pass} + {custom_fail} = {custom_total}")


# ==================================================================
# PART 3: ENFORCEMENT
# ==================================================================

print()
print("=" * 70)
print("PART 3: ENFORCEMENT — add_element rejects non-conforming elements")
print("=" * 70)

# Create a fresh model with enforcement specifications
model2 = BuildingInformationModel.template(schema="IFC4")
model2.specifications = [
    Specification(
        name="Wall common properties",
        ifc_types=["IfcWall", "IfcWallStandardCase"],
        required_psets={"Pset_WallCommon": Pset_WallCommon},
    ),
]

storey = list(model2.elements())[2]  # first storey

# Test 1: wall without required properties -> should be rejected
wall_bad = GenericElement(ifc_type="IfcWall", name="Non-Conforming Wall")
rejected = False
rejection_msg = ""
try:
    model2.add_element(wall_bad, parent=storey)
except ValueError as e:
    rejected = True
    rejection_msg = str(e)

print(f"\n  Test 1: Add wall without Pset_WallCommon")
print(f"    Rejected: {rejected}")
if rejected:
    print(f"    Message:  {rejection_msg[:120]}")
print()

# Test 2: wall with valid properties -> should be accepted
wall_good = GenericElement(ifc_type="IfcWall", name="Conforming Wall")
wall_good.properties = {
    "Pset_WallCommon": {
        "Reference": "CW-01",
        "IsExternal": True,
        "LoadBearing": False,
    }
}
accepted = False
try:
    model2.add_element(wall_good, parent=storey)
    accepted = True
except ValueError as e:
    accepted = False

print(f"  Test 2: Add wall with valid Pset_WallCommon")
print(f"    Accepted: {accepted}")
print()

# Test 3: non-applicable type -> should be accepted (no spec applies)
slab = GenericElement(ifc_type="IfcSlab", name="Unrestricted Slab")
slab_accepted = False
try:
    model2.add_element(slab, parent=storey)
    slab_accepted = True
except ValueError:
    slab_accepted = False

print(f"  Test 3: Add slab (no spec applies)")
print(f"    Accepted: {slab_accepted}")
print()

# Checks
check("Enforce: non-conforming wall rejected", rejected)
check("Enforce: conforming wall accepted", accepted)
check("Enforce: non-applicable type accepted", slab_accepted)


# ==================================================================
# PART 4: SCHEMA EXPORT & IDS COMPARISON
# ==================================================================

print()
print("=" * 70)
print("PART 4: SCHEMA EXPORT & IDS COMPARISON")
print("=" * 70)

# Export JSON Schema
schema_json = Pset_WallCommon.model_json_schema()
schema_str = json.dumps(schema_json, indent=2)
schema_lines = schema_str.split("\n")

print(f"\n  JSON Schema for Pset_WallCommon: {len(schema_lines)} lines")
print(f"  Required fields: {schema_json.get('required', [])}")

# Count schema properties
schema_props = list(schema_json.get("properties", {}).keys())
print(f"  Properties: {len(schema_props)} ({', '.join(schema_props)})")
print()

# Also export custom schema
custom_schema = FireSafetyWallSchema.model_json_schema()
custom_str = json.dumps(custom_schema, indent=2)
custom_lines = custom_str.split("\n")

print(f"  JSON Schema for FireSafetyWallSchema: {len(custom_lines)} lines")
print(f"  Required fields: {custom_schema.get('required', [])}")
print()

# Pydantic vs IDS line count comparison
# Count the Pydantic definition lines
pydantic_def = """class Pset_WallCommon(BaseModel):
    Reference: str = ""
    IsExternal: bool
    LoadBearing: bool = False
    ExtendToStructure: Optional[bool] = None
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0)
    FireRating: Optional[str] = None
    AcousticRating: Optional[str] = None

spec = Specification(
    name="Wall common properties",
    ifc_types=["IfcWall", "IfcWallStandardCase"],
    required_psets={"Pset_WallCommon": Pset_WallCommon},
)"""

# Equivalent IDS XML (based on buildingSMART IDS 1.0 specification)
ids_xml = """<ids:specification name="Wall common properties"
                   ifcVersion="IFC4">
  <ids:applicability minOccurs="0" maxOccurs="unbounded">
    <ids:entity>
      <ids:name>
        <ids:simpleValue>IFCWALL</ids:simpleValue>
      </ids:name>
    </ids:entity>
  </ids:applicability>
  <ids:requirements>
    <ids:property datatype="IFCLABEL" minOccurs="1">
      <ids:propertySet>
        <ids:simpleValue>Pset_WallCommon</ids:simpleValue>
      </ids:propertySet>
      <ids:baseName>
        <ids:simpleValue>Reference</ids:simpleValue>
      </ids:baseName>
    </ids:property>
    <ids:property datatype="IFCBOOLEAN" minOccurs="1">
      <ids:propertySet>
        <ids:simpleValue>Pset_WallCommon</ids:simpleValue>
      </ids:propertySet>
      <ids:baseName>
        <ids:simpleValue>IsExternal</ids:simpleValue>
      </ids:baseName>
    </ids:property>
    <ids:property datatype="IFCBOOLEAN" minOccurs="0">
      <ids:propertySet>
        <ids:simpleValue>Pset_WallCommon</ids:simpleValue>
      </ids:propertySet>
      <ids:baseName>
        <ids:simpleValue>LoadBearing</ids:simpleValue>
      </ids:baseName>
    </ids:property>
    <ids:property datatype="IFCBOOLEAN" minOccurs="0">
      <ids:propertySet>
        <ids:simpleValue>Pset_WallCommon</ids:simpleValue>
      </ids:propertySet>
      <ids:baseName>
        <ids:simpleValue>ExtendToStructure</ids:simpleValue>
      </ids:baseName>
    </ids:property>
    <ids:property datatype="IFCTHERMALTRANSMITTANCEMEASURE" minOccurs="0">
      <ids:propertySet>
        <ids:simpleValue>Pset_WallCommon</ids:simpleValue>
      </ids:propertySet>
      <ids:baseName>
        <ids:simpleValue>ThermalTransmittance</ids:simpleValue>
      </ids:baseName>
    </ids:property>
    <ids:property datatype="IFCLABEL" minOccurs="0">
      <ids:propertySet>
        <ids:simpleValue>Pset_WallCommon</ids:simpleValue>
      </ids:propertySet>
      <ids:baseName>
        <ids:simpleValue>FireRating</ids:simpleValue>
      </ids:baseName>
    </ids:property>
    <ids:property datatype="IFCLABEL" minOccurs="0">
      <ids:propertySet>
        <ids:simpleValue>Pset_WallCommon</ids:simpleValue>
      </ids:propertySet>
      <ids:baseName>
        <ids:simpleValue>AcousticRating</ids:simpleValue>
      </ids:baseName>
    </ids:property>
  </ids:requirements>
</ids:specification>"""

pydantic_line_count = len(pydantic_def.strip().split("\n"))
ids_line_count = len(ids_xml.strip().split("\n"))
reduction = ids_line_count - pydantic_line_count
reduction_pct = 100 - 100 * pydantic_line_count / ids_line_count

print(f"  Conciseness comparison (Pset_WallCommon, 7 properties):")
print(f"    {'Approach':<25s} {'Lines':>6s}")
print("    " + "-" * 35)
print(f"    {'Pydantic + Specification':<25s} {pydantic_line_count:6d}")
print(f"    {'IDS XML equivalent':<25s} {ids_line_count:6d}")
print(f"    {'Reduction':<25s} {reduction:6d} ({reduction_pct:.0f}%)")
print()

print(f"  Additional Pydantic capabilities (not available in IDS):")
print(f"    - Runtime type checking (not just existence)")
print(f"    - Value constraints (ge=0 for ThermalTransmittance)")
print(f"    - Default values for optional fields")
print(f"    - JSON Schema export via model_json_schema()")
print(f"    - Python IDE autocompletion and type hints")
print(f"    - Enforcement on add_element (reject non-conforming)")
print()

# Checks
check("Export: JSON Schema has required fields", len(schema_json.get("required", [])) >= 1,
      f"{schema_json.get('required', [])}")
check("Export: JSON Schema has all properties", len(schema_props) >= 7,
      f"{len(schema_props)}")
check("Export: Pydantic < IDS line count", pydantic_line_count < ids_line_count,
      f"{pydantic_line_count} vs {ids_line_count}")
check("Export: >= 70% reduction", reduction_pct >= 70, f"{reduction_pct:.0f}%")


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
    print("SUCCESS: All custom validation evaluation tests passed.")
else:
    print("WARNING: Some tests failed.")
    sys.exit(1)
