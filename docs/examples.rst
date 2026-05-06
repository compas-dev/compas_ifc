********************************************************************************
Examples
********************************************************************************

.. rst-class:: lead

Worked examples accompanying the tutorials.

The ``scripts/`` directory of the source repository contains numbered,
self-contained examples that exercise every part of the front-end API.
Each script is intended to be runnable from the repository root with the
``compas-ifc`` conda environment.

================================================================ ==================================================================
Script                                                            What it shows
================================================================ ==================================================================
``scripts/0.1_overview.py``                                       Quickstart: open Duplex_A and print its hierarchy.
``scripts/1.1_query_entities.py``                                 Filter elements by IFC type and by name.
``scripts/1.2_traverse_hierarchy.py``                             Walk a multi-storey project tree.
``scripts/2.1_project_info.py``                                   Project metadata, units, and contexts.
``scripts/2.2_site_info.py``                                      Site coordinates, north direction, building list.
``scripts/2.3_window_info.py``                                    Inspect a single window's properties and host opening.
``scripts/3.1_model_view.py``                                     Render a model in ``compas_viewer``.
``scripts/3.2_element_view.py``                                   Render only a sub-tree of elements.
``scripts/4.1_edit_export.py``                                    Modify properties and write the result back.
``scripts/4.2_create_new.py``                                     Build a model from scratch using the template factory.
``scripts/9.1_building_model_test.py``                            ``BuildingInformationModel`` smoke test.
``scripts/9.4_unified_properties.py``                             Mix schema attributes and pset properties through
                                                                  ``element.properties``.
``scripts/9.5_creation_test.py``                                  Programmatic creation of walls, slabs, beams.
``scripts/9.6_rectification_test.py``                             Placement-chain rectification on import.
``scripts/9.7_extraction_test.py``                                Granular subset extraction.
``scripts/9.8_graph_test.py``                                     Inspect the interaction graph.
``scripts/9.10_auto_connections_test.py``                         ``compute_connections`` on a real model.
``scripts/9.11_collision_test.py`` / ``9.12_collision_viewer.py`` Collision detection and interactive viewer.
``scripts/16_combined_roundtrip_test.py``                         All supported geometry types in one round-trip.
``scripts/17_duplex_roundtrip_test.py``                           Duplex round-trip parametric verification.
``scripts/18_hilo_roundtrip_test.py``                             HiLo round-trip parametric verification.
``scripts/8.1_brep_generate.py`` / ``8.2_brep_test.py``           Generate the 26 STEP fixtures for the B-Rep test corpus
                                                                  and round-trip them through ``IfcAdvancedBrep``.
================================================================ ==================================================================

The reproducible evaluation suite for chapter 4 of the thesis is in
``thesis/appendix/A/`` and includes ``run_all.py`` which executes every
section and writes a consolidated report to
``thesis/appendix/A/outputs/A-summary.txt``.
