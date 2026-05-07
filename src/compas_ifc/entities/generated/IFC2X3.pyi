"""Type stubs for IFC2X3 entities (auto-generated).

Do not edit by hand. Regenerate with:
    python -m compas_ifc.entities.generator
"""

from typing import Optional
from typing import Union

class IfcActionSourceTypeEnum(str):
    items: tuple = ('DEAD_LOAD_G', 'COMPLETION_G1', 'LIVE_LOAD_Q', 'SNOW_S', 'WIND_W', 'PRESTRESSING_P', 'SETTLEMENT_U', 'TEMPERATURE_T', 'EARTHQUAKE_E', 'FIRE', 'IMPULSE', 'IMPACT', 'TRANSPORT', 'ERECTION', 'PROPPING', 'SYSTEM_IMPERFECTION', 'SHRINKAGE', 'CREEP', 'LACK_OF_FIT', 'BUOYANCY', 'ICE', 'CURRENT', 'WAVE', 'RAIN', 'BRAKES', 'USERDEFINED', 'NOTDEFINED')


class IfcActionTypeEnum(str):
    items: tuple = ('PERMANENT_G', 'VARIABLE_Q', 'EXTRAORDINARY_A', 'USERDEFINED', 'NOTDEFINED')


class IfcActuatorTypeEnum(str):
    items: tuple = ('ELECTRICACTUATOR', 'HANDOPERATEDACTUATOR', 'HYDRAULICACTUATOR', 'PNEUMATICACTUATOR', 'THERMOSTATICACTUATOR', 'USERDEFINED', 'NOTDEFINED')


class IfcAddressTypeEnum(str):
    items: tuple = ('OFFICE', 'SITE', 'HOME', 'DISTRIBUTIONPOINT', 'USERDEFINED')


class IfcAheadOrBehind(str):
    items: tuple = ('AHEAD', 'BEHIND')


class IfcAirTerminalBoxTypeEnum(str):
    items: tuple = ('CONSTANTFLOW', 'VARIABLEFLOWPRESSUREDEPENDANT', 'VARIABLEFLOWPRESSUREINDEPENDANT', 'USERDEFINED', 'NOTDEFINED')


class IfcAirTerminalTypeEnum(str):
    items: tuple = ('GRILLE', 'REGISTER', 'DIFFUSER', 'EYEBALL', 'IRIS', 'LINEARGRILLE', 'LINEARDIFFUSER', 'USERDEFINED', 'NOTDEFINED')


class IfcAirToAirHeatRecoveryTypeEnum(str):
    items: tuple = ('FIXEDPLATECOUNTERFLOWEXCHANGER', 'FIXEDPLATECROSSFLOWEXCHANGER', 'FIXEDPLATEPARALLELFLOWEXCHANGER', 'ROTARYWHEEL', 'RUNAROUNDCOILLOOP', 'HEATPIPE', 'TWINTOWERENTHALPYRECOVERYLOOPS', 'THERMOSIPHONSEALEDTUBEHEATEXCHANGERS', 'THERMOSIPHONCOILTYPEHEATEXCHANGERS', 'USERDEFINED', 'NOTDEFINED')


class IfcAlarmTypeEnum(str):
    items: tuple = ('BELL', 'BREAKGLASSBUTTON', 'LIGHT', 'MANUALPULLBOX', 'SIREN', 'WHISTLE', 'USERDEFINED', 'NOTDEFINED')


class IfcAnalysisModelTypeEnum(str):
    items: tuple = ('IN_PLANE_LOADING_2D', 'OUT_PLANE_LOADING_2D', 'LOADING_3D', 'USERDEFINED', 'NOTDEFINED')


class IfcAnalysisTheoryTypeEnum(str):
    items: tuple = ('FIRST_ORDER_THEORY', 'SECOND_ORDER_THEORY', 'THIRD_ORDER_THEORY', 'FULL_NONLINEAR_THEORY', 'USERDEFINED', 'NOTDEFINED')


class IfcArithmeticOperatorEnum(str):
    items: tuple = ('ADD', 'DIVIDE', 'MULTIPLY', 'SUBTRACT')


class IfcAssemblyPlaceEnum(str):
    items: tuple = ('SITE', 'FACTORY', 'NOTDEFINED')


class IfcBSplineCurveForm(str):
    items: tuple = ('POLYLINE_FORM', 'CIRCULAR_ARC', 'ELLIPTIC_ARC', 'PARABOLIC_ARC', 'HYPERBOLIC_ARC', 'UNSPECIFIED')


class IfcBeamTypeEnum(str):
    items: tuple = ('BEAM', 'JOIST', 'LINTEL', 'T_BEAM', 'USERDEFINED', 'NOTDEFINED')


class IfcBenchmarkEnum(str):
    items: tuple = ('GREATERTHAN', 'GREATERTHANOREQUALTO', 'LESSTHAN', 'LESSTHANOREQUALTO', 'EQUALTO', 'NOTEQUALTO')


class IfcBoilerTypeEnum(str):
    items: tuple = ('WATER', 'STEAM', 'USERDEFINED', 'NOTDEFINED')


class IfcBooleanOperator(str):
    items: tuple = ('UNION', 'INTERSECTION', 'DIFFERENCE')


class IfcBuildingElementProxyTypeEnum(str):
    items: tuple = ('USERDEFINED', 'NOTDEFINED')


class IfcCableCarrierFittingTypeEnum(str):
    items: tuple = ('BEND', 'CROSS', 'REDUCER', 'TEE', 'USERDEFINED', 'NOTDEFINED')


class IfcCableCarrierSegmentTypeEnum(str):
    items: tuple = ('CABLELADDERSEGMENT', 'CABLETRAYSEGMENT', 'CABLETRUNKINGSEGMENT', 'CONDUITSEGMENT', 'USERDEFINED', 'NOTDEFINED')


class IfcCableSegmentTypeEnum(str):
    items: tuple = ('CABLESEGMENT', 'CONDUCTORSEGMENT', 'USERDEFINED', 'NOTDEFINED')


class IfcChangeActionEnum(str):
    items: tuple = ('NOCHANGE', 'MODIFIED', 'ADDED', 'DELETED', 'MODIFIEDADDED', 'MODIFIEDDELETED')


class IfcChillerTypeEnum(str):
    items: tuple = ('AIRCOOLED', 'WATERCOOLED', 'HEATRECOVERY', 'USERDEFINED', 'NOTDEFINED')


class IfcCoilTypeEnum(str):
    items: tuple = ('DXCOOLINGCOIL', 'WATERCOOLINGCOIL', 'STEAMHEATINGCOIL', 'WATERHEATINGCOIL', 'ELECTRICHEATINGCOIL', 'GASHEATINGCOIL', 'USERDEFINED', 'NOTDEFINED')


class IfcColumnTypeEnum(str):
    items: tuple = ('COLUMN', 'USERDEFINED', 'NOTDEFINED')


class IfcCompressorTypeEnum(str):
    items: tuple = ('DYNAMIC', 'RECIPROCATING', 'ROTARY', 'SCROLL', 'TROCHOIDAL', 'SINGLESTAGE', 'BOOSTER', 'OPENTYPE', 'HERMETIC', 'SEMIHERMETIC', 'WELDEDSHELLHERMETIC', 'ROLLINGPISTON', 'ROTARYVANE', 'SINGLESCREW', 'TWINSCREW', 'USERDEFINED', 'NOTDEFINED')


class IfcCondenserTypeEnum(str):
    items: tuple = ('WATERCOOLEDSHELLTUBE', 'WATERCOOLEDSHELLCOIL', 'WATERCOOLEDTUBEINTUBE', 'WATERCOOLEDBRAZEDPLATE', 'AIRCOOLED', 'EVAPORATIVECOOLED', 'USERDEFINED', 'NOTDEFINED')


class IfcConnectionTypeEnum(str):
    items: tuple = ('ATPATH', 'ATSTART', 'ATEND', 'NOTDEFINED')


class IfcConstraintEnum(str):
    items: tuple = ('HARD', 'SOFT', 'ADVISORY', 'USERDEFINED', 'NOTDEFINED')


class IfcControllerTypeEnum(str):
    items: tuple = ('FLOATING', 'PROPORTIONAL', 'PROPORTIONALINTEGRAL', 'PROPORTIONALINTEGRALDERIVATIVE', 'TIMEDTWOPOSITION', 'TWOPOSITION', 'USERDEFINED', 'NOTDEFINED')


class IfcCooledBeamTypeEnum(str):
    items: tuple = ('ACTIVE', 'PASSIVE', 'USERDEFINED', 'NOTDEFINED')


class IfcCoolingTowerTypeEnum(str):
    items: tuple = ('NATURALDRAFT', 'MECHANICALINDUCEDDRAFT', 'MECHANICALFORCEDDRAFT', 'USERDEFINED', 'NOTDEFINED')


class IfcCostScheduleTypeEnum(str):
    items: tuple = ('BUDGET', 'COSTPLAN', 'ESTIMATE', 'TENDER', 'PRICEDBILLOFQUANTITIES', 'UNPRICEDBILLOFQUANTITIES', 'SCHEDULEOFRATES', 'USERDEFINED', 'NOTDEFINED')


class IfcCoveringTypeEnum(str):
    items: tuple = ('CEILING', 'FLOORING', 'CLADDING', 'ROOFING', 'INSULATION', 'MEMBRANE', 'SLEEVING', 'WRAPPING', 'USERDEFINED', 'NOTDEFINED')


class IfcCurrencyEnum(str):
    items: tuple = ('AED', 'AES', 'ATS', 'AUD', 'BBD', 'BEG', 'BGL', 'BHD', 'BMD', 'BND', 'BRL', 'BSD', 'BWP', 'BZD', 'CAD', 'CBD', 'CHF', 'CLP', 'CNY', 'CYS', 'CZK', 'DDP', 'DEM', 'DKK', 'EGL', 'EST', 'EUR', 'FAK', 'FIM', 'FJD', 'FKP', 'FRF', 'GBP', 'GIP', 'GMD', 'GRX', 'HKD', 'HUF', 'ICK', 'IDR', 'ILS', 'INR', 'IRP', 'ITL', 'JMD', 'JOD', 'JPY', 'KES', 'KRW', 'KWD', 'KYD', 'LKR', 'LUF', 'MTL', 'MUR', 'MXN', 'MYR', 'NLG', 'NZD', 'OMR', 'PGK', 'PHP', 'PKR', 'PLN', 'PTN', 'QAR', 'RUR', 'SAR', 'SCR', 'SEK', 'SGD', 'SKP', 'THB', 'TRL', 'TTD', 'TWD', 'USD', 'VEB', 'VND', 'XEU', 'ZAR', 'ZWD', 'NOK')


class IfcCurtainWallTypeEnum(str):
    items: tuple = ('USERDEFINED', 'NOTDEFINED')


class IfcDamperTypeEnum(str):
    items: tuple = ('CONTROLDAMPER', 'FIREDAMPER', 'SMOKEDAMPER', 'FIRESMOKEDAMPER', 'BACKDRAFTDAMPER', 'RELIEFDAMPER', 'BLASTDAMPER', 'GRAVITYDAMPER', 'GRAVITYRELIEFDAMPER', 'BALANCINGDAMPER', 'FUMEHOODEXHAUST', 'USERDEFINED', 'NOTDEFINED')


class IfcDataOriginEnum(str):
    items: tuple = ('MEASURED', 'PREDICTED', 'SIMULATED', 'USERDEFINED', 'NOTDEFINED')


class IfcDerivedUnitEnum(str):
    items: tuple = ('ANGULARVELOCITYUNIT', 'COMPOUNDPLANEANGLEUNIT', 'DYNAMICVISCOSITYUNIT', 'HEATFLUXDENSITYUNIT', 'INTEGERCOUNTRATEUNIT', 'ISOTHERMALMOISTURECAPACITYUNIT', 'KINEMATICVISCOSITYUNIT', 'LINEARVELOCITYUNIT', 'MASSDENSITYUNIT', 'MASSFLOWRATEUNIT', 'MOISTUREDIFFUSIVITYUNIT', 'MOLECULARWEIGHTUNIT', 'SPECIFICHEATCAPACITYUNIT', 'THERMALADMITTANCEUNIT', 'THERMALCONDUCTANCEUNIT', 'THERMALRESISTANCEUNIT', 'THERMALTRANSMITTANCEUNIT', 'VAPORPERMEABILITYUNIT', 'VOLUMETRICFLOWRATEUNIT', 'ROTATIONALFREQUENCYUNIT', 'TORQUEUNIT', 'MOMENTOFINERTIAUNIT', 'LINEARMOMENTUNIT', 'LINEARFORCEUNIT', 'PLANARFORCEUNIT', 'MODULUSOFELASTICITYUNIT', 'SHEARMODULUSUNIT', 'LINEARSTIFFNESSUNIT', 'ROTATIONALSTIFFNESSUNIT', 'MODULUSOFSUBGRADEREACTIONUNIT', 'ACCELERATIONUNIT', 'CURVATUREUNIT', 'HEATINGVALUEUNIT', 'IONCONCENTRATIONUNIT', 'LUMINOUSINTENSITYDISTRIBUTIONUNIT', 'MASSPERLENGTHUNIT', 'MODULUSOFLINEARSUBGRADEREACTIONUNIT', 'MODULUSOFROTATIONALSUBGRADEREACTIONUNIT', 'PHUNIT', 'ROTATIONALMASSUNIT', 'SECTIONAREAINTEGRALUNIT', 'SECTIONMODULUSUNIT', 'SOUNDPOWERUNIT', 'SOUNDPRESSUREUNIT', 'TEMPERATUREGRADIENTUNIT', 'THERMALEXPANSIONCOEFFICIENTUNIT', 'WARPINGCONSTANTUNIT', 'WARPINGMOMENTUNIT', 'USERDEFINED')


class IfcDimensionExtentUsage(str):
    items: tuple = ('ORIGIN', 'TARGET')


class IfcDirectionSenseEnum(str):
    items: tuple = ('POSITIVE', 'NEGATIVE')


class IfcDistributionChamberElementTypeEnum(str):
    items: tuple = ('FORMEDDUCT', 'INSPECTIONCHAMBER', 'INSPECTIONPIT', 'MANHOLE', 'METERCHAMBER', 'SUMP', 'TRENCH', 'VALVECHAMBER', 'USERDEFINED', 'NOTDEFINED')


class IfcDocumentConfidentialityEnum(str):
    items: tuple = ('PUBLIC', 'RESTRICTED', 'CONFIDENTIAL', 'PERSONAL', 'USERDEFINED', 'NOTDEFINED')


class IfcDocumentStatusEnum(str):
    items: tuple = ('DRAFT', 'FINALDRAFT', 'FINAL', 'REVISION', 'NOTDEFINED')


class IfcDoorPanelOperationEnum(str):
    items: tuple = ('SWINGING', 'DOUBLE_ACTING', 'SLIDING', 'FOLDING', 'REVOLVING', 'ROLLINGUP', 'USERDEFINED', 'NOTDEFINED')


class IfcDoorPanelPositionEnum(str):
    items: tuple = ('LEFT', 'MIDDLE', 'RIGHT', 'NOTDEFINED')


class IfcDoorStyleConstructionEnum(str):
    items: tuple = ('ALUMINIUM', 'HIGH_GRADE_STEEL', 'STEEL', 'WOOD', 'ALUMINIUM_WOOD', 'ALUMINIUM_PLASTIC', 'PLASTIC', 'USERDEFINED', 'NOTDEFINED')


class IfcDoorStyleOperationEnum(str):
    items: tuple = ('SINGLE_SWING_LEFT', 'SINGLE_SWING_RIGHT', 'DOUBLE_DOOR_SINGLE_SWING', 'DOUBLE_DOOR_SINGLE_SWING_OPPOSITE_LEFT', 'DOUBLE_DOOR_SINGLE_SWING_OPPOSITE_RIGHT', 'DOUBLE_SWING_LEFT', 'DOUBLE_SWING_RIGHT', 'DOUBLE_DOOR_DOUBLE_SWING', 'SLIDING_TO_LEFT', 'SLIDING_TO_RIGHT', 'DOUBLE_DOOR_SLIDING', 'FOLDING_TO_LEFT', 'FOLDING_TO_RIGHT', 'DOUBLE_DOOR_FOLDING', 'REVOLVING', 'ROLLINGUP', 'USERDEFINED', 'NOTDEFINED')


class IfcDuctFittingTypeEnum(str):
    items: tuple = ('BEND', 'CONNECTOR', 'ENTRY', 'EXIT', 'JUNCTION', 'OBSTRUCTION', 'TRANSITION', 'USERDEFINED', 'NOTDEFINED')


class IfcDuctSegmentTypeEnum(str):
    items: tuple = ('RIGIDSEGMENT', 'FLEXIBLESEGMENT', 'USERDEFINED', 'NOTDEFINED')


class IfcDuctSilencerTypeEnum(str):
    items: tuple = ('FLATOVAL', 'RECTANGULAR', 'ROUND', 'USERDEFINED', 'NOTDEFINED')


class IfcElectricApplianceTypeEnum(str):
    items: tuple = ('COMPUTER', 'DIRECTWATERHEATER', 'DISHWASHER', 'ELECTRICCOOKER', 'ELECTRICHEATER', 'FACSIMILE', 'FREESTANDINGFAN', 'FREEZER', 'FRIDGE_FREEZER', 'HANDDRYER', 'INDIRECTWATERHEATER', 'MICROWAVE', 'PHOTOCOPIER', 'PRINTER', 'REFRIGERATOR', 'RADIANTHEATER', 'SCANNER', 'TELEPHONE', 'TUMBLEDRYER', 'TV', 'VENDINGMACHINE', 'WASHINGMACHINE', 'WATERHEATER', 'WATERCOOLER', 'USERDEFINED', 'NOTDEFINED')


class IfcElectricCurrentEnum(str):
    items: tuple = ('ALTERNATING', 'DIRECT', 'NOTDEFINED')


class IfcElectricDistributionPointFunctionEnum(str):
    items: tuple = ('ALARMPANEL', 'CONSUMERUNIT', 'CONTROLPANEL', 'DISTRIBUTIONBOARD', 'GASDETECTORPANEL', 'INDICATORPANEL', 'MIMICPANEL', 'MOTORCONTROLCENTRE', 'SWITCHBOARD', 'USERDEFINED', 'NOTDEFINED')


class IfcElectricFlowStorageDeviceTypeEnum(str):
    items: tuple = ('BATTERY', 'CAPACITORBANK', 'HARMONICFILTER', 'INDUCTORBANK', 'UPS', 'USERDEFINED', 'NOTDEFINED')


class IfcElectricGeneratorTypeEnum(str):
    items: tuple = ('USERDEFINED', 'NOTDEFINED')


class IfcElectricHeaterTypeEnum(str):
    items: tuple = ('ELECTRICPOINTHEATER', 'ELECTRICCABLEHEATER', 'ELECTRICMATHEATER', 'USERDEFINED', 'NOTDEFINED')


class IfcElectricMotorTypeEnum(str):
    items: tuple = ('DC', 'INDUCTION', 'POLYPHASE', 'RELUCTANCESYNCHRONOUS', 'SYNCHRONOUS', 'USERDEFINED', 'NOTDEFINED')


class IfcElectricTimeControlTypeEnum(str):
    items: tuple = ('TIMECLOCK', 'TIMEDELAY', 'RELAY', 'USERDEFINED', 'NOTDEFINED')


class IfcElementAssemblyTypeEnum(str):
    items: tuple = ('ACCESSORY_ASSEMBLY', 'ARCH', 'BEAM_GRID', 'BRACED_FRAME', 'GIRDER', 'REINFORCEMENT_UNIT', 'RIGID_FRAME', 'SLAB_FIELD', 'TRUSS', 'USERDEFINED', 'NOTDEFINED')


class IfcElementCompositionEnum(str):
    items: tuple = ('COMPLEX', 'ELEMENT', 'PARTIAL')


class IfcEnergySequenceEnum(str):
    items: tuple = ('PRIMARY', 'SECONDARY', 'TERTIARY', 'AUXILIARY', 'USERDEFINED', 'NOTDEFINED')


class IfcEnvironmentalImpactCategoryEnum(str):
    items: tuple = ('COMBINEDVALUE', 'DISPOSAL', 'EXTRACTION', 'INSTALLATION', 'MANUFACTURE', 'TRANSPORTATION', 'USERDEFINED', 'NOTDEFINED')


class IfcEvaporativeCoolerTypeEnum(str):
    items: tuple = ('DIRECTEVAPORATIVERANDOMMEDIAAIRCOOLER', 'DIRECTEVAPORATIVERIGIDMEDIAAIRCOOLER', 'DIRECTEVAPORATIVESLINGERSPACKAGEDAIRCOOLER', 'DIRECTEVAPORATIVEPACKAGEDROTARYAIRCOOLER', 'DIRECTEVAPORATIVEAIRWASHER', 'INDIRECTEVAPORATIVEPACKAGEAIRCOOLER', 'INDIRECTEVAPORATIVEWETCOIL', 'INDIRECTEVAPORATIVECOOLINGTOWERORCOILCOOLER', 'INDIRECTDIRECTCOMBINATION', 'USERDEFINED', 'NOTDEFINED')


class IfcEvaporatorTypeEnum(str):
    items: tuple = ('DIRECTEXPANSIONSHELLANDTUBE', 'DIRECTEXPANSIONTUBEINTUBE', 'DIRECTEXPANSIONBRAZEDPLATE', 'FLOODEDSHELLANDTUBE', 'SHELLANDCOIL', 'USERDEFINED', 'NOTDEFINED')


class IfcFanTypeEnum(str):
    items: tuple = ('CENTRIFUGALFORWARDCURVED', 'CENTRIFUGALRADIAL', 'CENTRIFUGALBACKWARDINCLINEDCURVED', 'CENTRIFUGALAIRFOIL', 'TUBEAXIAL', 'VANEAXIAL', 'PROPELLORAXIAL', 'USERDEFINED', 'NOTDEFINED')


class IfcFilterTypeEnum(str):
    items: tuple = ('AIRPARTICLEFILTER', 'ODORFILTER', 'OILFILTER', 'STRAINER', 'WATERFILTER', 'USERDEFINED', 'NOTDEFINED')


class IfcFireSuppressionTerminalTypeEnum(str):
    items: tuple = ('BREECHINGINLET', 'FIREHYDRANT', 'HOSEREEL', 'SPRINKLER', 'SPRINKLERDEFLECTOR', 'USERDEFINED', 'NOTDEFINED')


class IfcFlowDirectionEnum(str):
    items: tuple = ('SOURCE', 'SINK', 'SOURCEANDSINK', 'NOTDEFINED')


class IfcFlowInstrumentTypeEnum(str):
    items: tuple = ('PRESSUREGAUGE', 'THERMOMETER', 'AMMETER', 'FREQUENCYMETER', 'POWERFACTORMETER', 'PHASEANGLEMETER', 'VOLTMETER_PEAK', 'VOLTMETER_RMS', 'USERDEFINED', 'NOTDEFINED')


class IfcFlowMeterTypeEnum(str):
    items: tuple = ('ELECTRICMETER', 'ENERGYMETER', 'FLOWMETER', 'GASMETER', 'OILMETER', 'WATERMETER', 'USERDEFINED', 'NOTDEFINED')


class IfcFootingTypeEnum(str):
    items: tuple = ('FOOTING_BEAM', 'PAD_FOOTING', 'PILE_CAP', 'STRIP_FOOTING', 'USERDEFINED', 'NOTDEFINED')


class IfcGasTerminalTypeEnum(str):
    items: tuple = ('GASAPPLIANCE', 'GASBOOSTER', 'GASBURNER', 'USERDEFINED', 'NOTDEFINED')


class IfcGeometricProjectionEnum(str):
    items: tuple = ('GRAPH_VIEW', 'SKETCH_VIEW', 'MODEL_VIEW', 'PLAN_VIEW', 'REFLECTED_PLAN_VIEW', 'SECTION_VIEW', 'ELEVATION_VIEW', 'USERDEFINED', 'NOTDEFINED')


class IfcGlobalOrLocalEnum(str):
    items: tuple = ('GLOBAL_COORDS', 'LOCAL_COORDS')


class IfcHeatExchangerTypeEnum(str):
    items: tuple = ('PLATE', 'SHELLANDTUBE', 'USERDEFINED', 'NOTDEFINED')


class IfcHumidifierTypeEnum(str):
    items: tuple = ('STEAMINJECTION', 'ADIABATICAIRWASHER', 'ADIABATICPAN', 'ADIABATICWETTEDELEMENT', 'ADIABATICATOMIZING', 'ADIABATICULTRASONIC', 'ADIABATICRIGIDMEDIA', 'ADIABATICCOMPRESSEDAIRNOZZLE', 'ASSISTEDELECTRIC', 'ASSISTEDNATURALGAS', 'ASSISTEDPROPANE', 'ASSISTEDBUTANE', 'ASSISTEDSTEAM', 'USERDEFINED', 'NOTDEFINED')


class IfcInternalOrExternalEnum(str):
    items: tuple = ('INTERNAL', 'EXTERNAL', 'NOTDEFINED')


class IfcInventoryTypeEnum(str):
    items: tuple = ('ASSETINVENTORY', 'SPACEINVENTORY', 'FURNITUREINVENTORY', 'USERDEFINED', 'NOTDEFINED')


class IfcJunctionBoxTypeEnum(str):
    items: tuple = ('USERDEFINED', 'NOTDEFINED')


class IfcLampTypeEnum(str):
    items: tuple = ('COMPACTFLUORESCENT', 'FLUORESCENT', 'HIGHPRESSUREMERCURY', 'HIGHPRESSURESODIUM', 'METALHALIDE', 'TUNGSTENFILAMENT', 'USERDEFINED', 'NOTDEFINED')


class IfcLayerSetDirectionEnum(str):
    items: tuple = ('AXIS1', 'AXIS2', 'AXIS3')


class IfcLightDistributionCurveEnum(str):
    items: tuple = ('TYPE_A', 'TYPE_B', 'TYPE_C', 'NOTDEFINED')


class IfcLightEmissionSourceEnum(str):
    items: tuple = ('COMPACTFLUORESCENT', 'FLUORESCENT', 'HIGHPRESSUREMERCURY', 'HIGHPRESSURESODIUM', 'LIGHTEMITTINGDIODE', 'LOWPRESSURESODIUM', 'LOWVOLTAGEHALOGEN', 'MAINVOLTAGEHALOGEN', 'METALHALIDE', 'TUNGSTENFILAMENT', 'NOTDEFINED')


class IfcLightFixtureTypeEnum(str):
    items: tuple = ('POINTSOURCE', 'DIRECTIONSOURCE', 'USERDEFINED', 'NOTDEFINED')


class IfcLoadGroupTypeEnum(str):
    items: tuple = ('LOAD_GROUP', 'LOAD_CASE', 'LOAD_COMBINATION_GROUP', 'LOAD_COMBINATION', 'USERDEFINED', 'NOTDEFINED')


class IfcLogicalOperatorEnum(str):
    items: tuple = ('LOGICALAND', 'LOGICALOR')


class IfcMemberTypeEnum(str):
    items: tuple = ('BRACE', 'CHORD', 'COLLAR', 'MEMBER', 'MULLION', 'PLATE', 'POST', 'PURLIN', 'RAFTER', 'STRINGER', 'STRUT', 'STUD', 'USERDEFINED', 'NOTDEFINED')


class IfcMotorConnectionTypeEnum(str):
    items: tuple = ('BELTDRIVE', 'COUPLING', 'DIRECTDRIVE', 'USERDEFINED', 'NOTDEFINED')


class IfcNullStyle(str):
    items: tuple = ('NULL',)


class IfcObjectTypeEnum(str):
    items: tuple = ('PRODUCT', 'PROCESS', 'CONTROL', 'RESOURCE', 'ACTOR', 'GROUP', 'PROJECT', 'NOTDEFINED')


