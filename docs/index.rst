********************************************************************************
COMPAS IFC
********************************************************************************

.. note::
   COMPAS IFC is currently being upgraded to support COMPAS 2.0. This upgrade is scheduled to be completed by the end of January 2024.
   If you intend to use COMPAS IFC at its current state, please make sure to use it with COMPAS 1.x.
   


Industry Foundation Classes (IFC) is a data model that describes building and construction industry data. It is a platform neutral, open file format specification that is not controlled by a single vendor or group of vendors. It is an object-based file format with a data model developed by buildingSMART (formerly the International Alliance for Interoperability, IAI) to facilitate interoperability in the architecture, engineering and construction (AEC) industry, and is a commonly used collaboration format in Building information modeling (BIM) based projects. The latest IFC documentation and specification can be found at https://ifc43-docs.standards.buildingsmart.org/.

IFC is now widely adopted by industry and often the required format for BIM data exchange and project delivery. However Working direcly with IFC content is a highly complicated task, due to its multi-layered class inheritances and complex spatial heirarchies.

COMPAS IFC is a COMPAS extension developed to make our lives easier. It allows us to work with IFC files in an accessible, developer-friendly and pythonic way. By creating a two-way bridge between IFC files and COMPAS data structures, we can immediately benifit from wide range of tools for geometric processing and analysing from COMPAS ecosystem. COMPAS IFC also allows us to export processed data back to valid IFC files.

COMPAS IFC relies on IfcOpenShell(https://ifcopenshell.org/) for lower-level entity parsing, schema retriving and file manipulations. On top of that we additionally simplify the workflow to interact with IFC contents. 

Some of the core features of COMPAS IFC are:

- Prase IFC files and inspect its entities
- Traverse IFC spatial heirarchies in a user-friendly way
- View and edit IFC entity attributes and properties
- Extract geometric representations from IFC entities as COMPAS geometry and data structures
- Export selected IFC entities while maintaining minimal valid spatial structure
- Insert new IFC entities into existing IFC files.
- Create entirely new IFC files from scratch with valid spatial structure (in progress)


This package is still early stage of development. The repo structure is subject to change. If you have questions please do not hesitate create a new issue on github repo or contanct me directly at li.chen@arch.ethz.ch .


Table of Contents
=================

.. toctree::
   :maxdepth: 2
   :titlesonly:

   Introduction <self>
   installation
   tutorial
   examples
   api
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
