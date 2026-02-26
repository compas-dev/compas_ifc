"""Test interaction graph and void/fill tree hierarchy."""

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
print(f"  Space boundaries: {len(model.space_boundaries)}")

# ========================================
# 2. Verify opening elements are in the tree
# ========================================
print("\n=== 2. Opening elements (tree) ===")
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
# 3. Walk void->fill chains in the tree
# ========================================
print("\n=== 3. Void/fill chains in tree ===")
void_count = 0
fill_count = 0
for elem in all_elements:
    if elem.ifc_type == "IfcOpeningElement":
        parent = elem.parent
        void_count += 1
        fillers = [c for c in elem.children if c.ifc_type not in ("IfcOpeningElement",)]
        fill_count += len(fillers)

print(f"Void links (host -> opening): {void_count}")
print(f"Fill links (opening -> filler): {fill_count}")

# Show first few chains
chains_shown = 0
for elem in all_elements:
    if elem.ifc_type == "IfcOpeningElement" and chains_shown < 3:
        parent = elem.parent
        fillers = elem.children
        chain = f"  {parent.ifc_type} '{parent.name}' -> {elem.ifc_type} '{elem.name}'"
        for f in fillers:
            chain += f" -> {f.ifc_type} '{f.name}'"
        print(chain)
        chains_shown += 1

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
print(f"  Connections: {len(model2.connections)}")

# Walk the void/fill chain in tree
for elem in model2.elements():
    if elem.ifc_type == "IfcOpeningElement":
        parent = elem.parent
        print(f"Void: {parent.ifc_type} '{parent.name}' -> {elem.ifc_type} '{elem.name}'")
        for filler in elem.children:
            print(f"Fill: {elem.ifc_type} '{elem.name}' -> {filler.ifc_type} '{filler.name}'")

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
