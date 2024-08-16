"""
********************************************************************************
compas_ifc
********************************************************************************

.. currentmodule:: compas_ifc


.. toctree::
    :maxdepth: 1

    compas_ifc.attributes
    compas_ifc.entities
    compas_ifc.helpers
    compas_ifc.model
    compas_ifc.representation
    compas_ifc.resources
    compas_ifc.viewer

"""

from __future__ import print_function

import os


__author__ = ["tom van mele"]
__copyright__ = "ETH Zurich"
__license__ = "MIT License"
__email__ = "van.mele@arch.ethz.ch"
__version__ = "1.2.3"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

__all_plugins__ = [
    "compas_ifc.brep",
]
