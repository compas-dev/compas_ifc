"""Hand-written extensions applied to entities by IFC class.

Each extension is registered through the :func:`compas_ifc.entities.base.extends`
decorator. Importing this package executes those decorators and populates
``compas_ifc.entities.base._extension_registry``.
"""

from .IfcBuilding import IfcBuildingExtras  # noqa: F401
from .IfcContext import IfcContextExtras  # noqa: F401
from .IfcElement import IfcElementExtras  # noqa: F401
from .IfcObject import IfcObjectExtras  # noqa: F401
from .IfcObjectDefinition import IfcObjectDefinitionExtras  # noqa: F401
from .IfcProduct import IfcProductExtras  # noqa: F401
from .IfcProject import IfcProjectExtras  # noqa: F401
from .IfcSite import IfcSiteExtras  # noqa: F401
from .IfcSpatialElement import IfcSpatialContainerExtras  # noqa: F401
