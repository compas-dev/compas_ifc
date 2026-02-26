"""Integrated Workflow
====================

Pure workflow code — no test assertions or reporting.
Demonstrates all front-end model capabilities in a single script:

    custom element class -> template model -> validation enforcement ->
    array creation -> columns -> compute_connections -> save/reload -> extract

Uses ``temp/devday/rfs.stp`` as the funicular slab unit geometry.
"""

import math

from pydantic import BaseModel
from pydantic import Field

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Rotation
from compas.geometry import Transformation
from compas.geometry import Vector
from compas_occ.brep import OCCBrep

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.element import GenericElement
from compas_ifc.representations import Extrusion
from compas_ifc.validation import Specification
from compas_ifc.validation import validate_element
from compas_ifc.validation import validate_model

# ===========================================================================
# Property set schemas
# ===========================================================================


class SlabCommonSchema(BaseModel):
    """IFC standard Pset_SlabCommon (selected fields)."""

    Reference: str = Field(min_length=1)
    Status: str = Field(pattern="^(NEW|EXISTING|DEMOLISH|TEMPORARY)$")
    LoadBearing: bool
    IsExternal: bool
    FireRating: str = Field(min_length=1)
    ThermalTransmittance: float = Field(gt=0)


class EnvironmentalImpactSchema(BaseModel):
    """IFC standard Pset_EnvironmentalImpactIndicators (selected fields)."""

    ExpectedServiceLife: float = Field(gt=0)
    ClimateChangePerUnit: float = Field(gt=0)  # kg CO2 eq
    TotalPrimaryEnergyConsumptionPerUnit: float = Field(gt=0)  # MJ
    WaterConsumptionPerUnit: float = Field(gt=0)  # m3
    NonHazardousWastePerUnit: float = Field(ge=0)  # kg
    InertWastePerUnit: float = Field(ge=0)  # kg


class ConcreteRecipeSchema(BaseModel):
    """Custom pset based on concrete mix design."""

    RecipeName: str = Field(min_length=1)
    CementType: str = Field(min_length=1)
    AggregateType: str = Field(min_length=1)
    AggregateSize_mm: float = Field(gt=0)
    WaterContent_kg_m3: float = Field(gt=0)
    MixRatios: str = Field(min_length=1)
    UnitWeight_kg_m3: float = Field(gt=0)
    CompressiveStrength_MPa: float = Field(gt=0)
    Workability_mm: float = Field(gt=0)


class FunicularSlabSchema(BaseModel):
    """Combined schema — field names map to IFC property set names."""

    Pset_SlabCommon: SlabCommonSchema
    Pset_EnvironmentalImpactIndicators: EnvironmentalImpactSchema
    ConcreteRecipeProperties: ConcreteRecipeSchema


# ===========================================================================
# Custom element class
# ===========================================================================

GRID_SIZE = 3
COLUMN_SECTION = 0.3  # metres
COLUMN_HEIGHT = 3.0  # metres


class FunicularSlabUnit(GenericElement):
    """Prefabricated funicular slab unit.

    The geometry source (STEP file) and default structural, environmental,
    and material properties are defined as part of the class, making each
    instance self-describing.
    """

    STEP_PATH = "temp/devday/rfs.stp"
    STEP_SCALE = 0.001  # STEP file is in mm, IFC model is in m
    Schema = FunicularSlabSchema
    _cached_brep = None

    DEFAULTS_SLAB_COMMON = {
        "Reference": "FSU-01",
        "Status": "NEW",
        "LoadBearing": True,
        "IsExternal": False,
        "FireRating": "REI90",
        "ThermalTransmittance": 0.25,
    }

    DEFAULTS_ENVIRONMENTAL = {
        "ExpectedServiceLife": 50.0,
        "ClimateChangePerUnit": 42.5,
        "TotalPrimaryEnergyConsumptionPerUnit": 620.0,
        "WaterConsumptionPerUnit": 0.18,
        "NonHazardousWastePerUnit": 12.0,
        "InertWastePerUnit": 85.0,
    }

    DEFAULTS_RECIPE = {
        "RecipeName": "High-Strength Concrete Mix",
        "CementType": "Portland Cement Type I",
        "AggregateType": "Crushed Stone",
        "AggregateSize_mm": 20.0,
        "WaterContent_kg_m3": 200.0,
        "MixRatios": "1:1.5:3:0.4",
        "UnitWeight_kg_m3": 2400.0,
        "CompressiveStrength_MPa": 50.0,
        "Workability_mm": 100.0,
    }

    @classmethod
    def _load_geometry(cls):
        """Load, scale (mm -> m), and cache the BRep geometry."""
        if cls._cached_brep is None:
            cls._cached_brep = OCCBrep.from_step(cls.STEP_PATH).scaled(cls.STEP_SCALE)
        return cls._cached_brep

    @classmethod
    def specification(cls):
        """Return a Specification that enforces all three schemas."""
        return Specification(
            name="FunicularSlabUnit",
            ifc_types=["IfcSlab"],
            required_psets=cls.Schema,
        )

    def __init__(self, name=None, frame=None, slab_common=None, environmental=None, recipe=None, **kwargs):
        transformation = Transformation.from_frame(frame) if frame else None
        super().__init__(
            ifc_type="IfcSlab",
            geometry=self._load_geometry(),
            transformation=transformation,
            name=name,
            **kwargs,
        )
        self._properties = {
            "Pset_SlabCommon": {**self.DEFAULTS_SLAB_COMMON, **(slab_common or {})},
            "Pset_EnvironmentalImpactIndicators": {**self.DEFAULTS_ENVIRONMENTAL, **(environmental or {})},
            "ConcreteRecipeProperties": {**self.DEFAULTS_RECIPE, **(recipe or {})},
        }


