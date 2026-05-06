"""
********************************************************************************
compas_ifc
********************************************************************************

.. currentmodule:: compas_ifc

A front-end data model for Industry Foundation Classes (IFC).

The user-facing API is small: a single :class:`~compas_ifc.bim.BuildingInformationModel`
class is the entry point for opening, querying, modifying, and saving IFC
files; a single :class:`~compas_ifc.element.GenericElement` represents every
building element regardless of IFC type. The interaction graph,
spatial-hierarchy tree, geometry kernel, and validation engine are exposed
through this front end.

.. toctree::
    :maxdepth: 1

    compas_ifc.bim
    compas_ifc.element
    compas_ifc.factory
    compas_ifc.tree
    compas_ifc.interactions
    compas_ifc.validation
    compas_ifc.representations
    compas_ifc.brep

"""

from __future__ import print_function

import os


__author__ = ["Li Chen", "Tom Van Mele"]
__copyright__ = "ETH Zurich"
__license__ = "MIT License"
__email__ = "li.chen@arch.ethz.ch"
__version__ = "1.7.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

__all_plugins__ = [
    "compas_ifc.brep",
]
