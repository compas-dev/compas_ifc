from pprint import pprint
from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")

assert len(model.projects) > 0

project = model.projects[0]

# =============================================================================
# Info
# =============================================================================

print("\n" + "*" * 53)
print("Project")
print("*" * 53 + "\n")

project.print_inheritance()

print("\nAttributes")
print("=" * 53 + "\n")

pprint(project.attributes)

print("\nProperties")
print("=" * 53 + "\n")

pprint(project.properties)

print("\nRepresentation Contexts")
print("=" * 53 + "\n")

pprint(project.contexts)

print("\nUnits")
print("=" * 53 + "\n")

pprint(project.units)

print("\nModel Context")
print("=" * 53 + "\n")

print(f"Reference Frame: {project.frame}")
print(f"True North: {project.north}")

print("\nSites")
print("=" * 53 + "\n")

print(project.sites)

print()
