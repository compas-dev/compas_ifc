"""
12.2 Axis Viewer Test
======================

Visual test for Phase 2 axis representations.  Opens a viewer showing
body geometry (semi-transparent grey) overlaid with axis centerlines
(cyan, thicker lines).

- **Grey**  : Body geometry (semi-transparent)
- **Cyan**  : Axis centerlines
"""

from compas.colors import Color
from compas.geometry import Box, Sphere, Cone, Cylinder, Transformation, Polyline
from compas.datastructures import Mesh
from compas_ifc.bim import BuildingInformationModel
from compas_ifc.representations import Extrusion
from compas_ifc.brep import TessellatedBrep

# ------------------------------------------------------------------
# Colour palette
# ------------------------------------------------------------------
COLOR_BODY = Color(0.7, 0.7, 0.7)  # grey (semi-transparent)
COLOR_AXIS = Color(0.0, 0.9, 0.9)  # cyan

CSG_TYPES = (Box, Sphere, Cone, Cylinder)


def geometry_to_viewable(geom):
    """Convert parsed geometry to a viewer-compatible object + local transform."""
    if isinstance(geom, Extrusion):
        mesh = geom.to_mesh()
        if mesh is None:
            return None, None
        T_local = Transformation.from_frame(geom.frame)
        return mesh, T_local
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
body_group = viewer.scene.add_group(name="Body Geometry")
axis_group = viewer.scene.add_group(name="Axis Centerlines")

body_count = 0
axis_count = 0

for element in products:
    if element.ifc_type == "IfcSpace":
        continue

    name = f"[{element.ifc_type}] {element.name}"
    T_entity = Transformation.from_frame(element.frame) if element.frame else Transformation()

    # --- Body geometry ---
    geom = element.geometry
    if geom is not None:
        viewable, T_local = geometry_to_viewable(geom)
        if viewable is not None:
            body_count += 1
            try:
                obj = viewer.scene.add(
                    viewable,
                    name=name,
                    parent=body_group,
                    facecolor=COLOR_BODY,
                    opacity=0.3,
                    hide_coplanaredges=True,
                )
                obj.transformation = T_entity * T_local
            except Exception as e:
                print(f"  WARNING: Could not add body {name}: {e}")

    # --- Axis representation ---
    axis = element.axis
    if axis is not None:
        axis_count += 1
        # Transform axis points to world coordinates
        axis_world = axis.copy()
        axis_world.transform(T_entity)
        try:
            obj = viewer.scene.add(
                axis_world,
                name=f"Axis: {name}",
                parent=axis_group,
                linecolor=COLOR_AXIS,
                linewidth=3,
            )
        except Exception as e:
            print(f"  WARNING: Could not add axis {name}: {e}")

# ------------------------------------------------------------------
# Print summary
# ------------------------------------------------------------------

print("=" * 60)
print("Viewer: Body + Axis overlay")
print("=" * 60)
print(f"Body elements:   {body_count}")
print(f"Axis centerlines: {axis_count}")

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
