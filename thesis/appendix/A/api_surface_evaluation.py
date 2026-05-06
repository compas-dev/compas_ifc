"""
API Surface Evaluation
======================

Measures the number of user-facing (public) APIs exposed by the two main
classes: ``BuildingInformationModel`` and ``GenericElement``.

Public APIs are methods and properties whose name does NOT start with ``_``.
Inherited members from ``compas_model`` base classes are reported separately
so the table shows what ``compas_ifc`` *adds* on top of the framework.

Abstract method implementations (``compute_*`` stubs that ``compas_model``
requires subclasses to override) are counted separately since they fulfil a
framework contract rather than represent new functionality.

Output: a summary table suitable for inclusion in the thesis.
"""

import inspect

from compas_model.elements import Element
from compas_model.models import Model

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.element import GenericElement
from compas_ifc.factory import ElementFactoryMixin
from compas_ifc.interactions import InteractionMixin
from compas_ifc.tree import TreeMixin


# ==========================================================================
# Helpers
# ==========================================================================


def public_members(cls):
    """Return a sorted list of public method/property names defined on *cls* itself (not inherited)."""
    members = []
    for name, obj in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        # Only include if defined directly on cls (not inherited)
        for klass in cls.__mro__:
            if name in klass.__dict__:
                if klass is cls:
                    members.append(name)
                break
    return sorted(set(members))


def all_public_members(cls):
    """Return a sorted list of ALL public method/property names visible on *cls* (including inherited)."""
    return sorted({name for name, _ in inspect.getmembers(cls) if not name.startswith("_")})


def classify_member(cls, name):
    """Return 'property', 'classmethod', 'staticmethod', or 'method'."""
    for klass in cls.__mro__:
        if name in klass.__dict__:
            obj = klass.__dict__[name]
            if isinstance(obj, property):
                return "property"
            if isinstance(obj, classmethod):
                return "classmethod"
            if isinstance(obj, staticmethod):
                return "staticmethod"
            if callable(obj):
                return "method"
            break
    return "attribute"


def find_abstract_methods(base_cls):
    """Find methods on *base_cls* that raise NotImplementedError (abstract stubs).

    These are the methods that subclasses are required to override.
    """
    abstract = []
    for name in sorted(base_cls.__dict__):
        if name.startswith("_"):
            continue
        obj = base_cls.__dict__[name]
        if not callable(obj):
            continue
        try:
            source = inspect.getsource(obj)
            if "raise NotImplementedError" in source:
                abstract.append(name)
        except (TypeError, OSError):
            pass
    return abstract


# ==========================================================================
# Detect abstract methods from compas_model.Element
# ==========================================================================

element_abstract = find_abstract_methods(Element)
print(f"compas_model.Element abstract stubs ({len(element_abstract)}):")
for name in element_abstract:
    print(f"  {name}")

# ==========================================================================
# Analyse BuildingInformationModel
# ==========================================================================

print("\n" + "=" * 70)
print("API Surface: BuildingInformationModel")
print("=" * 70)

bim_own = public_members(BuildingInformationModel)
bim_from_factory = public_members(ElementFactoryMixin)
bim_from_interaction = public_members(InteractionMixin)
bim_from_tree = public_members(TreeMixin)
bim_from_model = public_members(Model)
bim_all = all_public_members(BuildingInformationModel)

print(f"\nTotal public API surface: {len(bim_all)} members")
print(f"  Defined on BuildingInformationModel:  {len(bim_own)}")
print(f"  From ElementFactoryMixin:             {len(bim_from_factory)}")
print(f"  From InteractionMixin:                {len(bim_from_interaction)}")
print(f"  From TreeMixin:                       {len(bim_from_tree)}")
print(f"  Inherited from compas_model.Model:    {len(bim_from_model)}")

print(f"\n--- BuildingInformationModel own ({len(bim_own)}) ---")
for name in bim_own:
    kind = classify_member(BuildingInformationModel, name)
    print(f"  {kind:12s}  {name}")

