from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Literal
from typing import Optional
from typing import overload

from compas_model.models import Model

from compas_ifc.element import GenericElement
from compas_ifc.factory import ElementFactoryMixin
from compas_ifc.file import IFCFile
from compas_ifc.interactions import InteractionMixin
from compas_ifc.tree import TreeMixin

if TYPE_CHECKING:
    # Wildcard import is intentional: the @overload chains below reference
    # every IFC product subclass by name, and listing each separately would
    # bloat the file without giving anything the wildcard doesn't.
    from compas_ifc.entities.generated.IFC4 import *  # noqa: F401, F403


class BuildingInformationModel(ElementFactoryMixin, InteractionMixin, TreeMixin, Model):
    """A building information model backed by an IFC file.

    Extends ``compas_model.Model`` to provide IFC-specific functionality
    including reading/writing IFC files, spatial hierarchy management,
    and IFC entity creation. The model's ``tree`` holds the spatial hierarchy
    and the ``graph`` holds non-hierarchical relationships (interactions).

    This class acts as a **bi-directional front-end**: every mutation
    (adding elements, changing geometry/properties/transforms) immediately
    updates the underlying IFC file. Calling ``save()`` writes the file.

    IfcProject-level information (units, schema, metadata) is managed
    directly by this class rather than as a separate element.

    Parameters
    ----------
    filepath : str, optional
        Path to an IFC file to load.
    schema : str, optional
        IFC schema to use when creating a new file. Default is "IFC4".
    use_occ : bool, optional
        Whether to use OpenCascade for geometry. Default is False.
    load_geometries : bool, optional
        Whether to pre-load geometries during import. Default is True.
    rectify_placements : bool, optional
        Whether to rewrite IFC placements during import so that each
        element's ``IfcLocalPlacement.PlacementRelTo`` points to its
        spatial parent's placement and ``RelativePlacement`` holds the
        local transform. Default is True.
    rectify_verbose : bool, optional
        If True and ``rectify_placements`` is True, print a line for each
        rectified placement showing what ``PlacementRelTo`` changed from
        and to (e.g. "IfcWall 'Wall A': PlacementRelTo IfcBuilding 'B1'
        -> IfcBuildingStorey 'S1'"). Default is False.
    name : str, optional
        Name of the model.

    """

    def __init__(
        self,
        filepath: str = None,
        schema: str = "IFC4",
        use_occ: bool = False,
        load_geometries: bool = True,
        rectify_placements: bool = True,
        rectify_verbose: bool = False,
        name: str = None,
        **kwargs,
    ) -> None:
        super().__init__(name=name, **kwargs)

        # IFC file wrapper — pass self so Base.model resolves to this instance
        self._file = IFCFile(
            self,
            filepath=filepath,
            schema=schema,
            use_occ=use_occ,
            load_geometries=load_geometries,
            verbose=False,
        )

        # Element lookup by IFC GlobalId
        self._elements_by_global_id: dict[str, GenericElement] = {}

        # Validation specifications (opt-in enforcement)
        self.specifications = []

        # Load spatial hierarchy if opening an existing file
        if filepath:
            self._load_from_ifc(rectify_placements=rectify_placements, rectify_verbose=rectify_verbose)

    # ==========================================================================
    # IFC entity creation — conversion functions call model._create()
    # ==========================================================================

    def _create(self, cls=None, parent=None, geometry=None, frame=None, properties=None, **kwargs):
        """Create an IFC entity. Delegates to IFCFile.create().

        This method satisfies the protocol expected by all conversion functions
        (representation.py, frame.py, pset.py, mesh.py, shapes.py, brep.py).
        """
        return self._file._create(cls=cls, parent=parent, geometry=geometry, frame=frame, properties=properties, **kwargs)

    def _create_value(self, value):
        """Create an IfcValue from a Python scalar. Delegates to IFCFile."""
        return self._file._create_value(value)

    # ==========================================================================
    # User-facing properties
    # ==========================================================================

    @property
    def project(self):
        """The underlying IfcProject entity (read-only escape hatch).

        Returns the Base-wrapped ``IfcProject`` entity, providing access to
        project-level attributes (``Name``, ``Description``, ``sites``,
        ``buildings``, ``contexts``, ``units``, ``north``, ``frame``, etc.).

        Returns ``None`` if no IfcProject exists in the file.
        """
        projects = self._file.get_entities_by_type("IfcProject")
        return projects[0] if projects else None

    @property
    def schema_name(self) -> str:
        return self._file.schema_name

    @property
    def unit(self) -> Optional[str]:
        projects = self._file.get_entities_by_type("IfcProject")
        if not projects:
            return None
        project = projects[0]
        length_unit = project.length_unit
        if length_unit.Name == "METRE" and length_unit.Prefix == "MILLI":
            return "mm"
        elif length_unit.Name == "METRE" and length_unit.Prefix == "CENTI":
            return "cm"
        elif length_unit.Name == "METRE" and not length_unit.Prefix:
            return "m"
        return None

    @unit.setter
    def unit(self, value: str):
        projects = self._file.get_entities_by_type("IfcProject")
        if not projects:
            return
        project = projects[0]
        if value == "mm":
            project.length_unit.Prefix = "MILLI"
        elif value == "cm":
            project.length_unit.Prefix = "CENTI"
        elif value == "m":
            project.length_unit.Prefix = None
        else:
            raise ValueError("Invalid unit. Use 'mm', 'cm', or 'm'.")

    # ==========================================================================
    # Element queries
    # ==========================================================================

    def get_element_by_global_id(self, global_id: str) -> Optional[GenericElement]:
        """Find an element by its IFC GlobalId."""
        return self._elements_by_global_id.get(global_id)

    # region overloads:get_elements_by_type
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcActuator"]) -> list[GenericElement[IfcActuator]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcAirTerminal"]) -> list[GenericElement[IfcAirTerminal]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcAirTerminalBox"]) -> list[GenericElement[IfcAirTerminalBox]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcAirToAirHeatRecovery"]) -> list[GenericElement[IfcAirToAirHeatRecovery]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcAlarm"]) -> list[GenericElement[IfcAlarm]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcAnnotation"]) -> list[GenericElement[IfcAnnotation]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcAudioVisualAppliance"]) -> list[GenericElement[IfcAudioVisualAppliance]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBeam"]) -> list[GenericElement[IfcBeam]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBeamStandardCase"]) -> list[GenericElement[IfcBeamStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBoiler"]) -> list[GenericElement[IfcBoiler]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBuilding"]) -> list[GenericElement[IfcBuilding]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBuildingElement"]) -> list[GenericElement[IfcBuildingElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBuildingElementPart"]) -> list[GenericElement[IfcBuildingElementPart]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBuildingElementProxy"]) -> list[GenericElement[IfcBuildingElementProxy]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBuildingStorey"]) -> list[GenericElement[IfcBuildingStorey]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcBurner"]) -> list[GenericElement[IfcBurner]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCableCarrierFitting"]) -> list[GenericElement[IfcCableCarrierFitting]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCableCarrierSegment"]) -> list[GenericElement[IfcCableCarrierSegment]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCableFitting"]) -> list[GenericElement[IfcCableFitting]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCableSegment"]) -> list[GenericElement[IfcCableSegment]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcChiller"]) -> list[GenericElement[IfcChiller]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcChimney"]) -> list[GenericElement[IfcChimney]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCivilElement"]) -> list[GenericElement[IfcCivilElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCoil"]) -> list[GenericElement[IfcCoil]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcColumn"]) -> list[GenericElement[IfcColumn]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcColumnStandardCase"]) -> list[GenericElement[IfcColumnStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCommunicationsAppliance"]) -> list[GenericElement[IfcCommunicationsAppliance]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCompressor"]) -> list[GenericElement[IfcCompressor]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCondenser"]) -> list[GenericElement[IfcCondenser]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcController"]) -> list[GenericElement[IfcController]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCooledBeam"]) -> list[GenericElement[IfcCooledBeam]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCoolingTower"]) -> list[GenericElement[IfcCoolingTower]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCovering"]) -> list[GenericElement[IfcCovering]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcCurtainWall"]) -> list[GenericElement[IfcCurtainWall]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDamper"]) -> list[GenericElement[IfcDamper]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDiscreteAccessory"]) -> list[GenericElement[IfcDiscreteAccessory]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDistributionChamberElement"]) -> list[GenericElement[IfcDistributionChamberElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDistributionControlElement"]) -> list[GenericElement[IfcDistributionControlElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDistributionElement"]) -> list[GenericElement[IfcDistributionElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDistributionFlowElement"]) -> list[GenericElement[IfcDistributionFlowElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDistributionPort"]) -> list[GenericElement[IfcDistributionPort]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDoor"]) -> list[GenericElement[IfcDoor]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDoorStandardCase"]) -> list[GenericElement[IfcDoorStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDuctFitting"]) -> list[GenericElement[IfcDuctFitting]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDuctSegment"]) -> list[GenericElement[IfcDuctSegment]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcDuctSilencer"]) -> list[GenericElement[IfcDuctSilencer]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElectricAppliance"]) -> list[GenericElement[IfcElectricAppliance]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElectricDistributionBoard"]) -> list[GenericElement[IfcElectricDistributionBoard]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElectricFlowStorageDevice"]) -> list[GenericElement[IfcElectricFlowStorageDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElectricGenerator"]) -> list[GenericElement[IfcElectricGenerator]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElectricMotor"]) -> list[GenericElement[IfcElectricMotor]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElectricTimeControl"]) -> list[GenericElement[IfcElectricTimeControl]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElement"]) -> list[GenericElement[IfcElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElementAssembly"]) -> list[GenericElement[IfcElementAssembly]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcElementComponent"]) -> list[GenericElement[IfcElementComponent]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcEnergyConversionDevice"]) -> list[GenericElement[IfcEnergyConversionDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcEngine"]) -> list[GenericElement[IfcEngine]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcEvaporativeCooler"]) -> list[GenericElement[IfcEvaporativeCooler]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcEvaporator"]) -> list[GenericElement[IfcEvaporator]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcExternalSpatialElement"]) -> list[GenericElement[IfcExternalSpatialElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcExternalSpatialStructureElement"]) -> list[GenericElement[IfcExternalSpatialStructureElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFan"]) -> list[GenericElement[IfcFan]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFastener"]) -> list[GenericElement[IfcFastener]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFeatureElement"]) -> list[GenericElement[IfcFeatureElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFeatureElementAddition"]) -> list[GenericElement[IfcFeatureElementAddition]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFeatureElementSubtraction"]) -> list[GenericElement[IfcFeatureElementSubtraction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFilter"]) -> list[GenericElement[IfcFilter]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFireSuppressionTerminal"]) -> list[GenericElement[IfcFireSuppressionTerminal]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowController"]) -> list[GenericElement[IfcFlowController]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowFitting"]) -> list[GenericElement[IfcFlowFitting]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowInstrument"]) -> list[GenericElement[IfcFlowInstrument]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowMeter"]) -> list[GenericElement[IfcFlowMeter]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowMovingDevice"]) -> list[GenericElement[IfcFlowMovingDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowSegment"]) -> list[GenericElement[IfcFlowSegment]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowStorageDevice"]) -> list[GenericElement[IfcFlowStorageDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowTerminal"]) -> list[GenericElement[IfcFlowTerminal]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFlowTreatmentDevice"]) -> list[GenericElement[IfcFlowTreatmentDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFooting"]) -> list[GenericElement[IfcFooting]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFurnishingElement"]) -> list[GenericElement[IfcFurnishingElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcFurniture"]) -> list[GenericElement[IfcFurniture]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcGeographicElement"]) -> list[GenericElement[IfcGeographicElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcGrid"]) -> list[GenericElement[IfcGrid]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcHeatExchanger"]) -> list[GenericElement[IfcHeatExchanger]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcHumidifier"]) -> list[GenericElement[IfcHumidifier]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcInterceptor"]) -> list[GenericElement[IfcInterceptor]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcJunctionBox"]) -> list[GenericElement[IfcJunctionBox]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcLamp"]) -> list[GenericElement[IfcLamp]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcLightFixture"]) -> list[GenericElement[IfcLightFixture]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcMechanicalFastener"]) -> list[GenericElement[IfcMechanicalFastener]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcMedicalDevice"]) -> list[GenericElement[IfcMedicalDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcMember"]) -> list[GenericElement[IfcMember]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcMemberStandardCase"]) -> list[GenericElement[IfcMemberStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcMotorConnection"]) -> list[GenericElement[IfcMotorConnection]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcOpeningElement"]) -> list[GenericElement[IfcOpeningElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcOpeningStandardCase"]) -> list[GenericElement[IfcOpeningStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcOutlet"]) -> list[GenericElement[IfcOutlet]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcPile"]) -> list[GenericElement[IfcPile]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcPipeFitting"]) -> list[GenericElement[IfcPipeFitting]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcPipeSegment"]) -> list[GenericElement[IfcPipeSegment]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcPlate"]) -> list[GenericElement[IfcPlate]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcPlateStandardCase"]) -> list[GenericElement[IfcPlateStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcPort"]) -> list[GenericElement[IfcPort]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcProduct"]) -> list[GenericElement[IfcProduct]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcProjectionElement"]) -> list[GenericElement[IfcProjectionElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcProtectiveDevice"]) -> list[GenericElement[IfcProtectiveDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcProtectiveDeviceTrippingUnit"]) -> list[GenericElement[IfcProtectiveDeviceTrippingUnit]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcProxy"]) -> list[GenericElement[IfcProxy]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcPump"]) -> list[GenericElement[IfcPump]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcRailing"]) -> list[GenericElement[IfcRailing]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcRamp"]) -> list[GenericElement[IfcRamp]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcRampFlight"]) -> list[GenericElement[IfcRampFlight]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcReinforcingBar"]) -> list[GenericElement[IfcReinforcingBar]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcReinforcingElement"]) -> list[GenericElement[IfcReinforcingElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcReinforcingMesh"]) -> list[GenericElement[IfcReinforcingMesh]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcRoof"]) -> list[GenericElement[IfcRoof]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSanitaryTerminal"]) -> list[GenericElement[IfcSanitaryTerminal]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSensor"]) -> list[GenericElement[IfcSensor]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcShadingDevice"]) -> list[GenericElement[IfcShadingDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSite"]) -> list[GenericElement[IfcSite]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSlab"]) -> list[GenericElement[IfcSlab]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSlabElementedCase"]) -> list[GenericElement[IfcSlabElementedCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSlabStandardCase"]) -> list[GenericElement[IfcSlabStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSolarDevice"]) -> list[GenericElement[IfcSolarDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSpace"]) -> list[GenericElement[IfcSpace]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSpaceHeater"]) -> list[GenericElement[IfcSpaceHeater]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSpatialElement"]) -> list[GenericElement[IfcSpatialElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSpatialStructureElement"]) -> list[GenericElement[IfcSpatialStructureElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSpatialZone"]) -> list[GenericElement[IfcSpatialZone]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStackTerminal"]) -> list[GenericElement[IfcStackTerminal]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStair"]) -> list[GenericElement[IfcStair]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStairFlight"]) -> list[GenericElement[IfcStairFlight]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralAction"]) -> list[GenericElement[IfcStructuralAction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralActivity"]) -> list[GenericElement[IfcStructuralActivity]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralConnection"]) -> list[GenericElement[IfcStructuralConnection]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralCurveAction"]) -> list[GenericElement[IfcStructuralCurveAction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralCurveConnection"]) -> list[GenericElement[IfcStructuralCurveConnection]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralCurveMember"]) -> list[GenericElement[IfcStructuralCurveMember]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralCurveMemberVarying"]) -> list[GenericElement[IfcStructuralCurveMemberVarying]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralCurveReaction"]) -> list[GenericElement[IfcStructuralCurveReaction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralItem"]) -> list[GenericElement[IfcStructuralItem]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralLinearAction"]) -> list[GenericElement[IfcStructuralLinearAction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralMember"]) -> list[GenericElement[IfcStructuralMember]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralPlanarAction"]) -> list[GenericElement[IfcStructuralPlanarAction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralPointAction"]) -> list[GenericElement[IfcStructuralPointAction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralPointConnection"]) -> list[GenericElement[IfcStructuralPointConnection]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralPointReaction"]) -> list[GenericElement[IfcStructuralPointReaction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralReaction"]) -> list[GenericElement[IfcStructuralReaction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralSurfaceAction"]) -> list[GenericElement[IfcStructuralSurfaceAction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralSurfaceConnection"]) -> list[GenericElement[IfcStructuralSurfaceConnection]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralSurfaceMember"]) -> list[GenericElement[IfcStructuralSurfaceMember]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralSurfaceMemberVarying"]) -> list[GenericElement[IfcStructuralSurfaceMemberVarying]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcStructuralSurfaceReaction"]) -> list[GenericElement[IfcStructuralSurfaceReaction]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSurfaceFeature"]) -> list[GenericElement[IfcSurfaceFeature]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSwitchingDevice"]) -> list[GenericElement[IfcSwitchingDevice]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcSystemFurnitureElement"]) -> list[GenericElement[IfcSystemFurnitureElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcTank"]) -> list[GenericElement[IfcTank]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcTendon"]) -> list[GenericElement[IfcTendon]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcTendonAnchor"]) -> list[GenericElement[IfcTendonAnchor]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcTransformer"]) -> list[GenericElement[IfcTransformer]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcTransportElement"]) -> list[GenericElement[IfcTransportElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcTubeBundle"]) -> list[GenericElement[IfcTubeBundle]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcUnitaryControlElement"]) -> list[GenericElement[IfcUnitaryControlElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcUnitaryEquipment"]) -> list[GenericElement[IfcUnitaryEquipment]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcValve"]) -> list[GenericElement[IfcValve]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcVibrationIsolator"]) -> list[GenericElement[IfcVibrationIsolator]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcVirtualElement"]) -> list[GenericElement[IfcVirtualElement]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcVoidingFeature"]) -> list[GenericElement[IfcVoidingFeature]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcWall"]) -> list[GenericElement[IfcWall]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcWallElementedCase"]) -> list[GenericElement[IfcWallElementedCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcWallStandardCase"]) -> list[GenericElement[IfcWallStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcWasteTerminal"]) -> list[GenericElement[IfcWasteTerminal]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcWindow"]) -> list[GenericElement[IfcWindow]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: Literal["IfcWindowStandardCase"]) -> list[GenericElement[IfcWindowStandardCase]]: ...
    @overload
    def get_elements_by_type(self, ifc_type: str) -> list[GenericElement]: ...
    # endregion overloads:get_elements_by_type
    def get_elements_by_type(self, ifc_type: str) -> list[GenericElement]:
        """Find all elements of a given IFC type (e.g. "IfcWall").

        Supports IFC class hierarchy matching: querying ``"IfcProduct"`` will
        match ``IfcWall``, ``IfcBeam``, ``IfcColumn``, etc.
        """
        results = []
        for e in self.elements():
            if e.ifc_type == ifc_type:
                results.append(e)
            elif e._ifc_entity is not None and e._ifc_entity.is_a(ifc_type):
                results.append(e)
        return results

    def get_elements_by_name(self, name: str) -> list[GenericElement]:
        """Find all elements with a given name."""
        return [e for e in self.elements() if e.name == name]

    @property
    def sites(self) -> list[GenericElement]:
        """All IfcSite elements."""
        return self.get_elements_by_type("IfcSite")

    @property
    def buildings(self) -> list[GenericElement]:
        """All IfcBuilding elements."""
        return self.get_elements_by_type("IfcBuilding")

    @property
    def storeys(self) -> list[GenericElement]:
        """All IfcBuildingStorey elements."""
        return self.get_elements_by_type("IfcBuildingStorey")

    @property
    def building_elements(self) -> list[GenericElement]:
        """All non-spatial building elements (walls, slabs, beams, etc.)."""
        return [e for e in self.elements() if not e._is_spatial]

    # ==========================================================================
    # Element add / remove (bi-directional sync)
    # ==========================================================================

    def add_element(self, element, parent=None, material=None):
        """Add a GenericElement to the model tree and create its IFC entity.

        For elements loaded from IFC (with an existing ``_ifc_entity``), only
        the compas_model bookkeeping is performed. For programmatically created
        elements, the IFC entity, relationship, geometry representation, and
        placement are all created in the underlying IFC file.

        Parameters
        ----------
        element : GenericElement
            The element to add.
        parent : GenericElement, optional
            Parent element in the spatial hierarchy.
        material : optional
            Material to assign (from compas_model).

        Returns
        -------
        GenericElement

        """
        # Let compas_model do tree/graph bookkeeping
        result = super().add_element(element, parent=parent, material=material)

        if element._ifc_entity is not None:
            # Import case: element already has an IFC entity, just index it
            if element.global_id:
                self._elements_by_global_id[element.global_id] = element
            return result

        # Programmatic creation: create IFC entity in the file
        ifc_parent = self._resolve_ifc_parent(parent)
        kwargs = {}
        if element.name:
            kwargs["Name"] = element.name

        ifc_entity = self._file._create(cls=element.ifc_type, parent=ifc_parent, **kwargs)
        element._ifc_entity = ifc_entity
        element._global_id = ifc_entity.GlobalId
        self._elements_by_global_id[ifc_entity.GlobalId] = element

        # Sync geometry → IFC representation
        if element._geometry is not None:
            ifc_entity.geometry = element._geometry

        # Sync transformation → IFC placement (with PlacementRelTo for hierarchy)
        if element.transformation:
            self._assign_ifc_placement(element, parent)

        # Sync properties → IFC schema attributes + property sets
        if element._properties:
            schema_attrs = {"Description", "ObjectType", "Tag", "PredefinedType"}
            psets = {k: v for k, v in element._properties.items() if k not in schema_attrs and isinstance(v, dict)}
            if psets:
                ifc_entity.property_sets = psets
            for attr in schema_attrs:
                if attr in element._properties:
                    setattr(ifc_entity, attr, element._properties[attr])

        # Enforce validation specifications if any are active
        if self.specifications:
            self._enforce_specifications(element)

        return result

    def remove_element(self, element):
        """Remove a GenericElement from the model and the IFC file.

        Parameters
        ----------
        element : GenericElement
            The element to remove.

        """
        if element._ifc_entity is not None:
            self._file.remove(element._ifc_entity)
            element._ifc_entity = None

        if element.global_id and element.global_id in self._elements_by_global_id:
            del self._elements_by_global_id[element.global_id]

        super().remove_element(element)

    # ==========================================================================
    # Validation
    # ==========================================================================

    def validate(self, specifications=None):
        """Validate all elements against information requirements.

        Parameters
        ----------
        specifications : list[:class:`~compas_ifc.validation.Specification`], optional
            Specifications to check. If ``None``, uses ``self.specifications``.

        Returns
        -------
        list[:class:`~compas_ifc.validation.ValidationResult`]
            One result per (element, applicable specification) pair.

        """
        from compas_ifc.validation import validate_model

        specs = specifications if specifications is not None else self.specifications
        return validate_model(self, specs)

    def _enforce_specifications(self, element):
        """Check an element against active specifications, raise on failure.

        Called automatically from ``add_element`` when ``self.specifications``
        is non-empty.

        Raises
        ------
        ValueError
            If the element fails any applicable specification.

        """
        from compas_ifc.validation import validate_element

        results = validate_element(element, self.specifications)
        failures = [r for r in results if r.status == "fail"]
        if failures:
            msgs = []
            for f in failures:
                parts = []
                if f.missing_psets:
                    parts.append(f"missing psets: {f.missing_psets}")
                if f.property_errors:
                    parts.append(f"property errors: {f.property_errors}")
                msgs.append(f"[{f.specification}] {'; '.join(parts)}")
            raise ValueError(f"Element '{element.name}' ({element.ifc_type}) failed validation: {' | '.join(msgs)}")

    # ==========================================================================
    # IFC Export
    # ==========================================================================

    def save(self, path: str, schema: str = None, tessellation_tolerance: float = 0.001):
        """Save the IFC file to disk, optionally converting to another schema.

        Since the model is a bi-directional front-end, the IFC file is always
        in sync with the model tree. When ``schema`` is ``None`` or matches the
        current schema, this simply writes the file.

        Cross-schema export — converting the model to a different IFC schema
        (``"IFC2X3"``, ``"IFC4"``, or ``"IFC4X3"``) on save, tessellating
        advanced B-Reps at ``tessellation_tolerance`` where the target schema
        cannot represent them — is not yet implemented.

        Parameters
        ----------
        path : str
            Output file path.
        schema : str, optional
            Target IFC schema. If ``None`` (default) or equal to the current
            schema, the model is written as-is. Any other value currently
            raises :class:`NotImplementedError`.
        tessellation_tolerance : float, optional
            Chord deviation (in metres) intended for tessellating advanced
            B-Reps during a downgrade export. Reserved for the not-yet-
            implemented cross-schema export path. Default ``0.001``.

        Raises
        ------
        NotImplementedError
            If ``schema`` names a different schema than the current one.

        """
        if schema is None or schema == self.schema_name:
            self._file.save(path)
            return
        raise NotImplementedError(
            f"Cross-schema export ({self.schema_name} -> {schema}) is not yet implemented. "
            "Save without the 'schema' argument to write the model in its current schema."
        )

    # ==========================================================================
    # Display
    # ==========================================================================

    def show(self, elements=None, keep_hierarchy=True):
        """Show the model (or specific elements and their children) in compas_viewer.

        Parameters
        ----------
        elements : :class:`GenericElement` or list[:class:`GenericElement`], optional
            One or more elements to show. Each element and its children are
            included. If ``None``, the entire model is shown.
        keep_hierarchy : bool, optional
            Only applies when ``elements`` is given. If ``True`` (default),
            each element's spatial ancestors are added to the scene as empty
            groups so that the element renders at its real world position
            and the treeform sidebar reflects the IFC spatial hierarchy.
            If ``False``, elements are attached directly to the scene root
            using only their local transformation — useful for inspecting
            components side-by-side at the origin, like a parts library.

        """
        try:
            from compas_viewer import Viewer
            from compas_viewer.components import Treeform
        except ImportError:
            raise ImportError("The show method requires compas_viewer to be installed.")

        viewer = Viewer()
        viewer.ui.sidebar.show_objectsetting = False

        if self.unit:
            viewer.unit = self.unit

        def _add_element(elem, parent=None):
            label = f"[{elem.ifc_type}] {elem.name}"
            obj = None

            visual = elem._visual_geometry
            skip_visual = elem.ifc_type in ("IfcSpace", "IfcOpeningElement")
            if visual is not None and not skip_visual:
                style_kwargs = elem._resolve_style() or {}
                obj = viewer.scene.add(
                    visual,
                    name=label,
                    parent=parent,
                    hide_coplanaredges=True,
                    **style_kwargs,
                )
            else:
                obj = viewer.scene.add_group(name=label, parent=parent)

            obj.transformation = elem.transformation
            obj.attributes["element"] = elem

            for child in elem.children:
                _add_element(child, parent=obj)

        def _add_ancestor_group(ancestor, parent_obj):
            label = f"[{ancestor.ifc_type}] {ancestor.name}"
            obj = viewer.scene.add_group(name=label, parent=parent_obj)
            obj.transformation = ancestor.transformation
            obj.attributes["element"] = ancestor
            return obj

        if elements is not None:
            if not isinstance(elements, (list, tuple)):
                elements = [elements]

            if keep_hierarchy:
                # Build per-element ancestor chains and dedupe groups across selection,
                # so e.g. all four Level-1 windows share one Site/Building/Storey/Wall.
                ancestor_objs: dict = {}
                for elem in elements:
                    chain = []
                    cur = elem.parent
                    while cur is not None:
                        chain.append(cur)
                        cur = cur.parent
                    chain.reverse()

                    parent_obj = None
                    for anc in chain:
                        key = id(anc)
                        if key in ancestor_objs:
                            parent_obj = ancestor_objs[key]
                        else:
                            parent_obj = _add_ancestor_group(anc, parent_obj)
                            ancestor_objs[key] = parent_obj

                    _add_element(elem, parent=parent_obj)
            else:
                for elem in elements:
                    _add_element(elem)
        else:
            for node in self.tree.root.children:
                _add_element(node.element)

        treeform = Treeform()
        viewer.ui.sidebar.add(treeform)

        def update_treeform(form, node):
            elem = node.attributes.get("element")
            if elem:
                info = {
                    "Type": elem.ifc_type,
                    "Name": elem.name,
                    "GlobalId": elem.global_id or "",
                }
                info.update(elem.properties)
                treeform.update_from_dict(info)

        viewer.ui.sidebar.sceneform.action = update_treeform
        viewer.show()
