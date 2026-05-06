"""Tests for :mod:`compas_ifc.validation`."""

from __future__ import annotations

import pytest
from pydantic import BaseModel
from pydantic import Field

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.validation import Specification
from compas_ifc.validation import validate_element
from compas_ifc.validation import validate_model


class PsetSlabSimple(BaseModel):
    LoadBearing: bool
    FireRating: str = Field(min_length=1)


def _model_with_validated_slab(load_bearing: bool = True, fire_rating: str = "REI60"):
    model = BuildingInformationModel.template(unit="m")
    storey = model.storeys[0]
    spec = Specification(
        name="Slab requirement",
        ifc_types=["IfcSlab"],
        required_psets={"Pset_SlabSimple": PsetSlabSimple},
    )
    model.specifications = [spec]
    slab = model.create_slab(
        name="Slab1",
        parent=storey,
        properties={"Pset_SlabSimple": {"LoadBearing": load_bearing, "FireRating": fire_rating}},
    )
    return model, slab, spec


def test_validate_model_pass():
    model, _slab, spec = _model_with_validated_slab()
    results = validate_model(model, [spec])
    assert results, "Expected at least one validation result"
    assert all(r.status == "pass" for r in results)


def test_validate_element_detects_missing_property():
    model = BuildingInformationModel.template(unit="m")
    storey = model.storeys[0]
    spec = Specification(
        name="Slab requirement",
        ifc_types=["IfcSlab"],
        required_psets={"Pset_SlabSimple": PsetSlabSimple},
    )
    slab = model.create_slab(name="Bad", parent=storey)  # no properties
    results = validate_element(slab, [spec])
    assert any(r.status == "fail" for r in results)


def test_specification_enforcement_rejects_at_insertion():
    model = BuildingInformationModel.template(unit="m")
    storey = model.storeys[0]
    model.specifications = [
        Specification(
            name="Slab requirement",
            ifc_types=["IfcSlab"],
            required_psets={"Pset_SlabSimple": PsetSlabSimple},
        )
    ]
    with pytest.raises(ValueError):
        model.create_slab(name="MissingProps", parent=storey)
