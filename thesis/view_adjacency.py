"""View adjacency graph overlaid on the integrated workflow model.

Shows slab and beam geometry in muted colors with graph edges drawn
as lines between the centroids of connected elements, lifted above
the model for clear top-view reading.
"""

from compas.colors import Color
from compas.geometry import Line
from compas.geometry import Point
from compas_viewer import Viewer
from compas_viewer.components import Treeform
from compas_viewer.scene.tagobject import Tag

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.brep import TessellatedBrep

TYPE_COLORS = {
    "IfcSlab": [0.76, 0.70, 0.60, 1.0],
    "IfcColumn": [0.65, 0.74, 0.78, 1.0],
    "IfcBeam": [0.70, 0.78, 0.65, 1.0],
}
DEFAULT_COLOR = [0.8, 0.8, 0.8, 1.0]

SLAB_EDGE_COLOR = Color(0.85, 0.25, 0.25)   # red for slab-slab
BEAM_EDGE_COLOR = Color(0.20, 0.45, 0.75)   # blue for slab-beam
BB_EDGE_COLOR = Color(0.20, 0.60, 0.30)     # green for beam-beam
NODE_COLOR = Color(0.3, 0.3, 0.3)
SLAB_LABEL_COLOR = Color(0.65, 0.15, 0.15)
BEAM_LABEL_COLOR = Color(0.15, 0.35, 0.60)
BB_LABEL_COLOR = Color(0.15, 0.50, 0.25)
GRAPH_LIFT = 0.8  # metres above top of slab
TAG_HEIGHT = 22

model = BuildingInformationModel("temp/thesis_integrated_workflow.ifc")

# Short display names: FSU_0_0 -> Slab1, BEAM_0_0 -> Beam1
_name_counter = {}


def short_name(elem):
    prefix = "Slab" if elem.ifc_type == "IfcSlab" else "Beam"
    key = (prefix, elem.global_id)
    if key not in _name_counter:
        _name_counter[key] = sum(1 for k in _name_counter if k[0] == prefix) + 1
    return f"{prefix}{_name_counter[key]}"

viewer = Viewer()
viewer.ui.sidebar.show_objectsetting = False
if model.unit:
    viewer.unit = model.unit

# -- Add building elements --------------------------------------------------


def add_element(elem, parent=None):
    label = f"[{elem.ifc_type}] {elem.name}"
    visual = elem._visual_geometry
    skip = elem.ifc_type in ("IfcSpace", "IfcOpeningElement")

    if visual is not None and not skip:
        rgba = TYPE_COLORS.get(elem.ifc_type, DEFAULT_COLOR)
        style = elem._resolve_style() or {}
        if isinstance(visual, TessellatedBrep):
            style["facecolors"] = [rgba] * (len(visual.faces) * 3)
        else:
            style["surfacecolor"] = Color(*rgba[:3])
        obj = viewer.scene.add(
            visual,
            name=label,
            parent=parent,
            hide_coplanaredges=True,
            **style,
        )
    else:
        obj = viewer.scene.add_group(name=label, parent=parent)

    obj.transformation = elem.transformation
    for child in elem.children:
        add_element(child, parent=obj)


for node in model.tree.root.children:
    add_element(node.element)

# -- Compute element centroids (lifted) --------------------------------------


def element_centroid(elem, z_offset=0):
    """Get the world-space centroid of an element, optionally lifted in Z."""
    geom = elem._visual_geometry
    if geom is None:
        return None
    if isinstance(geom, TessellatedBrep):
        pts = geom.vertices
    elif hasattr(geom, "points"):
        pts = geom.points
    else:
        return None
    t = elem.modeltransformation
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    cz = sum(p[2] for p in pts) / len(pts)
    pt = Point(cx, cy, cz)
    pt.transform(t)
    pt.z += z_offset
    return pt


# -- Collect centroids for slabs and beams -----------------------------------

slabs = [e for e in model.building_elements if e.ifc_type == "IfcSlab"]
beams = [e for e in model.building_elements if e.ifc_type == "IfcBeam"]

# Find the top Z of the model for the lift reference
all_z = []
for e in slabs + beams:
    c = element_centroid(e)
    if c:
        all_z.append(c.z)
lift = max(all_z) + GRAPH_LIFT if all_z else GRAPH_LIFT

slab_centroids = {}  # global_id -> lifted Point
for s in slabs:
    c = element_centroid(s, z_offset=lift - (max(all_z) if all_z else 0))
    if c:
        slab_centroids[s.global_id] = c

# For beams, split into per-bay segment centroids (one per slab row in Y)
slab_ys = sorted(set(round(c.y, 3) for c in slab_centroids.values()))
beam_segment_centroids = {}  # (global_id, j) -> lifted Point
z_off = lift - (max(all_z) if all_z else 0)
for b in beams:
    c = element_centroid(b)
    if not c:
        continue
    for j, sy in enumerate(slab_ys):
        pt = Point(c.x, sy, c.z + z_off)
        beam_segment_centroids[(b.global_id, j)] = pt

