from pprint import pprint
from compas_ifc.model import Model

model = Model("data/wall-with-opening-and-window.ifc")

project = model.project

# =============================================================================
# Info
# =============================================================================

print("\n" + "*" * 53)
print("Project")
print("*" * 53 + "\n")

print("\nAttributes")
print("=" * 53 + "\n")

pprint(project.to_dict())

project.print_attributes(max_depth=3)


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
