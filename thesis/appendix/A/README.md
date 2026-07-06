# Appendix A — COMPAS IFC evaluation suite

Reproducible evaluation scripts for chapter 4 of the PhD thesis *Future Data
Models for AEC: From Simplicity for Humans to Interoperability by AI*.

## Running

From the repository root, with the `compas-ifc` environment active:

```bash
python thesis/appendix/A/run_all.py
```

This runs every stage and writes a consolidated report to
`thesis/appendix/A/outputs/A-summary.txt`. The exit code is non-zero if any
stage fails or crashes.

## Determinism

The geometry iterator (`IFCFile.load_geometries`) evaluates shapes in
parallel by default, which can cause run-to-run variation in the tessellated
volume/area check counts. For reproducibility the runner pins single-worker
evaluation (`COMPAS_IFC_GEOM_WORKERS=1`) and a fixed hash seed
(`PYTHONHASHSEED=0`). Set the same variables when running a stage directly:

```bash
COMPAS_IFC_GEOM_WORKERS=1 PYTHONHASHSEED=0 python thesis/appendix/A/roundtrip_hilo.py
```

Note: the large real-world HiLo stage (`roundtrip_hilo.py`, ~1,400 elements)
may still show minor variation (order of ±1%) in its geometric check count.
Several checks are emitted conditionally (e.g. a volume comparison is only
made when the computed volume is positive), so borderline shapes near the
floating-point tessellation threshold can flip a handful of checks between
runs. Cite the HiLo geometric count as approximate, or fix a reference run.

## Input data

| Stage | Script | Input | Availability |
|-------|--------|-------|--------------|
| A.2.1 Synthetic | `roundtrip_generated.py` | generated in-memory | self-contained |
| A.2.2 BRep from STEP | `roundtrip_brep.py` | 26 STEP files in `temp/brep_conversion_tests/` | run `scripts/dev_tests/8.1_brep_generate.py` first to generate them |
| A.2.3 Duplex | `roundtrip_duplex.py` | `data/Duplex_A_20110907.ifc` | shipped in the repo |
| A.2.4 HiLo | `roundtrip_hilo.py` | `temp/HiLo_Model-Architecture.ifc` | **external model, not shipped** — place it in `temp/` |
| A.3.1 Hierarchy | `hierarchy_duplex.py`, `hierarchy_hilo.py` | Duplex / HiLo (as above) | see above |
| A.3.2 Granular export | `granular_export.py` | `data/Duplex_A_20110907.ifc` | shipped |
| A.4 Validation | `validation_evaluation.py` | `data/Duplex_A_20110907.ifc` | shipped |
| A.5 Integrated workflow | `integrated_workflow_test.py` | `thesis/data/slab.stp` | STEP input, not tracked by default |

Stages that depend on the external HiLo model or the STEP inputs are skipped
or error if the data is absent; the Duplex- and generator-based stages run
from a clean checkout.