class IfcObjectiveEnum(str):
    items: tuple = ('CODECOMPLIANCE', 'DESIGNINTENT', 'HEALTHANDSAFETY', 'REQUIREMENT', 'SPECIFICATION', 'TRIGGERCONDITION', 'USERDEFINED', 'NOTDEFINED')


class IfcOccupantTypeEnum(str):
    items: tuple = ('ASSIGNEE', 'ASSIGNOR', 'LESSEE', 'LESSOR', 'LETTINGAGENT', 'OWNER', 'TENANT', 'USERDEFINED', 'NOTDEFINED')


class IfcOutletTypeEnum(str):
    items: tuple = ('AUDIOVISUALOUTLET', 'COMMUNICATIONSOUTLET', 'POWEROUTLET', 'USERDEFINED', 'NOTDEFINED')


class IfcPermeableCoveringOperationEnum(str):
    items: tuple = ('GRILL', 'LOUVER', 'SCREEN', 'USERDEFINED', 'NOTDEFINED')


class IfcPhysicalOrVirtualEnum(str):
    items: tuple = ('PHYSICAL', 'VIRTUAL', 'NOTDEFINED')


class IfcPileConstructionEnum(str):
    items: tuple = ('CAST_IN_PLACE', 'COMPOSITE', 'PRECAST_CONCRETE', 'PREFAB_STEEL', 'USERDEFINED', 'NOTDEFINED')


class IfcPileTypeEnum(str):
    items: tuple = ('COHESION', 'FRICTION', 'SUPPORT', 'USERDEFINED', 'NOTDEFINED')


class IfcPipeFittingTypeEnum(str):
    items: tuple = ('BEND', 'CONNECTOR', 'ENTRY', 'EXIT', 'JUNCTION', 'OBSTRUCTION', 'TRANSITION', 'USERDEFINED', 'NOTDEFINED')


class IfcPipeSegmentTypeEnum(str):
    items: tuple = ('FLEXIBLESEGMENT', 'RIGIDSEGMENT', 'GUTTER', 'SPOOL', 'USERDEFINED', 'NOTDEFINED')


class IfcPlateTypeEnum(str):
    items: tuple = ('CURTAIN_PANEL', 'SHEET', 'USERDEFINED', 'NOTDEFINED')


class IfcProcedureTypeEnum(str):
    items: tuple = ('ADVICE_CAUTION', 'ADVICE_NOTE', 'ADVICE_WARNING', 'CALIBRATION', 'DIAGNOSTIC', 'SHUTDOWN', 'STARTUP', 'USERDEFINED', 'NOTDEFINED')


class IfcProfileTypeEnum(str):
    items: tuple = ('CURVE', 'AREA')


class IfcProjectOrderRecordTypeEnum(str):
    items: tuple = ('CHANGE', 'MAINTENANCE', 'MOVE', 'PURCHASE', 'WORK', 'USERDEFINED', 'NOTDEFINED')


class IfcProjectOrderTypeEnum(str):
    items: tuple = ('CHANGEORDER', 'MAINTENANCEWORKORDER', 'MOVEORDER', 'PURCHASEORDER', 'WORKORDER', 'USERDEFINED', 'NOTDEFINED')


class IfcProjectedOrTrueLengthEnum(str):
    items: tuple = ('PROJECTED_LENGTH', 'TRUE_LENGTH')


class IfcPropertySourceEnum(str):
    items: tuple = ('DESIGN', 'DESIGNMAXIMUM', 'DESIGNMINIMUM', 'SIMULATED', 'ASBUILT', 'COMMISSIONING', 'MEASURED', 'USERDEFINED', 'NOTKNOWN')


class IfcProtectiveDeviceTypeEnum(str):
    items: tuple = ('FUSEDISCONNECTOR', 'CIRCUITBREAKER', 'EARTHFAILUREDEVICE', 'RESIDUALCURRENTCIRCUITBREAKER', 'RESIDUALCURRENTSWITCH', 'VARISTOR', 'USERDEFINED', 'NOTDEFINED')


class IfcPumpTypeEnum(str):
    items: tuple = ('CIRCULATOR', 'ENDSUCTION', 'SPLITCASE', 'VERTICALINLINE', 'VERTICALTURBINE', 'USERDEFINED', 'NOTDEFINED')


class IfcRailingTypeEnum(str):
    items: tuple = ('HANDRAIL', 'GUARDRAIL', 'BALUSTRADE', 'USERDEFINED', 'NOTDEFINED')


class IfcRampFlightTypeEnum(str):
    items: tuple = ('STRAIGHT', 'SPIRAL', 'USERDEFINED', 'NOTDEFINED')


class IfcRampTypeEnum(str):
    items: tuple = ('STRAIGHT_RUN_RAMP', 'TWO_STRAIGHT_RUN_RAMP', 'QUARTER_TURN_RAMP', 'TWO_QUARTER_TURN_RAMP', 'HALF_TURN_RAMP', 'SPIRAL_RAMP', 'USERDEFINED', 'NOTDEFINED')


class IfcReflectanceMethodEnum(str):
    items: tuple = ('BLINN', 'FLAT', 'GLASS', 'MATT', 'METAL', 'MIRROR', 'PHONG', 'PLASTIC', 'STRAUSS', 'NOTDEFINED')


class IfcReinforcingBarRoleEnum(str):
    items: tuple = ('MAIN', 'SHEAR', 'LIGATURE', 'STUD', 'PUNCHING', 'EDGE', 'RING', 'USERDEFINED', 'NOTDEFINED')


class IfcReinforcingBarSurfaceEnum(str):
    items: tuple = ('PLAIN', 'TEXTURED')


class IfcResourceConsumptionEnum(str):
    items: tuple = ('CONSUMED', 'PARTIALLYCONSUMED', 'NOTCONSUMED', 'OCCUPIED', 'PARTIALLYOCCUPIED', 'NOTOCCUPIED', 'USERDEFINED', 'NOTDEFINED')


class IfcRibPlateDirectionEnum(str):
    items: tuple = ('DIRECTION_X', 'DIRECTION_Y')


class IfcRoleEnum(str):
    items: tuple = ('SUPPLIER', 'MANUFACTURER', 'CONTRACTOR', 'SUBCONTRACTOR', 'ARCHITECT', 'STRUCTURALENGINEER', 'COSTENGINEER', 'CLIENT', 'BUILDINGOWNER', 'BUILDINGOPERATOR', 'MECHANICALENGINEER', 'ELECTRICALENGINEER', 'PROJECTMANAGER', 'FACILITIESMANAGER', 'CIVILENGINEER', 'COMISSIONINGENGINEER', 'ENGINEER', 'OWNER', 'CONSULTANT', 'CONSTRUCTIONMANAGER', 'FIELDCONSTRUCTIONMANAGER', 'RESELLER', 'USERDEFINED')


class IfcRoofTypeEnum(str):
    items: tuple = ('FLAT_ROOF', 'SHED_ROOF', 'GABLE_ROOF', 'HIP_ROOF', 'HIPPED_GABLE_ROOF', 'GAMBREL_ROOF', 'MANSARD_ROOF', 'BARREL_ROOF', 'RAINBOW_ROOF', 'BUTTERFLY_ROOF', 'PAVILION_ROOF', 'DOME_ROOF', 'FREEFORM', 'NOTDEFINED')


class IfcSIPrefix(str):
    items: tuple = ('EXA', 'PETA', 'TERA', 'GIGA', 'MEGA', 'KILO', 'HECTO', 'DECA', 'DECI', 'CENTI', 'MILLI', 'MICRO', 'NANO', 'PICO', 'FEMTO', 'ATTO')


class IfcSIUnitName(str):
    items: tuple = ('AMPERE', 'BECQUEREL', 'CANDELA', 'COULOMB', 'CUBIC_METRE', 'DEGREE_CELSIUS', 'FARAD', 'GRAM', 'GRAY', 'HENRY', 'HERTZ', 'JOULE', 'KELVIN', 'LUMEN', 'LUX', 'METRE', 'MOLE', 'NEWTON', 'OHM', 'PASCAL', 'RADIAN', 'SECOND', 'SIEMENS', 'SIEVERT', 'SQUARE_METRE', 'STERADIAN', 'TESLA', 'VOLT', 'WATT', 'WEBER')


class IfcSanitaryTerminalTypeEnum(str):
    items: tuple = ('BATH', 'BIDET', 'CISTERN', 'SHOWER', 'SINK', 'SANITARYFOUNTAIN', 'TOILETPAN', 'URINAL', 'WASHHANDBASIN', 'WCSEAT', 'USERDEFINED', 'NOTDEFINED')


class IfcSectionTypeEnum(str):
    items: tuple = ('UNIFORM', 'TAPERED')


class IfcSensorTypeEnum(str):
    items: tuple = ('CO2SENSOR', 'FIRESENSOR', 'FLOWSENSOR', 'GASSENSOR', 'HEATSENSOR', 'HUMIDITYSENSOR', 'LIGHTSENSOR', 'MOISTURESENSOR', 'MOVEMENTSENSOR', 'PRESSURESENSOR', 'SMOKESENSOR', 'SOUNDSENSOR', 'TEMPERATURESENSOR', 'USERDEFINED', 'NOTDEFINED')


class IfcSequenceEnum(str):
    items: tuple = ('START_START', 'START_FINISH', 'FINISH_START', 'FINISH_FINISH', 'NOTDEFINED')


class IfcServiceLifeFactorTypeEnum(str):
    items: tuple = ('A_QUALITYOFCOMPONENTS', 'B_DESIGNLEVEL', 'C_WORKEXECUTIONLEVEL', 'D_INDOORENVIRONMENT', 'E_OUTDOORENVIRONMENT', 'F_INUSECONDITIONS', 'G_MAINTENANCELEVEL', 'USERDEFINED', 'NOTDEFINED')


class IfcServiceLifeTypeEnum(str):
    items: tuple = ('ACTUALSERVICELIFE', 'EXPECTEDSERVICELIFE', 'OPTIMISTICREFERENCESERVICELIFE', 'PESSIMISTICREFERENCESERVICELIFE', 'REFERENCESERVICELIFE')


class IfcSlabTypeEnum(str):
    items: tuple = ('FLOOR', 'ROOF', 'LANDING', 'BASESLAB', 'USERDEFINED', 'NOTDEFINED')


class IfcSoundScaleEnum(str):
    items: tuple = ('DBA', 'DBB', 'DBC', 'NC', 'NR', 'USERDEFINED', 'NOTDEFINED')


class IfcSpaceHeaterTypeEnum(str):
    items: tuple = ('SECTIONALRADIATOR', 'PANELRADIATOR', 'TUBULARRADIATOR', 'CONVECTOR', 'BASEBOARDHEATER', 'FINNEDTUBEUNIT', 'UNITHEATER', 'USERDEFINED', 'NOTDEFINED')


class IfcSpaceTypeEnum(str):
    items: tuple = ('USERDEFINED', 'NOTDEFINED')


class IfcStackTerminalTypeEnum(str):
    items: tuple = ('BIRDCAGE', 'COWL', 'RAINWATERHOPPER', 'USERDEFINED', 'NOTDEFINED')


class IfcStairFlightTypeEnum(str):
    items: tuple = ('STRAIGHT', 'WINDER', 'SPIRAL', 'CURVED', 'FREEFORM', 'USERDEFINED', 'NOTDEFINED')


class IfcStairTypeEnum(str):
    items: tuple = ('STRAIGHT_RUN_STAIR', 'TWO_STRAIGHT_RUN_STAIR', 'QUARTER_WINDING_STAIR', 'QUARTER_TURN_STAIR', 'HALF_WINDING_STAIR', 'HALF_TURN_STAIR', 'TWO_QUARTER_WINDING_STAIR', 'TWO_QUARTER_TURN_STAIR', 'THREE_QUARTER_WINDING_STAIR', 'THREE_QUARTER_TURN_STAIR', 'SPIRAL_STAIR', 'DOUBLE_RETURN_STAIR', 'CURVED_RUN_STAIR', 'TWO_CURVED_RUN_STAIR', 'USERDEFINED', 'NOTDEFINED')


class IfcStateEnum(str):
    items: tuple = ('READWRITE', 'READONLY', 'LOCKED', 'READWRITELOCKED', 'READONLYLOCKED')


class IfcStructuralCurveTypeEnum(str):
    items: tuple = ('RIGID_JOINED_MEMBER', 'PIN_JOINED_MEMBER', 'CABLE', 'TENSION_MEMBER', 'COMPRESSION_MEMBER', 'USERDEFINED', 'NOTDEFINED')


class IfcStructuralSurfaceTypeEnum(str):
    items: tuple = ('BENDING_ELEMENT', 'MEMBRANE_ELEMENT', 'SHELL', 'USERDEFINED', 'NOTDEFINED')


class IfcSurfaceSide(str):
    items: tuple = ('POSITIVE', 'NEGATIVE', 'BOTH')


class IfcSurfaceTextureEnum(str):
    items: tuple = ('BUMP', 'OPACITY', 'REFLECTION', 'SELFILLUMINATION', 'SHININESS', 'SPECULAR', 'TEXTURE', 'TRANSPARENCYMAP', 'NOTDEFINED')


class IfcSwitchingDeviceTypeEnum(str):
    items: tuple = ('CONTACTOR', 'EMERGENCYSTOP', 'STARTER', 'SWITCHDISCONNECTOR', 'TOGGLESWITCH', 'USERDEFINED', 'NOTDEFINED')


class IfcTankTypeEnum(str):
    items: tuple = ('PREFORMED', 'SECTIONAL', 'EXPANSION', 'PRESSUREVESSEL', 'USERDEFINED', 'NOTDEFINED')


class IfcTendonTypeEnum(str):
    items: tuple = ('STRAND', 'WIRE', 'BAR', 'COATED', 'USERDEFINED', 'NOTDEFINED')


class IfcTextPath(str):
    items: tuple = ('LEFT', 'RIGHT', 'UP', 'DOWN')


class IfcThermalLoadSourceEnum(str):
    items: tuple = ('PEOPLE', 'LIGHTING', 'EQUIPMENT', 'VENTILATIONINDOORAIR', 'VENTILATIONOUTSIDEAIR', 'RECIRCULATEDAIR', 'EXHAUSTAIR', 'AIREXCHANGERATE', 'DRYBULBTEMPERATURE', 'RELATIVEHUMIDITY', 'INFILTRATION', 'USERDEFINED', 'NOTDEFINED')


class IfcThermalLoadTypeEnum(str):
    items: tuple = ('SENSIBLE', 'LATENT', 'RADIANT', 'NOTDEFINED')


class IfcTimeSeriesDataTypeEnum(str):
    items: tuple = ('CONTINUOUS', 'DISCRETE', 'DISCRETEBINARY', 'PIECEWISEBINARY', 'PIECEWISECONSTANT', 'PIECEWISECONTINUOUS', 'NOTDEFINED')


class IfcTimeSeriesScheduleTypeEnum(str):
    items: tuple = ('ANNUAL', 'MONTHLY', 'WEEKLY', 'DAILY', 'USERDEFINED', 'NOTDEFINED')


class IfcTransformerTypeEnum(str):
    items: tuple = ('CURRENT', 'FREQUENCY', 'VOLTAGE', 'USERDEFINED', 'NOTDEFINED')


class IfcTransitionCode(str):
    items: tuple = ('DISCONTINUOUS', 'CONTINUOUS', 'CONTSAMEGRADIENT', 'CONTSAMEGRADIENTSAMECURVATURE')


class IfcTransportElementTypeEnum(str):
    items: tuple = ('ELEVATOR', 'ESCALATOR', 'MOVINGWALKWAY', 'USERDEFINED', 'NOTDEFINED')


class IfcTrimmingPreference(str):
    items: tuple = ('CARTESIAN', 'PARAMETER', 'UNSPECIFIED')


class IfcTubeBundleTypeEnum(str):
    items: tuple = ('FINNED', 'USERDEFINED', 'NOTDEFINED')


class IfcUnitEnum(str):
    items: tuple = ('ABSORBEDDOSEUNIT', 'AMOUNTOFSUBSTANCEUNIT', 'AREAUNIT', 'DOSEEQUIVALENTUNIT', 'ELECTRICCAPACITANCEUNIT', 'ELECTRICCHARGEUNIT', 'ELECTRICCONDUCTANCEUNIT', 'ELECTRICCURRENTUNIT', 'ELECTRICRESISTANCEUNIT', 'ELECTRICVOLTAGEUNIT', 'ENERGYUNIT', 'FORCEUNIT', 'FREQUENCYUNIT', 'ILLUMINANCEUNIT', 'INDUCTANCEUNIT', 'LENGTHUNIT', 'LUMINOUSFLUXUNIT', 'LUMINOUSINTENSITYUNIT', 'MAGNETICFLUXDENSITYUNIT', 'MAGNETICFLUXUNIT', 'MASSUNIT', 'PLANEANGLEUNIT', 'POWERUNIT', 'PRESSUREUNIT', 'RADIOACTIVITYUNIT', 'SOLIDANGLEUNIT', 'THERMODYNAMICTEMPERATUREUNIT', 'TIMEUNIT', 'VOLUMEUNIT', 'USERDEFINED')


class IfcUnitaryEquipmentTypeEnum(str):
    items: tuple = ('AIRHANDLER', 'AIRCONDITIONINGUNIT', 'SPLITSYSTEM', 'ROOFTOPUNIT', 'USERDEFINED', 'NOTDEFINED')


class IfcValveTypeEnum(str):
    items: tuple = ('AIRRELEASE', 'ANTIVACUUM', 'CHANGEOVER', 'CHECK', 'COMMISSIONING', 'DIVERTING', 'DRAWOFFCOCK', 'DOUBLECHECK', 'DOUBLEREGULATING', 'FAUCET', 'FLUSHING', 'GASCOCK', 'GASTAP', 'ISOLATING', 'MIXING', 'PRESSUREREDUCING', 'PRESSURERELIEF', 'REGULATING', 'SAFETYCUTOFF', 'STEAMTRAP', 'STOPCOCK', 'USERDEFINED', 'NOTDEFINED')


class IfcVibrationIsolatorTypeEnum(str):
    items: tuple = ('COMPRESSION', 'SPRING', 'USERDEFINED', 'NOTDEFINED')


class IfcWallTypeEnum(str):
    items: tuple = ('STANDARD', 'POLYGONAL', 'SHEAR', 'ELEMENTEDWALL', 'PLUMBINGWALL', 'USERDEFINED', 'NOTDEFINED')


class IfcWasteTerminalTypeEnum(str):
    items: tuple = ('FLOORTRAP', 'FLOORWASTE', 'GULLYSUMP', 'GULLYTRAP', 'GREASEINTERCEPTOR', 'OILINTERCEPTOR', 'PETROLINTERCEPTOR', 'ROOFDRAIN', 'WASTEDISPOSALUNIT', 'WASTETRAP', 'USERDEFINED', 'NOTDEFINED')


class IfcWindowPanelOperationEnum(str):
    items: tuple = ('SIDEHUNGRIGHTHAND', 'SIDEHUNGLEFTHAND', 'TILTANDTURNRIGHTHAND', 'TILTANDTURNLEFTHAND', 'TOPHUNG', 'BOTTOMHUNG', 'PIVOTHORIZONTAL', 'PIVOTVERTICAL', 'SLIDINGHORIZONTAL', 'SLIDINGVERTICAL', 'REMOVABLECASEMENT', 'FIXEDCASEMENT', 'OTHEROPERATION', 'NOTDEFINED')


class IfcWindowPanelPositionEnum(str):
    items: tuple = ('LEFT', 'MIDDLE', 'RIGHT', 'BOTTOM', 'TOP', 'NOTDEFINED')


class IfcWindowStyleConstructionEnum(str):
    items: tuple = ('ALUMINIUM', 'HIGH_GRADE_STEEL', 'STEEL', 'WOOD', 'ALUMINIUM_WOOD', 'PLASTIC', 'OTHER_CONSTRUCTION', 'NOTDEFINED')


class IfcWindowStyleOperationEnum(str):
    items: tuple = ('SINGLE_PANEL', 'DOUBLE_PANEL_VERTICAL', 'DOUBLE_PANEL_HORIZONTAL', 'TRIPLE_PANEL_VERTICAL', 'TRIPLE_PANEL_BOTTOM', 'TRIPLE_PANEL_TOP', 'TRIPLE_PANEL_LEFT', 'TRIPLE_PANEL_RIGHT', 'TRIPLE_PANEL_HORIZONTAL', 'USERDEFINED', 'NOTDEFINED')


class IfcWorkControlTypeEnum(str):
    items: tuple = ('ACTUAL', 'BASELINE', 'PLANNED', 'USERDEFINED', 'NOTDEFINED')


class IfcActorRole:
    """Wrapper class for IfcActorRole."""
    Role: "IfcRoleEnum"
    UserDefinedRole: Optional[str]
    Description: Optional[str]


class IfcAddress:
    """Wrapper class for IfcAddress."""
    Purpose: Optional["IfcAddressTypeEnum"]
    Description: Optional[str]
    UserDefinedPurpose: Optional[str]
    def OfPerson(self) -> tuple["IfcPerson", ...]: ...
    def OfOrganization(self) -> tuple["IfcOrganization", ...]: ...


class IfcApplication:
    """Wrapper class for IfcApplication."""
    ApplicationDeveloper: "IfcOrganization"
    Version: str
    ApplicationFullName: str
    ApplicationIdentifier: str


class IfcAppliedValue:
    """Wrapper class for IfcAppliedValue."""
    Name: Optional[str]
    Description: Optional[str]
    AppliedValue: Optional[Union["IfcMeasureWithUnit", float]]
    UnitBasis: Optional["IfcMeasureWithUnit"]
    ApplicableDate: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    FixedUntilDate: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    def ValuesReferenced(self) -> tuple["IfcReferencesValueDocument", ...]: ...
    def ValueOfComponents(self) -> tuple["IfcAppliedValueRelationship", ...]: ...
    def IsComponentIn(self) -> tuple["IfcAppliedValueRelationship", ...]: ...


class IfcAppliedValueRelationship:
    """Wrapper class for IfcAppliedValueRelationship."""
    ComponentOfTotal: "IfcAppliedValue"
    Components: list["IfcAppliedValue"]
    ArithmeticOperator: "IfcArithmeticOperatorEnum"
    Name: Optional[str]
    Description: Optional[str]


class IfcApproval:
    """Wrapper class for IfcApproval."""
    Description: Optional[str]
    ApprovalDateTime: Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]
    ApprovalStatus: Optional[str]
    ApprovalLevel: Optional[str]
    ApprovalQualifier: Optional[str]
    Name: str
    Identifier: str
    def Actors(self) -> tuple["IfcApprovalActorRelationship", ...]: ...
    def IsRelatedWith(self) -> tuple["IfcApprovalRelationship", ...]: ...
    def Relates(self) -> tuple["IfcApprovalRelationship", ...]: ...


class IfcApprovalActorRelationship:
    """Wrapper class for IfcApprovalActorRelationship."""
    Actor: Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]
    Approval: "IfcApproval"
    Role: "IfcActorRole"


class IfcApprovalPropertyRelationship:
    """Wrapper class for IfcApprovalPropertyRelationship."""
    ApprovedProperties: list["IfcProperty"]
    Approval: "IfcApproval"


class IfcApprovalRelationship:
    """Wrapper class for IfcApprovalRelationship."""
    RelatedApproval: "IfcApproval"
    RelatingApproval: "IfcApproval"
    Description: Optional[str]
    Name: str


class IfcBoundaryCondition:
    """Wrapper class for IfcBoundaryCondition."""
    Name: Optional[str]


class IfcCalendarDate:
    """Wrapper class for IfcCalendarDate."""
    DayComponent: int
    MonthComponent: int
    YearComponent: int


class IfcClassification:
    """Wrapper class for IfcClassification."""
    Source: str
    Edition: str
    EditionDate: Optional["IfcCalendarDate"]
    Name: str
    def Contains(self) -> tuple["IfcClassificationItem", ...]: ...


class IfcClassificationItem:
    """Wrapper class for IfcClassificationItem."""
    Notation: "IfcClassificationNotationFacet"
    ItemOf: Optional["IfcClassification"]
    Title: str
    def IsClassifiedItemIn(self) -> tuple["IfcClassificationItemRelationship", ...]: ...
    def IsClassifyingItemIn(self) -> tuple["IfcClassificationItemRelationship", ...]: ...


class IfcClassificationItemRelationship:
    """Wrapper class for IfcClassificationItemRelationship."""
    RelatingItem: "IfcClassificationItem"
    RelatedItems: list["IfcClassificationItem"]


class IfcClassificationNotation:
    """Wrapper class for IfcClassificationNotation."""
    NotationFacets: list["IfcClassificationNotationFacet"]


class IfcClassificationNotationFacet:
    """Wrapper class for IfcClassificationNotationFacet."""
    NotationValue: str


class IfcColourSpecification:
    """Wrapper class for IfcColourSpecification."""
    Name: Optional[str]


class IfcConnectionGeometry:
    """Wrapper class for IfcConnectionGeometry."""
    ...


class IfcConstraint:
    """Wrapper class for IfcConstraint."""
    Name: str
    Description: Optional[str]
    ConstraintGrade: "IfcConstraintEnum"
    ConstraintSource: Optional[str]
    CreatingActor: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    CreationTime: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    UserDefinedGrade: Optional[str]
    def ClassifiedAs(self) -> tuple["IfcConstraintClassificationRelationship", ...]: ...
    def RelatesConstraints(self) -> tuple["IfcConstraintRelationship", ...]: ...
    def IsRelatedWith(self) -> tuple["IfcConstraintRelationship", ...]: ...
    def PropertiesForConstraint(self) -> tuple["IfcPropertyConstraintRelationship", ...]: ...
    def Aggregates(self) -> tuple["IfcConstraintAggregationRelationship", ...]: ...
    def IsAggregatedIn(self) -> tuple["IfcConstraintAggregationRelationship", ...]: ...


class IfcConstraintAggregationRelationship:
    """Wrapper class for IfcConstraintAggregationRelationship."""
    Name: Optional[str]
    Description: Optional[str]
    RelatingConstraint: "IfcConstraint"
    RelatedConstraints: list["IfcConstraint"]
    LogicalAggregator: "IfcLogicalOperatorEnum"


class IfcConstraintClassificationRelationship:
    """Wrapper class for IfcConstraintClassificationRelationship."""
    ClassifiedConstraint: "IfcConstraint"
    RelatedClassifications: list[Union["IfcClassificationNotation", "IfcClassificationReference"]]


class IfcConstraintRelationship:
    """Wrapper class for IfcConstraintRelationship."""
    Name: Optional[str]
    Description: Optional[str]
    RelatingConstraint: "IfcConstraint"
    RelatedConstraints: list["IfcConstraint"]


class IfcCoordinatedUniversalTimeOffset:
    """Wrapper class for IfcCoordinatedUniversalTimeOffset."""
    HourOffset: int
    MinuteOffset: Optional[int]
    Sense: "IfcAheadOrBehind"


class IfcCurrencyRelationship:
    """Wrapper class for IfcCurrencyRelationship."""
    RelatingMonetaryUnit: "IfcMonetaryUnit"
    RelatedMonetaryUnit: "IfcMonetaryUnit"
    ExchangeRate: float
    RateDateTime: "IfcDateAndTime"
    RateSource: Optional["IfcLibraryInformation"]


class IfcCurveStyleFont:
    """Wrapper class for IfcCurveStyleFont."""
    Name: Optional[str]
    PatternList: list["IfcCurveStyleFontPattern"]


class IfcCurveStyleFontAndScaling:
    """Wrapper class for IfcCurveStyleFontAndScaling."""
    Name: Optional[str]
    CurveFont: Union["IfcCurveStyleFont", "IfcPreDefinedCurveFont"]
    CurveFontScaling: float


class IfcCurveStyleFontPattern:
    """Wrapper class for IfcCurveStyleFontPattern."""
    VisibleSegmentLength: float
    InvisibleSegmentLength: float


