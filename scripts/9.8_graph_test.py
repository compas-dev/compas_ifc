"""Test interaction graph: populate with non-spatial IFC relationships."""

from compas_ifc.bim import BuildingInformationModel

# ========================================
# Load Duplex model
# ========================================
print("Loading Duplex model...")
model = BuildingInformationModel(filepath="data/Duplex_A_20110907.ifc", load_geometries=False)

# ========================================
# 1. Verify graph edge counts
# ========================================
print("\n=== 1. Graph edge counts ===")
total_edges = len(list(model.graph.edges()))
print(f"Total graph edges: {total_edges}")
print(f"  Connections: {len(model.connections)}")
print(f"  Voids: {len(model.voids)}")
print(f"  Fills: {len(model.fills)}")
print(f"  Space boundaries: {len(model.space_boundaries)}")

# ========================================
# 2. Verify opening elements are graph-only
# ========================================
print("\n=== 2. Opening elements (graph-only) ===")
# model.elements() includes ALL registered elements (tree + graph-only).
# To check tree-only, walk the tree directly.
all_elements = list(model.elements())

def _tree_elements(model):
    """Collect elements that are actually in the tree (have a treenode)."""
    return [e for e in model._elements.values() if getattr(e, "treenode", None) is not None]

tree_only = _tree_elements(model)
openings = [e for e in all_elements if e.ifc_type == "IfcOpeningElement"]
tree_openings = [e for e in tree_only if e.ifc_type == "IfcOpeningElement"]

print(f"All registered elements: {len(all_elements)}")
print(f"Tree-only elements: {len(tree_only)}")
print(f"IfcOpeningElement total: {len(openings)}")
print(f"IfcOpeningElement in tree: {len(tree_openings)}")
print(f"IfcOpeningElement graph-only: {len(openings) - len(tree_openings)}")

# Graph node count should include tree + graph-only
graph_nodes = len(list(model.graph.nodes()))
print(f"Graph nodes: {graph_nodes}")
print(f"Expected: {len(all_elements)}")

# ========================================
# 3. Walk a void→fill chain
# ========================================
print("\n=== 3. Walk void→fill chain ===")
void_edges = model.voids
if void_edges:
    # Pick first void edge
    edge = void_edges[0]
    host, opening = model.edge_elements(edge)
    print(f"Void edge: {host.ifc_type} '{host.name}' -> {opening.ifc_type} '{opening.name}'")

    # Find the fill edge for this opening
    fill_edges = model.fills
    for fe in fill_edges:
        fe_opening, fe_filler = model.edge_elements(fe)
        if fe_opening is opening:
            print(f"Fill edge: {fe_opening.ifc_type} '{fe_opening.name}' -> {fe_filler.ifc_type} '{fe_filler.name}'")
            print(f"Full chain: {host.ifc_type} -> {opening.ifc_type} -> {fe_filler.ifc_type}")
            break

# ========================================
# 4. Connection edges detail
# ========================================
print("\n=== 4. Connection edges (first 5) ===")
for edge in model.connections[:5]:
    a, b = model.edge_elements(edge)
    print(f"  {a.ifc_type} '{a.name}' <-> {b.ifc_type} '{b.name}'")

# ========================================
# 5. Space boundary edges detail
# ========================================
print("\n=== 5. Space boundaries (first 5) ===")
for edge in model.space_boundaries[:5]:
    space, elem = model.edge_elements(edge)
    print(f"  {space.ifc_type} '{space.name}' <-> {elem.ifc_type} '{elem.name}'")

# ========================================
# 6. Small file test
# ========================================
print("\n=== 6. Small file test ===")
model2 = BuildingInformationModel(filepath="data/wall-with-opening-and-window.ifc", load_geometries=False)
print(f"Tree elements: {len(list(model2.elements()))}")
print(f"Graph edges: {len(list(model2.graph.edges()))}")
print(f"  Voids: {len(model2.voids)}")
print(f"  Fills: {len(model2.fills)}")
print(f"  Connections: {len(model2.connections)}")

if model2.voids:
    edge = model2.voids[0]
    host, opening = model2.edge_elements(edge)
    print(f"Void: {host.ifc_type} '{host.name}' -> {opening.ifc_type} '{opening.name}'")

if model2.fills:
    edge = model2.fills[0]
    opening, filler = model2.edge_elements(edge)
    print(f"Fill: {opening.ifc_type} '{opening.name}' -> {filler.ifc_type} '{filler.name}'")

# ========================================
# 7. Group-level queries
# ========================================
print("\n=== 7. Group-level queries ===")
for group_name in model.RELATIONSHIP_GROUPS:
    edges = model.get_interactions_by_group(group_name)
    print(f"  {group_name}: {len(edges)} edges")

# Verify group totals equal category totals
topology_edges = model.get_interactions_by_group("topology")
category_sum = (
    len(model.connections)
    + len(model.voids)
    + len(model.fills)
    + len(model.space_boundaries)
    + len(model.get_interactions_by_category("covering"))
    + len(model.get_interactions_by_category("interference"))
    + len(model.get_interactions_by_category("projection"))
)
print(f"\nTopology group edges: {len(topology_edges)}")
print(f"Sum of topology categories: {category_sum}")
print(f"Match: {len(topology_edges) == category_sum}")

# Verify all edges are accounted for by the three groups
all_group_edges = set()
for group_name in model.RELATIONSHIP_GROUPS:
    all_group_edges.update(model.get_interactions_by_group(group_name))
all_edges = set(model.graph.edges())
print(f"\nAll graph edges: {len(all_edges)}")
print(f"All group edges: {len(all_group_edges)}")
print(f"Coverage: {all_group_edges == all_edges}")

# Verify total relationship records == IFC relationship count
total_records = sum(len(model.edge_relationships(edge)) for edge in model.graph.edges())
print(f"\nTotal relationship records: {total_records}")
print(f"Total unique edges: {len(all_edges)}")

# Edges with multiple relationship records
multi = [edge for edge in model.graph.edges() if len(model.edge_relationships(edge)) > 1]
print(f"Edges with multiple records: {len(multi)}")
for edge in multi[:5]:
    a, b = model.edge_elements(edge)
    rels = model.edge_relationships(edge)
    cats = [r["category"] for r in rels]
    print(f"  {a.ifc_type} '{a.name}' <-> {b.ifc_type} '{b.name}': {len(rels)}x {cats}")

print("\nDone!")
