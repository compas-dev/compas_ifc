import os
from pprint import pprint

from compas_ifc.model import Model

HERE = os.path.dirname(__file__)
FILE = os.path.join(
    HERE,
    "..",
    "data",
    "wall-with-opening-and-window.ifc",
)

model = Model(FILE)
assert len(model.projects) > 0

project = model.projects[0]
assert len(project.sites) > 0

site = project.sites[0]

# =============================================================================
# Info
# =============================================================================

print("\n" + "*" * 53)
print("Site")
print("*" * 53 + "\n")

site.print_inheritance()

print("\nSpatial Structure")
print("=" * 53 + "\n")

site.print_spatial_hierarchy()

print("\nAttributes")
print("=" * 53 + "\n")

pprint(site.attributes)

print("\nProperties")
print("=" * 53 + "\n")

pprint(site.properties)

print("\nBuildings")
print("=" * 53 + "\n")

print(site.buildings)

print()
