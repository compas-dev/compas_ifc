"""Extension for spatial container entities — children traversal.

In IFC2X3 the canonical spatial-container parent is
``IfcSpatialStructureElement``. IFC4 introduced a new ``IfcSpatialElement``
superclass and made ``IfcSpatialStructureElement`` a subclass of it. This
extension binds to whichever class is canonical for the loaded schema:

- ``IfcSpatialElement`` in IFC4 and IFC4X3
- ``IfcSpatialStructureElement`` in IFC2X3 (which has no
  ``IfcSpatialElement``)

The schema-asymmetric binding is encoded as stacked ``@extends``
decorators rather than as a hand-maintained pair of cross-referenced
files. The synthetic-class de-dup in :meth:`Base.__new__` ensures the
extension is mixed in only once per entity, even when an entity (e.g.
an IFC4 ``IfcSite``) satisfies both registrations.
"""

from typing import TYPE_CHECKING

from compas_ifc.entities.base import Base
from compas_ifc.entities.base import extends

if TYPE_CHECKING:
    from compas_ifc.entities.generated import IfcSpatialElement


@extends("IfcSpatialElement")
@extends("IfcSpatialStructureElement", schemas={"IFC2X3"})
class IfcSpatialContainerExtras(Base):
    """Extras applied to IFC entities that act as spatial containers.

    Adds a unified :attr:`children` property that combines the entity's
    ``IsDecomposedBy`` aggregation children (provided by
    :class:`IfcObjectDefinitionExtras`) with the ``ContainsElements``
    spatial-containment children defined here.
    """

    @property
    def children(self: "IfcSpatialElement"):
        children = super().children
        children += sum(
            [relation.RelatedElements for relation in self.ContainsElements()],
            [],
        )
        return list(set(children))
