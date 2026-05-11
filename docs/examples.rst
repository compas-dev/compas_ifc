********************************************************************************
Examples
********************************************************************************

.. rst-class:: lead

Worked examples accompanying the tutorials.

The ``scripts/`` directory of the source repository is split into:

* ``scripts/tutorials/`` — short, focused examples that exercise the front-end
  API one feature at a time.
* ``scripts/dev_tests/`` — longer feature-regression scripts kept around for
  development. These are *not* pytest tests; the proper pytest suite lives in
  ``tests/``, and the formal evaluation suite for chapter 4 of the underlying
  thesis lives in ``thesis/appendix/A/`` with its own ``run_all.py`` runner.

Each script is intended to be runnable from the repository root with the
``compas-ifc`` conda environment.

Tutorials
=========

================================================================ ==================================================================
Script                                                            What it shows
================================================================ ==================================================================
``scripts/tutorials/0.1_overview.py``                             Quickstart: open a model and print its hierarchy.
``scripts/tutorials/1.1_query_entities.py``                       Filter elements by IFC type and by name.
``scripts/tutorials/1.2_traverse_hierarchy.py``                   Walk a multi-storey project tree.
``scripts/tutorials/2.1_project_info.py``                         Project metadata, units, and contexts.
``scripts/tutorials/2.2_site_info.py``                            Site coordinates, north direction, building list.
``scripts/tutorials/2.3_window_info.py``                          Inspect a single window's properties and host opening.
``scripts/tutorials/3.1_model_view.py``                           Render a model in ``compas_viewer``.
``scripts/tutorials/3.2_element_view.py``                         Render only a sub-tree of elements.
``scripts/tutorials/4.1_edit_export.py``                          Modify properties and write the result back.
``scripts/tutorials/4.2_create_new.py``                           Build a model from scratch using the template factory.
``scripts/tutorials/5.1_export_from_rhino.py``                    Draft Rhino-to-IFC export pipeline (run inside Rhino).
``scripts/tutorials/6.1_custom_extension.py``                     Add Python-side helpers to IFC entities via ``@extends``.
``scripts/tutorials/7.1_geometry_ops.py``                         Volume and surface-area queries on a single element.
================================================================ ==================================================================

Feature-regression scripts
==========================

================================================================ ==================================================================
Script                                                            What it shows
================================================================ ==================================================================
``scripts/dev_tests/8.1_brep_generate.py``                        Generates 26 STEP fixtures for the B-Rep test corpus.
``scripts/dev_tests/9.1_building_model_test.py``                  ``BuildingInformationModel`` smoke test.
``scripts/dev_tests/9.4_unified_properties.py``                   Mix schema attributes and pset properties through
                                                                  ``element.properties``.
``scripts/dev_tests/9.5_creation_test.py``                        Programmatic creation of walls, slabs, beams.
``scripts/dev_tests/9.6_rectification_test.py``                   Placement-chain rectification on import.
``scripts/dev_tests/9.7_extraction_test.py``                      Granular subset extraction across multiple scenarios.
``scripts/dev_tests/9.8_graph_test.py``                           Inspect the interaction graph.
``scripts/dev_tests/9.10_auto_connections_test.py``               ``compute_connections`` on a real model.
``scripts/dev_tests/9.11_collision_test.py`` /                    Collision detection and interactive viewer.
``scripts/dev_tests/9.12_collision_viewer.py``
================================================================ ==================================================================

The reproducible evaluation suite for chapter 4 of the thesis is in
``thesis/appendix/A/`` and includes ``run_all.py``, which executes every
section and writes a consolidated report to
``thesis/appendix/A/outputs/A-summary.txt``.
