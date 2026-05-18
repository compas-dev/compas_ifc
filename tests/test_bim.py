"""Smoke tests for :class:`compas_ifc.bim.BuildingInformationModel`."""

from __future__ import annotations

import os

import pytest
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

from compas_ifc.bim import BuildingInformationModel
from compas_ifc.element import GenericElement


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DUPLEX_PATH = os.path.join(REPO_ROOT, "data", "Duplex_A_20110907.ifc")
SMALL_PATH = os.path.join(REPO_ROOT, "data", "wall-with-opening-and-window.ifc")


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_template_creates_default_hierarchy():
    model = BuildingInformationModel.template(schema="IFC4", unit="m")
    assert model.schema_name == "IFC4"
    assert model.unit == "m"
    assert len(model.sites) == 1
    assert len(model.buildings) == 1
    assert len(model.storeys) == 1


def test_template_supports_multiple_buildings_and_storeys():
    model = BuildingInformationModel.template(building_count=2, storey_count=3, unit="m")
    assert len(model.buildings) == 2
    assert len(model.storeys) == 6


# ---------------------------------------------------------------------------
# Element factory + validation
# ---------------------------------------------------------------------------


def test_create_element_appends_to_storey():
    model = BuildingInformationModel.template(unit="m")
    storey = model.storeys[0]
    wall = model.create_wall(name="W1", parent=storey)
    assert isinstance(wall, GenericElement)
    assert wall.ifc_type == "IfcWall"
    assert wall in [c for c in storey.children]


def test_create_element_normalises_arbitrary_type_string():
    model = BuildingInformationModel.template(unit="m")
    storey = model.storeys[0]
    elem = model.create_element(ifc_type="CustomBracket", parent=storey, name="Bracket")
    # Custom (unknown) ifc types fall back to IfcBuildingElementProxy when written
    assert elem.ifc_type in {"CustomBracket", "IfcBuildingElementProxy"}


# ---------------------------------------------------------------------------
# Round-trip stability against a real model
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not os.path.exists(SMALL_PATH), reason="small reference IFC missing")
def test_open_small_model():
    model = BuildingInformationModel(SMALL_PATH, load_geometries=False)
    assert model.schema_name in {"IFC4", "IFC2X3", "IFC4X3"}
    assert len(model.building_elements) >= 1


@pytest.mark.skipif(not os.path.exists(DUPLEX_PATH), reason="Duplex IFC missing")
def test_duplex_hierarchy_is_loaded():
    model = BuildingInformationModel(DUPLEX_PATH, load_geometries=False)
    assert len(model.sites) >= 1
    assert len(model.storeys) >= 1
    assert len(model.building_elements) > 100


@pytest.mark.skipif(not os.path.exists(DUPLEX_PATH), reason="Duplex IFC missing")
def test_get_element_by_global_id_round_trips():
    model = BuildingInformationModel(DUPLEX_PATH, load_geometries=False)
    sample = model.building_elements[0]
    assert sample.global_id is not None
    assert model.get_element_by_global_id(sample.global_id) is sample


@pytest.mark.skipif(not os.path.exists(DUPLEX_PATH), reason="Duplex IFC missing")
def test_get_elements_by_type_filters_correctly():
    model = BuildingInformationModel(DUPLEX_PATH, load_geometries=False)
    walls = model.get_elements_by_type("IfcWall")
    assert all(e._ifc_entity.is_a("IfcWall") for e in walls)


# ---------------------------------------------------------------------------
# Clash detection — type filter must honour IFC subclass matching
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not os.path.exists(DUPLEX_PATH), reason="Duplex IFC missing")
def test_compute_collisions_type_filter_matches_subclasses():
    # Duplex's walls are IfcWallStandardCase (a subclass of IfcWall), so an
    # exact-match filter on "IfcWall" would silently skip them all and report
    # zero pairs. Subclass-aware matching should reach the same 15 structural+
    # envelope clashes whether you list the subclass explicitly or not.
    model = BuildingInformationModel(DUPLEX_PATH, rectify_placements=True)
    n = model.compute_collisions(
        element_types=["IfcBeam", "IfcSlab", "IfcWall"],
        create_ifc_relations=False,
    )
    assert n == 15


# ---------------------------------------------------------------------------
# Save/extract behaviour
# ---------------------------------------------------------------------------


def test_save_and_reload(tmp_path):
    model = BuildingInformationModel.template(unit="m")
    storey = model.storeys[0]
    model.create_wall(
        name="W1",
        parent=storey,
        frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0)),
    )
    out = tmp_path / "smoke.ifc"
    model.save(str(out))
    assert out.exists() and out.stat().st_size > 0

    reloaded = BuildingInformationModel(str(out), load_geometries=False)
    assert len(reloaded.storeys) == 1
    assert len(reloaded.get_elements_by_type("IfcWall")) == 1