class IfcDateAndTime:
    """Wrapper class for IfcDateAndTime."""
    DateComponent: "IfcCalendarDate"
    TimeComponent: "IfcLocalTime"


class IfcDerivedUnit:
    """Wrapper class for IfcDerivedUnit."""
    Elements: list["IfcDerivedUnitElement"]
    UnitType: "IfcDerivedUnitEnum"
    UserDefinedType: Optional[str]


class IfcDerivedUnitElement:
    """Wrapper class for IfcDerivedUnitElement."""
    Unit: "IfcNamedUnit"
    Exponent: int


class IfcDimensionalExponents:
    """Wrapper class for IfcDimensionalExponents."""
    LengthExponent: int
    MassExponent: int
    TimeExponent: int
    ElectricCurrentExponent: int
    ThermodynamicTemperatureExponent: int
    AmountOfSubstanceExponent: int
    LuminousIntensityExponent: int


class IfcDocumentElectronicFormat:
    """Wrapper class for IfcDocumentElectronicFormat."""
    FileExtension: Optional[str]
    MimeContentType: Optional[str]
    MimeSubtype: Optional[str]


class IfcDocumentInformation:
    """Wrapper class for IfcDocumentInformation."""
    DocumentId: str
    Name: str
    Description: Optional[str]
    DocumentReferences: Optional[list["IfcDocumentReference"]]
    Purpose: Optional[str]
    IntendedUse: Optional[str]
    Scope: Optional[str]
    Revision: Optional[str]
    DocumentOwner: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    Editors: Optional[list[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]]
    CreationTime: Optional["IfcDateAndTime"]
    LastRevisionTime: Optional["IfcDateAndTime"]
    ElectronicFormat: Optional["IfcDocumentElectronicFormat"]
    ValidFrom: Optional["IfcCalendarDate"]
    ValidUntil: Optional["IfcCalendarDate"]
    Confidentiality: Optional["IfcDocumentConfidentialityEnum"]
    Status: Optional["IfcDocumentStatusEnum"]
    def IsPointedTo(self) -> tuple["IfcDocumentInformationRelationship", ...]: ...
    def IsPointer(self) -> tuple["IfcDocumentInformationRelationship", ...]: ...


class IfcDocumentInformationRelationship:
    """Wrapper class for IfcDocumentInformationRelationship."""
    RelatingDocument: "IfcDocumentInformation"
    RelatedDocuments: list["IfcDocumentInformation"]
    RelationshipType: Optional[str]


class IfcDraughtingCalloutRelationship:
    """Wrapper class for IfcDraughtingCalloutRelationship."""
    Name: Optional[str]
    Description: Optional[str]
    RelatingDraughtingCallout: "IfcDraughtingCallout"
    RelatedDraughtingCallout: "IfcDraughtingCallout"


class IfcExternalReference:
    """Wrapper class for IfcExternalReference."""
    Location: Optional[str]
    ItemReference: Optional[str]
    Name: Optional[str]


class IfcGridAxis:
    """Wrapper class for IfcGridAxis."""
    AxisTag: Optional[str]
    AxisCurve: "IfcCurve"
    SameSense: bool
    def PartOfW(self) -> tuple["IfcGrid", ...]: ...
    def PartOfV(self) -> tuple["IfcGrid", ...]: ...
    def PartOfU(self) -> tuple["IfcGrid", ...]: ...
    def HasIntersections(self) -> tuple["IfcVirtualGridIntersection", ...]: ...


class IfcIrregularTimeSeriesValue:
    """Wrapper class for IfcIrregularTimeSeriesValue."""
    TimeStamp: Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]
    ListValues: list[Union[float, list[int], int, list[float], str, bool]]


class IfcLibraryInformation:
    """Wrapper class for IfcLibraryInformation."""
    Name: str
    Version: Optional[str]
    Publisher: Optional["IfcOrganization"]
    VersionDate: Optional["IfcCalendarDate"]
    LibraryReference: Optional[list["IfcLibraryReference"]]


class IfcLightDistributionData:
    """Wrapper class for IfcLightDistributionData."""
    MainPlaneAngle: float
    SecondaryPlaneAngle: list[float]
    LuminousIntensity: list[float]


class IfcLightIntensityDistribution:
    """Wrapper class for IfcLightIntensityDistribution."""
    LightDistributionCurve: "IfcLightDistributionCurveEnum"
    DistributionData: list["IfcLightDistributionData"]


class IfcLocalTime:
    """Wrapper class for IfcLocalTime."""
    HourComponent: int
    MinuteComponent: Optional[int]
    SecondComponent: Optional[float]
    Zone: Optional["IfcCoordinatedUniversalTimeOffset"]
    DaylightSavingOffset: Optional[int]


class IfcMaterial:
    """Wrapper class for IfcMaterial."""
    Name: str
    def HasRepresentation(self) -> tuple["IfcMaterialDefinitionRepresentation", ...]: ...
    def ClassifiedAs(self) -> tuple["IfcMaterialClassificationRelationship", ...]: ...


class IfcMaterialClassificationRelationship:
    """Wrapper class for IfcMaterialClassificationRelationship."""
    MaterialClassifications: list[Union["IfcClassificationNotation", "IfcClassificationReference"]]
    ClassifiedMaterial: "IfcMaterial"


class IfcMaterialLayer:
    """Wrapper class for IfcMaterialLayer."""
    Material: Optional["IfcMaterial"]
    LayerThickness: float
    IsVentilated: Optional[bool]
    def ToMaterialLayerSet(self) -> tuple["IfcMaterialLayerSet", ...]: ...


class IfcMaterialLayerSet:
    """Wrapper class for IfcMaterialLayerSet."""
    MaterialLayers: list["IfcMaterialLayer"]
    LayerSetName: Optional[str]


class IfcMaterialLayerSetUsage:
    """Wrapper class for IfcMaterialLayerSetUsage."""
    ForLayerSet: "IfcMaterialLayerSet"
    LayerSetDirection: "IfcLayerSetDirectionEnum"
    DirectionSense: "IfcDirectionSenseEnum"
    OffsetFromReferenceLine: float


class IfcMaterialList:
    """Wrapper class for IfcMaterialList."""
    Materials: list["IfcMaterial"]


class IfcMaterialProperties:
    """Wrapper class for IfcMaterialProperties."""
    Material: "IfcMaterial"


class IfcMeasureWithUnit:
    """Wrapper class for IfcMeasureWithUnit."""
    ValueComponent: Union[float, list[int], int, list[float], str, bool]
    UnitComponent: Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]


class IfcMonetaryUnit:
    """Wrapper class for IfcMonetaryUnit."""
    Currency: "IfcCurrencyEnum"


class IfcNamedUnit:
    """Wrapper class for IfcNamedUnit."""
    Dimensions: "IfcDimensionalExponents"
    UnitType: "IfcUnitEnum"


class IfcObjectPlacement:
    """Wrapper class for IfcObjectPlacement."""
    def PlacesObject(self) -> tuple["IfcProduct", ...]: ...
    def ReferencedByPlacements(self) -> tuple["IfcLocalPlacement", ...]: ...


class IfcOrganization:
    """Wrapper class for IfcOrganization."""
    Id: Optional[str]
    Name: str
    Description: Optional[str]
    Roles: Optional[list["IfcActorRole"]]
    Addresses: Optional[list["IfcAddress"]]
    def IsRelatedBy(self) -> tuple["IfcOrganizationRelationship", ...]: ...
    def Relates(self) -> tuple["IfcOrganizationRelationship", ...]: ...
    def Engages(self) -> tuple["IfcPersonAndOrganization", ...]: ...


class IfcOrganizationRelationship:
    """Wrapper class for IfcOrganizationRelationship."""
    Name: str
    Description: Optional[str]
    RelatingOrganization: "IfcOrganization"
    RelatedOrganizations: list["IfcOrganization"]


class IfcOwnerHistory:
    """Wrapper class for IfcOwnerHistory."""
    OwningUser: "IfcPersonAndOrganization"
    OwningApplication: "IfcApplication"
    State: Optional["IfcStateEnum"]
    ChangeAction: "IfcChangeActionEnum"
    LastModifiedDate: Optional[int]
    LastModifyingUser: Optional["IfcPersonAndOrganization"]
    LastModifyingApplication: Optional["IfcApplication"]
    CreationDate: int


class IfcPerson:
    """Wrapper class for IfcPerson."""
    Id: Optional[str]
    FamilyName: Optional[str]
    GivenName: Optional[str]
    MiddleNames: Optional[list[str]]
    PrefixTitles: Optional[list[str]]
    SuffixTitles: Optional[list[str]]
    Roles: Optional[list["IfcActorRole"]]
    Addresses: Optional[list["IfcAddress"]]
    def EngagedIn(self) -> tuple["IfcPersonAndOrganization", ...]: ...


class IfcPersonAndOrganization:
    """Wrapper class for IfcPersonAndOrganization."""
    ThePerson: "IfcPerson"
    TheOrganization: "IfcOrganization"
    Roles: Optional[list["IfcActorRole"]]


class IfcPhysicalQuantity:
    """Wrapper class for IfcPhysicalQuantity."""
    Name: str
    Description: Optional[str]
    def PartOfComplex(self) -> tuple["IfcPhysicalComplexQuantity", ...]: ...


class IfcPreDefinedItem:
    """Wrapper class for IfcPreDefinedItem."""
    Name: str


class IfcPresentationLayerAssignment:
    """Wrapper class for IfcPresentationLayerAssignment."""
    Name: str
    Description: Optional[str]
    AssignedItems: list[Union["IfcRepresentation", "IfcRepresentationItem"]]
    Identifier: Optional[str]


class IfcPresentationStyle:
    """Wrapper class for IfcPresentationStyle."""
    Name: Optional[str]


class IfcPresentationStyleAssignment:
    """Wrapper class for IfcPresentationStyleAssignment."""
    Styles: list[Union["IfcCurveStyle", "IfcFillAreaStyle", "IfcNullStyle", "IfcSurfaceStyle", "IfcSymbolStyle", "IfcTextStyle"]]


class IfcProductRepresentation:
    """Wrapper class for IfcProductRepresentation."""
    Name: Optional[str]
    Description: Optional[str]
    Representations: list["IfcRepresentation"]


class IfcProfileDef:
    """Wrapper class for IfcProfileDef."""
    ProfileType: "IfcProfileTypeEnum"
    ProfileName: Optional[str]


class IfcProfileProperties:
    """Wrapper class for IfcProfileProperties."""
    ProfileName: Optional[str]
    ProfileDefinition: Optional["IfcProfileDef"]


class IfcProperty:
    """Wrapper class for IfcProperty."""
    Name: str
    Description: Optional[str]
    def PropertyForDependance(self) -> tuple["IfcPropertyDependencyRelationship", ...]: ...
    def PropertyDependsOn(self) -> tuple["IfcPropertyDependencyRelationship", ...]: ...
    def PartOfComplex(self) -> tuple["IfcComplexProperty", ...]: ...


class IfcPropertyConstraintRelationship:
    """Wrapper class for IfcPropertyConstraintRelationship."""
    RelatingConstraint: "IfcConstraint"
    RelatedProperties: list["IfcProperty"]
    Name: Optional[str]
    Description: Optional[str]


class IfcPropertyDependencyRelationship:
    """Wrapper class for IfcPropertyDependencyRelationship."""
    DependingProperty: "IfcProperty"
    DependantProperty: "IfcProperty"
    Name: Optional[str]
    Description: Optional[str]
    Expression: Optional[str]


class IfcPropertyEnumeration:
    """Wrapper class for IfcPropertyEnumeration."""
    Name: str
    EnumerationValues: list[Union[float, list[int], int, list[float], str, bool]]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]


class IfcReferencesValueDocument:
    """Wrapper class for IfcReferencesValueDocument."""
    ReferencedDocument: Union["IfcDocumentInformation", "IfcDocumentReference"]
    ReferencingValues: list["IfcAppliedValue"]
    Name: Optional[str]
    Description: Optional[str]


class IfcReinforcementBarProperties:
    """Wrapper class for IfcReinforcementBarProperties."""
    TotalCrossSectionArea: float
    SteelGrade: str
    BarSurface: Optional["IfcReinforcingBarSurfaceEnum"]
    EffectiveDepth: Optional[float]
    NominalBarDiameter: Optional[float]
    BarCount: Optional[float]


class IfcRelaxation:
    """Wrapper class for IfcRelaxation."""
    RelaxationValue: float
    InitialStress: float


class IfcRepresentation:
    """Wrapper class for IfcRepresentation."""
    ContextOfItems: "IfcRepresentationContext"
    RepresentationIdentifier: Optional[str]
    RepresentationType: Optional[str]
    Items: list["IfcRepresentationItem"]
    def RepresentationMap(self) -> tuple["IfcRepresentationMap", ...]: ...
    def LayerAssignments(self) -> tuple["IfcPresentationLayerAssignment", ...]: ...
    def OfProductRepresentation(self) -> tuple["IfcProductRepresentation", ...]: ...


class IfcRepresentationContext:
    """Wrapper class for IfcRepresentationContext."""
    ContextIdentifier: Optional[str]
    ContextType: Optional[str]
    def RepresentationsInContext(self) -> tuple["IfcRepresentation", ...]: ...


class IfcRepresentationItem:
    """Wrapper class for IfcRepresentationItem."""
    def LayerAssignments(self) -> tuple["IfcPresentationLayerAssignment", ...]: ...
    def StyledByItem(self) -> tuple["IfcStyledItem", ...]: ...


class IfcRepresentationMap:
    """Wrapper class for IfcRepresentationMap."""
    MappingOrigin: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]
    MappedRepresentation: "IfcRepresentation"
    def MapUsage(self) -> tuple["IfcMappedItem", ...]: ...


class IfcRoot:
    """Wrapper class for IfcRoot."""
    GlobalId: str
    OwnerHistory: "IfcOwnerHistory"
    Name: Optional[str]
    Description: Optional[str]


class IfcSectionProperties:
    """Wrapper class for IfcSectionProperties."""
    SectionType: "IfcSectionTypeEnum"
    StartProfile: "IfcProfileDef"
    EndProfile: Optional["IfcProfileDef"]


class IfcSectionReinforcementProperties:
    """Wrapper class for IfcSectionReinforcementProperties."""
    LongitudinalStartPosition: float
    LongitudinalEndPosition: float
    TransversePosition: Optional[float]
    ReinforcementRole: "IfcReinforcingBarRoleEnum"
    SectionDefinition: "IfcSectionProperties"
    CrossSectionReinforcementDefinitions: list["IfcReinforcementBarProperties"]


class IfcShapeAspect:
    """Wrapper class for IfcShapeAspect."""
    ShapeRepresentations: list["IfcShapeModel"]
    Name: Optional[str]
    Description: Optional[str]
    ProductDefinitional: bool
    PartOfProductDefinitionShape: "IfcProductDefinitionShape"


class IfcStructuralConnectionCondition:
    """Wrapper class for IfcStructuralConnectionCondition."""
    Name: Optional[str]


class IfcStructuralLoad:
    """Wrapper class for IfcStructuralLoad."""
    Name: Optional[str]


class IfcSurfaceStyleLighting:
    """Wrapper class for IfcSurfaceStyleLighting."""
    DiffuseTransmissionColour: "IfcColourRgb"
    DiffuseReflectionColour: "IfcColourRgb"
    TransmissionColour: "IfcColourRgb"
    ReflectanceColour: "IfcColourRgb"


class IfcSurfaceStyleRefraction:
    """Wrapper class for IfcSurfaceStyleRefraction."""
    RefractionIndex: Optional[float]
    DispersionFactor: Optional[float]


class IfcSurfaceStyleShading:
    """Wrapper class for IfcSurfaceStyleShading."""
    SurfaceColour: "IfcColourRgb"


class IfcSurfaceStyleWithTextures:
    """Wrapper class for IfcSurfaceStyleWithTextures."""
    Textures: list["IfcSurfaceTexture"]


class IfcSurfaceTexture:
    """Wrapper class for IfcSurfaceTexture."""
    RepeatS: bool
    RepeatT: bool
    TextureType: "IfcSurfaceTextureEnum"
    TextureTransform: Optional["IfcCartesianTransformationOperator2D"]


class IfcTable:
    """Wrapper class for IfcTable."""
    Name: str
    Rows: list["IfcTableRow"]


class IfcTableRow:
    """Wrapper class for IfcTableRow."""
    RowCells: list[Union[float, list[int], int, list[float], str, bool]]
    IsHeading: bool
    def OfTable(self) -> tuple["IfcTable", ...]: ...


class IfcTextStyleForDefinedFont:
    """Wrapper class for IfcTextStyleForDefinedFont."""
    Colour: Union["IfcColourSpecification", "IfcPreDefinedColour"]
    BackgroundColour: Optional[Union["IfcColourSpecification", "IfcPreDefinedColour"]]


class IfcTextStyleTextModel:
    """Wrapper class for IfcTextStyleTextModel."""
    TextIndent: Optional[Union[str, float]]
    TextAlign: Optional[str]
    TextDecoration: Optional[str]
    LetterSpacing: Optional[Union[str, float]]
    WordSpacing: Optional[Union[str, float]]
    TextTransform: Optional[str]
    LineHeight: Optional[Union[str, float]]


class IfcTextStyleWithBoxCharacteristics:
    """Wrapper class for IfcTextStyleWithBoxCharacteristics."""
    BoxHeight: Optional[float]
    BoxWidth: Optional[float]
    BoxSlantAngle: Optional[float]
    BoxRotateAngle: Optional[float]
    CharacterSpacing: Optional[Union[str, float]]


class IfcTextureCoordinate:
    """Wrapper class for IfcTextureCoordinate."""
    def AnnotatedSurface(self) -> tuple["IfcAnnotationSurface", ...]: ...


class IfcTextureVertex:
    """Wrapper class for IfcTextureVertex."""
    Coordinates: list[float]


class IfcTimeSeries:
    """Wrapper class for IfcTimeSeries."""
    Name: str
    Description: Optional[str]
    StartTime: Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]
    EndTime: Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]
    TimeSeriesDataType: "IfcTimeSeriesDataTypeEnum"
    DataOrigin: "IfcDataOriginEnum"
    UserDefinedDataOrigin: Optional[str]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    def DocumentedBy(self) -> tuple["IfcTimeSeriesReferenceRelationship", ...]: ...


class IfcTimeSeriesReferenceRelationship:
    """Wrapper class for IfcTimeSeriesReferenceRelationship."""
    ReferencedTimeSeries: "IfcTimeSeries"
    TimeSeriesReferences: list[Union["IfcDocumentInformation", "IfcDocumentReference"]]


class IfcTimeSeriesValue:
    """Wrapper class for IfcTimeSeriesValue."""
    ListValues: list[Union[float, list[int], int, list[float], str, bool]]


class IfcUnitAssignment:
    """Wrapper class for IfcUnitAssignment."""
    Units: list[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]


class IfcVertexBasedTextureMap:
    """Wrapper class for IfcVertexBasedTextureMap."""
    TextureVertices: list["IfcTextureVertex"]
    TexturePoints: list["IfcCartesianPoint"]


class IfcVirtualGridIntersection:
    """Wrapper class for IfcVirtualGridIntersection."""
    IntersectingAxes: list["IfcGridAxis"]
    OffsetDistances: list[float]


class IfcArbitraryClosedProfileDef(IfcProfileDef):
    """Wrapper class for IfcArbitraryClosedProfileDef."""
    OuterCurve: "IfcCurve"


class IfcArbitraryOpenProfileDef(IfcProfileDef):
    """Wrapper class for IfcArbitraryOpenProfileDef."""
    Curve: "IfcBoundedCurve"


class IfcBlobTexture(IfcSurfaceTexture):
    """Wrapper class for IfcBlobTexture."""
    RasterFormat: str
    RasterCode: bool


class IfcBoundaryEdgeCondition(IfcBoundaryCondition):
    """Wrapper class for IfcBoundaryEdgeCondition."""
    LinearStiffnessByLengthX: Optional[float]
    LinearStiffnessByLengthY: Optional[float]
    LinearStiffnessByLengthZ: Optional[float]
    RotationalStiffnessByLengthX: Optional[float]
    RotationalStiffnessByLengthY: Optional[float]
    RotationalStiffnessByLengthZ: Optional[float]


class IfcBoundaryFaceCondition(IfcBoundaryCondition):
    """Wrapper class for IfcBoundaryFaceCondition."""
    LinearStiffnessByAreaX: Optional[float]
    LinearStiffnessByAreaY: Optional[float]
    LinearStiffnessByAreaZ: Optional[float]


class IfcBoundaryNodeCondition(IfcBoundaryCondition):
    """Wrapper class for IfcBoundaryNodeCondition."""
    LinearStiffnessX: Optional[float]
    LinearStiffnessY: Optional[float]
    LinearStiffnessZ: Optional[float]
    RotationalStiffnessX: Optional[float]
    RotationalStiffnessY: Optional[float]
    RotationalStiffnessZ: Optional[float]


class IfcClassificationReference(IfcExternalReference):
    """Wrapper class for IfcClassificationReference."""
    ReferencedSource: Optional["IfcClassification"]


class IfcColourRgb(IfcColourSpecification):
    """Wrapper class for IfcColourRgb."""
    Red: float
    Green: float
    Blue: float


class IfcComplexProperty(IfcProperty):
    """Wrapper class for IfcComplexProperty."""
    UsageName: str
    HasProperties: list["IfcProperty"]


class IfcCompositeProfileDef(IfcProfileDef):
    """Wrapper class for IfcCompositeProfileDef."""
    Profiles: list["IfcProfileDef"]
    Label: Optional[str]


class IfcConnectionCurveGeometry(IfcConnectionGeometry):
    """Wrapper class for IfcConnectionCurveGeometry."""
    CurveOnRelatingElement: Union["IfcBoundedCurve", "IfcEdgeCurve"]
    CurveOnRelatedElement: Optional[Union["IfcBoundedCurve", "IfcEdgeCurve"]]


class IfcConnectionPointGeometry(IfcConnectionGeometry):
    """Wrapper class for IfcConnectionPointGeometry."""
    PointOnRelatingElement: Union["IfcPoint", "IfcVertexPoint"]
    PointOnRelatedElement: Optional[Union["IfcPoint", "IfcVertexPoint"]]


class IfcConnectionPortGeometry(IfcConnectionGeometry):
    """Wrapper class for IfcConnectionPortGeometry."""
    LocationAtRelatingElement: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]
    LocationAtRelatedElement: Optional[Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]]
    ProfileOfPort: "IfcProfileDef"


class IfcConnectionSurfaceGeometry(IfcConnectionGeometry):
    """Wrapper class for IfcConnectionSurfaceGeometry."""
    SurfaceOnRelatingElement: Union["IfcFaceBasedSurfaceModel", "IfcFaceSurface", "IfcSurface"]
    SurfaceOnRelatedElement: Optional[Union["IfcFaceBasedSurfaceModel", "IfcFaceSurface", "IfcSurface"]]


class IfcContextDependentUnit(IfcNamedUnit):
    """Wrapper class for IfcContextDependentUnit."""
    Name: str


class IfcConversionBasedUnit(IfcNamedUnit):
    """Wrapper class for IfcConversionBasedUnit."""
    Name: str
    ConversionFactor: "IfcMeasureWithUnit"


class IfcCostValue(IfcAppliedValue):
    """Wrapper class for IfcCostValue."""
    CostType: str
    Condition: Optional[str]


class IfcCurveStyle(IfcPresentationStyle):
    """Wrapper class for IfcCurveStyle."""
    CurveFont: Optional[Union["IfcCurveStyleFontAndScaling", "IfcCurveStyleFont", "IfcPreDefinedCurveFont"]]
    CurveWidth: Optional[Union[str, float]]
    CurveColour: Optional[Union["IfcColourSpecification", "IfcPreDefinedColour"]]


class IfcDerivedProfileDef(IfcProfileDef):
    """Wrapper class for IfcDerivedProfileDef."""
    ParentProfile: "IfcProfileDef"
    Operator: "IfcCartesianTransformationOperator2D"
    Label: Optional[str]


class IfcDimensionCalloutRelationship(IfcDraughtingCalloutRelationship):
    """Wrapper class for IfcDimensionCalloutRelationship."""
    ...


class IfcDimensionPair(IfcDraughtingCalloutRelationship):
    """Wrapper class for IfcDimensionPair."""
    ...


class IfcDocumentReference(IfcExternalReference):
    """Wrapper class for IfcDocumentReference."""
    def ReferenceToDocument(self) -> tuple["IfcDocumentInformation", ...]: ...


class IfcEnvironmentalImpactValue(IfcAppliedValue):
    """Wrapper class for IfcEnvironmentalImpactValue."""
    ImpactType: str
    Category: "IfcEnvironmentalImpactCategoryEnum"
    UserDefinedCategory: Optional[str]


class IfcExtendedMaterialProperties(IfcMaterialProperties):
    """Wrapper class for IfcExtendedMaterialProperties."""
    ExtendedProperties: list["IfcProperty"]
    Description: Optional[str]
    Name: str


class IfcExternallyDefinedHatchStyle(IfcExternalReference):
    """Wrapper class for IfcExternallyDefinedHatchStyle."""
    ...


class IfcExternallyDefinedSurfaceStyle(IfcExternalReference):
    """Wrapper class for IfcExternallyDefinedSurfaceStyle."""
    ...


class IfcExternallyDefinedSymbol(IfcExternalReference):
    """Wrapper class for IfcExternallyDefinedSymbol."""
    ...


class IfcExternallyDefinedTextFont(IfcExternalReference):
    """Wrapper class for IfcExternallyDefinedTextFont."""
    ...


class IfcFailureConnectionCondition(IfcStructuralConnectionCondition):
    """Wrapper class for IfcFailureConnectionCondition."""
    TensionFailureX: Optional[float]
    TensionFailureY: Optional[float]
    TensionFailureZ: Optional[float]
    CompressionFailureX: Optional[float]
    CompressionFailureY: Optional[float]
    CompressionFailureZ: Optional[float]


class IfcFillAreaStyle(IfcPresentationStyle):
    """Wrapper class for IfcFillAreaStyle."""
    FillStyles: list[Union["IfcColourSpecification", "IfcPreDefinedColour", "IfcExternallyDefinedHatchStyle", "IfcFillAreaStyleHatching", "IfcFillAreaStyleTiles"]]


class IfcFuelProperties(IfcMaterialProperties):
    """Wrapper class for IfcFuelProperties."""
    CombustionTemperature: Optional[float]
    CarbonContent: Optional[float]
    LowerHeatingValue: Optional[float]
    HigherHeatingValue: Optional[float]


class IfcGeneralMaterialProperties(IfcMaterialProperties):
    """Wrapper class for IfcGeneralMaterialProperties."""
    MolecularWeight: Optional[float]
    Porosity: Optional[float]
    MassDensity: Optional[float]


class IfcGeneralProfileProperties(IfcProfileProperties):
    """Wrapper class for IfcGeneralProfileProperties."""
    PhysicalWeight: Optional[float]
    Perimeter: Optional[float]
    MinimumPlateThickness: Optional[float]
    MaximumPlateThickness: Optional[float]
    CrossSectionArea: Optional[float]


class IfcGeometricRepresentationContext(IfcRepresentationContext):
    """Wrapper class for IfcGeometricRepresentationContext."""
    CoordinateSpaceDimension: int
    Precision: Optional[float]
    WorldCoordinateSystem: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]
    TrueNorth: Optional["IfcDirection"]
    def HasSubContexts(self) -> tuple["IfcGeometricRepresentationSubContext", ...]: ...


class IfcGeometricRepresentationItem(IfcRepresentationItem):
    """Wrapper class for IfcGeometricRepresentationItem."""
    ...


class IfcGridPlacement(IfcObjectPlacement):
    """Wrapper class for IfcGridPlacement."""
    PlacementLocation: "IfcVirtualGridIntersection"
    PlacementRefDirection: Optional["IfcVirtualGridIntersection"]


