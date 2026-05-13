"""Command-line interface for compas_ifc.

Exposes a :data:`typer.Typer` app at :data:`app`, invoked via
``python -m compas_ifc <command>``.
"""

from compas_ifc.cli.main import app


__all__ = ["app"]
