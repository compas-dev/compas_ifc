"""Evaluation: Pydantic-based property validation vs IDS.

Demonstrates the validation system on the Duplex model and compares
conciseness with an equivalent IDS (Information Delivery Specification) XML.
"""

import json

from compas_ifc.bim import BuildingInformationModel
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

# ========================================
# 1. Load model
# ========================================
print("Loading Duplex model...")
model = BuildingInformationModel(filepath="data/Duplex_A_20110907.ifc", load_geometries=False)

# ========================================
# 2. Define specifications (Pydantic)
# ========================================
print("\n=== 2. Define specifications ===")

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

print(f"Defined {len(specifications)} specifications")
for spec in specifications:
    print(f"  {spec.name}: {spec.ifc_types} -> {list(spec.required_psets.keys())}")

# ========================================
# 3. Run validation
# ========================================
print("\n=== 3. Validation results ===")

results = model.validate(specifications)

total = len(results)
passed = sum(1 for r in results if r.status == "pass")
failed = sum(1 for r in results if r.status == "fail")

print(f"Total checks: {total}")
print(f"  Passed: {passed}")
print(f"  Failed: {failed}")

# Group by specification
print("\nBreakdown by specification:")
spec_names = sorted(set(r.specification for r in results))
for spec_name in spec_names:
    spec_results = [r for r in results if r.specification == spec_name]
    spec_pass = sum(1 for r in spec_results if r.status == "pass")
    spec_fail = sum(1 for r in spec_results if r.status == "fail")
    print(f"  {spec_name}: {len(spec_results)} elements, {spec_pass} pass, {spec_fail} fail")

# Show failure details
print("\nFailure details:")
for r in results:
    if r.status == "fail":
        if r.missing_psets:
            print(f"  [{r.specification}] {r.element_type} '{r.element_name}': missing {r.missing_psets}")
        if r.property_errors:
            for err in r.property_errors:
                print(f"  [{r.specification}] {r.element_type} '{r.element_name}': "
                      f"{err['pset']}.{err['property']} - {err['error']}")

# ========================================
# 4. Enforcement test
# ========================================
print("\n=== 4. Enforcement test ===")

model2 = BuildingInformationModel.template(schema="IFC4")
model2.specifications = [
    Specification(
        name="Wall common properties",
        ifc_types=["IfcWall", "IfcWallStandardCase"],
        required_psets={"Pset_WallCommon": Pset_WallCommon},
    ),
]

# Try adding a wall without required properties -> should fail
from compas_ifc.element import GenericElement

wall = GenericElement(ifc_type="IfcWall", name="Test Wall")
storey = list(model2.elements())[2]  # first storey

try:
    model2.add_element(wall, parent=storey)
    print("ERROR: Should have raised ValueError!")
except ValueError as e:
    print(f"Correctly rejected: {e}")

# Now add a wall with valid properties -> should pass
wall2 = GenericElement(ifc_type="IfcWall", name="Valid Wall")
wall2.properties = {
    "Pset_WallCommon": {
        "Reference": "Standard Wall",
        "IsExternal": True,
        "LoadBearing": False,
    }
}
try:
    model2.add_element(wall2, parent=storey)
    print(f"Correctly accepted: {wall2}")
except ValueError as e:
    print(f"ERROR: Should have passed: {e}")

# ========================================
# 5. JSON Schema export
# ========================================
print("\n=== 5. JSON Schema export (Pset_WallCommon) ===")
schema = Pset_WallCommon.model_json_schema()
print(json.dumps(schema, indent=2))

# ========================================
# 6. Conciseness comparison: Pydantic vs IDS
# ========================================
print("\n=== 6. Conciseness comparison ===")

# Count lines of our Pydantic specification
pydantic_lines = '''
class Pset_WallCommon(BaseModel):
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
)
'''.strip().split('\n')

# Equivalent IDS XML (simplified, based on buildingSMART IDS spec)
ids_xml_lines = '''
<ids:specification name="Wall common properties"
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
</ids:specification>
'''.strip().split('\n')

print(f"Pydantic definition: {len(pydantic_lines)} lines")
print(f"IDS XML equivalent:  {len(ids_xml_lines)} lines")
print(f"Reduction:           {len(ids_xml_lines) - len(pydantic_lines)} lines ({100 - 100 * len(pydantic_lines) / len(ids_xml_lines):.0f}%)")
print(f"\nPydantic also provides:")
print("  - Type checking at runtime (not just existence)")
print("  - Value constraints (ge=0 for ThermalTransmittance)")
print("  - Default values for optional fields")
print("  - JSON Schema export via model_json_schema()")
print("  - Python IDE autocompletion and type hints")

print("\nDone!")
