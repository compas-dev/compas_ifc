********************************************************************************
Installation
********************************************************************************

Install with conda (recommended)
================================

Create an environment named ``research`` and install COMPAS from the package channel ``conda-forge``.

.. code-block:: bash

    conda create -n ifc -c conda-forge compas compas_occ compas_view2

Activate the environment. 

.. code-block:: bash

    conda activate ifc

Verify that the installation was successful.

.. code-block:: bash

    pip install -e .