# -- Draw slab-slab graph edges (from model graph) --------------------------

graph_group = viewer.scene.add_group(name="Adjacency Graph")
slab_slab_group = viewer.scene.add_group(name="Slab-Slab", parent=graph_group)
slab_beam_group = viewer.scene.add_group(name="Slab-Beam", parent=graph_group)
beam_beam_group = viewer.scene.add_group(name="Beam-Beam", parent=graph_group)

node_points = set()
slab_slab_count = 0

for edge in model.graph.edges():
    elem_a, elem_b = model._edge_elements(edge)
    ca = slab_centroids.get(elem_a.global_id) or beam_centroids.get(elem_a.global_id)
    cb = slab_centroids.get(elem_b.global_id) or beam_centroids.get(elem_b.global_id)
    if ca and cb:
        viewer.scene.add(
            Line(ca, cb),
            name=f"{elem_a.name} - {elem_b.name}",
            parent=slab_slab_group,
            linecolor=SLAB_EDGE_COLOR,
            linewidth=3,
        )
        mid = Point((ca.x + cb.x) / 2, (ca.y + cb.y) / 2, (ca.z + cb.z) / 2)
        label = f"{short_name(elem_a)} <-> {short_name(elem_b)}"
        viewer.scene.add(
            Tag(label, mid, color=SLAB_LABEL_COLOR, height=TAG_HEIGHT),
            parent=slab_slab_group,
        )
        node_points.add((ca.x, ca.y, ca.z))
        node_points.add((cb.x, cb.y, cb.z))
        slab_slab_count += 1

# -- Compute slab-beam adjacency by X and Y proximity -----------------------

slab_xs = sorted(set(round(c.x, 3) for c in slab_centroids.values()))
spacing_x = slab_xs[1] - slab_xs[0] if len(slab_xs) > 1 else 10.0
spacing_y = slab_ys[1] - slab_ys[0] if len(slab_ys) > 1 else 10.0

slab_beam_count = 0
for b in beams:
    for j, sy in enumerate(slab_ys):
        bc = beam_segment_centroids.get((b.global_id, j))
        if not bc:
            continue
        for s in slabs:
            sc = slab_centroids.get(s.global_id)
            if not sc:
                continue
            if abs(sc.x - bc.x) < spacing_x * 0.6 and abs(sc.y - bc.y) < spacing_y * 0.6:
                viewer.scene.add(
                    Line(sc, bc),
                    name=f"{s.name} - {b.name}[{j}]",
                    parent=slab_beam_group,
                    linecolor=BEAM_EDGE_COLOR,
                    linewidth=3,
                )
                mid = Point((sc.x + bc.x) / 2, (sc.y + bc.y) / 2, (sc.z + bc.z) / 2)
                label = f"{short_name(s)} <-> {short_name(b)}"
                viewer.scene.add(
                    Tag(label, mid, color=BEAM_LABEL_COLOR, height=TAG_HEIGHT),
                    parent=slab_beam_group,
                )
                node_points.add((bc.x, bc.y, bc.z))
                slab_beam_count += 1

# -- Compute beam-beam adjacency (same X, consecutive Y bays) ---------------

# Group beams by X position
beam_by_x = {}
for b in beams:
    c = element_centroid(b)
    if c:
        xk = round(c.x, 3)
        beam_by_x.setdefault(xk, []).append(b)

beam_beam_count = 0
for xk, blist in beam_by_x.items():
    # Sort by Y centroid
    blist.sort(key=lambda b: element_centroid(b).y)
    for k in range(len(blist) - 1):
        b1, b2 = blist[k], blist[k + 1]
        c1 = element_centroid(b1, z_offset=z_off)
        c2 = element_centroid(b2, z_offset=z_off)
        if c1 and c2:
            viewer.scene.add(
                Line(c1, c2),
                name=f"{b1.name} - {b2.name}",
                parent=beam_beam_group,
                linecolor=BB_EDGE_COLOR,
                linewidth=3,
            )
            mid = Point((c1.x + c2.x) / 2, (c1.y + c2.y) / 2, (c1.z + c2.z) / 2)
            label = f"{short_name(b1)} <-> {short_name(b2)}"
            viewer.scene.add(
                Tag(label, mid, color=BB_LABEL_COLOR, height=TAG_HEIGHT),
                parent=beam_beam_group,
            )
            node_points.add((c1.x, c1.y, c1.z))
            node_points.add((c2.x, c2.y, c2.z))
            beam_beam_count += 1

# -- Draw nodes at centroids ------------------------------------------------

for pt in node_points:
    viewer.scene.add(
        Point(*pt),
        name="node",
        parent=graph_group,
        pointcolor=NODE_COLOR,
        pointsize=12,
    )

print(f"Graph: {slab_slab_count} slab-slab, {slab_beam_count} slab-beam, {beam_beam_count} beam-beam, {len(node_points)} nodes")

treeform = Treeform()
viewer.ui.sidebar.add(treeform)
viewer.show()
