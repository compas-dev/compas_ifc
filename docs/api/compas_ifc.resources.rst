********************************************************************************
resources
********************************************************************************

.. currentmodule:: compas_ifc.resources

This module contains functions for converting between IFC geometry resources and equivalent COMPAS geometry objects.

Functions
=========

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
    IfcCompoundPlaneAngleMeasure_to_degrees
    IfcGridPlacement_to_transformation
    IfcLocalPlacement_to_transformation
    IfcLocalPlacement_to_frame
    IfcAdvancedBrep_to_brep
    IfcAdvancedBrepWithVoids_to_brep
    IfcBlock_to_box
    IfcBooleanClippingResult_to_brep
    IfcBoundingBox_to_box
    IfcIndexedPolyCurve_to_lines
    IfcExtrudedAreaSolid_to_brep
    IfcFacetedBrep_to_brep
    IfcFacetedBrepWithVoids_to_brep
    IfcIndexedPolygonalFaceSet_to_brep
    IfcPolygonalBoundedHalfSpace_to_brep
    IfcPolygonalFaceSet_to_brep
    IfcTessellatedFaceSet_to_brep
    IfcTriangulatedFaceSet_to_brep
    IfcShape_to_brep
    IfcShape_to_tessellatedbrep
    frame_to_ifc_axis2_placement_3d
