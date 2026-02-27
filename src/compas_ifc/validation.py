"""Pydantic-based validation for IFC element properties.

This module provides a concise, Pythonic alternative to IDS (Information
Delivery Specification) for defining and checking BIM information requirements.

Standard IFC property set schemas are defined as Pydantic ``BaseModel``
subclasses. A ``Specification`` groups applicability criteria (which IFC
types) with required property-set schemas, mirroring the IDS structure
but in far fewer lines of code.

Example
-------
>>> from compas_ifc.validation import Specification, Pset_WallCommon, validate_model
>>> spec = Specification(
...     name="Wall common properties",
...     ifc_types=["IfcWall", "IfcWallStandardCase"],
...     required_psets={"Pset_WallCommon": Pset_WallCommon},
... )
>>> results = validate_model(model, [spec])

"""

from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError

# ==========================================================================
# Standard IFC property set schemas
# ==========================================================================


class Pset_WallCommon(BaseModel):
    """IFC standard property set for walls (Pset_WallCommon).

    See IFC4 documentation for the full property list. Fields listed here
    reflect the most commonly populated properties in real-world IFC files.
    """

    Reference: str = ""
    IsExternal: bool
    LoadBearing: bool = False
    ExtendToStructure: Optional[bool] = None
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0)
    FireRating: Optional[str] = None
    AcousticRating: Optional[str] = None


class Pset_SlabCommon(BaseModel):
    """IFC standard property set for slabs (Pset_SlabCommon)."""

    Reference: str = ""
    IsExternal: bool
    LoadBearing: bool = False
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0)
    FireRating: Optional[str] = None
    AcousticRating: Optional[str] = None
    PitchAngle: Optional[float] = None


class Pset_DoorCommon(BaseModel):
    """IFC standard property set for doors (Pset_DoorCommon)."""

    Reference: str = ""
    IsExternal: bool
    FireRating: Optional[str] = None
    AcousticRating: Optional[str] = None
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0)
    HandicapAccessible: Optional[bool] = None
    FireExit: Optional[bool] = None
    SelfClosing: Optional[bool] = None
    SmokeStop: Optional[bool] = None


class Pset_WindowCommon(BaseModel):
    """IFC standard property set for windows (Pset_WindowCommon)."""

    Reference: str = ""
    IsExternal: bool
    FireRating: Optional[str] = None
    AcousticRating: Optional[str] = None
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0)
    GlazingAreaFraction: Optional[float] = Field(default=None, ge=0, le=1)
    SmokeStop: Optional[bool] = None


class Pset_BeamCommon(BaseModel):
    """IFC standard property set for beams (Pset_BeamCommon)."""

    Reference: str = ""
    IsExternal: bool
    LoadBearing: bool = True
    Span: Optional[float] = Field(default=None, ge=0)
    Slope: Optional[float] = None
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0)
    FireRating: Optional[str] = None


class Pset_ColumnCommon(BaseModel):
    """IFC standard property set for columns (Pset_ColumnCommon)."""

    Reference: str = ""
    IsExternal: bool
    LoadBearing: bool = True
    Slope: Optional[float] = None
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0)
    FireRating: Optional[str] = None


class Pset_SpaceCommon(BaseModel):
    """IFC standard property set for spaces (Pset_SpaceCommon)."""

    Reference: str = ""
    IsExternal: Optional[bool] = None
    CeilingCovering: Optional[str] = None
    WallCovering: Optional[str] = None
    FloorCovering: Optional[str] = None
    GrossPlannedArea: Optional[float] = Field(default=None, ge=0)
    NetPlannedArea: Optional[float] = Field(default=None, ge=0)
    PubliclyAccessible: Optional[bool] = None
    HandicapAccessible: Optional[bool] = None


class Pset_RoofCommon(BaseModel):
    """IFC standard property set for roofs (Pset_RoofCommon)."""

    Reference: str = ""
    IsExternal: Optional[bool] = None
    TotalArea: Optional[float] = Field(default=None, ge=0)
    ProjectedArea: Optional[float] = Field(default=None, ge=0)
    ThermalTransmittance: Optional[float] = Field(default=None, ge=0)
    FireRating: Optional[str] = None


