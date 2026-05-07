"""Hand-written extensions applied to entities by IFC class.

Each extension is registered through the ``@extends`` decorator at class
definition time (Phase 2 of the stubs migration). During Phase 1 of the
migration, the existing extensions still inherit from ``object`` via the
``if TYPE_CHECKING`` placeholder pattern, so this module bootstraps the
extension registry by class name as a transitional step.
"""

from compas_ifc.entities.base import _extension_registry

from .IfcObjectDefinition import IfcObjectDefinition  # noqa: F401
from .IfcObject import IfcObject  # noqa: F401
from .IfcContext import IfcContext  # noqa: F401
from .IfcElement import IfcElement  # noqa: F401
from .IfcSpatialElement import IfcSpatialElement  # noqa: F401
from .IfcSpatialStructureElement import IfcSpatialStructureElement  # noqa: F401
from .IfcProduct import IfcProduct  # noqa: F401
from .IfcProject import IfcProject  # noqa: F401
from .IfcSite import IfcSite  # noqa: F401
from .IfcBuilding import IfcBuilding  # noqa: F401


# Phase-1 transitional bootstrap: register the existing class-name based
# extensions in the runtime registry. Phase 2 of the stubs migration will
# replace this block with explicit ``@extends`` decorators on each class.
for _ext in (
    IfcObjectDefinition,
    IfcObject,
    IfcContext,
    IfcElement,
    IfcSpatialElement,
    IfcSpatialStructureElement,
    IfcProduct,
    IfcProject,
    IfcSite,
    IfcBuilding,
):
    _extension_registry.setdefault(_ext.__name__, []).append((_ext, None))

del _ext
