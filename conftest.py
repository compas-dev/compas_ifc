import math

import compas
import numpy
import pytest
from compas.geometry import allclose

import compas_ifc


def pytest_ignore_collect(collection_path):
    p = str(collection_path)
    if "rhino" in p:
        return True
    if "blender" in p:
        return True
    if "ghpython" in p:
        return True
    if p.endswith("_cli.py"):
        return True


@pytest.fixture(autouse=True)
def add_compas(doctest_namespace):
    doctest_namespace["compas"] = compas


@pytest.fixture(autouse=True)
def add_compas_ifc(doctest_namespace):
    doctest_namespace["compas_ifc"] = compas_ifc


@pytest.fixture(autouse=True)
def add_math(doctest_namespace):
    doctest_namespace["math"] = math


@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace["np"] = numpy


@pytest.fixture(autouse=True)
def add_allclose(doctest_namespace):
    doctest_namespace["allclose"] = allclose
