"""
********************************************************************************
resources
********************************************************************************

.. currentmodule:: compas_ifc.resources

This module contains functions for converting between IFC geometry resources and equivalent COMPAS geometry objects.
For more information about IFC geometric entities see [geometricmodelresource]_, [geometryresource]_ and [geometricconstraintresource]_.


Functions
=========

Geometry
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    IfcCartesianPoint_to_point
    IfcDirection_to_vector
    IfcVector_to_vector
    IfcLine_to_line
    IfcPlane_to_plane
    IfcAxis2Placement3D_to_frame
    IfcCartesianTransformationOperator3D_to_frame


Geometric Constraint
--------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    IfcGridPlacement_to_transformation
    IfcLocalPlacement_to_transformation


Geometric Model
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    IfcAdvancedBrep_to_brep
    IfcAdvancedBrepWithVoids_to_brep
    IfcBlock_to_box
    IfcBooleanClippingResult_to_brep
    IfcBoundingBox_to_box
    IfcExtrudedAreaSolid_to_brep
    IfcFacetedBrep_to_brep
    IfcFacetedBrepWithVoids_to_brep
    IfcIndexedPolygonalFaceSet_to_brep
    IfcPolygonalBoundedHalfSpace_to_brep
    IfcPolygonalFaceSet_to_brep
    IfcTriangulatedFaceSet_to_brep


References
==========

.. [geometricmodelresource] :ifc:`ifcgeometricmodelresource`
.. [geometryresource] :ifc:`ifcgeometryresource`
.. [geometricconstraintresource] :ifc:`ifcgeometricconstraintresource`

.. [cartesianpoint] :ifc:`ifccartesianpoint`
.. [direction] :ifc:`ifcdirection`
.. [vector] :ifc:`ifcvector`
.. [line] :ifc:`ifcline`
.. [plane] :ifc:`ifcplane`
.. [axis2placement3d] :ifc:`ifcaxis2placement3d`
.. [cartesiantransformationoperator3d] :ifc:`ifccartesiantransformationoperator3d`

.. [gridplacement] :ifc:`ifcgridplacement`
.. [localplacement] :ifc:`ifclocalplacement`

.. [advancedbrep] :ifc:`ifcadvancedbrep`
.. [advancedbrepwithvoids] :ifc:`ifcadvancedbrepwithvoids`
.. [boundingbox] :ifc:`ifcboundingbox`

"""

from .geometry import IfcCartesianPoint_to_point  # noqa: F401
from .geometry import IfcDirection_to_vector  # noqa: F401
from .geometry import IfcVector_to_vector  # noqa: F401
from .geometry import IfcLine_to_line  # noqa: F401
from .geometry import IfcPlane_to_plane  # noqa: F401
from .geometry import IfcAxis2Placement3D_to_frame  # noqa: F401
from .geometry import IfcCartesianTransformationOperator3D_to_frame  # noqa: F401

from .geometricconstraint import IfcGridPlacement_to_transformation  # noqa: F401
from .geometricconstraint import IfcLocalPlacement_to_transformation  # noqa: F401

from .geometricmodel import IfcAdvancedBrep_to_brep  # noqa: F401
from .geometricmodel import IfcAdvancedBrepWithVoids_to_brep  # noqa: F401
from .geometricmodel import IfcBlock_to_box  # noqa: F401
from .geometricmodel import IfcBooleanClippingResult_to_brep  # noqa: F401
from .geometricmodel import IfcBoundingBox_to_box  # noqa: F401
from .geometricmodel import IfcIndexedPolyCurve_to_lines  # noqa: F401
from .geometricmodel import IfcExtrudedAreaSolid_to_brep  # noqa: F401
from .geometricmodel import IfcFacetedBrep_to_brep  # noqa: F401
from .geometricmodel import IfcFacetedBrepWithVoids_to_brep  # noqa: F401
from .geometricmodel import IfcIndexedPolygonalFaceSet_to_brep  # noqa: F401
from .geometricmodel import IfcPolygonalBoundedHalfSpace_to_brep  # noqa: F401
from .geometricmodel import IfcPolygonalFaceSet_to_brep  # noqa: F401
from .geometricmodel import IfcTessellatedFaceSet_to_brep  # noqa: F401
from .geometricmodel import IfcTriangulatedFaceSet_to_brep  # noqa: F401
from .geometricmodel import IfcShape_to_brep  # noqa: F401
from .geometricmodel import IfcShape_to_tessellatedbrep  # noqa: F401

# from .geometricmodel import IfcBoxedHalfSpace
# from .geometricmodel import IfcCartesianPointList