# Registry of standard Pset schemas (for convenience)
STANDARD_PSET_SCHEMAS = {
    "Pset_WallCommon": Pset_WallCommon,
    "Pset_SlabCommon": Pset_SlabCommon,
    "Pset_DoorCommon": Pset_DoorCommon,
    "Pset_WindowCommon": Pset_WindowCommon,
    "Pset_BeamCommon": Pset_BeamCommon,
    "Pset_ColumnCommon": Pset_ColumnCommon,
    "Pset_SpaceCommon": Pset_SpaceCommon,
    "Pset_RoofCommon": Pset_RoofCommon,
}


# ==========================================================================
# Specification & result types
# ==========================================================================


@dataclass
class Specification:
    """An information requirement specification (analogous to an IDS facet).

    Combines applicability criteria (which IFC element types) with property-set
    requirements (which Psets must be present and what schema they must satisfy).

    Parameters
    ----------
    name : str
        Human-readable name for this specification.
    ifc_types : list[str]
        IFC class names this specification applies to (e.g. ``["IfcWall"]``).
    required_psets : dict[str, type[BaseModel]] or type[BaseModel]
        Either a mapping of property-set name to Pydantic schema class, or a
        single Pydantic model whose field names are pset names and field types
        are per-pset schemas::

            class MySpec(BaseModel):
                Pset_SlabCommon: SlabCommonSchema
                Pset_EnvironmentalImpactIndicators: EnvSchema


            spec = Specification(..., required_psets=MySpec)

    description : str, optional
        Longer description of the requirement.

    """

    name: str
    ifc_types: list
    required_psets: object
    description: str = ""

    def resolved_psets(self):
        """Return ``required_psets`` as a ``dict[str, type[BaseModel]]``.

        If ``required_psets`` is already a dict it is returned as-is.
        If it is a ``BaseModel`` subclass, its fields are decomposed into
        ``{field_name: field_type}`` pairs.
        """
        if isinstance(self.required_psets, dict):
            return self.required_psets
        # BaseModel subclass — decompose fields
        return {name: info.annotation for name, info in self.required_psets.model_fields.items()}


@dataclass
class ValidationResult:
    """Validation outcome for a single element against a single specification.

    Parameters
    ----------
    element_name : str
        Name of the validated element.
    element_type : str
        IFC class of the element.
    specification : str
        Name of the specification that was checked.
    status : str
        ``"pass"`` or ``"fail"``.
    missing_psets : list[str]
        Property sets required by the spec but absent from the element.
    property_errors : list[dict]
        Pydantic validation errors per property (pset, property, error).

    """

    element_name: str
    element_type: str
    specification: str
    status: str
    missing_psets: list = field(default_factory=list)
    property_errors: list = field(default_factory=list)


# ==========================================================================
# Validation engine
# ==========================================================================


def validate_element(element, specifications):
    """Validate a single element against a list of specifications.

    Parameters
    ----------
    element : :class:`~compas_ifc.element.GenericElement`
        The element to validate.
    specifications : list[:class:`Specification`]
        Specifications to check.

    Returns
    -------
    list[:class:`ValidationResult`]
        One result per applicable specification (specs that don't match
        the element's IFC type are skipped).

    """
    results = []
    for spec in specifications:
        if element.ifc_type not in spec.ifc_types:
            continue

        props = element.properties
        missing = []
        errors = []

        for pset_name, schema_cls in spec.resolved_psets().items():
            pset_data = props.get(pset_name)
            if pset_data is None or not isinstance(pset_data, dict):
                missing.append(pset_name)
                continue

            try:
                schema_cls.model_validate(pset_data)
            except ValidationError as exc:
                for err in exc.errors():
                    errors.append(
                        {
                            "pset": pset_name,
                            "property": ".".join(str(loc) for loc in err["loc"]),
                            "error": err["msg"],
                            "type": err["type"],
                        }
                    )

        status = "fail" if missing or errors else "pass"
        results.append(
            ValidationResult(
                element_name=element.name or "",
                element_type=element.ifc_type,
                specification=spec.name,
                status=status,
                missing_psets=missing,
                property_errors=errors,
            )
        )

    return results


def validate_model(model, specifications):
    """Validate all elements in a model against a list of specifications.

    Parameters
    ----------
    model : :class:`~compas_ifc.bim.BuildingInformationModel`
        The model to validate.
    specifications : list[:class:`Specification`]
        Specifications to check.

    Returns
    -------
    list[:class:`ValidationResult`]
        One result per (element, applicable specification) pair.

    """
    results = []
    for element in model.elements():
        results.extend(validate_element(element, specifications))
    return results