class IfcHygroscopicMaterialProperties(IfcMaterialProperties):
    """Wrapper class for IfcHygroscopicMaterialProperties."""
    UpperVaporResistanceFactor: Optional[float]
    LowerVaporResistanceFactor: Optional[float]
    IsothermalMoistureCapacity: Optional[float]
    VaporPermeability: Optional[float]
    MoistureDiffusivity: Optional[float]


class IfcImageTexture(IfcSurfaceTexture):
    """Wrapper class for IfcImageTexture."""
    UrlReference: str


class IfcIrregularTimeSeries(IfcTimeSeries):
    """Wrapper class for IfcIrregularTimeSeries."""
    Values: list["IfcIrregularTimeSeriesValue"]


class IfcLibraryReference(IfcExternalReference):
    """Wrapper class for IfcLibraryReference."""
    def ReferenceIntoLibrary(self) -> tuple["IfcLibraryInformation", ...]: ...


class IfcLocalPlacement(IfcObjectPlacement):
    """Wrapper class for IfcLocalPlacement."""
    PlacementRelTo: Optional["IfcObjectPlacement"]
    RelativePlacement: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]


class IfcMappedItem(IfcRepresentationItem):
    """Wrapper class for IfcMappedItem."""
    MappingSource: "IfcRepresentationMap"
    MappingTarget: "IfcCartesianTransformationOperator"


class IfcMaterialDefinitionRepresentation(IfcProductRepresentation):
    """Wrapper class for IfcMaterialDefinitionRepresentation."""
    RepresentedMaterial: "IfcMaterial"


class IfcMechanicalMaterialProperties(IfcMaterialProperties):
    """Wrapper class for IfcMechanicalMaterialProperties."""
    DynamicViscosity: Optional[float]
    YoungModulus: Optional[float]
    ShearModulus: Optional[float]
    PoissonRatio: Optional[float]
    ThermalExpansionCoefficient: Optional[float]


class IfcMetric(IfcConstraint):
    """Wrapper class for IfcMetric."""
    Benchmark: "IfcBenchmarkEnum"
    ValueSource: Optional[str]
    DataValue: Union["IfcCostValue", "IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime", "IfcMeasureWithUnit", "IfcTable", str, "IfcTimeSeries"]


class IfcObjectDefinition(IfcRoot):
    """Wrapper class for IfcObjectDefinition."""
    def HasAssignments(self) -> tuple["IfcRelAssigns", ...]: ...
    def IsDecomposedBy(self) -> tuple["IfcRelDecomposes", ...]: ...
    def Decomposes(self) -> tuple["IfcRelDecomposes", ...]: ...
    def HasAssociations(self) -> tuple["IfcRelAssociates", ...]: ...
    @property
    def parent(self) -> object: ...
    @property
    def children(self) -> object: ...
    @property
    def descendants(self) -> object: ...
    @property
    def material(self) -> object: ...
    def children_by_type(self, type_name, recursive=False) -> object: ...


class IfcObjective(IfcConstraint):
    """Wrapper class for IfcObjective."""
    BenchmarkValues: Optional["IfcMetric"]
    ResultValues: Optional["IfcMetric"]
    ObjectiveQualifier: "IfcObjectiveEnum"
    UserDefinedQualifier: Optional[str]


class IfcOpticalMaterialProperties(IfcMaterialProperties):
    """Wrapper class for IfcOpticalMaterialProperties."""
    VisibleTransmittance: Optional[float]
    SolarTransmittance: Optional[float]
    ThermalIrTransmittance: Optional[float]
    ThermalIrEmissivityBack: Optional[float]
    ThermalIrEmissivityFront: Optional[float]
    VisibleReflectanceBack: Optional[float]
    VisibleReflectanceFront: Optional[float]
    SolarReflectanceFront: Optional[float]
    SolarReflectanceBack: Optional[float]


class IfcParameterizedProfileDef(IfcProfileDef):
    """Wrapper class for IfcParameterizedProfileDef."""
    Position: "IfcAxis2Placement2D"


class IfcPhysicalComplexQuantity(IfcPhysicalQuantity):
    """Wrapper class for IfcPhysicalComplexQuantity."""
    HasQuantities: list["IfcPhysicalQuantity"]
    Discrimination: str
    Quality: Optional[str]
    Usage: Optional[str]


class IfcPhysicalSimpleQuantity(IfcPhysicalQuantity):
    """Wrapper class for IfcPhysicalSimpleQuantity."""
    Unit: Optional["IfcNamedUnit"]


class IfcPixelTexture(IfcSurfaceTexture):
    """Wrapper class for IfcPixelTexture."""
    Width: int
    Height: int
    ColourComponents: int
    Pixel: list[bytes]


class IfcPostalAddress(IfcAddress):
    """Wrapper class for IfcPostalAddress."""
    InternalLocation: Optional[str]
    AddressLines: Optional[list[str]]
    PostalBox: Optional[str]
    Town: Optional[str]
    Region: Optional[str]
    PostalCode: Optional[str]
    Country: Optional[str]


class IfcPreDefinedColour(IfcPreDefinedItem):
    """Wrapper class for IfcPreDefinedColour."""
    ...


class IfcPreDefinedCurveFont(IfcPreDefinedItem):
    """Wrapper class for IfcPreDefinedCurveFont."""
    ...


class IfcPreDefinedSymbol(IfcPreDefinedItem):
    """Wrapper class for IfcPreDefinedSymbol."""
    ...


class IfcPreDefinedTextFont(IfcPreDefinedItem):
    """Wrapper class for IfcPreDefinedTextFont."""
    ...


class IfcPresentationLayerWithStyle(IfcPresentationLayerAssignment):
    """Wrapper class for IfcPresentationLayerWithStyle."""
    LayerOn: bool
    LayerFrozen: bool
    LayerBlocked: bool
    LayerStyles: list[Union["IfcCurveStyle", "IfcFillAreaStyle", "IfcNullStyle", "IfcSurfaceStyle", "IfcSymbolStyle", "IfcTextStyle"]]


class IfcProductDefinitionShape(IfcProductRepresentation):
    """Wrapper class for IfcProductDefinitionShape."""
    def ShapeOfProduct(self) -> tuple["IfcProduct", ...]: ...
    def HasShapeAspects(self) -> tuple["IfcShapeAspect", ...]: ...


class IfcProductsOfCombustionProperties(IfcMaterialProperties):
    """Wrapper class for IfcProductsOfCombustionProperties."""
    SpecificHeatCapacity: Optional[float]
    N20Content: Optional[float]
    COContent: Optional[float]
    CO2Content: Optional[float]


class IfcPropertyDefinition(IfcRoot):
    """Wrapper class for IfcPropertyDefinition."""
    def HasAssociations(self) -> tuple["IfcRelAssociates", ...]: ...


class IfcRegularTimeSeries(IfcTimeSeries):
    """Wrapper class for IfcRegularTimeSeries."""
    TimeStep: float
    Values: list["IfcTimeSeriesValue"]


class IfcRelationship(IfcRoot):
    """Wrapper class for IfcRelationship."""
    ...


class IfcRibPlateProfileProperties(IfcProfileProperties):
    """Wrapper class for IfcRibPlateProfileProperties."""
    Thickness: Optional[float]
    RibHeight: Optional[float]
    RibWidth: Optional[float]
    RibSpacing: Optional[float]
    Direction: "IfcRibPlateDirectionEnum"


class IfcSIUnit(IfcNamedUnit):
    """Wrapper class for IfcSIUnit."""
    Prefix: Optional["IfcSIPrefix"]
    Name: "IfcSIUnitName"


class IfcShapeModel(IfcRepresentation):
    """Wrapper class for IfcShapeModel."""
    def OfShapeAspect(self) -> tuple["IfcShapeAspect", ...]: ...


class IfcSimpleProperty(IfcProperty):
    """Wrapper class for IfcSimpleProperty."""
    ...


class IfcSlippageConnectionCondition(IfcStructuralConnectionCondition):
    """Wrapper class for IfcSlippageConnectionCondition."""
    SlippageX: Optional[float]
    SlippageY: Optional[float]
    SlippageZ: Optional[float]


class IfcStructuralLoadStatic(IfcStructuralLoad):
    """Wrapper class for IfcStructuralLoadStatic."""
    ...


class IfcStyleModel(IfcRepresentation):
    """Wrapper class for IfcStyleModel."""
    ...


class IfcStyledItem(IfcRepresentationItem):
    """Wrapper class for IfcStyledItem."""
    Item: Optional["IfcRepresentationItem"]
    Styles: list["IfcPresentationStyleAssignment"]
    Name: Optional[str]


class IfcSurfaceStyle(IfcPresentationStyle):
    """Wrapper class for IfcSurfaceStyle."""
    Side: "IfcSurfaceSide"
    Styles: list[Union["IfcExternallyDefinedSurfaceStyle", "IfcSurfaceStyleLighting", "IfcSurfaceStyleRefraction", "IfcSurfaceStyleShading", "IfcSurfaceStyleWithTextures"]]


class IfcSurfaceStyleRendering(IfcSurfaceStyleShading):
    """Wrapper class for IfcSurfaceStyleRendering."""
    Transparency: Optional[float]
    DiffuseColour: Optional[Union["IfcColourRgb", float]]
    TransmissionColour: Optional[Union["IfcColourRgb", float]]
    DiffuseTransmissionColour: Optional[Union["IfcColourRgb", float]]
    ReflectionColour: Optional[Union["IfcColourRgb", float]]
    SpecularColour: Optional[Union["IfcColourRgb", float]]
    SpecularHighlight: Optional[float]
    ReflectanceMethod: "IfcReflectanceMethodEnum"


class IfcSymbolStyle(IfcPresentationStyle):
    """Wrapper class for IfcSymbolStyle."""
    StyleOfSymbol: Union["IfcColourSpecification", "IfcPreDefinedColour"]


class IfcTelecomAddress(IfcAddress):
    """Wrapper class for IfcTelecomAddress."""
    TelephoneNumbers: Optional[list[str]]
    FacsimileNumbers: Optional[list[str]]
    PagerNumber: Optional[str]
    ElectronicMailAddresses: Optional[list[str]]
    WWWHomePageURL: Optional[str]


class IfcTextStyle(IfcPresentationStyle):
    """Wrapper class for IfcTextStyle."""
    TextCharacterAppearance: Optional["IfcTextStyleForDefinedFont"]
    TextStyle: Optional[Union["IfcTextStyleTextModel", "IfcTextStyleWithBoxCharacteristics"]]
    TextFontStyle: Union["IfcExternallyDefinedTextFont", "IfcPreDefinedTextFont"]


class IfcTextureCoordinateGenerator(IfcTextureCoordinate):
    """Wrapper class for IfcTextureCoordinateGenerator."""
    Mode: str
    Parameter: list[Union[bool, str, int, float]]


class IfcTextureMap(IfcTextureCoordinate):
    """Wrapper class for IfcTextureMap."""
    TextureMaps: list["IfcVertexBasedTextureMap"]


class IfcThermalMaterialProperties(IfcMaterialProperties):
    """Wrapper class for IfcThermalMaterialProperties."""
    SpecificHeatCapacity: Optional[float]
    BoilingPoint: Optional[float]
    FreezingPoint: Optional[float]
    ThermalConductivity: Optional[float]


class IfcTopologicalRepresentationItem(IfcRepresentationItem):
    """Wrapper class for IfcTopologicalRepresentationItem."""
    ...


class IfcWaterProperties(IfcMaterialProperties):
    """Wrapper class for IfcWaterProperties."""
    IsPotable: Optional[bool]
    Hardness: Optional[float]
    AlkalinityConcentration: Optional[float]
    AcidityConcentration: Optional[float]
    ImpuritiesContent: Optional[float]
    PHLevel: Optional[float]
    DissolvedSolidsContent: Optional[float]


class IfcAnnotationFillArea(IfcGeometricRepresentationItem):
    """Wrapper class for IfcAnnotationFillArea."""
    OuterBoundary: "IfcCurve"
    InnerBoundaries: Optional[list["IfcCurve"]]


class IfcAnnotationOccurrence(IfcStyledItem):
    """Wrapper class for IfcAnnotationOccurrence."""
    ...


class IfcAnnotationSurface(IfcGeometricRepresentationItem):
    """Wrapper class for IfcAnnotationSurface."""
    Item: "IfcGeometricRepresentationItem"
    TextureCoordinates: Optional["IfcTextureCoordinate"]


class IfcArbitraryProfileDefWithVoids(IfcArbitraryClosedProfileDef):
    """Wrapper class for IfcArbitraryProfileDefWithVoids."""
    InnerCurves: list["IfcCurve"]


class IfcBooleanResult(IfcGeometricRepresentationItem):
    """Wrapper class for IfcBooleanResult."""
    Operator: "IfcBooleanOperator"
    FirstOperand: Union["IfcBooleanResult", "IfcCsgPrimitive3D", "IfcHalfSpaceSolid", "IfcSolidModel"]
    SecondOperand: Union["IfcBooleanResult", "IfcCsgPrimitive3D", "IfcHalfSpaceSolid", "IfcSolidModel"]


class IfcBoundaryNodeConditionWarping(IfcBoundaryNodeCondition):
    """Wrapper class for IfcBoundaryNodeConditionWarping."""
    WarpingStiffness: Optional[float]


class IfcBoundingBox(IfcGeometricRepresentationItem):
    """Wrapper class for IfcBoundingBox."""
    Corner: "IfcCartesianPoint"
    XDim: float
    YDim: float
    ZDim: float


class IfcCShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcCShapeProfileDef."""
    Depth: float
    Width: float
    WallThickness: float
    Girth: float
    InternalFilletRadius: Optional[float]
    CentreOfGravityInX: Optional[float]


class IfcCartesianTransformationOperator(IfcGeometricRepresentationItem):
    """Wrapper class for IfcCartesianTransformationOperator."""
    Axis1: Optional["IfcDirection"]
    Axis2: Optional["IfcDirection"]
    LocalOrigin: "IfcCartesianPoint"
    Scale: Optional[float]


class IfcCenterLineProfileDef(IfcArbitraryOpenProfileDef):
    """Wrapper class for IfcCenterLineProfileDef."""
    Thickness: float


class IfcCircleProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcCircleProfileDef."""
    Radius: float


class IfcCompositeCurveSegment(IfcGeometricRepresentationItem):
    """Wrapper class for IfcCompositeCurveSegment."""
    Transition: "IfcTransitionCode"
    SameSense: bool
    ParentCurve: "IfcCurve"
    def UsingCurves(self) -> tuple["IfcCompositeCurve", ...]: ...


class IfcConnectedFaceSet(IfcTopologicalRepresentationItem):
    """Wrapper class for IfcConnectedFaceSet."""
    CfsFaces: list["IfcFace"]


class IfcConnectionPointEccentricity(IfcConnectionPointGeometry):
    """Wrapper class for IfcConnectionPointEccentricity."""
    EccentricityInX: Optional[float]
    EccentricityInY: Optional[float]
    EccentricityInZ: Optional[float]


class IfcCraneRailAShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcCraneRailAShapeProfileDef."""
    OverallHeight: float
    BaseWidth2: float
    Radius: Optional[float]
    HeadWidth: float
    HeadDepth2: float
    HeadDepth3: float
    WebThickness: float
    BaseWidth4: float
    BaseDepth1: float
    BaseDepth2: float
    BaseDepth3: float
    CentreOfGravityInY: Optional[float]


class IfcCraneRailFShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcCraneRailFShapeProfileDef."""
    OverallHeight: float
    HeadWidth: float
    Radius: Optional[float]
    HeadDepth2: float
    HeadDepth3: float
    WebThickness: float
    BaseDepth1: float
    BaseDepth2: float
    CentreOfGravityInY: Optional[float]


class IfcCsgPrimitive3D(IfcGeometricRepresentationItem):
    """Wrapper class for IfcCsgPrimitive3D."""
    Position: "IfcAxis2Placement3D"


class IfcCurve(IfcGeometricRepresentationItem):
    """Wrapper class for IfcCurve."""
    ...


class IfcDefinedSymbol(IfcGeometricRepresentationItem):
    """Wrapper class for IfcDefinedSymbol."""
    Definition: Union["IfcExternallyDefinedSymbol", "IfcPreDefinedSymbol"]
    Target: "IfcCartesianTransformationOperator2D"


class IfcDirection(IfcGeometricRepresentationItem):
    """Wrapper class for IfcDirection."""
    DirectionRatios: list[float]


class IfcDraughtingCallout(IfcGeometricRepresentationItem):
    """Wrapper class for IfcDraughtingCallout."""
    Contents: list[Union["IfcAnnotationCurveOccurrence", "IfcAnnotationSymbolOccurrence", "IfcAnnotationTextOccurrence"]]
    def IsRelatedFromCallout(self) -> tuple["IfcDraughtingCalloutRelationship", ...]: ...
    def IsRelatedToCallout(self) -> tuple["IfcDraughtingCalloutRelationship", ...]: ...


class IfcDraughtingPreDefinedColour(IfcPreDefinedColour):
    """Wrapper class for IfcDraughtingPreDefinedColour."""
    ...


class IfcDraughtingPreDefinedCurveFont(IfcPreDefinedCurveFont):
    """Wrapper class for IfcDraughtingPreDefinedCurveFont."""
    ...


class IfcDraughtingPreDefinedTextFont(IfcPreDefinedTextFont):
    """Wrapper class for IfcDraughtingPreDefinedTextFont."""
    ...


class IfcEdge(IfcTopologicalRepresentationItem):
    """Wrapper class for IfcEdge."""
    EdgeStart: "IfcVertex"
    EdgeEnd: "IfcVertex"


class IfcEllipseProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcEllipseProfileDef."""
    SemiAxis1: float
    SemiAxis2: float


class IfcFace(IfcTopologicalRepresentationItem):
    """Wrapper class for IfcFace."""
    Bounds: list["IfcFaceBound"]


class IfcFaceBasedSurfaceModel(IfcGeometricRepresentationItem):
    """Wrapper class for IfcFaceBasedSurfaceModel."""
    FbsmFaces: list["IfcConnectedFaceSet"]


class IfcFaceBound(IfcTopologicalRepresentationItem):
    """Wrapper class for IfcFaceBound."""
    Bound: "IfcLoop"
    Orientation: bool


class IfcFillAreaStyleHatching(IfcGeometricRepresentationItem):
    """Wrapper class for IfcFillAreaStyleHatching."""
    HatchLineAppearance: "IfcCurveStyle"
    StartOfNextHatchLine: Union["IfcOneDirectionRepeatFactor", float]
    PointOfReferenceHatchLine: Optional["IfcCartesianPoint"]
    PatternStart: Optional["IfcCartesianPoint"]
    HatchLineAngle: float


class IfcFillAreaStyleTileSymbolWithStyle(IfcGeometricRepresentationItem):
    """Wrapper class for IfcFillAreaStyleTileSymbolWithStyle."""
    Symbol: "IfcAnnotationSymbolOccurrence"


class IfcFillAreaStyleTiles(IfcGeometricRepresentationItem):
    """Wrapper class for IfcFillAreaStyleTiles."""
    TilingPattern: "IfcOneDirectionRepeatFactor"
    Tiles: list["IfcFillAreaStyleTileSymbolWithStyle"]
    TilingScale: float


class IfcGeometricRepresentationSubContext(IfcGeometricRepresentationContext):
    """Wrapper class for IfcGeometricRepresentationSubContext."""
    ParentContext: "IfcGeometricRepresentationContext"
    TargetScale: Optional[float]
    TargetView: "IfcGeometricProjectionEnum"
    UserDefinedTargetView: Optional[str]


class IfcGeometricSet(IfcGeometricRepresentationItem):
    """Wrapper class for IfcGeometricSet."""
    Elements: list[Union["IfcCurve", "IfcPoint", "IfcSurface"]]


class IfcHalfSpaceSolid(IfcGeometricRepresentationItem):
    """Wrapper class for IfcHalfSpaceSolid."""
    BaseSurface: "IfcSurface"
    AgreementFlag: bool


class IfcIShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcIShapeProfileDef."""
    OverallWidth: float
    OverallDepth: float
    WebThickness: float
    FlangeThickness: float
    FilletRadius: Optional[float]


class IfcLShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcLShapeProfileDef."""
    Depth: float
    Width: Optional[float]
    Thickness: float
    FilletRadius: Optional[float]
    EdgeRadius: Optional[float]
    LegSlope: Optional[float]
    CentreOfGravityInX: Optional[float]
    CentreOfGravityInY: Optional[float]


class IfcLightSource(IfcGeometricRepresentationItem):
    """Wrapper class for IfcLightSource."""
    Name: Optional[str]
    LightColour: "IfcColourRgb"
    AmbientIntensity: Optional[float]
    Intensity: Optional[float]


class IfcLoop(IfcTopologicalRepresentationItem):
    """Wrapper class for IfcLoop."""
    ...


class IfcMechanicalConcreteMaterialProperties(IfcMechanicalMaterialProperties):
    """Wrapper class for IfcMechanicalConcreteMaterialProperties."""
    CompressiveStrength: Optional[float]
    MaxAggregateSize: Optional[float]
    AdmixturesDescription: Optional[str]
    Workability: Optional[str]
    ProtectivePoreRatio: Optional[float]
    WaterImpermeability: Optional[str]


class IfcMechanicalSteelMaterialProperties(IfcMechanicalMaterialProperties):
    """Wrapper class for IfcMechanicalSteelMaterialProperties."""
    YieldStress: Optional[float]
    UltimateStress: Optional[float]
    UltimateStrain: Optional[float]
    HardeningModule: Optional[float]
    ProportionalStress: Optional[float]
    PlasticStrain: Optional[float]
    Relaxations: Optional[list["IfcRelaxation"]]


class IfcObject(IfcObjectDefinition):
    """Wrapper class for IfcObject."""
    ObjectType: Optional[str]
    def IsDefinedBy(self) -> tuple["IfcRelDefines", ...]: ...
    @property
    def psetsmap(self) -> object: ...
    @property
    def property_sets(self) -> object: ...
    @property_sets.setter
    def property_sets(self, value) -> None: ...
    @property
    def quantity_sets(self) -> object: ...


class IfcOneDirectionRepeatFactor(IfcGeometricRepresentationItem):
    """Wrapper class for IfcOneDirectionRepeatFactor."""
    RepeatFactor: "IfcVector"


class IfcPath(IfcTopologicalRepresentationItem):
    """Wrapper class for IfcPath."""
    EdgeList: list["IfcOrientedEdge"]


class IfcPlacement(IfcGeometricRepresentationItem):
    """Wrapper class for IfcPlacement."""
    Location: "IfcCartesianPoint"


class IfcPlanarExtent(IfcGeometricRepresentationItem):
    """Wrapper class for IfcPlanarExtent."""
    SizeInX: float
    SizeInY: float


class IfcPoint(IfcGeometricRepresentationItem):
    """Wrapper class for IfcPoint."""
    ...


class IfcPreDefinedDimensionSymbol(IfcPreDefinedSymbol):
    """Wrapper class for IfcPreDefinedDimensionSymbol."""
    ...


class IfcPreDefinedPointMarkerSymbol(IfcPreDefinedSymbol):
    """Wrapper class for IfcPreDefinedPointMarkerSymbol."""
    ...


class IfcPreDefinedTerminatorSymbol(IfcPreDefinedSymbol):
    """Wrapper class for IfcPreDefinedTerminatorSymbol."""
    ...


class IfcPropertyBoundedValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyBoundedValue."""
    UpperBoundValue: Optional[Union[float, list[int], int, list[float], str, bool]]
    LowerBoundValue: Optional[Union[float, list[int], int, list[float], str, bool]]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]


class IfcPropertyEnumeratedValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyEnumeratedValue."""
    EnumerationValues: list[Union[float, list[int], int, list[float], str, bool]]
    EnumerationReference: Optional["IfcPropertyEnumeration"]


class IfcPropertyListValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyListValue."""
    ListValues: list[Union[float, list[int], int, list[float], str, bool]]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]


class IfcPropertyReferenceValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyReferenceValue."""
    UsageName: Optional[str]
    PropertyReference: Union["IfcAddress", "IfcAppliedValue", "IfcCalendarDate", "IfcDateAndTime", "IfcExternalReference", "IfcLocalTime", "IfcMaterial", "IfcMaterialLayer", "IfcMaterialList", "IfcOrganization", "IfcPerson", "IfcPersonAndOrganization", "IfcTimeSeries"]


class IfcPropertySetDefinition(IfcPropertyDefinition):
    """Wrapper class for IfcPropertySetDefinition."""
    def PropertyDefinitionOf(self) -> tuple["IfcRelDefinesByProperties", ...]: ...
    def DefinesType(self) -> tuple["IfcTypeObject", ...]: ...


class IfcPropertySingleValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertySingleValue."""
    NominalValue: Optional[Union[float, list[int], int, list[float], str, bool]]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]


class IfcPropertyTableValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyTableValue."""
    DefiningValues: list[Union[float, list[int], int, list[float], str, bool]]
    DefinedValues: list[Union[float, list[int], int, list[float], str, bool]]
    Expression: Optional[str]
    DefiningUnit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    DefinedUnit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]


class IfcQuantityArea(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityArea."""
    AreaValue: float


