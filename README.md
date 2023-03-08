# COMPAS IFC

## Installation

Add the `conda-forge` package channel to the `conda` configuration file.
Note that you only have to do this once.

```bash
conda config --add channels conda-forge
```

Create an environment and install the dependencies.

```bash
conda create -n ifc python=3.9 compas compas_occ compas_cgal compas_view2 ifcopenshell --yes
```

Activate the environment.

```bash
conda activate ifc
```

Install the compas_ifc package.

```bash
pip install -e .
```