# ===========================================================================
# Workflow
# ===========================================================================


def run(out_path="temp/thesis_integrated_workflow.ifc", extract_path="temp/thesis_integrated_extract.ifc"):
    """Execute the full integrated workflow and return key objects for verification."""

    brep = FunicularSlabUnit._load_geometry()
    slab_bb = brep.aabb
    SPACING_X = slab_bb.xsize
    SPACING_Y = slab_bb.ysize

    # 1. Template model with specification enforcement
    model = BuildingInformationModel.template(schema="IFC4", unit="m", use_occ=True)
    spec = FunicularSlabUnit.specification()
    model.specifications = [spec]
    storey = model.storeys[0]

    # 2. Validate before adding
    bad = FunicularSlabUnit(name="bad_unit", environmental={"ClimateChangePerUnit": -1.0})
    bad_results = validate_element(bad, [spec])

    good = FunicularSlabUnit(name="good_unit")
    good_results = validate_element(good, [spec])

    # 3. Slab array (3x3, touching)
    units = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            u = FunicularSlabUnit(
                name=f"FSU_{i}_{j}",
                frame=Frame(Point(i * SPACING_X, j * SPACING_Y, 0), Vector.Xaxis(), Vector.Yaxis()),
            )
            model.add_element(u, parent=storey)
            units.append(u)

    # 4. Column array (4x4, at slab corners, rotated 45 deg)
    half_x = SPACING_X / 2
    half_y = SPACING_Y / 2
    slab_z_max = max(p.z for p in brep.points)
    R45 = Rotation.from_axis_and_angle(Vector.Zaxis(), math.radians(45))
    col_xaxis = Vector.Xaxis()
    col_yaxis = Vector.Yaxis()
    col_xaxis.transform(R45)
    col_yaxis.transform(R45)

    s = COLUMN_SECTION / 2
    col_profile = Polygon([Point(-s, -s, 0), Point(s, -s, 0), Point(s, s, 0), Point(-s, s, 0)])
    col_extrusion = Extrusion(profile=col_profile, direction=Vector(0, 0, 1), depth=COLUMN_HEIGHT)

    columns = []
    for ci in range(GRID_SIZE + 1):
        for cj in range(GRID_SIZE + 1):
            cx = ci * SPACING_X - half_x
            cy = cj * SPACING_Y - half_y
            cz = slab_z_max - COLUMN_HEIGHT
            col_frame = Frame(Point(cx, cy, cz), col_xaxis, col_yaxis)
            col = model.create_element(
                ifc_type="IfcColumn",
                name=f"COL_{ci}_{cj}",
                geometry=col_extrusion,
                frame=col_frame,
                parent=storey,
            )
            columns.append(col)

    # 5. Automatic connection detection
    edge_count = model.compute_connections(element_types=["IfcSlab"])

    # 6. Validate entire model
    model_results = validate_model(model, [spec])

    # 7. Save
    model.save(out_path)

    # 8. Reload
    model2 = BuildingInformationModel(out_path, rectify_placements=True, load_geometries=False)

    # 9. Granular extract
    storey2 = model2.storeys[0]
    sub = model2.extract(storey2, path=extract_path, load_geometries=False)

    return {
        "brep": brep,
        "model": model,
        "model2": model2,
        "sub": sub,
        "spec": spec,
        "units": units,
        "columns": columns,
        "bad_results": bad_results,
        "good_results": good_results,
        "model_results": model_results,
        "edge_count": edge_count,
        "out_path": out_path,
        "extract_path": extract_path,
        "SPACING_X": SPACING_X,
        "SPACING_Y": SPACING_Y,
    }
