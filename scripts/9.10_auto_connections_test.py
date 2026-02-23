"""Test automatic connection detection via geometric contact analysis.

Loads the Duplex model, extracts the 78 wall-wall connections that are
already defined as IfcRelConnectsPathElements in the IFC file, removes
them from the interaction graph, then runs compute_connections() to
rediscover connections from geometry alone.

Reports how many of the original IFC-defined connections were recovered
and how many new connections were found that the IFC file did not have.
"""

from compas_ifc.bim import BuildingInformationModel

# ==========================================================================
# 1. Load model and record original IFC connections
# ==========================================================================

print("Loading Duplex model...")
model = BuildingInformationModel("data/Duplex_A_20110907.ifc")

original_conn_edges = model.get_interactions_by_category("connection")
print(f"Original IFC connections: {len(original_conn_edges)}")

# Store original connection pairs as frozensets of GlobalIds for comparison
original_pairs = set()
for edge in original_conn_edges:
    a, b = model.edge_elements(edge)
    pair = frozenset([a.global_id, b.global_id])
    original_pairs.add(pair)

print(f"Unique original connection pairs (by GlobalId): {len(original_pairs)}")

# ==========================================================================
# 2. Remove connection records from the graph
# ==========================================================================

edges_removed = 0
edges_stripped = 0

for edge in list(model.graph.edges()):
    rels = model.graph.edge_attribute(edge, "relationships") or []
    non_conn = [r for r in rels if r["category"] != "connection"]
    conn_count = len(rels) - len(non_conn)
    if conn_count == 0:
        continue
    if non_conn:
        # Edge has other relationships — keep it, just strip connection records
        model.graph.edge_attribute(edge, "relationships", non_conn)
        edges_stripped += 1
    else:
        # Edge only had connections — remove entirely
        model.graph.delete_edge(edge)
        edges_removed += 1

# Also clear any contacts on remaining edges
for edge in model.graph.edges():
    model.graph.edge_attribute(edge, "contacts", None)

print(f"\nRemoved connection records from {edges_removed + edges_stripped} edges")
print(f"  Edges fully removed: {edges_removed}")
print(f"  Edges kept (had other rels): {edges_stripped}")

# Verify no connections remain
assert len(model.get_interactions_by_category("connection")) == 0, "Connections should be gone"
print("Verified: 0 connection edges remain in graph.")

# ==========================================================================
# 3. Run automatic connection detection
# ==========================================================================

print("\nRunning compute_connections()...")
import time

t0 = time.time()
wall_types = ["IfcWall", "IfcWallStandardCase"]
new_count = model.compute_connections(tolerance=1e-3, minimum_area=0.01, element_types=wall_types)
elapsed = time.time() - t0

print(f"compute_connections() found {new_count} connections in {elapsed:.2f}s")

# ==========================================================================
# 4. Compare with original IFC connections
# ==========================================================================

auto_conn_edges = model.get_interactions_by_category("connection")
print(f"\nTotal connection edges after compute_connections: {len(auto_conn_edges)}")

# Build set of auto-discovered pairs
auto_pairs = set()
for edge in auto_conn_edges:
    a, b = model.edge_elements(edge)
    pair = frozenset([a.global_id, b.global_id])
    auto_pairs.add(pair)

# Compute overlap
recovered = original_pairs & auto_pairs
missed = original_pairs - auto_pairs
newly_found = auto_pairs - original_pairs

print(f"\n{'='*60}")
print(f"RESULTS")
print(f"{'='*60}")
print(f"Original IFC connections:     {len(original_pairs)}")
print(f"Auto-discovered connections:  {len(auto_pairs)}")
print(f"Recovered (overlap):          {len(recovered)}  ({100*len(recovered)/max(len(original_pairs),1):.0f}%)")
print(f"Missed (in IFC, not found):   {len(missed)}")
print(f"New (found, not in IFC):      {len(newly_found)}")
print(f"{'='*60}")

# ==========================================================================
# 5. Detail: what was missed and what was newly found
# ==========================================================================

if missed:
    print(f"\nMissed connections ({len(missed)}):")
    for pair in sorted(missed, key=lambda p: str(p)):
        gids = list(pair)
        a = model.get_element_by_global_id(gids[0])
        b = model.get_element_by_global_id(gids[1])
        a_name = a.name if a else gids[0]
        b_name = b.name if b else gids[1]
        print(f"  {a_name}  <->  {b_name}")

if newly_found:
    print(f"\nNewly discovered connections ({len(newly_found)}):")
    for pair in sorted(list(newly_found)[:20], key=lambda p: str(p)):
        gids = list(pair)
        a = model.get_element_by_global_id(gids[0])
        b = model.get_element_by_global_id(gids[1])
        a_name = a.name if a else gids[0]
        b_name = b.name if b else gids[1]
        print(f"  {a_name}  <->  {b_name}")
    if len(newly_found) > 20:
        print(f"  ... and {len(newly_found) - 20} more")

# ==========================================================================
# 6. Detail: contacts on a sample connection
# ==========================================================================

if auto_conn_edges:
    sample_edge = auto_conn_edges[0]
    a, b = model.edge_elements(sample_edge)
    contacts = model.graph.edge_attribute(sample_edge, "contacts") or []
    print(f"\nSample connection: {a.name} <-> {b.name}")
    print(f"  Contact patches: {len(contacts)}")
    for i, c in enumerate(contacts):
        print(f"    [{i}] area={c.size:.4f} m²  vertices={len(c.points)}")