class IfcQuantityCount(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityCount."""
    CountValue: float


class IfcQuantityLength(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityLength."""
    LengthValue: float


class IfcQuantityTime(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityTime."""
    TimeValue: float


class IfcQuantityVolume(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityVolume."""
    VolumeValue: float


class IfcQuantityWeight(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityWeight."""
    WeightValue: float


class IfcRectangleProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcRectangleProfileDef."""
    XDim: float
    YDim: float


class IfcRelAssigns(IfcRelationship):
    """Wrapper class for IfcRelAssigns."""
    RelatedObjects: list["IfcObjectDefinition"]
    RelatedObjectsType: Optional["IfcObjectTypeEnum"]


class IfcRelAssociates(IfcRelationship):
    """Wrapper class for IfcRelAssociates."""
    RelatedObjects: list["IfcRoot"]


class IfcRelConnects(IfcRelationship):
    """Wrapper class for IfcRelConnects."""
    ...


class IfcRelDecomposes(IfcRelationship):
    """Wrapper class for IfcRelDecomposes."""
    RelatingObject: "IfcObjectDefinition"
    RelatedObjects: list["IfcObjectDefinition"]


class IfcRelDefines(IfcRelationship):
    """Wrapper class for IfcRelDefines."""
    RelatedObjects: list["IfcObject"]


class IfcSectionedSpine(IfcGeometricRepresentationItem):
    """Wrapper class for IfcSectionedSpine."""
    SpineCurve: "IfcCompositeCurve"
    CrossSections: list["IfcProfileDef"]
    CrossSectionPositions: list["IfcAxis2Placement3D"]


class IfcShapeRepresentation(IfcShapeModel):
    """Wrapper class for IfcShapeRepresentation."""
    ...


class IfcShellBasedSurfaceModel(IfcGeometricRepresentationItem):
    """Wrapper class for IfcShellBasedSurfaceModel."""
    SbsmBoundary: list[Union["IfcClosedShell", "IfcOpenShell"]]


class IfcSolidModel(IfcGeometricRepresentationItem):
    """Wrapper class for IfcSolidModel."""
    ...


class IfcStructuralLoadLinearForce(IfcStructuralLoadStatic):
    """Wrapper class for IfcStructuralLoadLinearForce."""
    LinearForceX: Optional[float]
    LinearForceY: Optional[float]
    LinearForceZ: Optional[float]
    LinearMomentX: Optional[float]
    LinearMomentY: Optional[float]
    LinearMomentZ: Optional[float]


class IfcStructuralLoadPlanarForce(IfcStructuralLoadStatic):
    """Wrapper class for IfcStructuralLoadPlanarForce."""
    PlanarForceX: Optional[float]
    PlanarForceY: Optional[float]
    PlanarForceZ: Optional[float]


class IfcStructuralLoadSingleDisplacement(IfcStructuralLoadStatic):
    """Wrapper class for IfcStructuralLoadSingleDisplacement."""
    DisplacementX: Optional[float]
    DisplacementY: Optional[float]
    DisplacementZ: Optional[float]
    RotationalDisplacementRX: Optional[float]
    RotationalDisplacementRY: Optional[float]
    RotationalDisplacementRZ: Optional[float]


class IfcStructuralLoadSingleForce(IfcStructuralLoadStatic):
    """Wrapper class for IfcStructuralLoadSingleForce."""
    ForceX: Optional[float]
    ForceY: Optional[float]
    ForceZ: Optional[float]
    MomentX: Optional[float]
    MomentY: Optional[float]
    MomentZ: Optional[float]


class IfcStructuralLoadTemperature(IfcStructuralLoadStatic):
    """Wrapper class for IfcStructuralLoadTemperature."""
    DeltaT_Constant: Optional[float]
    DeltaT_Y: Optional[float]
    DeltaT_Z: Optional[float]


class IfcStructuralProfileProperties(IfcGeneralProfileProperties):
    """Wrapper class for IfcStructuralProfileProperties."""
    TorsionalConstantX: Optional[float]
    MomentOfInertiaYZ: Optional[float]
    MomentOfInertiaY: Optional[float]
    MomentOfInertiaZ: Optional[float]
    WarpingConstant: Optional[float]
    ShearCentreZ: Optional[float]
    ShearCentreY: Optional[float]
    ShearDeformationAreaZ: Optional[float]
    ShearDeformationAreaY: Optional[float]
    MaximumSectionModulusY: Optional[float]
    MinimumSectionModulusY: Optional[float]
    MaximumSectionModulusZ: Optional[float]
    MinimumSectionModulusZ: Optional[float]
    TorsionalSectionModulus: Optional[float]
    CentreOfGravityInX: Optional[float]
    CentreOfGravityInY: Optional[float]


class IfcStyledRepresentation(IfcStyleModel):
    """Wrapper class for IfcStyledRepresentation."""
    ...


class IfcSurface(IfcGeometricRepresentationItem):
    """Wrapper class for IfcSurface."""
    ...


class IfcTShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcTShapeProfileDef."""
    Depth: float
    FlangeWidth: float
    WebThickness: float
    FlangeThickness: float
    FilletRadius: Optional[float]
    FlangeEdgeRadius: Optional[float]
    WebEdgeRadius: Optional[float]
    WebSlope: Optional[float]
    FlangeSlope: Optional[float]
    CentreOfGravityInY: Optional[float]


class IfcTextLiteral(IfcGeometricRepresentationItem):
    """Wrapper class for IfcTextLiteral."""
    Literal: str
    Placement: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]
    Path: "IfcTextPath"


class IfcTextStyleFontModel(IfcPreDefinedTextFont):
    """Wrapper class for IfcTextStyleFontModel."""
    FontFamily: Optional[list[str]]
    FontStyle: Optional[str]
    FontVariant: Optional[str]
    FontWeight: Optional[str]
    FontSize: Union[str, float]


class IfcTopologyRepresentation(IfcShapeModel):
    """Wrapper class for IfcTopologyRepresentation."""
    ...


class IfcTrapeziumProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcTrapeziumProfileDef."""
    BottomXDim: float
    TopXDim: float
    YDim: float
    TopXOffset: float


class IfcTypeObject(IfcObjectDefinition):
    """Wrapper class for IfcTypeObject."""
    ApplicableOccurrence: Optional[str]
    HasPropertySets: Optional[list["IfcPropertySetDefinition"]]
    def ObjectTypeOf(self) -> tuple["IfcRelDefinesByType", ...]: ...


class IfcUShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcUShapeProfileDef."""
    Depth: float
    FlangeWidth: float
    WebThickness: float
    FlangeThickness: float
    FilletRadius: Optional[float]
    EdgeRadius: Optional[float]
    FlangeSlope: Optional[float]
    CentreOfGravityInX: Optional[float]


class IfcVector(IfcGeometricRepresentationItem):
    """Wrapper class for IfcVector."""
    Orientation: "IfcDirection"
    Magnitude: float


class IfcVertex(IfcTopologicalRepresentationItem):
    """Wrapper class for IfcVertex."""
    ...


class IfcZShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcZShapeProfileDef."""
    Depth: float
    FlangeWidth: float
    WebThickness: float
    FlangeThickness: float
    FilletRadius: Optional[float]
    EdgeRadius: Optional[float]


class IfcActor(IfcObject):
    """Wrapper class for IfcActor."""
    TheActor: Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]
    def IsActingUpon(self) -> tuple["IfcRelAssignsToActor", ...]: ...


class IfcAnnotationCurveOccurrence(IfcAnnotationOccurrence):
    """Wrapper class for IfcAnnotationCurveOccurrence."""
    ...


class IfcAnnotationFillAreaOccurrence(IfcAnnotationOccurrence):
    """Wrapper class for IfcAnnotationFillAreaOccurrence."""
    FillStyleTarget: Optional["IfcPoint"]
    GlobalOrLocal: Optional["IfcGlobalOrLocalEnum"]


class IfcAnnotationSurfaceOccurrence(IfcAnnotationOccurrence):
    """Wrapper class for IfcAnnotationSurfaceOccurrence."""
    ...


class IfcAnnotationSymbolOccurrence(IfcAnnotationOccurrence):
    """Wrapper class for IfcAnnotationSymbolOccurrence."""
    ...


class IfcAnnotationTextOccurrence(IfcAnnotationOccurrence):
    """Wrapper class for IfcAnnotationTextOccurrence."""
    ...


class IfcAsymmetricIShapeProfileDef(IfcIShapeProfileDef):
    """Wrapper class for IfcAsymmetricIShapeProfileDef."""
    TopFlangeWidth: float
    TopFlangeThickness: Optional[float]
    TopFlangeFilletRadius: Optional[float]
    CentreOfGravityInY: Optional[float]


class IfcAxis1Placement(IfcPlacement):
    """Wrapper class for IfcAxis1Placement."""
    Axis: Optional["IfcDirection"]


class IfcAxis2Placement2D(IfcPlacement):
    """Wrapper class for IfcAxis2Placement2D."""
    RefDirection: Optional["IfcDirection"]


class IfcAxis2Placement3D(IfcPlacement):
    """Wrapper class for IfcAxis2Placement3D."""
    Axis: Optional["IfcDirection"]
    RefDirection: Optional["IfcDirection"]


class IfcBlock(IfcCsgPrimitive3D):
    """Wrapper class for IfcBlock."""
    XLength: float
    YLength: float
    ZLength: float


class IfcBooleanClippingResult(IfcBooleanResult):
    """Wrapper class for IfcBooleanClippingResult."""
    ...


class IfcBoundedCurve(IfcCurve):
    """Wrapper class for IfcBoundedCurve."""
    ...


class IfcBoundedSurface(IfcSurface):
    """Wrapper class for IfcBoundedSurface."""
    ...


class IfcBoxedHalfSpace(IfcHalfSpaceSolid):
    """Wrapper class for IfcBoxedHalfSpace."""
    Enclosure: "IfcBoundingBox"


class IfcCartesianPoint(IfcPoint):
    """Wrapper class for IfcCartesianPoint."""
    Coordinates: list[float]


class IfcCartesianTransformationOperator2D(IfcCartesianTransformationOperator):
    """Wrapper class for IfcCartesianTransformationOperator2D."""
    ...


class IfcCartesianTransformationOperator3D(IfcCartesianTransformationOperator):
    """Wrapper class for IfcCartesianTransformationOperator3D."""
    Axis3: Optional["IfcDirection"]


class IfcCircleHollowProfileDef(IfcCircleProfileDef):
    """Wrapper class for IfcCircleHollowProfileDef."""
    WallThickness: float


class IfcClosedShell(IfcConnectedFaceSet):
    """Wrapper class for IfcClosedShell."""
    ...


class IfcConic(IfcCurve):
    """Wrapper class for IfcConic."""
    Position: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]


class IfcControl(IfcObject):
    """Wrapper class for IfcControl."""
    def Controls(self) -> tuple["IfcRelAssignsToControl", ...]: ...


class IfcCsgSolid(IfcSolidModel):
    """Wrapper class for IfcCsgSolid."""
    TreeRootExpression: Union["IfcBooleanResult", "IfcCsgPrimitive3D"]


class IfcDimensionCurveDirectedCallout(IfcDraughtingCallout):
    """Wrapper class for IfcDimensionCurveDirectedCallout."""
    ...


class IfcDoorLiningProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcDoorLiningProperties."""
    LiningDepth: Optional[float]
    LiningThickness: Optional[float]
    ThresholdDepth: Optional[float]
    ThresholdThickness: Optional[float]
    TransomThickness: Optional[float]
    TransomOffset: Optional[float]
    LiningOffset: Optional[float]
    ThresholdOffset: Optional[float]
    CasingThickness: Optional[float]
    CasingDepth: Optional[float]
    ShapeAspectStyle: Optional["IfcShapeAspect"]


class IfcDoorPanelProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcDoorPanelProperties."""
    PanelDepth: Optional[float]
    PanelOperation: "IfcDoorPanelOperationEnum"
    PanelWidth: Optional[float]
    PanelPosition: "IfcDoorPanelPositionEnum"
    ShapeAspectStyle: Optional["IfcShapeAspect"]


class IfcEdgeCurve(IfcEdge):
    """Wrapper class for IfcEdgeCurve."""
    EdgeGeometry: "IfcCurve"
    SameSense: bool


class IfcEdgeLoop(IfcLoop):
    """Wrapper class for IfcEdgeLoop."""
    EdgeList: list["IfcOrientedEdge"]


class IfcElementQuantity(IfcPropertySetDefinition):
    """Wrapper class for IfcElementQuantity."""
    MethodOfMeasurement: Optional[str]
    Quantities: list["IfcPhysicalQuantity"]


class IfcElementarySurface(IfcSurface):
    """Wrapper class for IfcElementarySurface."""
    Position: "IfcAxis2Placement3D"


class IfcEnergyProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcEnergyProperties."""
    EnergySequence: Optional["IfcEnergySequenceEnum"]
    UserDefinedEnergySequence: Optional[str]


class IfcFaceOuterBound(IfcFaceBound):
    """Wrapper class for IfcFaceOuterBound."""
    ...


class IfcFaceSurface(IfcFace):
    """Wrapper class for IfcFaceSurface."""
    FaceSurface: "IfcSurface"
    SameSense: bool


class IfcFluidFlowProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcFluidFlowProperties."""
    PropertySource: "IfcPropertySourceEnum"
    FlowConditionTimeSeries: Optional["IfcTimeSeries"]
    VelocityTimeSeries: Optional["IfcTimeSeries"]
    FlowrateTimeSeries: Optional["IfcTimeSeries"]
    Fluid: "IfcMaterial"
    PressureTimeSeries: Optional["IfcTimeSeries"]
    UserDefinedPropertySource: Optional[str]
    TemperatureSingleValue: Optional[float]
    WetBulbTemperatureSingleValue: Optional[float]
    WetBulbTemperatureTimeSeries: Optional["IfcTimeSeries"]
    TemperatureTimeSeries: Optional["IfcTimeSeries"]
    FlowrateSingleValue: Optional[Union[float, list[int], int]]
    FlowConditionSingleValue: Optional[float]
    VelocitySingleValue: Optional[float]
    PressureSingleValue: Optional[float]


class IfcGeometricCurveSet(IfcGeometricSet):
    """Wrapper class for IfcGeometricCurveSet."""
    ...


class IfcGroup(IfcObject):
    """Wrapper class for IfcGroup."""
    def IsGroupedBy(self) -> tuple["IfcRelAssignsToGroup", ...]: ...


class IfcLightSourceAmbient(IfcLightSource):
    """Wrapper class for IfcLightSourceAmbient."""
    ...


class IfcLightSourceDirectional(IfcLightSource):
    """Wrapper class for IfcLightSourceDirectional."""
    Orientation: "IfcDirection"


class IfcLightSourceGoniometric(IfcLightSource):
    """Wrapper class for IfcLightSourceGoniometric."""
    Position: "IfcAxis2Placement3D"
    ColourAppearance: Optional["IfcColourRgb"]
    ColourTemperature: float
    LuminousFlux: float
    LightEmissionSource: "IfcLightEmissionSourceEnum"
    LightDistributionDataSource: Union["IfcExternalReference", "IfcLightIntensityDistribution"]


class IfcLightSourcePositional(IfcLightSource):
    """Wrapper class for IfcLightSourcePositional."""
    Position: "IfcCartesianPoint"
    Radius: float
    ConstantAttenuation: float
    DistanceAttenuation: float
    QuadricAttenuation: float


class IfcLine(IfcCurve):
    """Wrapper class for IfcLine."""
    Pnt: "IfcCartesianPoint"
    Dir: "IfcVector"


class IfcManifoldSolidBrep(IfcSolidModel):
    """Wrapper class for IfcManifoldSolidBrep."""
    Outer: "IfcClosedShell"


class IfcOffsetCurve2D(IfcCurve):
    """Wrapper class for IfcOffsetCurve2D."""
    BasisCurve: "IfcCurve"
    Distance: float
    SelfIntersect: bool


class IfcOffsetCurve3D(IfcCurve):
    """Wrapper class for IfcOffsetCurve3D."""
    BasisCurve: "IfcCurve"
    Distance: float
    SelfIntersect: bool
    RefDirection: "IfcDirection"


class IfcOpenShell(IfcConnectedFaceSet):
    """Wrapper class for IfcOpenShell."""
    ...


class IfcOrientedEdge(IfcEdge):
    """Wrapper class for IfcOrientedEdge."""
    EdgeElement: "IfcEdge"
    Orientation: bool


class IfcPermeableCoveringProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcPermeableCoveringProperties."""
    OperationType: "IfcPermeableCoveringOperationEnum"
    PanelPosition: "IfcWindowPanelPositionEnum"
    FrameDepth: Optional[float]
    FrameThickness: Optional[float]
    ShapeAspectStyle: Optional["IfcShapeAspect"]


class IfcPlanarBox(IfcPlanarExtent):
    """Wrapper class for IfcPlanarBox."""
    Placement: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]


class IfcPointOnCurve(IfcPoint):
    """Wrapper class for IfcPointOnCurve."""
    BasisCurve: "IfcCurve"
    PointParameter: float


class IfcPointOnSurface(IfcPoint):
    """Wrapper class for IfcPointOnSurface."""
    BasisSurface: "IfcSurface"
    PointParameterU: float
    PointParameterV: float


class IfcPolyLoop(IfcLoop):
    """Wrapper class for IfcPolyLoop."""
    Polygon: list["IfcCartesianPoint"]


class IfcPolygonalBoundedHalfSpace(IfcHalfSpaceSolid):
    """Wrapper class for IfcPolygonalBoundedHalfSpace."""
    Position: "IfcAxis2Placement3D"
    PolygonalBoundary: "IfcBoundedCurve"


class IfcProcess(IfcObject):
    """Wrapper class for IfcProcess."""
    def OperatesOn(self) -> tuple["IfcRelAssignsToProcess", ...]: ...
    def IsSuccessorFrom(self) -> tuple["IfcRelSequence", ...]: ...
    def IsPredecessorTo(self) -> tuple["IfcRelSequence", ...]: ...


class IfcProduct(IfcObject):
    """Wrapper class for IfcProduct."""
    ObjectPlacement: Optional["IfcObjectPlacement"]
    Representation: Optional["IfcProductRepresentation"]
    def ReferencedBy(self) -> tuple["IfcRelAssignsToProduct", ...]: ...
    @property
    def style(self) -> object: ...
    @property
    def visual_geometry(self) -> object: ...
    @visual_geometry.setter
    def visual_geometry(self, value) -> None: ...
    @property
    def geometry(self) -> object: ...
    @geometry.setter
    def geometry(self, value) -> None: ...
    @property
    def volume(self) -> object: ...
    @property
    def surface_area(self) -> object: ...
    @property
    def axis(self) -> object: ...
    @axis.setter
    def axis(self, value) -> None: ...
    @property
    def frame(self) -> object: ...
    @frame.setter
    def frame(self, value) -> None: ...


class IfcProject(IfcObject):
    """Wrapper class for IfcProject."""
    LongName: Optional[str]
    Phase: Optional[str]
    RepresentationContexts: list["IfcRepresentationContext"]
    UnitsInContext: "IfcUnitAssignment"
    @property
    def sites(self) -> object: ...
    @property
    def buildings(self) -> object: ...
    @property
    def building_elements(self) -> object: ...
    @property
    def geographic_elements(self) -> object: ...
    @property
    def contexts(self) -> object: ...
    @property
    def units(self) -> object: ...
    @property
    def length_unit(self) -> object: ...
    @property
    def length_scale(self) -> object: ...
    @property
    def frame(self) -> object: ...
    @property
    def north(self) -> object: ...


class IfcPropertySet(IfcPropertySetDefinition):
    """Wrapper class for IfcPropertySet."""
    HasProperties: list["IfcProperty"]


class IfcRectangleHollowProfileDef(IfcRectangleProfileDef):
    """Wrapper class for IfcRectangleHollowProfileDef."""
    WallThickness: float
    InnerFilletRadius: Optional[float]
    OuterFilletRadius: Optional[float]


class IfcRectangularPyramid(IfcCsgPrimitive3D):
    """Wrapper class for IfcRectangularPyramid."""
    XLength: float
    YLength: float
    Height: float


class IfcReinforcementDefinitionProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcReinforcementDefinitionProperties."""
    DefinitionType: Optional[str]
    ReinforcementSectionDefinitions: list["IfcSectionReinforcementProperties"]


class IfcRelAggregates(IfcRelDecomposes):
    """Wrapper class for IfcRelAggregates."""
    ...


class IfcRelAssignsToActor(IfcRelAssigns):
    """Wrapper class for IfcRelAssignsToActor."""
    RelatingActor: "IfcActor"
    ActingRole: Optional["IfcActorRole"]


class IfcRelAssignsToControl(IfcRelAssigns):
    """Wrapper class for IfcRelAssignsToControl."""
    RelatingControl: "IfcControl"


class IfcRelAssignsToGroup(IfcRelAssigns):
    """Wrapper class for IfcRelAssignsToGroup."""
    RelatingGroup: "IfcGroup"


class IfcRelAssignsToProcess(IfcRelAssigns):
    """Wrapper class for IfcRelAssignsToProcess."""
    RelatingProcess: "IfcProcess"
    QuantityInProcess: Optional["IfcMeasureWithUnit"]


class IfcRelAssignsToProduct(IfcRelAssigns):
    """Wrapper class for IfcRelAssignsToProduct."""
    RelatingProduct: "IfcProduct"


class IfcRelAssignsToResource(IfcRelAssigns):
    """Wrapper class for IfcRelAssignsToResource."""
    RelatingResource: "IfcResource"


class IfcRelAssociatesAppliedValue(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesAppliedValue."""
    RelatingAppliedValue: "IfcAppliedValue"


class IfcRelAssociatesApproval(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesApproval."""
    RelatingApproval: "IfcApproval"


class IfcRelAssociatesClassification(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesClassification."""
    RelatingClassification: Union["IfcClassificationNotation", "IfcClassificationReference"]


class IfcRelAssociatesConstraint(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesConstraint."""
    Intent: str
    RelatingConstraint: "IfcConstraint"


class IfcRelAssociatesDocument(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesDocument."""
    RelatingDocument: Union["IfcDocumentInformation", "IfcDocumentReference"]


class IfcRelAssociatesLibrary(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesLibrary."""
    RelatingLibrary: Union["IfcLibraryInformation", "IfcLibraryReference"]


class IfcRelAssociatesMaterial(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesMaterial."""
    RelatingMaterial: Union["IfcMaterial", "IfcMaterialLayer", "IfcMaterialLayerSet", "IfcMaterialLayerSetUsage", "IfcMaterialList"]


class IfcRelAssociatesProfileProperties(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesProfileProperties."""
    RelatingProfileProperties: "IfcProfileProperties"
    ProfileSectionLocation: Optional["IfcShapeAspect"]
    ProfileOrientation: Optional[Union["IfcDirection", float]]


class IfcRelConnectsElements(IfcRelConnects):
    """Wrapper class for IfcRelConnectsElements."""
    ConnectionGeometry: Optional["IfcConnectionGeometry"]
    RelatingElement: "IfcElement"
    RelatedElement: "IfcElement"


class IfcRelConnectsPortToElement(IfcRelConnects):
    """Wrapper class for IfcRelConnectsPortToElement."""
    RelatingPort: "IfcPort"
    RelatedElement: "IfcElement"


class IfcRelConnectsPorts(IfcRelConnects):
    """Wrapper class for IfcRelConnectsPorts."""
    RelatingPort: "IfcPort"
    RelatedPort: "IfcPort"
    RealizingElement: Optional["IfcElement"]


class IfcRelConnectsStructuralActivity(IfcRelConnects):
    """Wrapper class for IfcRelConnectsStructuralActivity."""
    RelatingElement: Union["IfcElement", "IfcStructuralItem"]
    RelatedStructuralActivity: "IfcStructuralActivity"


class IfcRelConnectsStructuralElement(IfcRelConnects):
    """Wrapper class for IfcRelConnectsStructuralElement."""
    RelatingElement: "IfcElement"
    RelatedStructuralMember: "IfcStructuralMember"


class IfcRelConnectsStructuralMember(IfcRelConnects):
    """Wrapper class for IfcRelConnectsStructuralMember."""
    RelatingStructuralMember: "IfcStructuralMember"
    RelatedStructuralConnection: "IfcStructuralConnection"
    AppliedCondition: Optional["IfcBoundaryCondition"]
    AdditionalConditions: Optional["IfcStructuralConnectionCondition"]
    SupportedLength: Optional[float]
    ConditionCoordinateSystem: Optional["IfcAxis2Placement3D"]


class IfcRelContainedInSpatialStructure(IfcRelConnects):
    """Wrapper class for IfcRelContainedInSpatialStructure."""
    RelatedElements: list["IfcProduct"]
    RelatingStructure: "IfcSpatialStructureElement"


class IfcRelCoversBldgElements(IfcRelConnects):
    """Wrapper class for IfcRelCoversBldgElements."""
    RelatingBuildingElement: "IfcElement"
    RelatedCoverings: list["IfcCovering"]


class IfcRelCoversSpaces(IfcRelConnects):
    """Wrapper class for IfcRelCoversSpaces."""
    RelatedSpace: "IfcSpace"
    RelatedCoverings: list["IfcCovering"]


class IfcRelDefinesByProperties(IfcRelDefines):
    """Wrapper class for IfcRelDefinesByProperties."""
    RelatingPropertyDefinition: "IfcPropertySetDefinition"


class IfcRelDefinesByType(IfcRelDefines):
    """Wrapper class for IfcRelDefinesByType."""
    RelatingType: "IfcTypeObject"


class IfcRelFillsElement(IfcRelConnects):
    """Wrapper class for IfcRelFillsElement."""
    RelatingOpeningElement: "IfcOpeningElement"
    RelatedBuildingElement: "IfcElement"


class IfcRelFlowControlElements(IfcRelConnects):
    """Wrapper class for IfcRelFlowControlElements."""
    RelatedControlElements: list["IfcDistributionControlElement"]
    RelatingFlowElement: "IfcDistributionFlowElement"


class IfcRelInteractionRequirements(IfcRelConnects):
    """Wrapper class for IfcRelInteractionRequirements."""
    DailyInteraction: Optional[float]
    ImportanceRating: Optional[float]
    LocationOfInteraction: Optional["IfcSpatialStructureElement"]
    RelatedSpaceProgram: "IfcSpaceProgram"
    RelatingSpaceProgram: "IfcSpaceProgram"


class IfcRelNests(IfcRelDecomposes):
    """Wrapper class for IfcRelNests."""
    ...


class IfcRelProjectsElement(IfcRelConnects):
    """Wrapper class for IfcRelProjectsElement."""
    RelatingElement: "IfcElement"
    RelatedFeatureElement: "IfcFeatureElementAddition"


class IfcRelReferencedInSpatialStructure(IfcRelConnects):
    """Wrapper class for IfcRelReferencedInSpatialStructure."""
    RelatedElements: list["IfcProduct"]
    RelatingStructure: "IfcSpatialStructureElement"


class IfcRelSequence(IfcRelConnects):
    """Wrapper class for IfcRelSequence."""
    RelatingProcess: "IfcProcess"
    RelatedProcess: "IfcProcess"
    TimeLag: float
    SequenceType: "IfcSequenceEnum"


class IfcRelServicesBuildings(IfcRelConnects):
    """Wrapper class for IfcRelServicesBuildings."""
    RelatingSystem: "IfcSystem"
    RelatedBuildings: list["IfcSpatialStructureElement"]


class IfcRelSpaceBoundary(IfcRelConnects):
    """Wrapper class for IfcRelSpaceBoundary."""
    RelatingSpace: "IfcSpace"
    RelatedBuildingElement: Optional["IfcElement"]
    ConnectionGeometry: Optional["IfcConnectionGeometry"]
    PhysicalOrVirtualBoundary: "IfcPhysicalOrVirtualEnum"
    InternalOrExternalBoundary: "IfcInternalOrExternalEnum"


class IfcRelVoidsElement(IfcRelConnects):
    """Wrapper class for IfcRelVoidsElement."""
    RelatingBuildingElement: "IfcElement"
    RelatedOpeningElement: "IfcFeatureElementSubtraction"


class IfcResource(IfcObject):
    """Wrapper class for IfcResource."""
    def ResourceOf(self) -> tuple["IfcRelAssignsToResource", ...]: ...


class IfcRightCircularCone(IfcCsgPrimitive3D):
    """Wrapper class for IfcRightCircularCone."""
    Height: float
    BottomRadius: float


class IfcRightCircularCylinder(IfcCsgPrimitive3D):
    """Wrapper class for IfcRightCircularCylinder."""
    Height: float
    Radius: float


class IfcRoundedRectangleProfileDef(IfcRectangleProfileDef):
    """Wrapper class for IfcRoundedRectangleProfileDef."""
    RoundingRadius: float


class IfcServiceLifeFactor(IfcPropertySetDefinition):
    """Wrapper class for IfcServiceLifeFactor."""
    PredefinedType: "IfcServiceLifeFactorTypeEnum"
    UpperValue: Optional[Union[float, list[float], str]]
    MostUsedValue: Union[float, list[float], str]
    LowerValue: Optional[Union[float, list[float], str]]


class IfcSoundProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcSoundProperties."""
    IsAttenuating: bool
    SoundScale: Optional["IfcSoundScaleEnum"]
    SoundValues: list["IfcSoundValue"]


class IfcSoundValue(IfcPropertySetDefinition):
    """Wrapper class for IfcSoundValue."""
    SoundLevelTimeSeries: Optional["IfcTimeSeries"]
    Frequency: float
    SoundLevelSingleValue: Optional[Union[float, list[int], int]]


class IfcSpaceThermalLoadProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcSpaceThermalLoadProperties."""
    ApplicableValueRatio: Optional[float]
    ThermalLoadSource: "IfcThermalLoadSourceEnum"
    PropertySource: "IfcPropertySourceEnum"
    SourceDescription: Optional[str]
    MaximumValue: float
    MinimumValue: Optional[float]
    ThermalLoadTimeSeriesValues: Optional["IfcTimeSeries"]
    UserDefinedThermalLoadSource: Optional[str]
    UserDefinedPropertySource: Optional[str]
    ThermalLoadType: "IfcThermalLoadTypeEnum"


class IfcSphere(IfcCsgPrimitive3D):
    """Wrapper class for IfcSphere."""
    Radius: float


class IfcStructuralLoadSingleDisplacementDistortion(IfcStructuralLoadSingleDisplacement):
    """Wrapper class for IfcStructuralLoadSingleDisplacementDistortion."""
    Distortion: Optional[float]


class IfcStructuralLoadSingleForceWarping(IfcStructuralLoadSingleForce):
    """Wrapper class for IfcStructuralLoadSingleForceWarping."""
    WarpingMoment: Optional[float]


class IfcStructuralSteelProfileProperties(IfcStructuralProfileProperties):
    """Wrapper class for IfcStructuralSteelProfileProperties."""
    ShearAreaZ: Optional[float]
    ShearAreaY: Optional[float]
    PlasticShapeFactorY: Optional[float]
    PlasticShapeFactorZ: Optional[float]


class IfcStructuredDimensionCallout(IfcDraughtingCallout):
    """Wrapper class for IfcStructuredDimensionCallout."""
    ...


class IfcSubedge(IfcEdge):
    """Wrapper class for IfcSubedge."""
    ParentEdge: "IfcEdge"


class IfcSweptAreaSolid(IfcSolidModel):
    """Wrapper class for IfcSweptAreaSolid."""
    SweptArea: "IfcProfileDef"
    Position: "IfcAxis2Placement3D"


class IfcSweptDiskSolid(IfcSolidModel):
    """Wrapper class for IfcSweptDiskSolid."""
    Directrix: "IfcCurve"
    Radius: float
    InnerRadius: Optional[float]
    StartParam: float
    EndParam: float


class IfcSweptSurface(IfcSurface):
    """Wrapper class for IfcSweptSurface."""
    SweptCurve: "IfcProfileDef"
    Position: "IfcAxis2Placement3D"


class IfcTextLiteralWithExtent(IfcTextLiteral):
    """Wrapper class for IfcTextLiteralWithExtent."""
    Extent: "IfcPlanarExtent"
    BoxAlignment: str


class IfcTwoDirectionRepeatFactor(IfcOneDirectionRepeatFactor):
    """Wrapper class for IfcTwoDirectionRepeatFactor."""
    SecondRepeatFactor: "IfcVector"


class IfcTypeProduct(IfcTypeObject):
    """Wrapper class for IfcTypeProduct."""
    RepresentationMaps: Optional[list["IfcRepresentationMap"]]
    Tag: Optional[str]


class IfcVertexLoop(IfcLoop):
    """Wrapper class for IfcVertexLoop."""
    LoopVertex: "IfcVertex"


class IfcVertexPoint(IfcVertex):
    """Wrapper class for IfcVertexPoint."""
    VertexGeometry: "IfcPoint"


class IfcWindowLiningProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcWindowLiningProperties."""
    LiningDepth: Optional[float]
    LiningThickness: Optional[float]
    TransomThickness: Optional[float]
    MullionThickness: Optional[float]
    FirstTransomOffset: Optional[float]
    SecondTransomOffset: Optional[float]
    FirstMullionOffset: Optional[float]
    SecondMullionOffset: Optional[float]
    ShapeAspectStyle: Optional["IfcShapeAspect"]


class IfcWindowPanelProperties(IfcPropertySetDefinition):
    """Wrapper class for IfcWindowPanelProperties."""
    OperationType: "IfcWindowPanelOperationEnum"
    PanelPosition: "IfcWindowPanelPositionEnum"
    FrameDepth: Optional[float]
    FrameThickness: Optional[float]
    ShapeAspectStyle: Optional["IfcShapeAspect"]


class IfcActionRequest(IfcControl):
    """Wrapper class for IfcActionRequest."""
    RequestID: str


class IfcAngularDimension(IfcDimensionCurveDirectedCallout):
    """Wrapper class for IfcAngularDimension."""
    ...


class IfcAnnotation(IfcProduct):
    """Wrapper class for IfcAnnotation."""
    def ContainedInStructure(self) -> tuple["IfcRelContainedInSpatialStructure", ...]: ...


class IfcAsset(IfcGroup):
    """Wrapper class for IfcAsset."""
    AssetID: str
    OriginalValue: "IfcCostValue"
    CurrentValue: "IfcCostValue"
    TotalReplacementCost: "IfcCostValue"
    Owner: Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]
    User: Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]
    ResponsiblePerson: "IfcPerson"
    IncorporationDate: "IfcCalendarDate"
    DepreciatedValue: "IfcCostValue"


class IfcBSplineCurve(IfcBoundedCurve):
    """Wrapper class for IfcBSplineCurve."""
    Degree: int
    ControlPointsList: list["IfcCartesianPoint"]
    CurveForm: "IfcBSplineCurveForm"
    ClosedCurve: bool
    SelfIntersect: bool


class IfcCartesianTransformationOperator2DnonUniform(IfcCartesianTransformationOperator2D):
    """Wrapper class for IfcCartesianTransformationOperator2DnonUniform."""
    Scale2: Optional[float]


class IfcCartesianTransformationOperator3DnonUniform(IfcCartesianTransformationOperator3D):
    """Wrapper class for IfcCartesianTransformationOperator3DnonUniform."""
    Scale2: Optional[float]
    Scale3: Optional[float]


class IfcCircle(IfcConic):
    """Wrapper class for IfcCircle."""
    Radius: float


class IfcCompositeCurve(IfcBoundedCurve):
    """Wrapper class for IfcCompositeCurve."""
    Segments: list["IfcCompositeCurveSegment"]
    SelfIntersect: bool


class IfcCondition(IfcGroup):
    """Wrapper class for IfcCondition."""
    ...


class IfcConditionCriterion(IfcControl):
    """Wrapper class for IfcConditionCriterion."""
    Criterion: Union[str, "IfcMeasureWithUnit"]
    CriterionDateTime: Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]


class IfcConstructionResource(IfcResource):
    """Wrapper class for IfcConstructionResource."""
    ResourceIdentifier: Optional[str]
    ResourceGroup: Optional[str]
    ResourceConsumption: Optional["IfcResourceConsumptionEnum"]
    BaseQuantity: Optional["IfcMeasureWithUnit"]


class IfcCostItem(IfcControl):
    """Wrapper class for IfcCostItem."""
    ...


class IfcCostSchedule(IfcControl):
    """Wrapper class for IfcCostSchedule."""
    SubmittedBy: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    PreparedBy: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    SubmittedOn: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    Status: Optional[str]
    TargetUsers: Optional[list[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]]
    UpdateDate: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    ID: str
    PredefinedType: "IfcCostScheduleTypeEnum"


class IfcCurveBoundedPlane(IfcBoundedSurface):
    """Wrapper class for IfcCurveBoundedPlane."""
    BasisSurface: "IfcPlane"
    OuterBoundary: "IfcCurve"
    InnerBoundaries: list["IfcCurve"]


class IfcDiameterDimension(IfcDimensionCurveDirectedCallout):
    """Wrapper class for IfcDiameterDimension."""
    ...


class IfcDimensionCurve(IfcAnnotationCurveOccurrence):
    """Wrapper class for IfcDimensionCurve."""
    def AnnotatedBySymbols(self) -> tuple["IfcTerminatorSymbol", ...]: ...


class IfcDoorStyle(IfcTypeProduct):
    """Wrapper class for IfcDoorStyle."""
    OperationType: "IfcDoorStyleOperationEnum"
    ConstructionType: "IfcDoorStyleConstructionEnum"
    ParameterTakesPrecedence: bool
    Sizeable: bool


class IfcElectricalBaseProperties(IfcEnergyProperties):
    """Wrapper class for IfcElectricalBaseProperties."""
    ElectricCurrentType: Optional["IfcElectricCurrentEnum"]
    InputVoltage: float
    InputFrequency: float
    FullLoadCurrent: Optional[float]
    MinimumCircuitCurrent: Optional[float]
    MaximumPowerInput: Optional[float]
    RatedPowerInput: Optional[float]
    InputPhase: int


class IfcElement(IfcProduct):
    """Wrapper class for IfcElement."""
    Tag: Optional[str]
    def HasStructuralMember(self) -> tuple["IfcRelConnectsStructuralElement", ...]: ...
    def FillsVoids(self) -> tuple["IfcRelFillsElement", ...]: ...
    def ConnectedTo(self) -> tuple["IfcRelConnectsElements", ...]: ...
    def HasCoverings(self) -> tuple["IfcRelCoversBldgElements", ...]: ...
    def HasProjections(self) -> tuple["IfcRelProjectsElement", ...]: ...
    def ReferencedInStructures(self) -> tuple["IfcRelReferencedInSpatialStructure", ...]: ...
    def HasPorts(self) -> tuple["IfcRelConnectsPortToElement", ...]: ...
    def HasOpenings(self) -> tuple["IfcRelVoidsElement", ...]: ...
    def IsConnectionRealization(self) -> tuple["IfcRelConnectsWithRealizingElements", ...]: ...
    def ProvidesBoundaries(self) -> tuple["IfcRelSpaceBoundary", ...]: ...
    def ConnectedFrom(self) -> tuple["IfcRelConnectsElements", ...]: ...
    def ContainedInStructure(self) -> tuple["IfcRelContainedInSpatialStructure", ...]: ...
    @property
    def parent(self) -> object: ...


class IfcElementType(IfcTypeProduct):
    """Wrapper class for IfcElementType."""
    ElementType: Optional[str]


class IfcEllipse(IfcConic):
    """Wrapper class for IfcEllipse."""
    SemiAxis1: float
    SemiAxis2: float


class IfcEquipmentStandard(IfcControl):
    """Wrapper class for IfcEquipmentStandard."""
    ...


class IfcExtrudedAreaSolid(IfcSweptAreaSolid):
    """Wrapper class for IfcExtrudedAreaSolid."""
    ExtrudedDirection: "IfcDirection"
    Depth: float


class IfcFacetedBrep(IfcManifoldSolidBrep):
    """Wrapper class for IfcFacetedBrep."""
    ...


class IfcFacetedBrepWithVoids(IfcManifoldSolidBrep):
    """Wrapper class for IfcFacetedBrepWithVoids."""
    Voids: list["IfcClosedShell"]


class IfcFurnitureStandard(IfcControl):
    """Wrapper class for IfcFurnitureStandard."""
    ...


class IfcGrid(IfcProduct):
    """Wrapper class for IfcGrid."""
    UAxes: list["IfcGridAxis"]
    VAxes: list["IfcGridAxis"]
    WAxes: Optional[list["IfcGridAxis"]]
    def ContainedInStructure(self) -> tuple["IfcRelContainedInSpatialStructure", ...]: ...


class IfcInventory(IfcGroup):
    """Wrapper class for IfcInventory."""
    InventoryType: "IfcInventoryTypeEnum"
    Jurisdiction: Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]
    ResponsiblePersons: list["IfcPerson"]
    LastUpdateDate: "IfcCalendarDate"
    CurrentValue: Optional["IfcCostValue"]
    OriginalValue: Optional["IfcCostValue"]


class IfcLightSourceSpot(IfcLightSourcePositional):
    """Wrapper class for IfcLightSourceSpot."""
    Orientation: "IfcDirection"
    ConcentrationExponent: Optional[float]
    SpreadAngle: float
    BeamWidthAngle: float


class IfcLinearDimension(IfcDimensionCurveDirectedCallout):
    """Wrapper class for IfcLinearDimension."""
    ...


class IfcOccupant(IfcActor):
    """Wrapper class for IfcOccupant."""
    PredefinedType: "IfcOccupantTypeEnum"


class IfcPerformanceHistory(IfcControl):
    """Wrapper class for IfcPerformanceHistory."""
    LifeCyclePhase: str


class IfcPermit(IfcControl):
    """Wrapper class for IfcPermit."""
    PermitID: str


class IfcPlane(IfcElementarySurface):
    """Wrapper class for IfcPlane."""
    ...


class IfcPolyline(IfcBoundedCurve):
    """Wrapper class for IfcPolyline."""
    Points: list["IfcCartesianPoint"]


class IfcPort(IfcProduct):
    """Wrapper class for IfcPort."""
    def ContainedIn(self) -> tuple["IfcRelConnectsPortToElement", ...]: ...
    def ConnectedFrom(self) -> tuple["IfcRelConnectsPorts", ...]: ...
    def ConnectedTo(self) -> tuple["IfcRelConnectsPorts", ...]: ...


class IfcProcedure(IfcProcess):
    """Wrapper class for IfcProcedure."""
    ProcedureID: str
    ProcedureType: "IfcProcedureTypeEnum"
    UserDefinedProcedureType: Optional[str]


class IfcProjectOrder(IfcControl):
    """Wrapper class for IfcProjectOrder."""
    ID: str
    PredefinedType: "IfcProjectOrderTypeEnum"
    Status: Optional[str]


class IfcProjectOrderRecord(IfcControl):
    """Wrapper class for IfcProjectOrderRecord."""
    Records: list["IfcRelAssignsToProjectOrder"]
    PredefinedType: "IfcProjectOrderRecordTypeEnum"


class IfcProjectionCurve(IfcAnnotationCurveOccurrence):
    """Wrapper class for IfcProjectionCurve."""
    ...


class IfcProxy(IfcProduct):
    """Wrapper class for IfcProxy."""
    ProxyType: "IfcObjectTypeEnum"
    Tag: Optional[str]


class IfcRadiusDimension(IfcDimensionCurveDirectedCallout):
    """Wrapper class for IfcRadiusDimension."""
    ...


class IfcRectangularTrimmedSurface(IfcBoundedSurface):
    """Wrapper class for IfcRectangularTrimmedSurface."""
    BasisSurface: "IfcSurface"
    U1: float
    V1: float
    U2: float
    V2: float
    Usense: bool
    Vsense: bool


class IfcRelAssignsTasks(IfcRelAssignsToControl):
    """Wrapper class for IfcRelAssignsTasks."""
    TimeForTask: Optional["IfcScheduleTimeControl"]


class IfcRelAssignsToProjectOrder(IfcRelAssignsToControl):
    """Wrapper class for IfcRelAssignsToProjectOrder."""
    ...


class IfcRelConnectsPathElements(IfcRelConnectsElements):
    """Wrapper class for IfcRelConnectsPathElements."""
    RelatingPriorities: list[int]
    RelatedPriorities: list[int]
    RelatedConnectionType: "IfcConnectionTypeEnum"
    RelatingConnectionType: "IfcConnectionTypeEnum"


class IfcRelConnectsWithEccentricity(IfcRelConnectsStructuralMember):
    """Wrapper class for IfcRelConnectsWithEccentricity."""
    ConnectionConstraint: "IfcConnectionGeometry"


class IfcRelConnectsWithRealizingElements(IfcRelConnectsElements):
    """Wrapper class for IfcRelConnectsWithRealizingElements."""
    RealizingElements: list["IfcElement"]
    ConnectionType: Optional[str]


class IfcRelOccupiesSpaces(IfcRelAssignsToActor):
    """Wrapper class for IfcRelOccupiesSpaces."""
    ...


class IfcRelOverridesProperties(IfcRelDefinesByProperties):
    """Wrapper class for IfcRelOverridesProperties."""
    OverridingProperties: list["IfcProperty"]


class IfcRelSchedulesCostItems(IfcRelAssignsToControl):
    """Wrapper class for IfcRelSchedulesCostItems."""
    ...


class IfcRevolvedAreaSolid(IfcSweptAreaSolid):
    """Wrapper class for IfcRevolvedAreaSolid."""
    Axis: "IfcAxis1Placement"
    Angle: float


class IfcScheduleTimeControl(IfcControl):
    """Wrapper class for IfcScheduleTimeControl."""
    ActualStart: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    EarlyStart: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    LateStart: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    ScheduleStart: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    ActualFinish: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    EarlyFinish: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    LateFinish: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    ScheduleFinish: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    ScheduleDuration: Optional[float]
    ActualDuration: Optional[float]
    RemainingTime: Optional[float]
    FreeFloat: Optional[float]
    TotalFloat: Optional[float]
    IsCritical: Optional[bool]
    StatusTime: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    StartFloat: Optional[float]
    FinishFloat: Optional[float]
    Completion: Optional[float]
    def ScheduleTimeControlAssigned(self) -> tuple["IfcRelAssignsTasks", ...]: ...


class IfcServiceLife(IfcControl):
    """Wrapper class for IfcServiceLife."""
    ServiceLifeType: "IfcServiceLifeTypeEnum"
    ServiceLifeDuration: float


class IfcSpaceProgram(IfcControl):
    """Wrapper class for IfcSpaceProgram."""
    SpaceProgramIdentifier: str
    MaxRequiredArea: Optional[float]
    MinRequiredArea: Optional[float]
    RequestedLocation: Optional["IfcSpatialStructureElement"]
    StandardRequiredArea: float
    def HasInteractionReqsFrom(self) -> tuple["IfcRelInteractionRequirements", ...]: ...
    def HasInteractionReqsTo(self) -> tuple["IfcRelInteractionRequirements", ...]: ...


class IfcSpatialStructureElement(IfcProduct):
    """Wrapper class for IfcSpatialStructureElement."""
    LongName: Optional[str]
    CompositionType: "IfcElementCompositionEnum"
    def ReferencesElements(self) -> tuple["IfcRelReferencedInSpatialStructure", ...]: ...
    def ServicedBySystems(self) -> tuple["IfcRelServicesBuildings", ...]: ...
    def ContainsElements(self) -> tuple["IfcRelContainedInSpatialStructure", ...]: ...
    @property
    def children(self) -> object: ...


class IfcStructuralActivity(IfcProduct):
    """Wrapper class for IfcStructuralActivity."""
    AppliedLoad: "IfcStructuralLoad"
    GlobalOrLocal: "IfcGlobalOrLocalEnum"
    def AssignedToStructuralItem(self) -> tuple["IfcRelConnectsStructuralActivity", ...]: ...


class IfcStructuralItem(IfcProduct):
    """Wrapper class for IfcStructuralItem."""
    def AssignedStructuralActivity(self) -> tuple["IfcRelConnectsStructuralActivity", ...]: ...


class IfcStructuralLoadGroup(IfcGroup):
    """Wrapper class for IfcStructuralLoadGroup."""
    PredefinedType: "IfcLoadGroupTypeEnum"
    ActionType: "IfcActionTypeEnum"
    ActionSource: "IfcActionSourceTypeEnum"
    Coefficient: Optional[float]
    Purpose: Optional[str]
    def SourceOfResultGroup(self) -> tuple["IfcStructuralResultGroup", ...]: ...
    def LoadGroupFor(self) -> tuple["IfcStructuralAnalysisModel", ...]: ...


class IfcStructuralResultGroup(IfcGroup):
    """Wrapper class for IfcStructuralResultGroup."""
    TheoryType: "IfcAnalysisTheoryTypeEnum"
    ResultForLoadGroup: Optional["IfcStructuralLoadGroup"]
    IsLinear: bool
    def ResultGroupFor(self) -> tuple["IfcStructuralAnalysisModel", ...]: ...


class IfcSurfaceCurveSweptAreaSolid(IfcSweptAreaSolid):
    """Wrapper class for IfcSurfaceCurveSweptAreaSolid."""
    Directrix: "IfcCurve"
    StartParam: float
    EndParam: float
    ReferenceSurface: "IfcSurface"


class IfcSurfaceOfLinearExtrusion(IfcSweptSurface):
    """Wrapper class for IfcSurfaceOfLinearExtrusion."""
    ExtrudedDirection: "IfcDirection"
    Depth: float


class IfcSurfaceOfRevolution(IfcSweptSurface):
    """Wrapper class for IfcSurfaceOfRevolution."""
    AxisPosition: "IfcAxis1Placement"


class IfcSystem(IfcGroup):
    """Wrapper class for IfcSystem."""
    def ServicesBuildings(self) -> tuple["IfcRelServicesBuildings", ...]: ...


class IfcTask(IfcProcess):
    """Wrapper class for IfcTask."""
    TaskId: str
    Status: Optional[str]
    WorkMethod: Optional[str]
    IsMilestone: bool
    Priority: Optional[int]


class IfcTerminatorSymbol(IfcAnnotationSymbolOccurrence):
    """Wrapper class for IfcTerminatorSymbol."""
    AnnotatedCurve: "IfcAnnotationCurveOccurrence"


class IfcTimeSeriesSchedule(IfcControl):
    """Wrapper class for IfcTimeSeriesSchedule."""
    ApplicableDates: Optional[list[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]]
    TimeSeriesScheduleType: "IfcTimeSeriesScheduleTypeEnum"
    TimeSeries: "IfcTimeSeries"


class IfcTrimmedCurve(IfcBoundedCurve):
    """Wrapper class for IfcTrimmedCurve."""
    BasisCurve: "IfcCurve"
    Trim1: list[Union["IfcCartesianPoint", float]]
    Trim2: list[Union["IfcCartesianPoint", float]]
    SenseAgreement: bool
    MasterRepresentation: "IfcTrimmingPreference"


class IfcWindowStyle(IfcTypeProduct):
    """Wrapper class for IfcWindowStyle."""
    ConstructionType: "IfcWindowStyleConstructionEnum"
    OperationType: "IfcWindowStyleOperationEnum"
    ParameterTakesPrecedence: bool
    Sizeable: bool


class IfcWorkControl(IfcControl):
    """Wrapper class for IfcWorkControl."""
    Identifier: str
    CreationDate: Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]
    Creators: Optional[list["IfcPerson"]]
    Purpose: Optional[str]
    Duration: Optional[float]
    TotalFloat: Optional[float]
    StartTime: Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]
    FinishTime: Optional[Union["IfcCalendarDate", "IfcDateAndTime", "IfcLocalTime"]]
    WorkControlType: Optional["IfcWorkControlTypeEnum"]
    UserDefinedControlType: Optional[str]


class IfcZone(IfcGroup):
    """Wrapper class for IfcZone."""
    ...


class Ifc2DCompositeCurve(IfcCompositeCurve):
    """Wrapper class for Ifc2DCompositeCurve."""
    ...


class IfcBezierCurve(IfcBSplineCurve):
    """Wrapper class for IfcBezierCurve."""
    ...


class IfcBuilding(IfcSpatialStructureElement):
    """Wrapper class for IfcBuilding."""
    ElevationOfRefHeight: Optional[float]
    ElevationOfTerrain: Optional[float]
    BuildingAddress: Optional["IfcPostalAddress"]
    @property
    def building_elements(self) -> list: ...
    @property
    def geographic_elements(self) -> list: ...
    @property
    def storeys(self) -> list: ...


class IfcBuildingElement(IfcElement):
    """Wrapper class for IfcBuildingElement."""
    ...


class IfcBuildingElementType(IfcElementType):
    """Wrapper class for IfcBuildingElementType."""
    ...


class IfcBuildingStorey(IfcSpatialStructureElement):
    """Wrapper class for IfcBuildingStorey."""
    Elevation: Optional[float]


class IfcConstructionEquipmentResource(IfcConstructionResource):
    """Wrapper class for IfcConstructionEquipmentResource."""
    ...


class IfcConstructionMaterialResource(IfcConstructionResource):
    """Wrapper class for IfcConstructionMaterialResource."""
    Suppliers: Optional[list[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]]
    UsageRatio: Optional[float]


class IfcConstructionProductResource(IfcConstructionResource):
    """Wrapper class for IfcConstructionProductResource."""
    ...


class IfcCrewResource(IfcConstructionResource):
    """Wrapper class for IfcCrewResource."""
    ...


class IfcDimensionCurveTerminator(IfcTerminatorSymbol):
    """Wrapper class for IfcDimensionCurveTerminator."""
    Role: "IfcDimensionExtentUsage"


class IfcDistributionElement(IfcElement):
    """Wrapper class for IfcDistributionElement."""
    ...


class IfcDistributionElementType(IfcElementType):
    """Wrapper class for IfcDistributionElementType."""
    ...


class IfcDistributionPort(IfcPort):
    """Wrapper class for IfcDistributionPort."""
    FlowDirection: Optional["IfcFlowDirectionEnum"]


class IfcElectricalCircuit(IfcSystem):
    """Wrapper class for IfcElectricalCircuit."""
    ...


class IfcElectricalElement(IfcElement):
    """Wrapper class for IfcElectricalElement."""
    ...


class IfcElementAssembly(IfcElement):
    """Wrapper class for IfcElementAssembly."""
    AssemblyPlace: Optional["IfcAssemblyPlaceEnum"]
    PredefinedType: "IfcElementAssemblyTypeEnum"


class IfcElementComponent(IfcElement):
    """Wrapper class for IfcElementComponent."""
    ...


class IfcElementComponentType(IfcElementType):
    """Wrapper class for IfcElementComponentType."""
    ...


class IfcEquipmentElement(IfcElement):
    """Wrapper class for IfcEquipmentElement."""
    ...


class IfcFeatureElement(IfcElement):
    """Wrapper class for IfcFeatureElement."""
    ...


class IfcFurnishingElement(IfcElement):
    """Wrapper class for IfcFurnishingElement."""
    ...


class IfcFurnishingElementType(IfcElementType):
    """Wrapper class for IfcFurnishingElementType."""
    ...


class IfcLaborResource(IfcConstructionResource):
    """Wrapper class for IfcLaborResource."""
    SkillSet: Optional[str]


class IfcMove(IfcTask):
    """Wrapper class for IfcMove."""
    MoveFrom: "IfcSpatialStructureElement"
    MoveTo: "IfcSpatialStructureElement"
    PunchList: Optional[list[str]]


class IfcOrderAction(IfcTask):
    """Wrapper class for IfcOrderAction."""
    ActionID: str


class IfcSite(IfcSpatialStructureElement):
    """Wrapper class for IfcSite."""
    RefLatitude: Optional[list[int]]
    RefLongitude: Optional[list[int]]
    RefElevation: Optional[float]
    LandTitleNumber: Optional[str]
    SiteAddress: Optional["IfcPostalAddress"]
    @property
    def buildings(self) -> object: ...
    @property
    def building_elements(self) -> object: ...
    @property
    def geographic_elements(self) -> object: ...
    @property
    def location(self) -> object: ...


class IfcSpace(IfcSpatialStructureElement):
    """Wrapper class for IfcSpace."""
    InteriorOrExteriorSpace: "IfcInternalOrExternalEnum"
    ElevationWithFlooring: Optional[float]
    def HasCoverings(self) -> tuple["IfcRelCoversSpaces", ...]: ...
    def BoundedBy(self) -> tuple["IfcRelSpaceBoundary", ...]: ...


class IfcSpatialStructureElementType(IfcElementType):
    """Wrapper class for IfcSpatialStructureElementType."""
    ...


class IfcStructuralAction(IfcStructuralActivity):
    """Wrapper class for IfcStructuralAction."""
    DestabilizingLoad: bool
    CausedBy: Optional["IfcStructuralReaction"]


class IfcStructuralAnalysisModel(IfcSystem):
    """Wrapper class for IfcStructuralAnalysisModel."""
    PredefinedType: "IfcAnalysisModelTypeEnum"
    OrientationOf2DPlane: Optional["IfcAxis2Placement3D"]
    LoadedBy: Optional[list["IfcStructuralLoadGroup"]]
    HasResults: Optional[list["IfcStructuralResultGroup"]]


class IfcStructuralConnection(IfcStructuralItem):
    """Wrapper class for IfcStructuralConnection."""
    AppliedCondition: Optional["IfcBoundaryCondition"]
    def ConnectsStructuralMembers(self) -> tuple["IfcRelConnectsStructuralMember", ...]: ...


class IfcStructuralMember(IfcStructuralItem):
    """Wrapper class for IfcStructuralMember."""
    def ReferencesElement(self) -> tuple["IfcRelConnectsStructuralElement", ...]: ...
    def ConnectedBy(self) -> tuple["IfcRelConnectsStructuralMember", ...]: ...


class IfcStructuralReaction(IfcStructuralActivity):
    """Wrapper class for IfcStructuralReaction."""
    def Causes(self) -> tuple["IfcStructuralAction", ...]: ...


class IfcSubContractResource(IfcConstructionResource):
    """Wrapper class for IfcSubContractResource."""
    SubContractor: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    JobDescription: Optional[str]


class IfcTransportElement(IfcElement):
    """Wrapper class for IfcTransportElement."""
    OperationType: Optional["IfcTransportElementTypeEnum"]
    CapacityByWeight: Optional[float]
    CapacityByNumber: Optional[float]


class IfcTransportElementType(IfcElementType):
    """Wrapper class for IfcTransportElementType."""
    PredefinedType: "IfcTransportElementTypeEnum"


class IfcVirtualElement(IfcElement):
    """Wrapper class for IfcVirtualElement."""
    ...


class IfcWorkPlan(IfcWorkControl):
    """Wrapper class for IfcWorkPlan."""
    ...


class IfcWorkSchedule(IfcWorkControl):
    """Wrapper class for IfcWorkSchedule."""
    ...


class IfcBeam(IfcBuildingElement):
    """Wrapper class for IfcBeam."""
    ...


class IfcBeamType(IfcBuildingElementType):
    """Wrapper class for IfcBeamType."""
    PredefinedType: "IfcBeamTypeEnum"


class IfcBuildingElementComponent(IfcBuildingElement):
    """Wrapper class for IfcBuildingElementComponent."""
    ...


class IfcBuildingElementProxy(IfcBuildingElement):
    """Wrapper class for IfcBuildingElementProxy."""
    CompositionType: Optional["IfcElementCompositionEnum"]


class IfcBuildingElementProxyType(IfcBuildingElementType):
    """Wrapper class for IfcBuildingElementProxyType."""
    PredefinedType: "IfcBuildingElementProxyTypeEnum"


class IfcColumn(IfcBuildingElement):
    """Wrapper class for IfcColumn."""
    ...


class IfcColumnType(IfcBuildingElementType):
    """Wrapper class for IfcColumnType."""
    PredefinedType: "IfcColumnTypeEnum"


class IfcCovering(IfcBuildingElement):
    """Wrapper class for IfcCovering."""
    PredefinedType: Optional["IfcCoveringTypeEnum"]
    def CoversSpaces(self) -> tuple["IfcRelCoversSpaces", ...]: ...
    def Covers(self) -> tuple["IfcRelCoversBldgElements", ...]: ...


class IfcCoveringType(IfcBuildingElementType):
    """Wrapper class for IfcCoveringType."""
    PredefinedType: "IfcCoveringTypeEnum"


class IfcCurtainWall(IfcBuildingElement):
    """Wrapper class for IfcCurtainWall."""
    ...


class IfcCurtainWallType(IfcBuildingElementType):
    """Wrapper class for IfcCurtainWallType."""
    PredefinedType: "IfcCurtainWallTypeEnum"


class IfcDiscreteAccessory(IfcElementComponent):
    """Wrapper class for IfcDiscreteAccessory."""
    ...


class IfcDiscreteAccessoryType(IfcElementComponentType):
    """Wrapper class for IfcDiscreteAccessoryType."""
    ...


class IfcDistributionControlElement(IfcDistributionElement):
    """Wrapper class for IfcDistributionControlElement."""
    ControlElementId: Optional[str]
    def AssignedToFlowElement(self) -> tuple["IfcRelFlowControlElements", ...]: ...


class IfcDistributionControlElementType(IfcDistributionElementType):
    """Wrapper class for IfcDistributionControlElementType."""
    ...


class IfcDistributionFlowElement(IfcDistributionElement):
    """Wrapper class for IfcDistributionFlowElement."""
    def HasControlElements(self) -> tuple["IfcRelFlowControlElements", ...]: ...


class IfcDistributionFlowElementType(IfcDistributionElementType):
    """Wrapper class for IfcDistributionFlowElementType."""
    ...


class IfcDoor(IfcBuildingElement):
    """Wrapper class for IfcDoor."""
    OverallHeight: Optional[float]
    OverallWidth: Optional[float]


class IfcFastener(IfcElementComponent):
    """Wrapper class for IfcFastener."""
    ...


class IfcFastenerType(IfcElementComponentType):
    """Wrapper class for IfcFastenerType."""
    ...


class IfcFeatureElementAddition(IfcFeatureElement):
    """Wrapper class for IfcFeatureElementAddition."""
    def ProjectsElements(self) -> tuple["IfcRelProjectsElement", ...]: ...


class IfcFeatureElementSubtraction(IfcFeatureElement):
    """Wrapper class for IfcFeatureElementSubtraction."""
    def VoidsElements(self) -> tuple["IfcRelVoidsElement", ...]: ...


class IfcFooting(IfcBuildingElement):
    """Wrapper class for IfcFooting."""
    PredefinedType: "IfcFootingTypeEnum"


class IfcFurnitureType(IfcFurnishingElementType):
    """Wrapper class for IfcFurnitureType."""
    AssemblyPlace: "IfcAssemblyPlaceEnum"


class IfcMember(IfcBuildingElement):
    """Wrapper class for IfcMember."""
    ...


class IfcMemberType(IfcBuildingElementType):
    """Wrapper class for IfcMemberType."""
    PredefinedType: "IfcMemberTypeEnum"


class IfcPile(IfcBuildingElement):
    """Wrapper class for IfcPile."""
    PredefinedType: "IfcPileTypeEnum"
    ConstructionType: Optional["IfcPileConstructionEnum"]


class IfcPlate(IfcBuildingElement):
    """Wrapper class for IfcPlate."""
    ...


class IfcPlateType(IfcBuildingElementType):
    """Wrapper class for IfcPlateType."""
    PredefinedType: "IfcPlateTypeEnum"


class IfcRailing(IfcBuildingElement):
    """Wrapper class for IfcRailing."""
    PredefinedType: Optional["IfcRailingTypeEnum"]


class IfcRailingType(IfcBuildingElementType):
    """Wrapper class for IfcRailingType."""
    PredefinedType: "IfcRailingTypeEnum"


class IfcRamp(IfcBuildingElement):
    """Wrapper class for IfcRamp."""
    ShapeType: "IfcRampTypeEnum"


class IfcRampFlight(IfcBuildingElement):
    """Wrapper class for IfcRampFlight."""
    ...


class IfcRampFlightType(IfcBuildingElementType):
    """Wrapper class for IfcRampFlightType."""
    PredefinedType: "IfcRampFlightTypeEnum"


class IfcRationalBezierCurve(IfcBezierCurve):
    """Wrapper class for IfcRationalBezierCurve."""
    WeightsData: list[float]


class IfcRoof(IfcBuildingElement):
    """Wrapper class for IfcRoof."""
    ShapeType: "IfcRoofTypeEnum"


class IfcSlab(IfcBuildingElement):
    """Wrapper class for IfcSlab."""
    PredefinedType: Optional["IfcSlabTypeEnum"]


class IfcSlabType(IfcBuildingElementType):
    """Wrapper class for IfcSlabType."""
    PredefinedType: "IfcSlabTypeEnum"


class IfcSpaceType(IfcSpatialStructureElementType):
    """Wrapper class for IfcSpaceType."""
    PredefinedType: "IfcSpaceTypeEnum"


class IfcStair(IfcBuildingElement):
    """Wrapper class for IfcStair."""
    ShapeType: "IfcStairTypeEnum"


class IfcStairFlight(IfcBuildingElement):
    """Wrapper class for IfcStairFlight."""
    NumberOfRiser: Optional[int]
    NumberOfTreads: Optional[int]
    RiserHeight: Optional[float]
    TreadLength: Optional[float]


class IfcStairFlightType(IfcBuildingElementType):
    """Wrapper class for IfcStairFlightType."""
    PredefinedType: "IfcStairFlightTypeEnum"


class IfcStructuralCurveConnection(IfcStructuralConnection):
    """Wrapper class for IfcStructuralCurveConnection."""
    ...


class IfcStructuralCurveMember(IfcStructuralMember):
    """Wrapper class for IfcStructuralCurveMember."""
    PredefinedType: "IfcStructuralCurveTypeEnum"


class IfcStructuralLinearAction(IfcStructuralAction):
    """Wrapper class for IfcStructuralLinearAction."""
    ProjectedOrTrue: "IfcProjectedOrTrueLengthEnum"


class IfcStructuralPlanarAction(IfcStructuralAction):
    """Wrapper class for IfcStructuralPlanarAction."""
    ProjectedOrTrue: "IfcProjectedOrTrueLengthEnum"


class IfcStructuralPointAction(IfcStructuralAction):
    """Wrapper class for IfcStructuralPointAction."""
    ...


class IfcStructuralPointConnection(IfcStructuralConnection):
    """Wrapper class for IfcStructuralPointConnection."""
    ...


class IfcStructuralPointReaction(IfcStructuralReaction):
    """Wrapper class for IfcStructuralPointReaction."""
    ...


class IfcStructuralSurfaceConnection(IfcStructuralConnection):
    """Wrapper class for IfcStructuralSurfaceConnection."""
    ...


class IfcStructuralSurfaceMember(IfcStructuralMember):
    """Wrapper class for IfcStructuralSurfaceMember."""
    PredefinedType: "IfcStructuralSurfaceTypeEnum"
    Thickness: Optional[float]


class IfcSystemFurnitureElementType(IfcFurnishingElementType):
    """Wrapper class for IfcSystemFurnitureElementType."""
    ...


class IfcWall(IfcBuildingElement):
    """Wrapper class for IfcWall."""
    ...


class IfcWallType(IfcBuildingElementType):
    """Wrapper class for IfcWallType."""
    PredefinedType: "IfcWallTypeEnum"


class IfcWindow(IfcBuildingElement):
    """Wrapper class for IfcWindow."""
    OverallHeight: Optional[float]
    OverallWidth: Optional[float]


class IfcActuatorType(IfcDistributionControlElementType):
    """Wrapper class for IfcActuatorType."""
    PredefinedType: "IfcActuatorTypeEnum"


class IfcAlarmType(IfcDistributionControlElementType):
    """Wrapper class for IfcAlarmType."""
    PredefinedType: "IfcAlarmTypeEnum"


class IfcBuildingElementPart(IfcBuildingElementComponent):
    """Wrapper class for IfcBuildingElementPart."""
    ...


class IfcControllerType(IfcDistributionControlElementType):
    """Wrapper class for IfcControllerType."""
    PredefinedType: "IfcControllerTypeEnum"


class IfcDistributionChamberElement(IfcDistributionFlowElement):
    """Wrapper class for IfcDistributionChamberElement."""
    ...


class IfcDistributionChamberElementType(IfcDistributionFlowElementType):
    """Wrapper class for IfcDistributionChamberElementType."""
    PredefinedType: "IfcDistributionChamberElementTypeEnum"


class IfcEdgeFeature(IfcFeatureElementSubtraction):
    """Wrapper class for IfcEdgeFeature."""
    FeatureLength: Optional[float]


class IfcEnergyConversionDevice(IfcDistributionFlowElement):
    """Wrapper class for IfcEnergyConversionDevice."""
    ...


class IfcEnergyConversionDeviceType(IfcDistributionFlowElementType):
    """Wrapper class for IfcEnergyConversionDeviceType."""
    ...


class IfcFlowController(IfcDistributionFlowElement):
    """Wrapper class for IfcFlowController."""
    ...


class IfcFlowControllerType(IfcDistributionFlowElementType):
    """Wrapper class for IfcFlowControllerType."""
    ...


class IfcFlowFitting(IfcDistributionFlowElement):
    """Wrapper class for IfcFlowFitting."""
    ...


class IfcFlowFittingType(IfcDistributionFlowElementType):
    """Wrapper class for IfcFlowFittingType."""
    ...


class IfcFlowInstrumentType(IfcDistributionControlElementType):
    """Wrapper class for IfcFlowInstrumentType."""
    PredefinedType: "IfcFlowInstrumentTypeEnum"


class IfcFlowMovingDevice(IfcDistributionFlowElement):
    """Wrapper class for IfcFlowMovingDevice."""
    ...


class IfcFlowMovingDeviceType(IfcDistributionFlowElementType):
    """Wrapper class for IfcFlowMovingDeviceType."""
    ...


class IfcFlowSegment(IfcDistributionFlowElement):
    """Wrapper class for IfcFlowSegment."""
    ...


class IfcFlowSegmentType(IfcDistributionFlowElementType):
    """Wrapper class for IfcFlowSegmentType."""
    ...


class IfcFlowStorageDevice(IfcDistributionFlowElement):
    """Wrapper class for IfcFlowStorageDevice."""
    ...


class IfcFlowStorageDeviceType(IfcDistributionFlowElementType):
    """Wrapper class for IfcFlowStorageDeviceType."""
    ...


class IfcFlowTerminal(IfcDistributionFlowElement):
    """Wrapper class for IfcFlowTerminal."""
    ...


class IfcFlowTerminalType(IfcDistributionFlowElementType):
    """Wrapper class for IfcFlowTerminalType."""
    ...


class IfcFlowTreatmentDevice(IfcDistributionFlowElement):
    """Wrapper class for IfcFlowTreatmentDevice."""
    ...


class IfcFlowTreatmentDeviceType(IfcDistributionFlowElementType):
    """Wrapper class for IfcFlowTreatmentDeviceType."""
    ...


class IfcMechanicalFastener(IfcFastener):
    """Wrapper class for IfcMechanicalFastener."""
    NominalDiameter: Optional[float]
    NominalLength: Optional[float]


class IfcMechanicalFastenerType(IfcFastenerType):
    """Wrapper class for IfcMechanicalFastenerType."""
    ...


class IfcOpeningElement(IfcFeatureElementSubtraction):
    """Wrapper class for IfcOpeningElement."""
    def HasFillings(self) -> tuple["IfcRelFillsElement", ...]: ...


class IfcProjectionElement(IfcFeatureElementAddition):
    """Wrapper class for IfcProjectionElement."""
    ...


class IfcReinforcingElement(IfcBuildingElementComponent):
    """Wrapper class for IfcReinforcingElement."""
    SteelGrade: Optional[str]


class IfcSensorType(IfcDistributionControlElementType):
    """Wrapper class for IfcSensorType."""
    PredefinedType: "IfcSensorTypeEnum"


class IfcStructuralCurveMemberVarying(IfcStructuralCurveMember):
    """Wrapper class for IfcStructuralCurveMemberVarying."""
    ...


class IfcStructuralLinearActionVarying(IfcStructuralLinearAction):
    """Wrapper class for IfcStructuralLinearActionVarying."""
    VaryingAppliedLoadLocation: "IfcShapeAspect"
    SubsequentAppliedLoads: list["IfcStructuralLoad"]


class IfcStructuralPlanarActionVarying(IfcStructuralPlanarAction):
    """Wrapper class for IfcStructuralPlanarActionVarying."""
    VaryingAppliedLoadLocation: "IfcShapeAspect"
    SubsequentAppliedLoads: list["IfcStructuralLoad"]


class IfcStructuralSurfaceMemberVarying(IfcStructuralSurfaceMember):
    """Wrapper class for IfcStructuralSurfaceMemberVarying."""
    SubsequentThickness: list[float]
    VaryingThicknessLocation: "IfcShapeAspect"


class IfcVibrationIsolatorType(IfcDiscreteAccessoryType):
    """Wrapper class for IfcVibrationIsolatorType."""
    PredefinedType: "IfcVibrationIsolatorTypeEnum"


class IfcWallStandardCase(IfcWall):
    """Wrapper class for IfcWallStandardCase."""
    ...


class IfcAirTerminalBoxType(IfcFlowControllerType):
    """Wrapper class for IfcAirTerminalBoxType."""
    PredefinedType: "IfcAirTerminalBoxTypeEnum"


class IfcAirTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcAirTerminalType."""
    PredefinedType: "IfcAirTerminalTypeEnum"


class IfcAirToAirHeatRecoveryType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcAirToAirHeatRecoveryType."""
    PredefinedType: "IfcAirToAirHeatRecoveryTypeEnum"


class IfcBoilerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcBoilerType."""
    PredefinedType: "IfcBoilerTypeEnum"


class IfcCableCarrierFittingType(IfcFlowFittingType):
    """Wrapper class for IfcCableCarrierFittingType."""
    PredefinedType: "IfcCableCarrierFittingTypeEnum"


class IfcCableCarrierSegmentType(IfcFlowSegmentType):
    """Wrapper class for IfcCableCarrierSegmentType."""
    PredefinedType: "IfcCableCarrierSegmentTypeEnum"


class IfcCableSegmentType(IfcFlowSegmentType):
    """Wrapper class for IfcCableSegmentType."""
    PredefinedType: "IfcCableSegmentTypeEnum"


class IfcChamferEdgeFeature(IfcEdgeFeature):
    """Wrapper class for IfcChamferEdgeFeature."""
    Width: Optional[float]
    Height: Optional[float]


class IfcChillerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcChillerType."""
    PredefinedType: "IfcChillerTypeEnum"


class IfcCoilType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcCoilType."""
    PredefinedType: "IfcCoilTypeEnum"


class IfcCompressorType(IfcFlowMovingDeviceType):
    """Wrapper class for IfcCompressorType."""
    PredefinedType: "IfcCompressorTypeEnum"


class IfcCondenserType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcCondenserType."""
    PredefinedType: "IfcCondenserTypeEnum"


class IfcCooledBeamType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcCooledBeamType."""
    PredefinedType: "IfcCooledBeamTypeEnum"


class IfcCoolingTowerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcCoolingTowerType."""
    PredefinedType: "IfcCoolingTowerTypeEnum"


class IfcDamperType(IfcFlowControllerType):
    """Wrapper class for IfcDamperType."""
    PredefinedType: "IfcDamperTypeEnum"


class IfcDuctFittingType(IfcFlowFittingType):
    """Wrapper class for IfcDuctFittingType."""
    PredefinedType: "IfcDuctFittingTypeEnum"


class IfcDuctSegmentType(IfcFlowSegmentType):
    """Wrapper class for IfcDuctSegmentType."""
    PredefinedType: "IfcDuctSegmentTypeEnum"


class IfcDuctSilencerType(IfcFlowTreatmentDeviceType):
    """Wrapper class for IfcDuctSilencerType."""
    PredefinedType: "IfcDuctSilencerTypeEnum"


class IfcElectricApplianceType(IfcFlowTerminalType):
    """Wrapper class for IfcElectricApplianceType."""
    PredefinedType: "IfcElectricApplianceTypeEnum"


class IfcElectricDistributionPoint(IfcFlowController):
    """Wrapper class for IfcElectricDistributionPoint."""
    DistributionPointFunction: "IfcElectricDistributionPointFunctionEnum"
    UserDefinedFunction: Optional[str]


class IfcElectricFlowStorageDeviceType(IfcFlowStorageDeviceType):
    """Wrapper class for IfcElectricFlowStorageDeviceType."""
    PredefinedType: "IfcElectricFlowStorageDeviceTypeEnum"


class IfcElectricGeneratorType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcElectricGeneratorType."""
    PredefinedType: "IfcElectricGeneratorTypeEnum"


class IfcElectricHeaterType(IfcFlowTerminalType):
    """Wrapper class for IfcElectricHeaterType."""
    PredefinedType: "IfcElectricHeaterTypeEnum"


class IfcElectricMotorType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcElectricMotorType."""
    PredefinedType: "IfcElectricMotorTypeEnum"


class IfcElectricTimeControlType(IfcFlowControllerType):
    """Wrapper class for IfcElectricTimeControlType."""
    PredefinedType: "IfcElectricTimeControlTypeEnum"


class IfcEvaporativeCoolerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcEvaporativeCoolerType."""
    PredefinedType: "IfcEvaporativeCoolerTypeEnum"


class IfcEvaporatorType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcEvaporatorType."""
    PredefinedType: "IfcEvaporatorTypeEnum"


class IfcFanType(IfcFlowMovingDeviceType):
    """Wrapper class for IfcFanType."""
    PredefinedType: "IfcFanTypeEnum"


class IfcFilterType(IfcFlowTreatmentDeviceType):
    """Wrapper class for IfcFilterType."""
    PredefinedType: "IfcFilterTypeEnum"


class IfcFireSuppressionTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcFireSuppressionTerminalType."""
    PredefinedType: "IfcFireSuppressionTerminalTypeEnum"


class IfcFlowMeterType(IfcFlowControllerType):
    """Wrapper class for IfcFlowMeterType."""
    PredefinedType: "IfcFlowMeterTypeEnum"


class IfcGasTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcGasTerminalType."""
    PredefinedType: "IfcGasTerminalTypeEnum"


class IfcHeatExchangerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcHeatExchangerType."""
    PredefinedType: "IfcHeatExchangerTypeEnum"


class IfcHumidifierType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcHumidifierType."""
    PredefinedType: "IfcHumidifierTypeEnum"


class IfcJunctionBoxType(IfcFlowFittingType):
    """Wrapper class for IfcJunctionBoxType."""
    PredefinedType: "IfcJunctionBoxTypeEnum"


class IfcLampType(IfcFlowTerminalType):
    """Wrapper class for IfcLampType."""
    PredefinedType: "IfcLampTypeEnum"


class IfcLightFixtureType(IfcFlowTerminalType):
    """Wrapper class for IfcLightFixtureType."""
    PredefinedType: "IfcLightFixtureTypeEnum"


class IfcMotorConnectionType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcMotorConnectionType."""
    PredefinedType: "IfcMotorConnectionTypeEnum"


class IfcOutletType(IfcFlowTerminalType):
    """Wrapper class for IfcOutletType."""
    PredefinedType: "IfcOutletTypeEnum"


class IfcPipeFittingType(IfcFlowFittingType):
    """Wrapper class for IfcPipeFittingType."""
    PredefinedType: "IfcPipeFittingTypeEnum"


class IfcPipeSegmentType(IfcFlowSegmentType):
    """Wrapper class for IfcPipeSegmentType."""
    PredefinedType: "IfcPipeSegmentTypeEnum"


class IfcProtectiveDeviceType(IfcFlowControllerType):
    """Wrapper class for IfcProtectiveDeviceType."""
    PredefinedType: "IfcProtectiveDeviceTypeEnum"


class IfcPumpType(IfcFlowMovingDeviceType):
    """Wrapper class for IfcPumpType."""
    PredefinedType: "IfcPumpTypeEnum"


class IfcReinforcingBar(IfcReinforcingElement):
    """Wrapper class for IfcReinforcingBar."""
    NominalDiameter: float
    CrossSectionArea: float
    BarLength: Optional[float]
    BarRole: "IfcReinforcingBarRoleEnum"
    BarSurface: Optional["IfcReinforcingBarSurfaceEnum"]


class IfcReinforcingMesh(IfcReinforcingElement):
    """Wrapper class for IfcReinforcingMesh."""
    MeshLength: Optional[float]
    MeshWidth: Optional[float]
    LongitudinalBarNominalDiameter: float
    TransverseBarNominalDiameter: float
    LongitudinalBarCrossSectionArea: float
    TransverseBarCrossSectionArea: float
    LongitudinalBarSpacing: float
    TransverseBarSpacing: float


class IfcRoundedEdgeFeature(IfcEdgeFeature):
    """Wrapper class for IfcRoundedEdgeFeature."""
    Radius: Optional[float]


class IfcSanitaryTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcSanitaryTerminalType."""
    PredefinedType: "IfcSanitaryTerminalTypeEnum"


class IfcSpaceHeaterType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcSpaceHeaterType."""
    PredefinedType: "IfcSpaceHeaterTypeEnum"


class IfcStackTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcStackTerminalType."""
    PredefinedType: "IfcStackTerminalTypeEnum"


class IfcSwitchingDeviceType(IfcFlowControllerType):
    """Wrapper class for IfcSwitchingDeviceType."""
    PredefinedType: "IfcSwitchingDeviceTypeEnum"


class IfcTankType(IfcFlowStorageDeviceType):
    """Wrapper class for IfcTankType."""
    PredefinedType: "IfcTankTypeEnum"


class IfcTendon(IfcReinforcingElement):
    """Wrapper class for IfcTendon."""
    PredefinedType: "IfcTendonTypeEnum"
    NominalDiameter: float
    CrossSectionArea: float
    TensionForce: Optional[float]
    PreStress: Optional[float]
    FrictionCoefficient: Optional[float]
    AnchorageSlip: Optional[float]
    MinCurvatureRadius: Optional[float]


class IfcTendonAnchor(IfcReinforcingElement):
    """Wrapper class for IfcTendonAnchor."""
    ...


class IfcTransformerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcTransformerType."""
    PredefinedType: "IfcTransformerTypeEnum"


class IfcTubeBundleType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcTubeBundleType."""
    PredefinedType: "IfcTubeBundleTypeEnum"


class IfcUnitaryEquipmentType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcUnitaryEquipmentType."""
    PredefinedType: "IfcUnitaryEquipmentTypeEnum"


class IfcValveType(IfcFlowControllerType):
    """Wrapper class for IfcValveType."""
    PredefinedType: "IfcValveTypeEnum"


class IfcWasteTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcWasteTerminalType."""
    PredefinedType: "IfcWasteTerminalTypeEnum"


__all__ = [
    "Ifc2DCompositeCurve",
    "IfcActionRequest",
    "IfcActionSourceTypeEnum",
    "IfcActionTypeEnum",
    "IfcActor",
    "IfcActorRole",
    "IfcActuatorType",
    "IfcActuatorTypeEnum",
    "IfcAddress",
    "IfcAddressTypeEnum",
    "IfcAheadOrBehind",
    "IfcAirTerminalBoxType",
    "IfcAirTerminalBoxTypeEnum",
    "IfcAirTerminalType",
    "IfcAirTerminalTypeEnum",
    "IfcAirToAirHeatRecoveryType",
    "IfcAirToAirHeatRecoveryTypeEnum",
    "IfcAlarmType",
    "IfcAlarmTypeEnum",
    "IfcAnalysisModelTypeEnum",
    "IfcAnalysisTheoryTypeEnum",
    "IfcAngularDimension",
    "IfcAnnotation",
    "IfcAnnotationCurveOccurrence",
    "IfcAnnotationFillArea",
    "IfcAnnotationFillAreaOccurrence",
    "IfcAnnotationOccurrence",
    "IfcAnnotationSurface",
    "IfcAnnotationSurfaceOccurrence",
    "IfcAnnotationSymbolOccurrence",
    "IfcAnnotationTextOccurrence",
    "IfcApplication",
    "IfcAppliedValue",
    "IfcAppliedValueRelationship",
    "IfcApproval",
    "IfcApprovalActorRelationship",
    "IfcApprovalPropertyRelationship",
    "IfcApprovalRelationship",
    "IfcArbitraryClosedProfileDef",
    "IfcArbitraryOpenProfileDef",
    "IfcArbitraryProfileDefWithVoids",
    "IfcArithmeticOperatorEnum",
    "IfcAssemblyPlaceEnum",
    "IfcAsset",
    "IfcAsymmetricIShapeProfileDef",
    "IfcAxis1Placement",
    "IfcAxis2Placement2D",
    "IfcAxis2Placement3D",
    "IfcBSplineCurve",
    "IfcBSplineCurveForm",
    "IfcBeam",
    "IfcBeamType",
    "IfcBeamTypeEnum",
    "IfcBenchmarkEnum",
    "IfcBezierCurve",
    "IfcBlobTexture",
    "IfcBlock",
    "IfcBoilerType",
    "IfcBoilerTypeEnum",
    "IfcBooleanClippingResult",
    "IfcBooleanOperator",
    "IfcBooleanResult",
    "IfcBoundaryCondition",
    "IfcBoundaryEdgeCondition",
    "IfcBoundaryFaceCondition",
    "IfcBoundaryNodeCondition",
    "IfcBoundaryNodeConditionWarping",
    "IfcBoundedCurve",
    "IfcBoundedSurface",
    "IfcBoundingBox",
    "IfcBoxedHalfSpace",
    "IfcBuilding",
    "IfcBuildingElement",
    "IfcBuildingElementComponent",
    "IfcBuildingElementPart",
    "IfcBuildingElementProxy",
    "IfcBuildingElementProxyType",
    "IfcBuildingElementProxyTypeEnum",
    "IfcBuildingElementType",
    "IfcBuildingStorey",
    "IfcCShapeProfileDef",
    "IfcCableCarrierFittingType",
    "IfcCableCarrierFittingTypeEnum",
    "IfcCableCarrierSegmentType",
    "IfcCableCarrierSegmentTypeEnum",
    "IfcCableSegmentType",
    "IfcCableSegmentTypeEnum",
    "IfcCalendarDate",
    "IfcCartesianPoint",
    "IfcCartesianTransformationOperator",
    "IfcCartesianTransformationOperator2D",
    "IfcCartesianTransformationOperator2DnonUniform",
    "IfcCartesianTransformationOperator3D",
    "IfcCartesianTransformationOperator3DnonUniform",
    "IfcCenterLineProfileDef",
    "IfcChamferEdgeFeature",
    "IfcChangeActionEnum",
    "IfcChillerType",
    "IfcChillerTypeEnum",
    "IfcCircle",
    "IfcCircleHollowProfileDef",
    "IfcCircleProfileDef",
    "IfcClassification",
    "IfcClassificationItem",
    "IfcClassificationItemRelationship",
    "IfcClassificationNotation",
    "IfcClassificationNotationFacet",
    "IfcClassificationReference",
    "IfcClosedShell",
    "IfcCoilType",
    "IfcCoilTypeEnum",
    "IfcColourRgb",
    "IfcColourSpecification",
    "IfcColumn",
    "IfcColumnType",
    "IfcColumnTypeEnum",
    "IfcComplexProperty",
    "IfcCompositeCurve",
    "IfcCompositeCurveSegment",
    "IfcCompositeProfileDef",
    "IfcCompressorType",
    "IfcCompressorTypeEnum",
    "IfcCondenserType",
    "IfcCondenserTypeEnum",
    "IfcCondition",
    "IfcConditionCriterion",
    "IfcConic",
    "IfcConnectedFaceSet",
    "IfcConnectionCurveGeometry",
    "IfcConnectionGeometry",
    "IfcConnectionPointEccentricity",
    "IfcConnectionPointGeometry",
    "IfcConnectionPortGeometry",
    "IfcConnectionSurfaceGeometry",
    "IfcConnectionTypeEnum",
    "IfcConstraint",
    "IfcConstraintAggregationRelationship",
    "IfcConstraintClassificationRelationship",
    "IfcConstraintEnum",
    "IfcConstraintRelationship",
    "IfcConstructionEquipmentResource",
    "IfcConstructionMaterialResource",
    "IfcConstructionProductResource",
    "IfcConstructionResource",
    "IfcContextDependentUnit",
    "IfcControl",
    "IfcControllerType",
    "IfcControllerTypeEnum",
    "IfcConversionBasedUnit",
    "IfcCooledBeamType",
    "IfcCooledBeamTypeEnum",
    "IfcCoolingTowerType",
    "IfcCoolingTowerTypeEnum",
    "IfcCoordinatedUniversalTimeOffset",
    "IfcCostItem",
    "IfcCostSchedule",
    "IfcCostScheduleTypeEnum",
    "IfcCostValue",
    "IfcCovering",
    "IfcCoveringType",
    "IfcCoveringTypeEnum",
    "IfcCraneRailAShapeProfileDef",
    "IfcCraneRailFShapeProfileDef",
    "IfcCrewResource",
    "IfcCsgPrimitive3D",
    "IfcCsgSolid",
    "IfcCurrencyEnum",
    "IfcCurrencyRelationship",
    "IfcCurtainWall",
    "IfcCurtainWallType",
    "IfcCurtainWallTypeEnum",
    "IfcCurve",
    "IfcCurveBoundedPlane",
    "IfcCurveStyle",
    "IfcCurveStyleFont",
    "IfcCurveStyleFontAndScaling",
    "IfcCurveStyleFontPattern",
    "IfcDamperType",
    "IfcDamperTypeEnum",
    "IfcDataOriginEnum",
    "IfcDateAndTime",
    "IfcDefinedSymbol",
    "IfcDerivedProfileDef",
    "IfcDerivedUnit",
    "IfcDerivedUnitElement",
    "IfcDerivedUnitEnum",
    "IfcDiameterDimension",
    "IfcDimensionCalloutRelationship",
    "IfcDimensionCurve",
    "IfcDimensionCurveDirectedCallout",
    "IfcDimensionCurveTerminator",
    "IfcDimensionExtentUsage",
    "IfcDimensionPair",
    "IfcDimensionalExponents",
    "IfcDirection",
    "IfcDirectionSenseEnum",
    "IfcDiscreteAccessory",
    "IfcDiscreteAccessoryType",
    "IfcDistributionChamberElement",
    "IfcDistributionChamberElementType",
    "IfcDistributionChamberElementTypeEnum",
    "IfcDistributionControlElement",
    "IfcDistributionControlElementType",
    "IfcDistributionElement",
    "IfcDistributionElementType",
    "IfcDistributionFlowElement",
    "IfcDistributionFlowElementType",
    "IfcDistributionPort",
    "IfcDocumentConfidentialityEnum",
    "IfcDocumentElectronicFormat",
    "IfcDocumentInformation",
    "IfcDocumentInformationRelationship",
    "IfcDocumentReference",
    "IfcDocumentStatusEnum",
    "IfcDoor",
    "IfcDoorLiningProperties",
    "IfcDoorPanelOperationEnum",
    "IfcDoorPanelPositionEnum",
    "IfcDoorPanelProperties",
    "IfcDoorStyle",
    "IfcDoorStyleConstructionEnum",
    "IfcDoorStyleOperationEnum",
    "IfcDraughtingCallout",
    "IfcDraughtingCalloutRelationship",
    "IfcDraughtingPreDefinedColour",
    "IfcDraughtingPreDefinedCurveFont",
    "IfcDraughtingPreDefinedTextFont",
    "IfcDuctFittingType",
    "IfcDuctFittingTypeEnum",
    "IfcDuctSegmentType",
    "IfcDuctSegmentTypeEnum",
    "IfcDuctSilencerType",
    "IfcDuctSilencerTypeEnum",
    "IfcEdge",
    "IfcEdgeCurve",
    "IfcEdgeFeature",
    "IfcEdgeLoop",
    "IfcElectricApplianceType",
    "IfcElectricApplianceTypeEnum",
    "IfcElectricCurrentEnum",
    "IfcElectricDistributionPoint",
    "IfcElectricDistributionPointFunctionEnum",
    "IfcElectricFlowStorageDeviceType",
    "IfcElectricFlowStorageDeviceTypeEnum",
    "IfcElectricGeneratorType",
    "IfcElectricGeneratorTypeEnum",
    "IfcElectricHeaterType",
    "IfcElectricHeaterTypeEnum",
    "IfcElectricMotorType",
    "IfcElectricMotorTypeEnum",
    "IfcElectricTimeControlType",
    "IfcElectricTimeControlTypeEnum",
    "IfcElectricalBaseProperties",
    "IfcElectricalCircuit",
    "IfcElectricalElement",
    "IfcElement",
    "IfcElementAssembly",
    "IfcElementAssemblyTypeEnum",
    "IfcElementComponent",
    "IfcElementComponentType",
    "IfcElementCompositionEnum",
    "IfcElementQuantity",
    "IfcElementType",
    "IfcElementarySurface",
    "IfcEllipse",
    "IfcEllipseProfileDef",
    "IfcEnergyConversionDevice",
    "IfcEnergyConversionDeviceType",
    "IfcEnergyProperties",
    "IfcEnergySequenceEnum",
    "IfcEnvironmentalImpactCategoryEnum",
    "IfcEnvironmentalImpactValue",
    "IfcEquipmentElement",
    "IfcEquipmentStandard",
    "IfcEvaporativeCoolerType",
    "IfcEvaporativeCoolerTypeEnum",
    "IfcEvaporatorType",
    "IfcEvaporatorTypeEnum",
    "IfcExtendedMaterialProperties",
    "IfcExternalReference",
    "IfcExternallyDefinedHatchStyle",
    "IfcExternallyDefinedSurfaceStyle",
    "IfcExternallyDefinedSymbol",
    "IfcExternallyDefinedTextFont",
    "IfcExtrudedAreaSolid",
    "IfcFace",
    "IfcFaceBasedSurfaceModel",
    "IfcFaceBound",
    "IfcFaceOuterBound",
    "IfcFaceSurface",
    "IfcFacetedBrep",
    "IfcFacetedBrepWithVoids",
    "IfcFailureConnectionCondition",
    "IfcFanType",
    "IfcFanTypeEnum",
    "IfcFastener",
    "IfcFastenerType",
    "IfcFeatureElement",
    "IfcFeatureElementAddition",
    "IfcFeatureElementSubtraction",
    "IfcFillAreaStyle",
    "IfcFillAreaStyleHatching",
    "IfcFillAreaStyleTileSymbolWithStyle",
    "IfcFillAreaStyleTiles",
    "IfcFilterType",
    "IfcFilterTypeEnum",
    "IfcFireSuppressionTerminalType",
    "IfcFireSuppressionTerminalTypeEnum",
    "IfcFlowController",
    "IfcFlowControllerType",
    "IfcFlowDirectionEnum",
    "IfcFlowFitting",
    "IfcFlowFittingType",
    "IfcFlowInstrumentType",
    "IfcFlowInstrumentTypeEnum",
    "IfcFlowMeterType",
    "IfcFlowMeterTypeEnum",
    "IfcFlowMovingDevice",
    "IfcFlowMovingDeviceType",
    "IfcFlowSegment",
    "IfcFlowSegmentType",
    "IfcFlowStorageDevice",
    "IfcFlowStorageDeviceType",
    "IfcFlowTerminal",
    "IfcFlowTerminalType",
    "IfcFlowTreatmentDevice",
    "IfcFlowTreatmentDeviceType",
    "IfcFluidFlowProperties",
    "IfcFooting",
    "IfcFootingTypeEnum",
    "IfcFuelProperties",
    "IfcFurnishingElement",
    "IfcFurnishingElementType",
    "IfcFurnitureStandard",
    "IfcFurnitureType",
    "IfcGasTerminalType",
    "IfcGasTerminalTypeEnum",
    "IfcGeneralMaterialProperties",
    "IfcGeneralProfileProperties",
    "IfcGeometricCurveSet",
    "IfcGeometricProjectionEnum",
    "IfcGeometricRepresentationContext",
    "IfcGeometricRepresentationItem",
    "IfcGeometricRepresentationSubContext",
    "IfcGeometricSet",
    "IfcGlobalOrLocalEnum",
    "IfcGrid",
    "IfcGridAxis",
    "IfcGridPlacement",
    "IfcGroup",
    "IfcHalfSpaceSolid",
    "IfcHeatExchangerType",
    "IfcHeatExchangerTypeEnum",
    "IfcHumidifierType",
    "IfcHumidifierTypeEnum",
    "IfcHygroscopicMaterialProperties",
    "IfcIShapeProfileDef",
    "IfcImageTexture",
    "IfcInternalOrExternalEnum",
    "IfcInventory",
    "IfcInventoryTypeEnum",
    "IfcIrregularTimeSeries",
    "IfcIrregularTimeSeriesValue",
    "IfcJunctionBoxType",
    "IfcJunctionBoxTypeEnum",
    "IfcLShapeProfileDef",
    "IfcLaborResource",
    "IfcLampType",
    "IfcLampTypeEnum",
    "IfcLayerSetDirectionEnum",
    "IfcLibraryInformation",
    "IfcLibraryReference",
    "IfcLightDistributionCurveEnum",
    "IfcLightDistributionData",
    "IfcLightEmissionSourceEnum",
    "IfcLightFixtureType",
    "IfcLightFixtureTypeEnum",
    "IfcLightIntensityDistribution",
    "IfcLightSource",
    "IfcLightSourceAmbient",
    "IfcLightSourceDirectional",
    "IfcLightSourceGoniometric",
    "IfcLightSourcePositional",
    "IfcLightSourceSpot",
    "IfcLine",
    "IfcLinearDimension",
    "IfcLoadGroupTypeEnum",
    "IfcLocalPlacement",
    "IfcLocalTime",
    "IfcLogicalOperatorEnum",
    "IfcLoop",
    "IfcManifoldSolidBrep",
    "IfcMappedItem",
    "IfcMaterial",
    "IfcMaterialClassificationRelationship",
    "IfcMaterialDefinitionRepresentation",
    "IfcMaterialLayer",
    "IfcMaterialLayerSet",
    "IfcMaterialLayerSetUsage",
    "IfcMaterialList",
    "IfcMaterialProperties",
    "IfcMeasureWithUnit",
    "IfcMechanicalConcreteMaterialProperties",
    "IfcMechanicalFastener",
    "IfcMechanicalFastenerType",
    "IfcMechanicalMaterialProperties",
    "IfcMechanicalSteelMaterialProperties",
    "IfcMember",
    "IfcMemberType",
    "IfcMemberTypeEnum",
    "IfcMetric",
    "IfcMonetaryUnit",
    "IfcMotorConnectionType",
    "IfcMotorConnectionTypeEnum",
    "IfcMove",
    "IfcNamedUnit",
    "IfcNullStyle",
    "IfcObject",
    "IfcObjectDefinition",
    "IfcObjectPlacement",
    "IfcObjectTypeEnum",
    "IfcObjective",
    "IfcObjectiveEnum",
    "IfcOccupant",
    "IfcOccupantTypeEnum",
    "IfcOffsetCurve2D",
    "IfcOffsetCurve3D",
    "IfcOneDirectionRepeatFactor",
    "IfcOpenShell",
    "IfcOpeningElement",
    "IfcOpticalMaterialProperties",
    "IfcOrderAction",
    "IfcOrganization",
    "IfcOrganizationRelationship",
    "IfcOrientedEdge",
    "IfcOutletType",
    "IfcOutletTypeEnum",
    "IfcOwnerHistory",
    "IfcParameterizedProfileDef",
    "IfcPath",
    "IfcPerformanceHistory",
    "IfcPermeableCoveringOperationEnum",
    "IfcPermeableCoveringProperties",
    "IfcPermit",
    "IfcPerson",
    "IfcPersonAndOrganization",
    "IfcPhysicalComplexQuantity",
    "IfcPhysicalOrVirtualEnum",
    "IfcPhysicalQuantity",
    "IfcPhysicalSimpleQuantity",
    "IfcPile",
    "IfcPileConstructionEnum",
    "IfcPileTypeEnum",
    "IfcPipeFittingType",
    "IfcPipeFittingTypeEnum",
    "IfcPipeSegmentType",
    "IfcPipeSegmentTypeEnum",
    "IfcPixelTexture",
    "IfcPlacement",
    "IfcPlanarBox",
    "IfcPlanarExtent",
    "IfcPlane",
    "IfcPlate",
    "IfcPlateType",
    "IfcPlateTypeEnum",
    "IfcPoint",
    "IfcPointOnCurve",
    "IfcPointOnSurface",
    "IfcPolyLoop",
    "IfcPolygonalBoundedHalfSpace",
    "IfcPolyline",
    "IfcPort",
    "IfcPostalAddress",
    "IfcPreDefinedColour",
    "IfcPreDefinedCurveFont",
    "IfcPreDefinedDimensionSymbol",
    "IfcPreDefinedItem",
    "IfcPreDefinedPointMarkerSymbol",
    "IfcPreDefinedSymbol",
    "IfcPreDefinedTerminatorSymbol",
    "IfcPreDefinedTextFont",
    "IfcPresentationLayerAssignment",
    "IfcPresentationLayerWithStyle",
    "IfcPresentationStyle",
    "IfcPresentationStyleAssignment",
    "IfcProcedure",
    "IfcProcedureTypeEnum",
    "IfcProcess",
    "IfcProduct",
    "IfcProductDefinitionShape",
    "IfcProductRepresentation",
    "IfcProductsOfCombustionProperties",
    "IfcProfileDef",
    "IfcProfileProperties",
    "IfcProfileTypeEnum",
    "IfcProject",
    "IfcProjectOrder",
    "IfcProjectOrderRecord",
    "IfcProjectOrderRecordTypeEnum",
    "IfcProjectOrderTypeEnum",
    "IfcProjectedOrTrueLengthEnum",
    "IfcProjectionCurve",
    "IfcProjectionElement",
    "IfcProperty",
    "IfcPropertyBoundedValue",
    "IfcPropertyConstraintRelationship",
    "IfcPropertyDefinition",
    "IfcPropertyDependencyRelationship",
    "IfcPropertyEnumeratedValue",
    "IfcPropertyEnumeration",
    "IfcPropertyListValue",
    "IfcPropertyReferenceValue",
    "IfcPropertySet",
    "IfcPropertySetDefinition",
    "IfcPropertySingleValue",
    "IfcPropertySourceEnum",
    "IfcPropertyTableValue",
    "IfcProtectiveDeviceType",
    "IfcProtectiveDeviceTypeEnum",
    "IfcProxy",
    "IfcPumpType",
    "IfcPumpTypeEnum",
    "IfcQuantityArea",
    "IfcQuantityCount",
    "IfcQuantityLength",
    "IfcQuantityTime",
    "IfcQuantityVolume",
    "IfcQuantityWeight",
    "IfcRadiusDimension",
    "IfcRailing",
    "IfcRailingType",
    "IfcRailingTypeEnum",
    "IfcRamp",
    "IfcRampFlight",
    "IfcRampFlightType",
    "IfcRampFlightTypeEnum",
    "IfcRampTypeEnum",
    "IfcRationalBezierCurve",
    "IfcRectangleHollowProfileDef",
    "IfcRectangleProfileDef",
    "IfcRectangularPyramid",
    "IfcRectangularTrimmedSurface",
    "IfcReferencesValueDocument",
    "IfcReflectanceMethodEnum",
    "IfcRegularTimeSeries",
    "IfcReinforcementBarProperties",
    "IfcReinforcementDefinitionProperties",
    "IfcReinforcingBar",
    "IfcReinforcingBarRoleEnum",
    "IfcReinforcingBarSurfaceEnum",
    "IfcReinforcingElement",
    "IfcReinforcingMesh",
    "IfcRelAggregates",
    "IfcRelAssigns",
    "IfcRelAssignsTasks",
    "IfcRelAssignsToActor",
    "IfcRelAssignsToControl",
    "IfcRelAssignsToGroup",
    "IfcRelAssignsToProcess",
    "IfcRelAssignsToProduct",
    "IfcRelAssignsToProjectOrder",
    "IfcRelAssignsToResource",
    "IfcRelAssociates",
    "IfcRelAssociatesAppliedValue",
    "IfcRelAssociatesApproval",
    "IfcRelAssociatesClassification",
    "IfcRelAssociatesConstraint",
    "IfcRelAssociatesDocument",
    "IfcRelAssociatesLibrary",
    "IfcRelAssociatesMaterial",
    "IfcRelAssociatesProfileProperties",
    "IfcRelConnects",
    "IfcRelConnectsElements",
    "IfcRelConnectsPathElements",
    "IfcRelConnectsPortToElement",
    "IfcRelConnectsPorts",
    "IfcRelConnectsStructuralActivity",
    "IfcRelConnectsStructuralElement",
    "IfcRelConnectsStructuralMember",
    "IfcRelConnectsWithEccentricity",
    "IfcRelConnectsWithRealizingElements",
    "IfcRelContainedInSpatialStructure",
    "IfcRelCoversBldgElements",
    "IfcRelCoversSpaces",
    "IfcRelDecomposes",
    "IfcRelDefines",
    "IfcRelDefinesByProperties",
    "IfcRelDefinesByType",
    "IfcRelFillsElement",
    "IfcRelFlowControlElements",
    "IfcRelInteractionRequirements",
    "IfcRelNests",
    "IfcRelOccupiesSpaces",
    "IfcRelOverridesProperties",
    "IfcRelProjectsElement",
    "IfcRelReferencedInSpatialStructure",
    "IfcRelSchedulesCostItems",
    "IfcRelSequence",
    "IfcRelServicesBuildings",
    "IfcRelSpaceBoundary",
    "IfcRelVoidsElement",
    "IfcRelationship",
    "IfcRelaxation",
    "IfcRepresentation",
    "IfcRepresentationContext",
    "IfcRepresentationItem",
    "IfcRepresentationMap",
    "IfcResource",
    "IfcResourceConsumptionEnum",
    "IfcRevolvedAreaSolid",
    "IfcRibPlateDirectionEnum",
    "IfcRibPlateProfileProperties",
    "IfcRightCircularCone",
    "IfcRightCircularCylinder",
    "IfcRoleEnum",
    "IfcRoof",
    "IfcRoofTypeEnum",
    "IfcRoot",
    "IfcRoundedEdgeFeature",
    "IfcRoundedRectangleProfileDef",
    "IfcSIPrefix",
    "IfcSIUnit",
    "IfcSIUnitName",
    "IfcSanitaryTerminalType",
    "IfcSanitaryTerminalTypeEnum",
    "IfcScheduleTimeControl",
    "IfcSectionProperties",
    "IfcSectionReinforcementProperties",
    "IfcSectionTypeEnum",
    "IfcSectionedSpine",
    "IfcSensorType",
    "IfcSensorTypeEnum",
    "IfcSequenceEnum",
    "IfcServiceLife",
    "IfcServiceLifeFactor",
    "IfcServiceLifeFactorTypeEnum",
    "IfcServiceLifeTypeEnum",
    "IfcShapeAspect",
    "IfcShapeModel",
    "IfcShapeRepresentation",
    "IfcShellBasedSurfaceModel",
    "IfcSimpleProperty",
    "IfcSite",
    "IfcSlab",
    "IfcSlabType",
    "IfcSlabTypeEnum",
    "IfcSlippageConnectionCondition",
    "IfcSolidModel",
    "IfcSoundProperties",
    "IfcSoundScaleEnum",
    "IfcSoundValue",
    "IfcSpace",
    "IfcSpaceHeaterType",
    "IfcSpaceHeaterTypeEnum",
    "IfcSpaceProgram",
    "IfcSpaceThermalLoadProperties",
    "IfcSpaceType",
    "IfcSpaceTypeEnum",
    "IfcSpatialStructureElement",
    "IfcSpatialStructureElementType",
    "IfcSphere",
    "IfcStackTerminalType",
    "IfcStackTerminalTypeEnum",
    "IfcStair",
    "IfcStairFlight",
    "IfcStairFlightType",
    "IfcStairFlightTypeEnum",
    "IfcStairTypeEnum",
    "IfcStateEnum",
    "IfcStructuralAction",
    "IfcStructuralActivity",
    "IfcStructuralAnalysisModel",
    "IfcStructuralConnection",
    "IfcStructuralConnectionCondition",
    "IfcStructuralCurveConnection",
    "IfcStructuralCurveMember",
    "IfcStructuralCurveMemberVarying",
    "IfcStructuralCurveTypeEnum",
    "IfcStructuralItem",
    "IfcStructuralLinearAction",
    "IfcStructuralLinearActionVarying",
    "IfcStructuralLoad",
    "IfcStructuralLoadGroup",
    "IfcStructuralLoadLinearForce",
    "IfcStructuralLoadPlanarForce",
    "IfcStructuralLoadSingleDisplacement",
    "IfcStructuralLoadSingleDisplacementDistortion",
    "IfcStructuralLoadSingleForce",
    "IfcStructuralLoadSingleForceWarping",
    "IfcStructuralLoadStatic",
    "IfcStructuralLoadTemperature",
    "IfcStructuralMember",
    "IfcStructuralPlanarAction",
    "IfcStructuralPlanarActionVarying",
    "IfcStructuralPointAction",
    "IfcStructuralPointConnection",
    "IfcStructuralPointReaction",
    "IfcStructuralProfileProperties",
    "IfcStructuralReaction",
    "IfcStructuralResultGroup",
    "IfcStructuralSteelProfileProperties",
    "IfcStructuralSurfaceConnection",
    "IfcStructuralSurfaceMember",
    "IfcStructuralSurfaceMemberVarying",
    "IfcStructuralSurfaceTypeEnum",
    "IfcStructuredDimensionCallout",
    "IfcStyleModel",
    "IfcStyledItem",
    "IfcStyledRepresentation",
    "IfcSubContractResource",
    "IfcSubedge",
    "IfcSurface",
    "IfcSurfaceCurveSweptAreaSolid",
    "IfcSurfaceOfLinearExtrusion",
    "IfcSurfaceOfRevolution",
    "IfcSurfaceSide",
    "IfcSurfaceStyle",
    "IfcSurfaceStyleLighting",
    "IfcSurfaceStyleRefraction",
    "IfcSurfaceStyleRendering",
    "IfcSurfaceStyleShading",
    "IfcSurfaceStyleWithTextures",
    "IfcSurfaceTexture",
    "IfcSurfaceTextureEnum",
    "IfcSweptAreaSolid",
    "IfcSweptDiskSolid",
    "IfcSweptSurface",
    "IfcSwitchingDeviceType",
    "IfcSwitchingDeviceTypeEnum",
    "IfcSymbolStyle",
    "IfcSystem",
    "IfcSystemFurnitureElementType",
    "IfcTShapeProfileDef",
    "IfcTable",
    "IfcTableRow",
    "IfcTankType",
    "IfcTankTypeEnum",
    "IfcTask",
    "IfcTelecomAddress",
    "IfcTendon",
    "IfcTendonAnchor",
    "IfcTendonTypeEnum",
    "IfcTerminatorSymbol",
    "IfcTextLiteral",
    "IfcTextLiteralWithExtent",
    "IfcTextPath",
    "IfcTextStyle",
    "IfcTextStyleFontModel",
    "IfcTextStyleForDefinedFont",
    "IfcTextStyleTextModel",
    "IfcTextStyleWithBoxCharacteristics",
    "IfcTextureCoordinate",
    "IfcTextureCoordinateGenerator",
    "IfcTextureMap",
    "IfcTextureVertex",
    "IfcThermalLoadSourceEnum",
    "IfcThermalLoadTypeEnum",
    "IfcThermalMaterialProperties",
    "IfcTimeSeries",
    "IfcTimeSeriesDataTypeEnum",
    "IfcTimeSeriesReferenceRelationship",
    "IfcTimeSeriesSchedule",
    "IfcTimeSeriesScheduleTypeEnum",
    "IfcTimeSeriesValue",
    "IfcTopologicalRepresentationItem",
    "IfcTopologyRepresentation",
    "IfcTransformerType",
    "IfcTransformerTypeEnum",
    "IfcTransitionCode",
    "IfcTransportElement",
    "IfcTransportElementType",
    "IfcTransportElementTypeEnum",
    "IfcTrapeziumProfileDef",
    "IfcTrimmedCurve",
    "IfcTrimmingPreference",
    "IfcTubeBundleType",
    "IfcTubeBundleTypeEnum",
    "IfcTwoDirectionRepeatFactor",
    "IfcTypeObject",
    "IfcTypeProduct",
    "IfcUShapeProfileDef",
    "IfcUnitAssignment",
    "IfcUnitEnum",
    "IfcUnitaryEquipmentType",
    "IfcUnitaryEquipmentTypeEnum",
    "IfcValveType",
    "IfcValveTypeEnum",
    "IfcVector",
    "IfcVertex",
    "IfcVertexBasedTextureMap",
    "IfcVertexLoop",
    "IfcVertexPoint",
    "IfcVibrationIsolatorType",
    "IfcVibrationIsolatorTypeEnum",
    "IfcVirtualElement",
    "IfcVirtualGridIntersection",
    "IfcWall",
    "IfcWallStandardCase",
    "IfcWallType",
    "IfcWallTypeEnum",
    "IfcWasteTerminalType",
    "IfcWasteTerminalTypeEnum",
    "IfcWaterProperties",
    "IfcWindow",
    "IfcWindowLiningProperties",
    "IfcWindowPanelOperationEnum",
    "IfcWindowPanelPositionEnum",
    "IfcWindowPanelProperties",
    "IfcWindowStyle",
    "IfcWindowStyleConstructionEnum",
    "IfcWindowStyleOperationEnum",
    "IfcWorkControl",
    "IfcWorkControlTypeEnum",
    "IfcWorkPlan",
    "IfcWorkSchedule",
    "IfcZShapeProfileDef",
    "IfcZone",
]