print(f"\n--- ElementFactoryMixin ({len(bim_from_factory)}) ---")
for name in bim_from_factory:
    kind = classify_member(ElementFactoryMixin, name)
    print(f"  {kind:12s}  {name}")

print(f"\n--- InteractionMixin ({len(bim_from_interaction)}) ---")
for name in bim_from_interaction:
    kind = classify_member(InteractionMixin, name)
    print(f"  {kind:12s}  {name}")

print(f"\n--- TreeMixin ({len(bim_from_tree)}) ---")
for name in bim_from_tree:
    kind = classify_member(TreeMixin, name)
    print(f"  {kind:12s}  {name}")

# ==========================================================================
# Analyse GenericElement
# ==========================================================================

print("\n" + "=" * 70)
print("API Surface: GenericElement")
print("=" * 70)

elem_own = public_members(GenericElement)
elem_from_element = public_members(Element)
elem_all = all_public_members(GenericElement)

# Split own into abstract overrides vs novel API
elem_abstract_overrides = [n for n in elem_own if n in element_abstract]
elem_novel = [n for n in elem_own if n not in element_abstract]

print(f"\nTotal public API surface: {len(elem_all)} members")
print(f"  Defined on GenericElement:            {len(elem_own)}")
print(f"    Novel (compas_ifc-specific):        {len(elem_novel)}")
print(f"    Abstract overrides (compas_model):  {len(elem_abstract_overrides)}")
print(f"  Inherited from compas_model.Element:  {len(elem_from_element)}")

print(f"\n--- GenericElement novel API ({len(elem_novel)}) ---")
for name in elem_novel:
    kind = classify_member(GenericElement, name)
    print(f"  {kind:12s}  {name}")

print(f"\n--- Abstract overrides ({len(elem_abstract_overrides)}) ---")
for name in elem_abstract_overrides:
    kind = classify_member(GenericElement, name)
    print(f"  {kind:12s}  {name}")

# ==========================================================================
# Summary table
# ==========================================================================

print("\n" + "=" * 70)
print("SUMMARY TABLE")
print("=" * 70)

# compas_ifc-specific public API = own + mixin contributions (excluding abstract overrides)
bim_compas_ifc = sorted(set(bim_own) | set(bim_from_factory) | set(bim_from_interaction) | set(bim_from_tree))

print(f"\n{'Class':<35s} {'Novel API':>10s} {'Abstract':>10s} {'Inherited':>10s} {'Total':>8s}")
print("-" * 75)
print(f"{'BuildingInformationModel':<35s} {len(bim_compas_ifc):>10d} {0:>10d} {len(bim_all) - len(bim_compas_ifc):>10d} {len(bim_all):>8d}")
print(f"{'GenericElement':<35s} {len(elem_novel):>10d} {len(elem_abstract_overrides):>10d} {len(elem_all) - len(elem_own):>10d} {len(elem_all):>8d}")
print("-" * 75)
total_novel = len(bim_compas_ifc) + len(elem_novel)
total_abstract = len(elem_abstract_overrides)
print(f"{'TOTAL':<35s} {total_novel:>10d} {total_abstract:>10d}")

print(f"\n--- Novel compas_ifc API on BuildingInformationModel ({len(bim_compas_ifc)}) ---")
for name in bim_compas_ifc:
    source = "bim"
    if name in bim_from_factory:
        source = "ElementFactoryMixin"
    elif name in bim_from_interaction:
        source = "InteractionMixin"
    elif name in bim_from_tree:
        source = "TreeMixin"
    kind = classify_member(BuildingInformationModel, name)
    print(f"  {kind:12s}  {name:40s}  [{source}]")

print(f"\n--- Novel compas_ifc API on GenericElement ({len(elem_novel)}) ---")
for name in elem_novel:
    kind = classify_member(GenericElement, name)
    print(f"  {kind:12s}  {name}")
