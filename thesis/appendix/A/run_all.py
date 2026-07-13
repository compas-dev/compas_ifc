"""Run every Appendix A evaluation script and consolidate the output.

Executes the eight evaluation scripts (excluding ``api_surface_evaluation``
which only produces a measurement) and writes a combined report to
``thesis/appendix/A/outputs/A-summary.txt``.

Run from the repository root with::

    conda run -n compas-ifc python thesis/appendix/A/run_all.py

The exit code is non-zero if any script fails.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
OUTPUT_DIR = HERE / "outputs"
SUMMARY_PATH = OUTPUT_DIR / "A-summary.txt"


# Order matches the appendix sections.
SECTIONS = [
    ("A.1  API Surface Measurement", "api_surface_evaluation.py", None),
    ("A.2.1 Stage 1: Synthetic Model", "roundtrip_generated.py", "PASS"),
    ("A.2.2 Stage 2: BRep from STEP", "roundtrip_brep.py", "PASS"),
    ("A.2.3 Stage 3a: Duplex A", "roundtrip_duplex.py", "PASS"),
    ("A.2.4 Stage 3b: HiLo", "roundtrip_hilo.py", "PASS"),
    ("A.3.1.1 Hierarchy: Duplex A", "hierarchy_duplex.py", "PASS"),
    ("A.3.1.2 Hierarchy: HiLo", "hierarchy_hilo.py", "PASS"),
    ("A.3.2  Granular Export", "granular_export.py", "PASS"),
    ("A.4   Custom Validation", "validation_evaluation.py", "PASS"),
    ("A.5   Integrated Workflow", "integrated_workflow_test.py", "PASS"),
]


PASS_PATTERN = re.compile(r"(\d+)\s+PASS\s*/\s*(\d+)\s+FAIL")


def _extract_counts(output: str) -> tuple[int, int]:
    """Pull the last ``N PASS / M FAIL`` line out of stdout."""
    matches = PASS_PATTERN.findall(output)
    if not matches:
        return 0, 0
    last = matches[-1]
    return int(last[0]), int(last[1])


def _run_script(name: str) -> subprocess.CompletedProcess:
    # Pin single-worker geometry evaluation so the suite is deterministic and
    # reproduces identical check counts run-to-run (parallel geometry workers
    # otherwise cause small variation in tessellated volume/area counts).
    env = {**os.environ, "COMPAS_IFC_GEOM_WORKERS": "1", "PYTHONHASHSEED": "0"}
    return subprocess.run(
        [sys.executable, str(HERE / name)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )


def _banner(title: str, width: int = 64) -> str:
    return "-" * width + "\n" + title + "\n" + "-" * width


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    section_outputs: list[str] = []
    section_results: list[tuple[str, Optional[int], Optional[int], int]] = []
    overall_pass = 0
    overall_fail = 0
    any_error = False

    for label, script, kind in SECTIONS:
        print(f"==> {label}")
        result = _run_script(script)

        section_outputs.append(_banner(label))
        section_outputs.append(result.stdout.strip())
        if result.stderr.strip():
            section_outputs.append("[stderr]")
            section_outputs.append(result.stderr.strip())
        section_outputs.append("")

        if result.returncode != 0:
            any_error = True

        if kind == "PASS":
            matched = PASS_PATTERN.findall(result.stdout)
            if result.returncode != 0 or not matched:
                # Stage crashed or produced no pass/fail line: surface it as an
                # error rather than silently recording "0 PASS / 0 FAIL".
                any_error = True
                section_results.append((label, "ERROR", None, result.returncode))
            else:
                p, f = _extract_counts(result.stdout)
                section_results.append((label, p, f, result.returncode))
                overall_pass += p
                overall_fail += f
        else:
            section_results.append((label, None, None, result.returncode))

    # Compose summary
    width = 64
    header = "=" * width + "\n"
    header += "APPENDIX A — COMPAS IFC: EVALUATION RESULTS\n"
    header += "=" * width + "\n\n"
    header += "Run from: %s\n" % REPO_ROOT
    header += "Python:   %s\n\n" % sys.version.split()[0]

    body = "\n".join(section_outputs)

    summary_lines = ["", "=" * width, "TOTAL", "=" * width, ""]
    for label, p, f, rc in section_results:
        if p == "ERROR":
            summary_lines.append(f"  {label:40s}   *** ERROR / CRASHED  rc={rc} ***")
        elif p is None:
            summary_lines.append(f"  {label:40s}   (no pass/fail)  rc={rc}")
        else:
            summary_lines.append(f"  {label:40s}   {p:4d} PASS / {f} FAIL")
    summary_lines.append("-" * width)
    status = "  (SOME STAGES ERRORED)" if any_error else ""
    summary_lines.append(f"  {'Overall':40s}   {overall_pass:4d} PASS / {overall_fail} FAIL{status}")
    summary = "\n".join(summary_lines) + "\n"

    SUMMARY_PATH.write_text(header + body + summary, encoding="utf-8")

    print()
    print(summary)
    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)}")

    if any_error or overall_fail:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
