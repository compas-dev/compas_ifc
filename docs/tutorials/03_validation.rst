********************************************************************************
Validate custom properties
********************************************************************************

The :mod:`compas_ifc.validation` module ties IFC types to
`Pydantic <https://docs.pydantic.dev/>`_ schemas, so project-specific
property requirements can be checked automatically.

Defining a specification
========================

.. code-block:: python

    from pydantic import BaseModel, Field
    from compas_ifc.validation import Specification

    class ConcreteRecipe(BaseModel):
        strength_class: str = Field(pattern=r"^C\d{2}/\d{2}$")
        cement_type: str
        cover_mm: float = Field(gt=0)

    spec = Specification(
        name="Concrete recipe",
        ifc_types=["IfcSlab"],
        required_psets={"ConcreteRecipe": ConcreteRecipe},
    )

The schema can use any Pydantic feature: nested models, regex
constraints, enums, defaults, etc. It exports to JSON Schema for
downstream tooling.

Advisory mode (``model.validate``)
==================================

.. code-block:: python

    from compas_ifc.bim import BuildingInformationModel

    model = BuildingInformationModel("project.ifc")
    results = model.validate([spec])

    for r in results:
        if r.status == "fail":
            print(r.element.name, "failed:", r.property_errors)

``model.validate`` reports issues without modifying the model.

Enforcement mode (``model.specifications``)
===========================================

When specifications are attached to ``model.specifications``, validation
runs inside ``add_element`` and ``create_element`` and rejects
non-conforming insertions immediately:

.. code-block:: python

    model = BuildingInformationModel.template(unit="m")
    model.specifications = [spec]
    storey = model.storeys[0]

    # raises ValueError because no ConcreteRecipe pset is attached
    try:
        model.create_slab(name="Slab1", parent=storey)
    except ValueError as e:
        print(e)

    # passes, because the required pset is provided
    model.create_slab(
        name="Slab2",
        parent=storey,
        properties={"ConcreteRecipe": {
            "strength_class": "C30/37",
            "cement_type": "CEM I",
            "cover_mm": 25.0,
        }},
    )

Shared schemas
==============

Specifications are plain Python objects; they can be version-controlled,
imported, and shared across projects. A specification can apply to
multiple IFC types and reuse Pydantic schemas across other tooling.
