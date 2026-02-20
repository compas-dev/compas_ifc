"""Test the new BuildingModel + BuildingElement integration with compas_model."""

from compas_ifc.bim import BuildingInformationModel as BuildingModel

# Load
model = BuildingModel(filepath="data/Duplex_A_20110907.ifc")

# Print hierarchy
model.print_hierarchy(max_depth=3)

# Query
print("\n--- Sites ---")
for site in model.sites:
    print(f"  {site.name} ({site.ifc_type})")

print("\n--- Buildings ---")
for building in model.buildings:
    print(f"  {building.name} ({building.ifc_type})")

print("\n--- Storeys ---")
for storey in model.storeys:
    print(f"  {storey.name} ({storey.ifc_type})")
    children = storey.children
    print(f"    {len(children)} children")

print("\n--- Building Elements ---")
elements = model.building_elements
print(f"Total: {len(elements)} non-spatial elements")

# Check types
from collections import Counter
type_counts = Counter(e.ifc_type for e in elements)
for ifc_type, count in type_counts.most_common():
    print(f"  {ifc_type}: {count}")

# Check geometry
with_geom = [e for e in elements if e.geometry is not None]
print(f"\n--- Geometry ---")
print(f"Elements with geometry: {len(with_geom)} / {len(elements)}")

# Check transformations
print("\n--- Transformations (first 5 elements with geometry) ---")
for e in with_geom[:5]:
    frame = e.frame
    print(f"  {e.ifc_type} '{e.name}': frame.point = {frame.point}")

# Check parent chain
print("\n--- Parent chain (first element) ---")
if with_geom:
    e = with_geom[0]
    chain = []
    current = e
    while current is not None:
        chain.append(f"{current.ifc_type}: {current.name}")
        current = current.parent
    for i, c in enumerate(chain):
        print(f"  {'  ' * i}{c}")

# Check tree structure
print(f"\n--- Tree ---")
print(f"Tree nodes: {len(list(model.tree.nodes))}")
print(f"Graph nodes: {model.graph.number_of_nodes()}")
print(f"Elements: {len(list(model.elements()))}")

print("\nDone!")
