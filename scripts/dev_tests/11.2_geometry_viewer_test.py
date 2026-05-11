"""
11.2 Geometry Viewer Test
=========================

Visual test for Phase 1 geometry reading.  Opens a viewer showing
all parsed COMPAS geometries from the Duplex model, colour-coded
and grouped by representation type:

- **Blue**   : Extrusion  (IfcExtrudedAreaSolid)
- **Green**  : Mesh       (IfcFaceBasedSurfaceModel / IfcPolygonalFaceSet)
- **Orange** : Fallback   (TessellatedBrep — unparsed, e.g. IfcBooleanClipping)
- **Red**    : CSG prim   (Box, Sphere, Cone, Cylinder)

Extrusion objects are converted to meshes via ``Extrusion.to_mesh()``
and the extrusion's local frame is composed with the entity placement
so the viewer can render them at the correct world position.
"""

from compas.colors import Color
from compas.geometry import Box, Sphere, Cone, Cylinder, Transformation
from compas.datastructures import Mesh
from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import Extrusion
from compas_ifc.brep import TessellatedBrep

# ------------------------------------------------------------------
# Colour palette
# ------------------------------------------------------------------
COLOR_EXTRUSION = Color(0.3, 0.5, 0.9)  # blue
COLOR_MESH = Color(0.3, 0.8, 0.4)  # green
COLOR_FALLBACK = Color(0.9, 0.6, 0.2)  # orange
COLOR_CSG = Color(0.9, 0.3, 0.3)  # red

CSG_TYPES = (Box, Sphere, Cone, Cylinder)

# Map geometry type → (group label, colour)
GROUP_INFO = {
    "Extrusion": ("Extrusions (IfcExtrudedAreaSolid)", COLOR_EXTRUSION),
    "Mesh": ("Meshes (IfcFaceBasedSurfaceModel)", COLOR_MESH),
    "TessellatedBrep": ("Fallbacks (TessellatedBrep)", COLOR_FALLBACK),
    "CSG": ("CSG Primitives (Box/Sphere/...)", COLOR_CSG),
}


def classify_geometry(geom):
    """Return the group key for a parsed geometry object."""
    if isinstance(geom, Extrusion):
        return "Extrusion"
    if isinstance(geom, CSG_TYPES):
        return "CSG"
    if isinstance(geom, Mesh):
        return "Mesh"
    if isinstance(geom, TessellatedBrep):
        return "TessellatedBrep"
    return "TessellatedBrep"  # unknown → fallback group


def geometry_to_viewable(geom):
    """Convert parsed geometry to a viewer-compatible object + world transform.

    For Extrusions the mesh is generated via ``to_mesh()`` and the
    extrusion's local frame is baked into the returned transformation
    so it composes correctly with the entity placement.

    Returns ``(viewable, local_transform)`` or ``(None, None)``.
    *local_transform* is a :class:`Transformation` that should be
    pre-composed with the entity placement.
    """
    if isinstance(geom, Extrusion):
        mesh = geom.to_mesh()
        if mesh is None:
            return None, None
        # The mesh vertices are in extrusion-local coords.
        # We need to apply Extrusion.frame to map them into the
        # product's local coordinate system.
        T_local = Transformation.from_frame(geom.frame)
        return mesh, T_local

    # All other types already store coordinates in the product-local
    # coordinate system — no additional sub-placement needed.
    return geom, Transformation()


# ------------------------------------------------------------------
# Load model
# ------------------------------------------------------------------

model = BuildingInformationModel("data/Duplex_A_20110907.ifc")
products = model.get_elements_by_type("IfcProduct")

# ------------------------------------------------------------------
# Build viewer
# ------------------------------------------------------------------

try:
    from compas_viewer import Viewer
    from compas_viewer.components import Treeform
except ImportError:
    raise ImportError("This script requires compas_viewer.")

viewer = Viewer()
viewer.unit = model.unit

# Create groups
groups = {}
for key, (label, _color) in GROUP_INFO.items():
    groups[key] = viewer.scene.add_group(name=label)

type_counts = {}
total = 0

for element in products:
    if element.ifc_type == "IfcSpace":
        continue

    geom = element.geometry
    if geom is None:
        continue

    viewable, T_local = geometry_to_viewable(geom)
    if viewable is None:
        continue

    total += 1
    group_key = classify_geometry(geom)
    type_name = type(geom).__name__
    type_counts[type_name] = type_counts.get(type_name, 0) + 1

    _, color = GROUP_INFO[group_key]
    parent_group = groups[group_key]
    name = f"[{element.ifc_type}] {element.name}"

    try:
        obj = viewer.scene.add(
            viewable,
            name=name,
            parent=parent_group,
            facecolor=color,
            hide_coplanaredges=True,
        )
        # Compose: entity placement (world) * extrusion sub-placement (local)
        T_entity = Transformation.from_frame(element.frame) if element.frame else Transformation()
        obj.transformation = T_entity * T_local
    except Exception as e:
        print(f"  WARNING: Could not add {name}: {e}")

# ------------------------------------------------------------------
# Print summary
# ------------------------------------------------------------------

print("=" * 60)
print("Viewer: Geometry type distribution")
print("=" * 60)
print(f"Total displayed: {total}\n")
for tname, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    pct = count / total * 100
    print(f"  {tname:30s}  {count:4d}  ({pct:5.1f}%)")
print()
print("Colour legend:")
print("  Blue   = Extrusion  (IfcExtrudedAreaSolid)")
print("  Green  = Mesh       (IfcFaceBasedSurfaceModel)")
print("  Orange = Fallback   (TessellatedBrep)")
print("  Red    = CSG prim   (Box, Sphere, Cone, Cylinder)")

# ------------------------------------------------------------------
# Add sidebar info
# ------------------------------------------------------------------

treeform = Treeform()
viewer.ui.sidebar.add(treeform)


def update_treeform(form, node):
    attrs = node.attributes or {}
    treeform.update_from_dict(attrs)


viewer.ui.sidebar.sceneform.action = update_treeform

viewer.show()
