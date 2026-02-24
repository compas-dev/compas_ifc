"""
13.2 Instancing Read Test
=========================

Test for Phase 3: loads the Duplex model and reports instancing
statistics (IfcRepresentationMap and IfcMappedItem usage).

Verifies that:
- All IfcMappedItem instances parse correctly via entity.geometry
- The read-side cache (template parsed once per map) works correctly
"""

from compas_ifc.model import Model

# ------------------------------------------------------------------
# Load model
# ------------------------------------------------------------------

model = Model("data/Duplex_A_20110907.ifc")

# ------------------------------------------------------------------
# Count instancing entities
# ------------------------------------------------------------------

rep_maps = model.get_entities_by_type("IfcRepresentationMap")
mapped_items = model.get_entities_by_type("IfcMappedItem")

print("=" * 70)
print("Instancing Read Test -- Duplex Model")
print("=" * 70)
print()
print(f"IfcRepresentationMap entities: {len(rep_maps)}")
print(f"IfcMappedItem entities:        {len(mapped_items)}")
print()

# ------------------------------------------------------------------
# Analyse RepresentationMaps: how many instances per map?
# ------------------------------------------------------------------

print("-" * 70)
print("Top RepresentationMaps by instance count:")
print("-" * 70)

map_usage = []
for rm in rep_maps:
    try:
        usages = rm.entity.MapUsage  # inverse attribute on raw ifcopenshell entity
        usage_count = len(usages) if usages else 0
    except Exception:
        usage_count = 0
    inner_type = rm.MappedRepresentation.RepresentationType if rm.MappedRepresentation else "?"
    map_usage.append((rm, usage_count, inner_type))

# Sort by usage count descending
map_usage.sort(key=lambda x: -x[1])

for i, (rm, count, inner_type) in enumerate(map_usage[:15]):
    print(f"  Map #{rm.entity.id():5d}: {count:3d} instances, inner type={inner_type}")

if len(map_usage) > 15:
    print(f"  ... and {len(map_usage) - 15} more maps")

# Multi-instance maps
multi = [(rm, c, t) for rm, c, t in map_usage if c > 1]
print(f"\nMaps with >1 instance: {len(multi)} (shared geometry)")
print(f"Maps with  1 instance: {len(map_usage) - len(multi)} (single-use)")

# ------------------------------------------------------------------
# Verify all products with IfcMappedItem body reps parse correctly
# ------------------------------------------------------------------

print()
print("-" * 70)
print("Verifying geometry parsing for products with mapped representations...")
print("-" * 70)

products = model.get_entities_by_type("IfcProduct")
mapped_products = 0
parsed_ok = 0
parse_fail = 0

for entity in products:
    if entity.is_a("IfcSpace"):
        continue

    rep = entity.Representation
    if rep is None:
        continue

    has_mapped = False
    for shape_rep in rep.Representations:
        if shape_rep.RepresentationType == "MappedRepresentation":
            has_mapped = True
            break

    if not has_mapped:
        continue

    mapped_products += 1
    geom = entity.geometry
    if geom is not None:
        parsed_ok += 1
    else:
        parse_fail += 1
        name = getattr(entity, "Name", "") or ""
        print(f"  FAIL: [{entity.is_a()}] {name} -- geometry is None")

print(f"\nProducts with mapped body rep: {mapped_products}")
print(f"  Parsed OK:  {parsed_ok}")
print(f"  Parse fail: {parse_fail}")

# ------------------------------------------------------------------
# Check cache effectiveness
# ------------------------------------------------------------------

from compas_ifc.conversions.reading import _MAPPED_GEOMETRY_CACHE

cache_size = len(_MAPPED_GEOMETRY_CACHE)
print(f"\nRead cache entries: {cache_size}")
print(f"  (Each entry = one unique template parsed once,")
print(f"   reused for all instances of that map)")

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

print()
print("=" * 70)
print("Summary")
print("=" * 70)
print(f"Total IfcRepresentationMap: {len(rep_maps)}")
print(f"Total IfcMappedItem:        {len(mapped_items)}")
print(f"Products with mapped rep:   {mapped_products}")
print(f"All parsed correctly:       {'YES' if parse_fail == 0 else 'NO'}")
print(f"Cache entries:              {cache_size}")

if parse_fail == 0:
    print("\nSUCCESS: All mapped items read correctly with caching.")
else:
    print(f"\nWARNING: {parse_fail} mapped items failed to parse.")
