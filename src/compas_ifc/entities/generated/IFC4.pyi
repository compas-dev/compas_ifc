"""Type stubs for IFC4 entities (auto-generated).

Do not edit by hand. Regenerate with:
    python -m compas_ifc.entities.generator
"""

from typing import Optional
from typing import Union

class IfcActionRequestTypeEnum(str):
    items: tuple = ("EMAIL", "FAX", "PHONE", "POST", "VERBAL", "USERDEFINED", "NOTDEFINED")

class IfcActionSourceTypeEnum(str):
    items: tuple = (
        "DEAD_LOAD_G",
        "COMPLETION_G1",
        "LIVE_LOAD_Q",
        "SNOW_S",
        "WIND_W",
        "PRESTRESSING_P",
        "SETTLEMENT_U",
        "TEMPERATURE_T",
        "EARTHQUAKE_E",
        "FIRE",
        "IMPULSE",
        "IMPACT",
        "TRANSPORT",
        "ERECTION",
        "PROPPING",
        "SYSTEM_IMPERFECTION",
        "SHRINKAGE",
        "CREEP",
        "LACK_OF_FIT",
        "BUOYANCY",
        "ICE",
        "CURRENT",
        "WAVE",
        "RAIN",
        "BRAKES",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcActionTypeEnum(str):
    items: tuple = ("PERMANENT_G", "VARIABLE_Q", "EXTRAORDINARY_A", "USERDEFINED", "NOTDEFINED")

class IfcActuatorTypeEnum(str):
    items: tuple = ("ELECTRICACTUATOR", "HANDOPERATEDACTUATOR", "HYDRAULICACTUATOR", "PNEUMATICACTUATOR", "THERMOSTATICACTUATOR", "USERDEFINED", "NOTDEFINED")

class IfcAddressTypeEnum(str):
    items: tuple = ("OFFICE", "SITE", "HOME", "DISTRIBUTIONPOINT", "USERDEFINED")

class IfcAirTerminalBoxTypeEnum(str):
    items: tuple = ("CONSTANTFLOW", "VARIABLEFLOWPRESSUREDEPENDANT", "VARIABLEFLOWPRESSUREINDEPENDANT", "USERDEFINED", "NOTDEFINED")

class IfcAirTerminalTypeEnum(str):
    items: tuple = ("DIFFUSER", "GRILLE", "LOUVRE", "REGISTER", "USERDEFINED", "NOTDEFINED")

class IfcAirToAirHeatRecoveryTypeEnum(str):
    items: tuple = (
        "FIXEDPLATECOUNTERFLOWEXCHANGER",
        "FIXEDPLATECROSSFLOWEXCHANGER",
        "FIXEDPLATEPARALLELFLOWEXCHANGER",
        "ROTARYWHEEL",
        "RUNAROUNDCOILLOOP",
        "HEATPIPE",
        "TWINTOWERENTHALPYRECOVERYLOOPS",
        "THERMOSIPHONSEALEDTUBEHEATEXCHANGERS",
        "THERMOSIPHONCOILTYPEHEATEXCHANGERS",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcAlarmTypeEnum(str):
    items: tuple = ("BELL", "BREAKGLASSBUTTON", "LIGHT", "MANUALPULLBOX", "SIREN", "WHISTLE", "USERDEFINED", "NOTDEFINED")

class IfcAnalysisModelTypeEnum(str):
    items: tuple = ("IN_PLANE_LOADING_2D", "OUT_PLANE_LOADING_2D", "LOADING_3D", "USERDEFINED", "NOTDEFINED")

class IfcAnalysisTheoryTypeEnum(str):
    items: tuple = ("FIRST_ORDER_THEORY", "SECOND_ORDER_THEORY", "THIRD_ORDER_THEORY", "FULL_NONLINEAR_THEORY", "USERDEFINED", "NOTDEFINED")

class IfcArithmeticOperatorEnum(str):
    items: tuple = ("ADD", "DIVIDE", "MULTIPLY", "SUBTRACT")

class IfcAssemblyPlaceEnum(str):
    items: tuple = ("SITE", "FACTORY", "NOTDEFINED")

class IfcAudioVisualApplianceTypeEnum(str):
    items: tuple = ("AMPLIFIER", "CAMERA", "DISPLAY", "MICROPHONE", "PLAYER", "PROJECTOR", "RECEIVER", "SPEAKER", "SWITCHER", "TELEPHONE", "TUNER", "USERDEFINED", "NOTDEFINED")

class IfcBSplineCurveForm(str):
    items: tuple = ("POLYLINE_FORM", "CIRCULAR_ARC", "ELLIPTIC_ARC", "PARABOLIC_ARC", "HYPERBOLIC_ARC", "UNSPECIFIED")

class IfcBSplineSurfaceForm(str):
    items: tuple = (
        "PLANE_SURF",
        "CYLINDRICAL_SURF",
        "CONICAL_SURF",
        "SPHERICAL_SURF",
        "TOROIDAL_SURF",
        "SURF_OF_REVOLUTION",
        "RULED_SURF",
        "GENERALISED_CONE",
        "QUADRIC_SURF",
        "SURF_OF_LINEAR_EXTRUSION",
        "UNSPECIFIED",
    )

class IfcBeamTypeEnum(str):
    items: tuple = ("BEAM", "JOIST", "HOLLOWCORE", "LINTEL", "SPANDREL", "T_BEAM", "USERDEFINED", "NOTDEFINED")

class IfcBenchmarkEnum(str):
    items: tuple = ("GREATERTHAN", "GREATERTHANOREQUALTO", "LESSTHAN", "LESSTHANOREQUALTO", "EQUALTO", "NOTEQUALTO", "INCLUDES", "NOTINCLUDES", "INCLUDEDIN", "NOTINCLUDEDIN")

class IfcBoilerTypeEnum(str):
    items: tuple = ("WATER", "STEAM", "USERDEFINED", "NOTDEFINED")

class IfcBooleanOperator(str):
    items: tuple = ("UNION", "INTERSECTION", "DIFFERENCE")

class IfcBuildingElementPartTypeEnum(str):
    items: tuple = ("INSULATION", "PRECASTPANEL", "USERDEFINED", "NOTDEFINED")

class IfcBuildingElementProxyTypeEnum(str):
    items: tuple = ("COMPLEX", "ELEMENT", "PARTIAL", "PROVISIONFORVOID", "PROVISIONFORSPACE", "USERDEFINED", "NOTDEFINED")

class IfcBuildingSystemTypeEnum(str):
    items: tuple = ("FENESTRATION", "FOUNDATION", "LOADBEARING", "OUTERSHELL", "SHADING", "TRANSPORT", "USERDEFINED", "NOTDEFINED")

class IfcBurnerTypeEnum(str):
    items: tuple = ("USERDEFINED", "NOTDEFINED")

class IfcCableCarrierFittingTypeEnum(str):
    items: tuple = ("BEND", "CROSS", "REDUCER", "TEE", "USERDEFINED", "NOTDEFINED")

class IfcCableCarrierSegmentTypeEnum(str):
    items: tuple = ("CABLELADDERSEGMENT", "CABLETRAYSEGMENT", "CABLETRUNKINGSEGMENT", "CONDUITSEGMENT", "USERDEFINED", "NOTDEFINED")

class IfcCableFittingTypeEnum(str):
    items: tuple = ("CONNECTOR", "ENTRY", "EXIT", "JUNCTION", "TRANSITION", "USERDEFINED", "NOTDEFINED")

class IfcCableSegmentTypeEnum(str):
    items: tuple = ("BUSBARSEGMENT", "CABLESEGMENT", "CONDUCTORSEGMENT", "CORESEGMENT", "USERDEFINED", "NOTDEFINED")

class IfcChangeActionEnum(str):
    items: tuple = ("NOCHANGE", "MODIFIED", "ADDED", "DELETED", "NOTDEFINED")

class IfcChillerTypeEnum(str):
    items: tuple = ("AIRCOOLED", "WATERCOOLED", "HEATRECOVERY", "USERDEFINED", "NOTDEFINED")

class IfcChimneyTypeEnum(str):
    items: tuple = ("USERDEFINED", "NOTDEFINED")

class IfcCoilTypeEnum(str):
    items: tuple = (
        "DXCOOLINGCOIL",
        "ELECTRICHEATINGCOIL",
        "GASHEATINGCOIL",
        "HYDRONICCOIL",
        "STEAMHEATINGCOIL",
        "WATERCOOLINGCOIL",
        "WATERHEATINGCOIL",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcColumnTypeEnum(str):
    items: tuple = ("COLUMN", "PILASTER", "USERDEFINED", "NOTDEFINED")

class IfcCommunicationsApplianceTypeEnum(str):
    items: tuple = (
        "ANTENNA",
        "COMPUTER",
        "FAX",
        "GATEWAY",
        "MODEM",
        "NETWORKAPPLIANCE",
        "NETWORKBRIDGE",
        "NETWORKHUB",
        "PRINTER",
        "REPEATER",
        "ROUTER",
        "SCANNER",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcComplexPropertyTemplateTypeEnum(str):
    items: tuple = ("P_COMPLEX", "Q_COMPLEX")

class IfcCompressorTypeEnum(str):
    items: tuple = (
        "DYNAMIC",
        "RECIPROCATING",
        "ROTARY",
        "SCROLL",
        "TROCHOIDAL",
        "SINGLESTAGE",
        "BOOSTER",
        "OPENTYPE",
        "HERMETIC",
        "SEMIHERMETIC",
        "WELDEDSHELLHERMETIC",
        "ROLLINGPISTON",
        "ROTARYVANE",
        "SINGLESCREW",
        "TWINSCREW",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcCondenserTypeEnum(str):
    items: tuple = (
        "AIRCOOLED",
        "EVAPORATIVECOOLED",
        "WATERCOOLED",
        "WATERCOOLEDBRAZEDPLATE",
        "WATERCOOLEDSHELLCOIL",
        "WATERCOOLEDSHELLTUBE",
        "WATERCOOLEDTUBEINTUBE",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcConnectionTypeEnum(str):
    items: tuple = ("ATPATH", "ATSTART", "ATEND", "NOTDEFINED")

class IfcConstraintEnum(str):
    items: tuple = ("HARD", "SOFT", "ADVISORY", "USERDEFINED", "NOTDEFINED")

class IfcConstructionEquipmentResourceTypeEnum(str):
    items: tuple = ("DEMOLISHING", "EARTHMOVING", "ERECTING", "HEATING", "LIGHTING", "PAVING", "PUMPING", "TRANSPORTING", "USERDEFINED", "NOTDEFINED")

class IfcConstructionMaterialResourceTypeEnum(str):
    items: tuple = ("AGGREGATES", "CONCRETE", "DRYWALL", "FUEL", "GYPSUM", "MASONRY", "METAL", "PLASTIC", "WOOD", "NOTDEFINED", "USERDEFINED")

class IfcConstructionProductResourceTypeEnum(str):
    items: tuple = ("ASSEMBLY", "FORMWORK", "USERDEFINED", "NOTDEFINED")

class IfcControllerTypeEnum(str):
    items: tuple = ("FLOATING", "PROGRAMMABLE", "PROPORTIONAL", "MULTIPOSITION", "TWOPOSITION", "USERDEFINED", "NOTDEFINED")

class IfcCooledBeamTypeEnum(str):
    items: tuple = ("ACTIVE", "PASSIVE", "USERDEFINED", "NOTDEFINED")

class IfcCoolingTowerTypeEnum(str):
    items: tuple = ("NATURALDRAFT", "MECHANICALINDUCEDDRAFT", "MECHANICALFORCEDDRAFT", "USERDEFINED", "NOTDEFINED")

class IfcCostItemTypeEnum(str):
    items: tuple = ("USERDEFINED", "NOTDEFINED")

class IfcCostScheduleTypeEnum(str):
    items: tuple = ("BUDGET", "COSTPLAN", "ESTIMATE", "TENDER", "PRICEDBILLOFQUANTITIES", "UNPRICEDBILLOFQUANTITIES", "SCHEDULEOFRATES", "USERDEFINED", "NOTDEFINED")

class IfcCoveringTypeEnum(str):
    items: tuple = ("CEILING", "FLOORING", "CLADDING", "ROOFING", "MOLDING", "SKIRTINGBOARD", "INSULATION", "MEMBRANE", "SLEEVING", "WRAPPING", "USERDEFINED", "NOTDEFINED")

class IfcCrewResourceTypeEnum(str):
    items: tuple = ("OFFICE", "SITE", "USERDEFINED", "NOTDEFINED")

class IfcCurtainWallTypeEnum(str):
    items: tuple = ("USERDEFINED", "NOTDEFINED")

class IfcCurveInterpolationEnum(str):
    items: tuple = ("LINEAR", "LOG_LINEAR", "LOG_LOG", "NOTDEFINED")

class IfcDamperTypeEnum(str):
    items: tuple = (
        "BACKDRAFTDAMPER",
        "BALANCINGDAMPER",
        "BLASTDAMPER",
        "CONTROLDAMPER",
        "FIREDAMPER",
        "FIRESMOKEDAMPER",
        "FUMEHOODEXHAUST",
        "GRAVITYDAMPER",
        "GRAVITYRELIEFDAMPER",
        "RELIEFDAMPER",
        "SMOKEDAMPER",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcDataOriginEnum(str):
    items: tuple = ("MEASURED", "PREDICTED", "SIMULATED", "USERDEFINED", "NOTDEFINED")

class IfcDerivedUnitEnum(str):
    items: tuple = (
        "ANGULARVELOCITYUNIT",
        "AREADENSITYUNIT",
        "COMPOUNDPLANEANGLEUNIT",
        "DYNAMICVISCOSITYUNIT",
        "HEATFLUXDENSITYUNIT",
        "INTEGERCOUNTRATEUNIT",
        "ISOTHERMALMOISTURECAPACITYUNIT",
        "KINEMATICVISCOSITYUNIT",
        "LINEARVELOCITYUNIT",
        "MASSDENSITYUNIT",
        "MASSFLOWRATEUNIT",
        "MOISTUREDIFFUSIVITYUNIT",
        "MOLECULARWEIGHTUNIT",
        "SPECIFICHEATCAPACITYUNIT",
        "THERMALADMITTANCEUNIT",
        "THERMALCONDUCTANCEUNIT",
        "THERMALRESISTANCEUNIT",
        "THERMALTRANSMITTANCEUNIT",
        "VAPORPERMEABILITYUNIT",
        "VOLUMETRICFLOWRATEUNIT",
        "ROTATIONALFREQUENCYUNIT",
        "TORQUEUNIT",
        "MOMENTOFINERTIAUNIT",
        "LINEARMOMENTUNIT",
        "LINEARFORCEUNIT",
        "PLANARFORCEUNIT",
        "MODULUSOFELASTICITYUNIT",
        "SHEARMODULUSUNIT",
        "LINEARSTIFFNESSUNIT",
        "ROTATIONALSTIFFNESSUNIT",
        "MODULUSOFSUBGRADEREACTIONUNIT",
        "ACCELERATIONUNIT",
        "CURVATUREUNIT",
        "HEATINGVALUEUNIT",
        "IONCONCENTRATIONUNIT",
        "LUMINOUSINTENSITYDISTRIBUTIONUNIT",
        "MASSPERLENGTHUNIT",
        "MODULUSOFLINEARSUBGRADEREACTIONUNIT",
        "MODULUSOFROTATIONALSUBGRADEREACTIONUNIT",
        "PHUNIT",
        "ROTATIONALMASSUNIT",
        "SECTIONAREAINTEGRALUNIT",
        "SECTIONMODULUSUNIT",
        "SOUNDPOWERLEVELUNIT",
        "SOUNDPOWERUNIT",
        "SOUNDPRESSURELEVELUNIT",
        "SOUNDPRESSUREUNIT",
        "TEMPERATUREGRADIENTUNIT",
        "TEMPERATURERATEOFCHANGEUNIT",
        "THERMALEXPANSIONCOEFFICIENTUNIT",
        "WARPINGCONSTANTUNIT",
        "WARPINGMOMENTUNIT",
        "USERDEFINED",
    )

class IfcDirectionSenseEnum(str):
    items: tuple = ("POSITIVE", "NEGATIVE")

class IfcDiscreteAccessoryTypeEnum(str):
    items: tuple = ("ANCHORPLATE", "BRACKET", "SHOE", "USERDEFINED", "NOTDEFINED")

class IfcDistributionChamberElementTypeEnum(str):
    items: tuple = ("FORMEDDUCT", "INSPECTIONCHAMBER", "INSPECTIONPIT", "MANHOLE", "METERCHAMBER", "SUMP", "TRENCH", "VALVECHAMBER", "USERDEFINED", "NOTDEFINED")

class IfcDistributionPortTypeEnum(str):
    items: tuple = ("CABLE", "CABLECARRIER", "DUCT", "PIPE", "USERDEFINED", "NOTDEFINED")

class IfcDistributionSystemEnum(str):
    items: tuple = (
        "AIRCONDITIONING",
        "AUDIOVISUAL",
        "CHEMICAL",
        "CHILLEDWATER",
        "COMMUNICATION",
        "COMPRESSEDAIR",
        "CONDENSERWATER",
        "CONTROL",
        "CONVEYING",
        "DATA",
        "DISPOSAL",
        "DOMESTICCOLDWATER",
        "DOMESTICHOTWATER",
        "DRAINAGE",
        "EARTHING",
        "ELECTRICAL",
        "ELECTROACOUSTIC",
        "EXHAUST",
        "FIREPROTECTION",
        "FUEL",
        "GAS",
        "HAZARDOUS",
        "HEATING",
        "LIGHTING",
        "LIGHTNINGPROTECTION",
        "MUNICIPALSOLIDWASTE",
        "OIL",
        "OPERATIONAL",
        "POWERGENERATION",
        "RAINWATER",
        "REFRIGERATION",
        "SECURITY",
        "SEWAGE",
        "SIGNAL",
        "STORMWATER",
        "TELEPHONE",
        "TV",
        "VACUUM",
        "VENT",
        "VENTILATION",
        "WASTEWATER",
        "WATERSUPPLY",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcDocumentConfidentialityEnum(str):
    items: tuple = ("PUBLIC", "RESTRICTED", "CONFIDENTIAL", "PERSONAL", "USERDEFINED", "NOTDEFINED")

class IfcDocumentStatusEnum(str):
    items: tuple = ("DRAFT", "FINALDRAFT", "FINAL", "REVISION", "NOTDEFINED")

class IfcDoorPanelOperationEnum(str):
    items: tuple = ("SWINGING", "DOUBLE_ACTING", "SLIDING", "FOLDING", "REVOLVING", "ROLLINGUP", "FIXEDPANEL", "USERDEFINED", "NOTDEFINED")

class IfcDoorPanelPositionEnum(str):
    items: tuple = ("LEFT", "MIDDLE", "RIGHT", "NOTDEFINED")

class IfcDoorStyleConstructionEnum(str):
    items: tuple = ("ALUMINIUM", "HIGH_GRADE_STEEL", "STEEL", "WOOD", "ALUMINIUM_WOOD", "ALUMINIUM_PLASTIC", "PLASTIC", "USERDEFINED", "NOTDEFINED")

class IfcDoorStyleOperationEnum(str):
    items: tuple = (
        "SINGLE_SWING_LEFT",
        "SINGLE_SWING_RIGHT",
        "DOUBLE_DOOR_SINGLE_SWING",
        "DOUBLE_DOOR_SINGLE_SWING_OPPOSITE_LEFT",
        "DOUBLE_DOOR_SINGLE_SWING_OPPOSITE_RIGHT",
        "DOUBLE_SWING_LEFT",
        "DOUBLE_SWING_RIGHT",
        "DOUBLE_DOOR_DOUBLE_SWING",
        "SLIDING_TO_LEFT",
        "SLIDING_TO_RIGHT",
        "DOUBLE_DOOR_SLIDING",
        "FOLDING_TO_LEFT",
        "FOLDING_TO_RIGHT",
        "DOUBLE_DOOR_FOLDING",
        "REVOLVING",
        "ROLLINGUP",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcDoorTypeEnum(str):
    items: tuple = ("DOOR", "GATE", "TRAPDOOR", "USERDEFINED", "NOTDEFINED")

class IfcDoorTypeOperationEnum(str):
    items: tuple = (
        "SINGLE_SWING_LEFT",
        "SINGLE_SWING_RIGHT",
        "DOUBLE_DOOR_SINGLE_SWING",
        "DOUBLE_DOOR_SINGLE_SWING_OPPOSITE_LEFT",
        "DOUBLE_DOOR_SINGLE_SWING_OPPOSITE_RIGHT",
        "DOUBLE_SWING_LEFT",
        "DOUBLE_SWING_RIGHT",
        "DOUBLE_DOOR_DOUBLE_SWING",
        "SLIDING_TO_LEFT",
        "SLIDING_TO_RIGHT",
        "DOUBLE_DOOR_SLIDING",
        "FOLDING_TO_LEFT",
        "FOLDING_TO_RIGHT",
        "DOUBLE_DOOR_FOLDING",
        "REVOLVING",
        "ROLLINGUP",
        "SWING_FIXED_LEFT",
        "SWING_FIXED_RIGHT",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcDuctFittingTypeEnum(str):
    items: tuple = ("BEND", "CONNECTOR", "ENTRY", "EXIT", "JUNCTION", "OBSTRUCTION", "TRANSITION", "USERDEFINED", "NOTDEFINED")

class IfcDuctSegmentTypeEnum(str):
    items: tuple = ("RIGIDSEGMENT", "FLEXIBLESEGMENT", "USERDEFINED", "NOTDEFINED")

class IfcDuctSilencerTypeEnum(str):
    items: tuple = ("FLATOVAL", "RECTANGULAR", "ROUND", "USERDEFINED", "NOTDEFINED")

class IfcElectricApplianceTypeEnum(str):
    items: tuple = (
        "DISHWASHER",
        "ELECTRICCOOKER",
        "FREESTANDINGELECTRICHEATER",
        "FREESTANDINGFAN",
        "FREESTANDINGWATERHEATER",
        "FREESTANDINGWATERCOOLER",
        "FREEZER",
        "FRIDGE_FREEZER",
        "HANDDRYER",
        "KITCHENMACHINE",
        "MICROWAVE",
        "PHOTOCOPIER",
        "REFRIGERATOR",
        "TUMBLEDRYER",
        "VENDINGMACHINE",
        "WASHINGMACHINE",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcElectricDistributionBoardTypeEnum(str):
    items: tuple = ("CONSUMERUNIT", "DISTRIBUTIONBOARD", "MOTORCONTROLCENTRE", "SWITCHBOARD", "USERDEFINED", "NOTDEFINED")

class IfcElectricFlowStorageDeviceTypeEnum(str):
    items: tuple = ("BATTERY", "CAPACITORBANK", "HARMONICFILTER", "INDUCTORBANK", "UPS", "USERDEFINED", "NOTDEFINED")

class IfcElectricGeneratorTypeEnum(str):
    items: tuple = ("CHP", "ENGINEGENERATOR", "STANDALONE", "USERDEFINED", "NOTDEFINED")

class IfcElectricMotorTypeEnum(str):
    items: tuple = ("DC", "INDUCTION", "POLYPHASE", "RELUCTANCESYNCHRONOUS", "SYNCHRONOUS", "USERDEFINED", "NOTDEFINED")

class IfcElectricTimeControlTypeEnum(str):
    items: tuple = ("TIMECLOCK", "TIMEDELAY", "RELAY", "USERDEFINED", "NOTDEFINED")

class IfcElementAssemblyTypeEnum(str):
    items: tuple = ("ACCESSORY_ASSEMBLY", "ARCH", "BEAM_GRID", "BRACED_FRAME", "GIRDER", "REINFORCEMENT_UNIT", "RIGID_FRAME", "SLAB_FIELD", "TRUSS", "USERDEFINED", "NOTDEFINED")

class IfcElementCompositionEnum(str):
    items: tuple = ("COMPLEX", "ELEMENT", "PARTIAL")

class IfcEngineTypeEnum(str):
    items: tuple = ("EXTERNALCOMBUSTION", "INTERNALCOMBUSTION", "USERDEFINED", "NOTDEFINED")

class IfcEvaporativeCoolerTypeEnum(str):
    items: tuple = (
        "DIRECTEVAPORATIVERANDOMMEDIAAIRCOOLER",
        "DIRECTEVAPORATIVERIGIDMEDIAAIRCOOLER",
        "DIRECTEVAPORATIVESLINGERSPACKAGEDAIRCOOLER",
        "DIRECTEVAPORATIVEPACKAGEDROTARYAIRCOOLER",
        "DIRECTEVAPORATIVEAIRWASHER",
        "INDIRECTEVAPORATIVEPACKAGEAIRCOOLER",
        "INDIRECTEVAPORATIVEWETCOIL",
        "INDIRECTEVAPORATIVECOOLINGTOWERORCOILCOOLER",
        "INDIRECTDIRECTCOMBINATION",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcEvaporatorTypeEnum(str):
    items: tuple = (
        "DIRECTEXPANSION",
        "DIRECTEXPANSIONSHELLANDTUBE",
        "DIRECTEXPANSIONTUBEINTUBE",
        "DIRECTEXPANSIONBRAZEDPLATE",
        "FLOODEDSHELLANDTUBE",
        "SHELLANDCOIL",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcEventTriggerTypeEnum(str):
    items: tuple = ("EVENTRULE", "EVENTMESSAGE", "EVENTTIME", "EVENTCOMPLEX", "USERDEFINED", "NOTDEFINED")

class IfcEventTypeEnum(str):
    items: tuple = ("STARTEVENT", "ENDEVENT", "INTERMEDIATEEVENT", "USERDEFINED", "NOTDEFINED")

class IfcExternalSpatialElementTypeEnum(str):
    items: tuple = ("EXTERNAL", "EXTERNAL_EARTH", "EXTERNAL_WATER", "EXTERNAL_FIRE", "USERDEFINED", "NOTDEFINED")

class IfcFanTypeEnum(str):
    items: tuple = (
        "CENTRIFUGALFORWARDCURVED",
        "CENTRIFUGALRADIAL",
        "CENTRIFUGALBACKWARDINCLINEDCURVED",
        "CENTRIFUGALAIRFOIL",
        "TUBEAXIAL",
        "VANEAXIAL",
        "PROPELLORAXIAL",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcFastenerTypeEnum(str):
    items: tuple = ("GLUE", "MORTAR", "WELD", "USERDEFINED", "NOTDEFINED")

class IfcFilterTypeEnum(str):
    items: tuple = ("AIRPARTICLEFILTER", "COMPRESSEDAIRFILTER", "ODORFILTER", "OILFILTER", "STRAINER", "WATERFILTER", "USERDEFINED", "NOTDEFINED")

class IfcFireSuppressionTerminalTypeEnum(str):
    items: tuple = ("BREECHINGINLET", "FIREHYDRANT", "HOSEREEL", "SPRINKLER", "SPRINKLERDEFLECTOR", "USERDEFINED", "NOTDEFINED")

class IfcFlowDirectionEnum(str):
    items: tuple = ("SOURCE", "SINK", "SOURCEANDSINK", "NOTDEFINED")

class IfcFlowInstrumentTypeEnum(str):
    items: tuple = (
        "PRESSUREGAUGE",
        "THERMOMETER",
        "AMMETER",
        "FREQUENCYMETER",
        "POWERFACTORMETER",
        "PHASEANGLEMETER",
        "VOLTMETER_PEAK",
        "VOLTMETER_RMS",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcFlowMeterTypeEnum(str):
    items: tuple = ("ENERGYMETER", "GASMETER", "OILMETER", "WATERMETER", "USERDEFINED", "NOTDEFINED")

class IfcFootingTypeEnum(str):
    items: tuple = ("CAISSON_FOUNDATION", "FOOTING_BEAM", "PAD_FOOTING", "PILE_CAP", "STRIP_FOOTING", "USERDEFINED", "NOTDEFINED")

class IfcFurnitureTypeEnum(str):
    items: tuple = ("CHAIR", "TABLE", "DESK", "BED", "FILECABINET", "SHELF", "SOFA", "USERDEFINED", "NOTDEFINED")

class IfcGeographicElementTypeEnum(str):
    items: tuple = ("TERRAIN", "USERDEFINED", "NOTDEFINED")

class IfcGeometricProjectionEnum(str):
    items: tuple = ("GRAPH_VIEW", "SKETCH_VIEW", "MODEL_VIEW", "PLAN_VIEW", "REFLECTED_PLAN_VIEW", "SECTION_VIEW", "ELEVATION_VIEW", "USERDEFINED", "NOTDEFINED")

class IfcGlobalOrLocalEnum(str):
    items: tuple = ("GLOBAL_COORDS", "LOCAL_COORDS")

class IfcGridTypeEnum(str):
    items: tuple = ("RECTANGULAR", "RADIAL", "TRIANGULAR", "IRREGULAR", "USERDEFINED", "NOTDEFINED")

class IfcHeatExchangerTypeEnum(str):
    items: tuple = ("PLATE", "SHELLANDTUBE", "USERDEFINED", "NOTDEFINED")

class IfcHumidifierTypeEnum(str):
    items: tuple = (
        "STEAMINJECTION",
        "ADIABATICAIRWASHER",
        "ADIABATICPAN",
        "ADIABATICWETTEDELEMENT",
        "ADIABATICATOMIZING",
        "ADIABATICULTRASONIC",
        "ADIABATICRIGIDMEDIA",
        "ADIABATICCOMPRESSEDAIRNOZZLE",
        "ASSISTEDELECTRIC",
        "ASSISTEDNATURALGAS",
        "ASSISTEDPROPANE",
        "ASSISTEDBUTANE",
        "ASSISTEDSTEAM",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcInterceptorTypeEnum(str):
    items: tuple = ("CYCLONIC", "GREASE", "OIL", "PETROL", "USERDEFINED", "NOTDEFINED")

class IfcInternalOrExternalEnum(str):
    items: tuple = ("INTERNAL", "EXTERNAL", "EXTERNAL_EARTH", "EXTERNAL_WATER", "EXTERNAL_FIRE", "NOTDEFINED")

class IfcInventoryTypeEnum(str):
    items: tuple = ("ASSETINVENTORY", "SPACEINVENTORY", "FURNITUREINVENTORY", "USERDEFINED", "NOTDEFINED")

class IfcJunctionBoxTypeEnum(str):
    items: tuple = ("DATA", "POWER", "USERDEFINED", "NOTDEFINED")

class IfcKnotType(str):
    items: tuple = ("UNIFORM_KNOTS", "QUASI_UNIFORM_KNOTS", "PIECEWISE_BEZIER_KNOTS", "UNSPECIFIED")

class IfcLaborResourceTypeEnum(str):
    items: tuple = (
        "ADMINISTRATION",
        "CARPENTRY",
        "CLEANING",
        "CONCRETE",
        "DRYWALL",
        "ELECTRIC",
        "FINISHING",
        "FLOORING",
        "GENERAL",
        "HVAC",
        "LANDSCAPING",
        "MASONRY",
        "PAINTING",
        "PAVING",
        "PLUMBING",
        "ROOFING",
        "SITEGRADING",
        "STEELWORK",
        "SURVEYING",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcLampTypeEnum(str):
    items: tuple = (
        "COMPACTFLUORESCENT",
        "FLUORESCENT",
        "HALOGEN",
        "HIGHPRESSUREMERCURY",
        "HIGHPRESSURESODIUM",
        "LED",
        "METALHALIDE",
        "OLED",
        "TUNGSTENFILAMENT",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcLayerSetDirectionEnum(str):
    items: tuple = ("AXIS1", "AXIS2", "AXIS3")

class IfcLightDistributionCurveEnum(str):
    items: tuple = ("TYPE_A", "TYPE_B", "TYPE_C", "NOTDEFINED")

class IfcLightEmissionSourceEnum(str):
    items: tuple = (
        "COMPACTFLUORESCENT",
        "FLUORESCENT",
        "HIGHPRESSUREMERCURY",
        "HIGHPRESSURESODIUM",
        "LIGHTEMITTINGDIODE",
        "LOWPRESSURESODIUM",
        "LOWVOLTAGEHALOGEN",
        "MAINVOLTAGEHALOGEN",
        "METALHALIDE",
        "TUNGSTENFILAMENT",
        "NOTDEFINED",
    )

class IfcLightFixtureTypeEnum(str):
    items: tuple = ("POINTSOURCE", "DIRECTIONSOURCE", "SECURITYLIGHTING", "USERDEFINED", "NOTDEFINED")

class IfcLoadGroupTypeEnum(str):
    items: tuple = ("LOAD_GROUP", "LOAD_CASE", "LOAD_COMBINATION", "USERDEFINED", "NOTDEFINED")

class IfcLogicalOperatorEnum(str):
    items: tuple = ("LOGICALAND", "LOGICALOR", "LOGICALXOR", "LOGICALNOTAND", "LOGICALNOTOR")

class IfcMechanicalFastenerTypeEnum(str):
    items: tuple = ("ANCHORBOLT", "BOLT", "DOWEL", "NAIL", "NAILPLATE", "RIVET", "SCREW", "SHEARCONNECTOR", "STAPLE", "STUDSHEARCONNECTOR", "USERDEFINED", "NOTDEFINED")

class IfcMedicalDeviceTypeEnum(str):
    items: tuple = ("AIRSTATION", "FEEDAIRUNIT", "OXYGENGENERATOR", "OXYGENPLANT", "VACUUMSTATION", "USERDEFINED", "NOTDEFINED")

class IfcMemberTypeEnum(str):
    items: tuple = ("BRACE", "CHORD", "COLLAR", "MEMBER", "MULLION", "PLATE", "POST", "PURLIN", "RAFTER", "STRINGER", "STRUT", "STUD", "USERDEFINED", "NOTDEFINED")

class IfcMotorConnectionTypeEnum(str):
    items: tuple = ("BELTDRIVE", "COUPLING", "DIRECTDRIVE", "USERDEFINED", "NOTDEFINED")

class IfcNullStyle(str):
    items: tuple = ("NULL",)

class IfcObjectTypeEnum(str):
    items: tuple = ("PRODUCT", "PROCESS", "CONTROL", "RESOURCE", "ACTOR", "GROUP", "PROJECT", "NOTDEFINED")

class IfcObjectiveEnum(str):
    items: tuple = (
        "CODECOMPLIANCE",
        "CODEWAIVER",
        "DESIGNINTENT",
        "EXTERNAL",
        "HEALTHANDSAFETY",
        "MERGECONFLICT",
        "MODELVIEW",
        "PARAMETER",
        "REQUIREMENT",
        "SPECIFICATION",
        "TRIGGERCONDITION",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcOccupantTypeEnum(str):
    items: tuple = ("ASSIGNEE", "ASSIGNOR", "LESSEE", "LESSOR", "LETTINGAGENT", "OWNER", "TENANT", "USERDEFINED", "NOTDEFINED")

class IfcOpeningElementTypeEnum(str):
    items: tuple = ("OPENING", "RECESS", "USERDEFINED", "NOTDEFINED")

class IfcOutletTypeEnum(str):
    items: tuple = ("AUDIOVISUALOUTLET", "COMMUNICATIONSOUTLET", "POWEROUTLET", "DATAOUTLET", "TELEPHONEOUTLET", "USERDEFINED", "NOTDEFINED")

class IfcPerformanceHistoryTypeEnum(str):
    items: tuple = ("USERDEFINED", "NOTDEFINED")

class IfcPermeableCoveringOperationEnum(str):
    items: tuple = ("GRILL", "LOUVER", "SCREEN", "USERDEFINED", "NOTDEFINED")

class IfcPermitTypeEnum(str):
    items: tuple = ("ACCESS", "BUILDING", "WORK", "USERDEFINED", "NOTDEFINED")

class IfcPhysicalOrVirtualEnum(str):
    items: tuple = ("PHYSICAL", "VIRTUAL", "NOTDEFINED")

class IfcPileConstructionEnum(str):
    items: tuple = ("CAST_IN_PLACE", "COMPOSITE", "PRECAST_CONCRETE", "PREFAB_STEEL", "USERDEFINED", "NOTDEFINED")

class IfcPileTypeEnum(str):
    items: tuple = ("BORED", "DRIVEN", "JETGROUTING", "COHESION", "FRICTION", "SUPPORT", "USERDEFINED", "NOTDEFINED")

class IfcPipeFittingTypeEnum(str):
    items: tuple = ("BEND", "CONNECTOR", "ENTRY", "EXIT", "JUNCTION", "OBSTRUCTION", "TRANSITION", "USERDEFINED", "NOTDEFINED")

class IfcPipeSegmentTypeEnum(str):
    items: tuple = ("CULVERT", "FLEXIBLESEGMENT", "RIGIDSEGMENT", "GUTTER", "SPOOL", "USERDEFINED", "NOTDEFINED")

class IfcPlateTypeEnum(str):
    items: tuple = ("CURTAIN_PANEL", "SHEET", "USERDEFINED", "NOTDEFINED")

class IfcPreferredSurfaceCurveRepresentation(str):
    items: tuple = ("CURVE3D", "PCURVE_S1", "PCURVE_S2")

class IfcProcedureTypeEnum(str):
    items: tuple = ("ADVICE_CAUTION", "ADVICE_NOTE", "ADVICE_WARNING", "CALIBRATION", "DIAGNOSTIC", "SHUTDOWN", "STARTUP", "USERDEFINED", "NOTDEFINED")

class IfcProfileTypeEnum(str):
    items: tuple = ("CURVE", "AREA")

class IfcProjectOrderTypeEnum(str):
    items: tuple = ("CHANGEORDER", "MAINTENANCEWORKORDER", "MOVEORDER", "PURCHASEORDER", "WORKORDER", "USERDEFINED", "NOTDEFINED")

class IfcProjectedOrTrueLengthEnum(str):
    items: tuple = ("PROJECTED_LENGTH", "TRUE_LENGTH")

class IfcProjectionElementTypeEnum(str):
    items: tuple = ("USERDEFINED", "NOTDEFINED")

class IfcPropertySetTemplateTypeEnum(str):
    items: tuple = (
        "PSET_TYPEDRIVENONLY",
        "PSET_TYPEDRIVENOVERRIDE",
        "PSET_OCCURRENCEDRIVEN",
        "PSET_PERFORMANCEDRIVEN",
        "QTO_TYPEDRIVENONLY",
        "QTO_TYPEDRIVENOVERRIDE",
        "QTO_OCCURRENCEDRIVEN",
        "NOTDEFINED",
    )

class IfcProtectiveDeviceTrippingUnitTypeEnum(str):
    items: tuple = ("ELECTRONIC", "ELECTROMAGNETIC", "RESIDUALCURRENT", "THERMAL", "USERDEFINED", "NOTDEFINED")

class IfcProtectiveDeviceTypeEnum(str):
    items: tuple = (
        "CIRCUITBREAKER",
        "EARTHLEAKAGECIRCUITBREAKER",
        "EARTHINGSWITCH",
        "FUSEDISCONNECTOR",
        "RESIDUALCURRENTCIRCUITBREAKER",
        "RESIDUALCURRENTSWITCH",
        "VARISTOR",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcPumpTypeEnum(str):
    items: tuple = ("CIRCULATOR", "ENDSUCTION", "SPLITCASE", "SUBMERSIBLEPUMP", "SUMPPUMP", "VERTICALINLINE", "VERTICALTURBINE", "USERDEFINED", "NOTDEFINED")

class IfcRailingTypeEnum(str):
    items: tuple = ("HANDRAIL", "GUARDRAIL", "BALUSTRADE", "USERDEFINED", "NOTDEFINED")

class IfcRampFlightTypeEnum(str):
    items: tuple = ("STRAIGHT", "SPIRAL", "USERDEFINED", "NOTDEFINED")

class IfcRampTypeEnum(str):
    items: tuple = ("STRAIGHT_RUN_RAMP", "TWO_STRAIGHT_RUN_RAMP", "QUARTER_TURN_RAMP", "TWO_QUARTER_TURN_RAMP", "HALF_TURN_RAMP", "SPIRAL_RAMP", "USERDEFINED", "NOTDEFINED")

class IfcRecurrenceTypeEnum(str):
    items: tuple = ("DAILY", "WEEKLY", "MONTHLY_BY_DAY_OF_MONTH", "MONTHLY_BY_POSITION", "BY_DAY_COUNT", "BY_WEEKDAY_COUNT", "YEARLY_BY_DAY_OF_MONTH", "YEARLY_BY_POSITION")

class IfcReflectanceMethodEnum(str):
    items: tuple = ("BLINN", "FLAT", "GLASS", "MATT", "METAL", "MIRROR", "PHONG", "PLASTIC", "STRAUSS", "NOTDEFINED")

class IfcReinforcingBarRoleEnum(str):
    items: tuple = ("MAIN", "SHEAR", "LIGATURE", "STUD", "PUNCHING", "EDGE", "RING", "ANCHORING", "USERDEFINED", "NOTDEFINED")

class IfcReinforcingBarSurfaceEnum(str):
    items: tuple = ("PLAIN", "TEXTURED")

class IfcReinforcingBarTypeEnum(str):
    items: tuple = ("ANCHORING", "EDGE", "LIGATURE", "MAIN", "PUNCHING", "RING", "SHEAR", "STUD", "USERDEFINED", "NOTDEFINED")

class IfcReinforcingMeshTypeEnum(str):
    items: tuple = ("USERDEFINED", "NOTDEFINED")

class IfcRoleEnum(str):
    items: tuple = (
        "SUPPLIER",
        "MANUFACTURER",
        "CONTRACTOR",
        "SUBCONTRACTOR",
        "ARCHITECT",
        "STRUCTURALENGINEER",
        "COSTENGINEER",
        "CLIENT",
        "BUILDINGOWNER",
        "BUILDINGOPERATOR",
        "MECHANICALENGINEER",
        "ELECTRICALENGINEER",
        "PROJECTMANAGER",
        "FACILITIESMANAGER",
        "CIVILENGINEER",
        "COMMISSIONINGENGINEER",
        "ENGINEER",
        "OWNER",
        "CONSULTANT",
        "CONSTRUCTIONMANAGER",
        "FIELDCONSTRUCTIONMANAGER",
        "RESELLER",
        "USERDEFINED",
    )

class IfcRoofTypeEnum(str):
    items: tuple = (
        "FLAT_ROOF",
        "SHED_ROOF",
        "GABLE_ROOF",
        "HIP_ROOF",
        "HIPPED_GABLE_ROOF",
        "GAMBREL_ROOF",
        "MANSARD_ROOF",
        "BARREL_ROOF",
        "RAINBOW_ROOF",
        "BUTTERFLY_ROOF",
        "PAVILION_ROOF",
        "DOME_ROOF",
        "FREEFORM",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcSIPrefix(str):
    items: tuple = ("EXA", "PETA", "TERA", "GIGA", "MEGA", "KILO", "HECTO", "DECA", "DECI", "CENTI", "MILLI", "MICRO", "NANO", "PICO", "FEMTO", "ATTO")

class IfcSIUnitName(str):
    items: tuple = (
        "AMPERE",
        "BECQUEREL",
        "CANDELA",
        "COULOMB",
        "CUBIC_METRE",
        "DEGREE_CELSIUS",
        "FARAD",
        "GRAM",
        "GRAY",
        "HENRY",
        "HERTZ",
        "JOULE",
        "KELVIN",
        "LUMEN",
        "LUX",
        "METRE",
        "MOLE",
        "NEWTON",
        "OHM",
        "PASCAL",
        "RADIAN",
        "SECOND",
        "SIEMENS",
        "SIEVERT",
        "SQUARE_METRE",
        "STERADIAN",
        "TESLA",
        "VOLT",
        "WATT",
        "WEBER",
    )

class IfcSanitaryTerminalTypeEnum(str):
    items: tuple = ("BATH", "BIDET", "CISTERN", "SHOWER", "SINK", "SANITARYFOUNTAIN", "TOILETPAN", "URINAL", "WASHHANDBASIN", "WCSEAT", "USERDEFINED", "NOTDEFINED")

class IfcSectionTypeEnum(str):
    items: tuple = ("UNIFORM", "TAPERED")

class IfcSensorTypeEnum(str):
    items: tuple = (
        "COSENSOR",
        "CO2SENSOR",
        "CONDUCTANCESENSOR",
        "CONTACTSENSOR",
        "FIRESENSOR",
        "FLOWSENSOR",
        "FROSTSENSOR",
        "GASSENSOR",
        "HEATSENSOR",
        "HUMIDITYSENSOR",
        "IDENTIFIERSENSOR",
        "IONCONCENTRATIONSENSOR",
        "LEVELSENSOR",
        "LIGHTSENSOR",
        "MOISTURESENSOR",
        "MOVEMENTSENSOR",
        "PHSENSOR",
        "PRESSURESENSOR",
        "RADIATIONSENSOR",
        "RADIOACTIVITYSENSOR",
        "SMOKESENSOR",
        "SOUNDSENSOR",
        "TEMPERATURESENSOR",
        "WINDSENSOR",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcSequenceEnum(str):
    items: tuple = ("START_START", "START_FINISH", "FINISH_START", "FINISH_FINISH", "USERDEFINED", "NOTDEFINED")

class IfcShadingDeviceTypeEnum(str):
    items: tuple = ("JALOUSIE", "SHUTTER", "AWNING", "USERDEFINED", "NOTDEFINED")

class IfcSimplePropertyTemplateTypeEnum(str):
    items: tuple = (
        "P_SINGLEVALUE",
        "P_ENUMERATEDVALUE",
        "P_BOUNDEDVALUE",
        "P_LISTVALUE",
        "P_TABLEVALUE",
        "P_REFERENCEVALUE",
        "Q_LENGTH",
        "Q_AREA",
        "Q_VOLUME",
        "Q_COUNT",
        "Q_WEIGHT",
        "Q_TIME",
    )

class IfcSlabTypeEnum(str):
    items: tuple = ("FLOOR", "ROOF", "LANDING", "BASESLAB", "USERDEFINED", "NOTDEFINED")

class IfcSolarDeviceTypeEnum(str):
    items: tuple = ("SOLARCOLLECTOR", "SOLARPANEL", "USERDEFINED", "NOTDEFINED")

class IfcSpaceHeaterTypeEnum(str):
    items: tuple = ("CONVECTOR", "RADIATOR", "USERDEFINED", "NOTDEFINED")

class IfcSpaceTypeEnum(str):
    items: tuple = ("SPACE", "PARKING", "GFA", "INTERNAL", "EXTERNAL", "USERDEFINED", "NOTDEFINED")

class IfcSpatialZoneTypeEnum(str):
    items: tuple = ("CONSTRUCTION", "FIRESAFETY", "LIGHTING", "OCCUPANCY", "SECURITY", "THERMAL", "TRANSPORT", "VENTILATION", "USERDEFINED", "NOTDEFINED")

class IfcStackTerminalTypeEnum(str):
    items: tuple = ("BIRDCAGE", "COWL", "RAINWATERHOPPER", "USERDEFINED", "NOTDEFINED")

class IfcStairFlightTypeEnum(str):
    items: tuple = ("STRAIGHT", "WINDER", "SPIRAL", "CURVED", "FREEFORM", "USERDEFINED", "NOTDEFINED")

class IfcStairTypeEnum(str):
    items: tuple = (
        "STRAIGHT_RUN_STAIR",
        "TWO_STRAIGHT_RUN_STAIR",
        "QUARTER_WINDING_STAIR",
        "QUARTER_TURN_STAIR",
        "HALF_WINDING_STAIR",
        "HALF_TURN_STAIR",
        "TWO_QUARTER_WINDING_STAIR",
        "TWO_QUARTER_TURN_STAIR",
        "THREE_QUARTER_WINDING_STAIR",
        "THREE_QUARTER_TURN_STAIR",
        "SPIRAL_STAIR",
        "DOUBLE_RETURN_STAIR",
        "CURVED_RUN_STAIR",
        "TWO_CURVED_RUN_STAIR",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcStateEnum(str):
    items: tuple = ("READWRITE", "READONLY", "LOCKED", "READWRITELOCKED", "READONLYLOCKED")

class IfcStructuralCurveActivityTypeEnum(str):
    items: tuple = ("CONST", "LINEAR", "POLYGONAL", "EQUIDISTANT", "SINUS", "PARABOLA", "DISCRETE", "USERDEFINED", "NOTDEFINED")

class IfcStructuralCurveMemberTypeEnum(str):
    items: tuple = ("RIGID_JOINED_MEMBER", "PIN_JOINED_MEMBER", "CABLE", "TENSION_MEMBER", "COMPRESSION_MEMBER", "USERDEFINED", "NOTDEFINED")

class IfcStructuralSurfaceActivityTypeEnum(str):
    items: tuple = ("CONST", "BILINEAR", "DISCRETE", "ISOCONTOUR", "USERDEFINED", "NOTDEFINED")

class IfcStructuralSurfaceMemberTypeEnum(str):
    items: tuple = ("BENDING_ELEMENT", "MEMBRANE_ELEMENT", "SHELL", "USERDEFINED", "NOTDEFINED")

class IfcSubContractResourceTypeEnum(str):
    items: tuple = ("PURCHASE", "WORK", "USERDEFINED", "NOTDEFINED")

class IfcSurfaceFeatureTypeEnum(str):
    items: tuple = ("MARK", "TAG", "TREATMENT", "USERDEFINED", "NOTDEFINED")

class IfcSurfaceSide(str):
    items: tuple = ("POSITIVE", "NEGATIVE", "BOTH")

class IfcSwitchingDeviceTypeEnum(str):
    items: tuple = (
        "CONTACTOR",
        "DIMMERSWITCH",
        "EMERGENCYSTOP",
        "KEYPAD",
        "MOMENTARYSWITCH",
        "SELECTORSWITCH",
        "STARTER",
        "SWITCHDISCONNECTOR",
        "TOGGLESWITCH",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcSystemFurnitureElementTypeEnum(str):
    items: tuple = ("PANEL", "WORKSURFACE", "USERDEFINED", "NOTDEFINED")

class IfcTankTypeEnum(str):
    items: tuple = ("BASIN", "BREAKPRESSURE", "EXPANSION", "FEEDANDEXPANSION", "PRESSUREVESSEL", "STORAGE", "VESSEL", "USERDEFINED", "NOTDEFINED")

class IfcTaskDurationEnum(str):
    items: tuple = ("ELAPSEDTIME", "WORKTIME", "NOTDEFINED")

class IfcTaskTypeEnum(str):
    items: tuple = (
        "ATTENDANCE",
        "CONSTRUCTION",
        "DEMOLITION",
        "DISMANTLE",
        "DISPOSAL",
        "INSTALLATION",
        "LOGISTIC",
        "MAINTENANCE",
        "MOVE",
        "OPERATION",
        "REMOVAL",
        "RENOVATION",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcTendonAnchorTypeEnum(str):
    items: tuple = ("COUPLER", "FIXED_END", "TENSIONING_END", "USERDEFINED", "NOTDEFINED")

class IfcTendonTypeEnum(str):
    items: tuple = ("BAR", "COATED", "STRAND", "WIRE", "USERDEFINED", "NOTDEFINED")

class IfcTextPath(str):
    items: tuple = ("LEFT", "RIGHT", "UP", "DOWN")

class IfcTimeSeriesDataTypeEnum(str):
    items: tuple = ("CONTINUOUS", "DISCRETE", "DISCRETEBINARY", "PIECEWISEBINARY", "PIECEWISECONSTANT", "PIECEWISECONTINUOUS", "NOTDEFINED")

class IfcTransformerTypeEnum(str):
    items: tuple = ("CURRENT", "FREQUENCY", "INVERTER", "RECTIFIER", "VOLTAGE", "USERDEFINED", "NOTDEFINED")

class IfcTransitionCode(str):
    items: tuple = ("DISCONTINUOUS", "CONTINUOUS", "CONTSAMEGRADIENT", "CONTSAMEGRADIENTSAMECURVATURE")

class IfcTransportElementTypeEnum(str):
    items: tuple = ("ELEVATOR", "ESCALATOR", "MOVINGWALKWAY", "CRANEWAY", "LIFTINGGEAR", "USERDEFINED", "NOTDEFINED")

class IfcTrimmingPreference(str):
    items: tuple = ("CARTESIAN", "PARAMETER", "UNSPECIFIED")

class IfcTubeBundleTypeEnum(str):
    items: tuple = ("FINNED", "USERDEFINED", "NOTDEFINED")

class IfcUnitEnum(str):
    items: tuple = (
        "ABSORBEDDOSEUNIT",
        "AMOUNTOFSUBSTANCEUNIT",
        "AREAUNIT",
        "DOSEEQUIVALENTUNIT",
        "ELECTRICCAPACITANCEUNIT",
        "ELECTRICCHARGEUNIT",
        "ELECTRICCONDUCTANCEUNIT",
        "ELECTRICCURRENTUNIT",
        "ELECTRICRESISTANCEUNIT",
        "ELECTRICVOLTAGEUNIT",
        "ENERGYUNIT",
        "FORCEUNIT",
        "FREQUENCYUNIT",
        "ILLUMINANCEUNIT",
        "INDUCTANCEUNIT",
        "LENGTHUNIT",
        "LUMINOUSFLUXUNIT",
        "LUMINOUSINTENSITYUNIT",
        "MAGNETICFLUXDENSITYUNIT",
        "MAGNETICFLUXUNIT",
        "MASSUNIT",
        "PLANEANGLEUNIT",
        "POWERUNIT",
        "PRESSUREUNIT",
        "RADIOACTIVITYUNIT",
        "SOLIDANGLEUNIT",
        "THERMODYNAMICTEMPERATUREUNIT",
        "TIMEUNIT",
        "VOLUMEUNIT",
        "USERDEFINED",
    )

class IfcUnitaryControlElementTypeEnum(str):
    items: tuple = ("ALARMPANEL", "CONTROLPANEL", "GASDETECTIONPANEL", "INDICATORPANEL", "MIMICPANEL", "HUMIDISTAT", "THERMOSTAT", "WEATHERSTATION", "USERDEFINED", "NOTDEFINED")

class IfcUnitaryEquipmentTypeEnum(str):
    items: tuple = ("AIRHANDLER", "AIRCONDITIONINGUNIT", "DEHUMIDIFIER", "SPLITSYSTEM", "ROOFTOPUNIT", "USERDEFINED", "NOTDEFINED")

class IfcValveTypeEnum(str):
    items: tuple = (
        "AIRRELEASE",
        "ANTIVACUUM",
        "CHANGEOVER",
        "CHECK",
        "COMMISSIONING",
        "DIVERTING",
        "DRAWOFFCOCK",
        "DOUBLECHECK",
        "DOUBLEREGULATING",
        "FAUCET",
        "FLUSHING",
        "GASCOCK",
        "GASTAP",
        "ISOLATING",
        "MIXING",
        "PRESSUREREDUCING",
        "PRESSURERELIEF",
        "REGULATING",
        "SAFETYCUTOFF",
        "STEAMTRAP",
        "STOPCOCK",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcVibrationIsolatorTypeEnum(str):
    items: tuple = ("COMPRESSION", "SPRING", "USERDEFINED", "NOTDEFINED")

class IfcVoidingFeatureTypeEnum(str):
    items: tuple = ("CUTOUT", "NOTCH", "HOLE", "MITER", "CHAMFER", "EDGE", "USERDEFINED", "NOTDEFINED")

class IfcWallTypeEnum(str):
    items: tuple = ("MOVABLE", "PARAPET", "PARTITIONING", "PLUMBINGWALL", "SHEAR", "SOLIDWALL", "STANDARD", "POLYGONAL", "ELEMENTEDWALL", "USERDEFINED", "NOTDEFINED")

class IfcWasteTerminalTypeEnum(str):
    items: tuple = ("FLOORTRAP", "FLOORWASTE", "GULLYSUMP", "GULLYTRAP", "ROOFDRAIN", "WASTEDISPOSALUNIT", "WASTETRAP", "USERDEFINED", "NOTDEFINED")

class IfcWindowPanelOperationEnum(str):
    items: tuple = (
        "SIDEHUNGRIGHTHAND",
        "SIDEHUNGLEFTHAND",
        "TILTANDTURNRIGHTHAND",
        "TILTANDTURNLEFTHAND",
        "TOPHUNG",
        "BOTTOMHUNG",
        "PIVOTHORIZONTAL",
        "PIVOTVERTICAL",
        "SLIDINGHORIZONTAL",
        "SLIDINGVERTICAL",
        "REMOVABLECASEMENT",
        "FIXEDCASEMENT",
        "OTHEROPERATION",
        "NOTDEFINED",
    )

class IfcWindowPanelPositionEnum(str):
    items: tuple = ("LEFT", "MIDDLE", "RIGHT", "BOTTOM", "TOP", "NOTDEFINED")

class IfcWindowStyleConstructionEnum(str):
    items: tuple = ("ALUMINIUM", "HIGH_GRADE_STEEL", "STEEL", "WOOD", "ALUMINIUM_WOOD", "PLASTIC", "OTHER_CONSTRUCTION", "NOTDEFINED")

class IfcWindowStyleOperationEnum(str):
    items: tuple = (
        "SINGLE_PANEL",
        "DOUBLE_PANEL_VERTICAL",
        "DOUBLE_PANEL_HORIZONTAL",
        "TRIPLE_PANEL_VERTICAL",
        "TRIPLE_PANEL_BOTTOM",
        "TRIPLE_PANEL_TOP",
        "TRIPLE_PANEL_LEFT",
        "TRIPLE_PANEL_RIGHT",
        "TRIPLE_PANEL_HORIZONTAL",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcWindowTypeEnum(str):
    items: tuple = ("WINDOW", "SKYLIGHT", "LIGHTDOME", "USERDEFINED", "NOTDEFINED")

class IfcWindowTypePartitioningEnum(str):
    items: tuple = (
        "SINGLE_PANEL",
        "DOUBLE_PANEL_VERTICAL",
        "DOUBLE_PANEL_HORIZONTAL",
        "TRIPLE_PANEL_VERTICAL",
        "TRIPLE_PANEL_BOTTOM",
        "TRIPLE_PANEL_TOP",
        "TRIPLE_PANEL_LEFT",
        "TRIPLE_PANEL_RIGHT",
        "TRIPLE_PANEL_HORIZONTAL",
        "USERDEFINED",
        "NOTDEFINED",
    )

class IfcWorkCalendarTypeEnum(str):
    items: tuple = ("FIRSTSHIFT", "SECONDSHIFT", "THIRDSHIFT", "USERDEFINED", "NOTDEFINED")

class IfcWorkPlanTypeEnum(str):
    items: tuple = ("ACTUAL", "BASELINE", "PLANNED", "USERDEFINED", "NOTDEFINED")

class IfcWorkScheduleTypeEnum(str):
    items: tuple = ("ACTUAL", "BASELINE", "PLANNED", "USERDEFINED", "NOTDEFINED")

class IfcActorRole:
    """Wrapper class for IfcActorRole."""

    Role: "IfcRoleEnum"
    UserDefinedRole: Optional[str]
    Description: Optional[str]
    def HasExternalReference(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...

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
    AppliedValue: Optional[Union["IfcMeasureWithUnit", "IfcReference", float, list[int], int, list[float], str, bytes, bool]]
    UnitBasis: Optional["IfcMeasureWithUnit"]
    ApplicableDate: Optional[str]
    FixedUntilDate: Optional[str]
    Category: Optional[str]
    Condition: Optional[str]
    ArithmeticOperator: Optional["IfcArithmeticOperatorEnum"]
    Components: Optional[list["IfcAppliedValue"]]
    def HasExternalReference(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...

class IfcApproval:
    """Wrapper class for IfcApproval."""

    Identifier: Optional[str]
    Name: Optional[str]
    Description: Optional[str]
    TimeOfApproval: Optional[str]
    Status: Optional[str]
    Level: Optional[str]
    Qualifier: Optional[str]
    RequestingApproval: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    GivingApproval: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    def HasExternalReferences(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...
    def ApprovedObjects(self) -> tuple["IfcRelAssociatesApproval", ...]: ...
    def ApprovedResources(self) -> tuple["IfcResourceApprovalRelationship", ...]: ...
    def IsRelatedWith(self) -> tuple["IfcApprovalRelationship", ...]: ...
    def Relates(self) -> tuple["IfcApprovalRelationship", ...]: ...

class IfcApprovalRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcApprovalRelationship."""

    RelatingApproval: "IfcApproval"
    RelatedApprovals: list["IfcApproval"]

class IfcBoundaryCondition:
    """Wrapper class for IfcBoundaryCondition."""

    Name: Optional[str]

class IfcClassification(IfcExternalInformation):
    """Wrapper class for IfcClassification."""

    Source: Optional[str]
    Edition: Optional[str]
    EditionDate: Optional[str]
    Name: str
    Description: Optional[str]
    Location: Optional[str]
    ReferenceTokens: Optional[list[str]]
    def ClassificationForObjects(self) -> tuple["IfcRelAssociatesClassification", ...]: ...
    def HasReferences(self) -> tuple["IfcClassificationReference", ...]: ...

class IfcColourSpecification(IfcPresentationItem):
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
    CreationTime: Optional[str]
    UserDefinedGrade: Optional[str]
    def HasExternalReferences(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...
    def PropertiesForConstraint(self) -> tuple["IfcResourceConstraintRelationship", ...]: ...

class IfcCoordinateOperation:
    """Wrapper class for IfcCoordinateOperation."""

    SourceCRS: Union["IfcCoordinateReferenceSystem", "IfcGeometricRepresentationContext"]
    TargetCRS: "IfcCoordinateReferenceSystem"

class IfcCoordinateReferenceSystem:
    """Wrapper class for IfcCoordinateReferenceSystem."""

    Name: str
    Description: Optional[str]
    GeodeticDatum: Optional[str]
    VerticalDatum: Optional[str]
    def HasCoordinateOperation(self) -> tuple["IfcCoordinateOperation", ...]: ...

class IfcCurrencyRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcCurrencyRelationship."""

    RelatingMonetaryUnit: "IfcMonetaryUnit"
    RelatedMonetaryUnit: "IfcMonetaryUnit"
    ExchangeRate: float
    RateDateTime: Optional[str]
    RateSource: Optional["IfcLibraryInformation"]

class IfcCurveStyleFont(IfcPresentationItem):
    """Wrapper class for IfcCurveStyleFont."""

    Name: Optional[str]
    PatternList: list["IfcCurveStyleFontPattern"]

class IfcCurveStyleFontAndScaling(IfcPresentationItem):
    """Wrapper class for IfcCurveStyleFontAndScaling."""

    Name: Optional[str]
    CurveFont: Union["IfcCurveStyleFont", "IfcPreDefinedCurveFont"]
    CurveFontScaling: float

class IfcCurveStyleFontPattern(IfcPresentationItem):
    """Wrapper class for IfcCurveStyleFontPattern."""

    VisibleSegmentLength: float
    InvisibleSegmentLength: float

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

class IfcDocumentInformation(IfcExternalInformation):
    """Wrapper class for IfcDocumentInformation."""

    Identification: str
    Name: str
    Description: Optional[str]
    Location: Optional[str]
    Purpose: Optional[str]
    IntendedUse: Optional[str]
    Scope: Optional[str]
    Revision: Optional[str]
    DocumentOwner: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    Editors: Optional[list[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]]
    CreationTime: Optional[str]
    LastRevisionTime: Optional[str]
    ElectronicFormat: Optional[str]
    ValidFrom: Optional[str]
    ValidUntil: Optional[str]
    Confidentiality: Optional["IfcDocumentConfidentialityEnum"]
    Status: Optional["IfcDocumentStatusEnum"]
    def DocumentInfoForObjects(self) -> tuple["IfcRelAssociatesDocument", ...]: ...
    def HasDocumentReferences(self) -> tuple["IfcDocumentReference", ...]: ...
    def IsPointedTo(self) -> tuple["IfcDocumentInformationRelationship", ...]: ...
    def IsPointer(self) -> tuple["IfcDocumentInformationRelationship", ...]: ...

class IfcDocumentInformationRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcDocumentInformationRelationship."""

    RelatingDocument: "IfcDocumentInformation"
    RelatedDocuments: list["IfcDocumentInformation"]
    RelationshipType: Optional[str]

class IfcExternalInformation:
    """Wrapper class for IfcExternalInformation."""

    ...

class IfcExternalReference:
    """Wrapper class for IfcExternalReference."""

    Location: Optional[str]
    Identification: Optional[str]
    Name: Optional[str]
    def ExternalReferenceForResources(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...

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

    TimeStamp: str
    ListValues: list[Union[float, list[int], int, list[float], str, bytes, bool]]

class IfcLibraryInformation(IfcExternalInformation):
    """Wrapper class for IfcLibraryInformation."""

    Name: str
    Version: Optional[str]
    Publisher: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    VersionDate: Optional[str]
    Location: Optional[str]
    Description: Optional[str]
    def LibraryInfoForObjects(self) -> tuple["IfcRelAssociatesLibrary", ...]: ...
    def HasLibraryReferences(self) -> tuple["IfcLibraryReference", ...]: ...

class IfcLightDistributionData:
    """Wrapper class for IfcLightDistributionData."""

    MainPlaneAngle: float
    SecondaryPlaneAngle: list[float]
    LuminousIntensity: list[float]

class IfcLightIntensityDistribution:
    """Wrapper class for IfcLightIntensityDistribution."""

    LightDistributionCurve: "IfcLightDistributionCurveEnum"
    DistributionData: list["IfcLightDistributionData"]

class IfcMaterial(IfcMaterialDefinition):
    """Wrapper class for IfcMaterial."""

    Name: str
    Description: Optional[str]
    Category: Optional[str]
    def HasRepresentation(self) -> tuple["IfcMaterialDefinitionRepresentation", ...]: ...
    def IsRelatedWith(self) -> tuple["IfcMaterialRelationship", ...]: ...
    def RelatesTo(self) -> tuple["IfcMaterialRelationship", ...]: ...

class IfcMaterialClassificationRelationship:
    """Wrapper class for IfcMaterialClassificationRelationship."""

    MaterialClassifications: list[Union["IfcClassification", "IfcClassificationReference"]]
    ClassifiedMaterial: "IfcMaterial"

class IfcMaterialDefinition:
    """Wrapper class for IfcMaterialDefinition."""
    def AssociatedTo(self) -> tuple["IfcRelAssociatesMaterial", ...]: ...
    def HasExternalReferences(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...
    def HasProperties(self) -> tuple["IfcMaterialProperties", ...]: ...

class IfcMaterialLayer(IfcMaterialDefinition):
    """Wrapper class for IfcMaterialLayer."""

    Material: Optional["IfcMaterial"]
    LayerThickness: float
    IsVentilated: Optional[bool]
    Name: Optional[str]
    Description: Optional[str]
    Category: Optional[str]
    Priority: Optional[int]
    def ToMaterialLayerSet(self) -> tuple["IfcMaterialLayerSet", ...]: ...

class IfcMaterialLayerSet(IfcMaterialDefinition):
    """Wrapper class for IfcMaterialLayerSet."""

    MaterialLayers: list["IfcMaterialLayer"]
    LayerSetName: Optional[str]
    Description: Optional[str]

class IfcMaterialLayerSetUsage(IfcMaterialUsageDefinition):
    """Wrapper class for IfcMaterialLayerSetUsage."""

    ForLayerSet: "IfcMaterialLayerSet"
    LayerSetDirection: "IfcLayerSetDirectionEnum"
    DirectionSense: "IfcDirectionSenseEnum"
    OffsetFromReferenceLine: float
    ReferenceExtent: Optional[float]

class IfcMaterialList:
    """Wrapper class for IfcMaterialList."""

    Materials: list["IfcMaterial"]

class IfcMaterialProperties(IfcExtendedProperties):
    """Wrapper class for IfcMaterialProperties."""

    Material: "IfcMaterialDefinition"

class IfcMaterialUsageDefinition:
    """Wrapper class for IfcMaterialUsageDefinition."""
    def AssociatedTo(self) -> tuple["IfcRelAssociatesMaterial", ...]: ...

class IfcMeasureWithUnit:
    """Wrapper class for IfcMeasureWithUnit."""

    ValueComponent: Union[float, list[int], int, list[float], str, bytes, bool]
    UnitComponent: Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]

class IfcMonetaryUnit:
    """Wrapper class for IfcMonetaryUnit."""

    Currency: str

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

    Identification: Optional[str]
    Name: str
    Description: Optional[str]
    Roles: Optional[list["IfcActorRole"]]
    Addresses: Optional[list["IfcAddress"]]
    def IsRelatedBy(self) -> tuple["IfcOrganizationRelationship", ...]: ...
    def Relates(self) -> tuple["IfcOrganizationRelationship", ...]: ...
    def Engages(self) -> tuple["IfcPersonAndOrganization", ...]: ...

class IfcOrganizationRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcOrganizationRelationship."""

    RelatingOrganization: "IfcOrganization"
    RelatedOrganizations: list["IfcOrganization"]

class IfcOwnerHistory:
    """Wrapper class for IfcOwnerHistory."""

    OwningUser: "IfcPersonAndOrganization"
    OwningApplication: "IfcApplication"
    State: Optional["IfcStateEnum"]
    ChangeAction: Optional["IfcChangeActionEnum"]
    LastModifiedDate: Optional[int]
    LastModifyingUser: Optional["IfcPersonAndOrganization"]
    LastModifyingApplication: Optional["IfcApplication"]
    CreationDate: int

class IfcPerson:
    """Wrapper class for IfcPerson."""

    Identification: Optional[str]
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
    def HasExternalReferences(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...
    def PartOfComplex(self) -> tuple["IfcPhysicalComplexQuantity", ...]: ...

class IfcPreDefinedItem(IfcPresentationItem):
    """Wrapper class for IfcPreDefinedItem."""

    Name: str

class IfcPresentationItem:
    """Wrapper class for IfcPresentationItem."""

    ...

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

    Styles: list[Union["IfcCurveStyle", "IfcFillAreaStyle", "IfcNullStyle", "IfcSurfaceStyle", "IfcTextStyle"]]

class IfcProductRepresentation:
    """Wrapper class for IfcProductRepresentation."""

    Name: Optional[str]
    Description: Optional[str]
    Representations: list["IfcRepresentation"]

class IfcProfileDef:
    """Wrapper class for IfcProfileDef."""

    ProfileType: "IfcProfileTypeEnum"
    ProfileName: Optional[str]
    def HasExternalReference(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...
    def HasProperties(self) -> tuple["IfcProfileProperties", ...]: ...

class IfcProfileProperties(IfcExtendedProperties):
    """Wrapper class for IfcProfileProperties."""

    ProfileDefinition: "IfcProfileDef"

class IfcProperty(IfcPropertyAbstraction):
    """Wrapper class for IfcProperty."""

    Name: str
    Description: Optional[str]
    def PartOfPset(self) -> tuple["IfcPropertySet", ...]: ...
    def PropertyForDependance(self) -> tuple["IfcPropertyDependencyRelationship", ...]: ...
    def PropertyDependsOn(self) -> tuple["IfcPropertyDependencyRelationship", ...]: ...
    def PartOfComplex(self) -> tuple["IfcComplexProperty", ...]: ...
    def HasConstraints(self) -> tuple["IfcResourceConstraintRelationship", ...]: ...
    def HasApprovals(self) -> tuple["IfcResourceApprovalRelationship", ...]: ...

class IfcPropertyAbstraction:
    """Wrapper class for IfcPropertyAbstraction."""
    def HasExternalReferences(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...

class IfcPropertyDependencyRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcPropertyDependencyRelationship."""

    DependingProperty: "IfcProperty"
    DependantProperty: "IfcProperty"
    Expression: Optional[str]

class IfcPropertyEnumeration(IfcPropertyAbstraction):
    """Wrapper class for IfcPropertyEnumeration."""

    Name: str
    EnumerationValues: list[Union[float, list[int], int, list[float], str, bytes, bool]]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]

class IfcRecurrencePattern:
    """Wrapper class for IfcRecurrencePattern."""

    RecurrenceType: "IfcRecurrenceTypeEnum"
    DayComponent: Optional[list[int]]
    WeekdayComponent: Optional[list[int]]
    MonthComponent: Optional[list[int]]
    Position: Optional[int]
    Interval: Optional[int]
    Occurrences: Optional[int]
    TimePeriods: Optional[list["IfcTimePeriod"]]

class IfcReference:
    """Wrapper class for IfcReference."""

    TypeIdentifier: Optional[str]
    AttributeIdentifier: Optional[str]
    InstanceName: Optional[str]
    ListPositions: Optional[list[int]]
    InnerReference: Optional["IfcReference"]

class IfcReinforcementBarProperties(IfcPreDefinedProperties):
    """Wrapper class for IfcReinforcementBarProperties."""

    TotalCrossSectionArea: float
    SteelGrade: str
    BarSurface: Optional["IfcReinforcingBarSurfaceEnum"]
    EffectiveDepth: Optional[float]
    NominalBarDiameter: Optional[float]
    BarCount: Optional[float]

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
    def LayerAssignment(self) -> tuple["IfcPresentationLayerAssignment", ...]: ...
    def StyledByItem(self) -> tuple["IfcStyledItem", ...]: ...

class IfcRepresentationMap:
    """Wrapper class for IfcRepresentationMap."""

    MappingOrigin: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]
    MappedRepresentation: "IfcRepresentation"
    def HasShapeAspects(self) -> tuple["IfcShapeAspect", ...]: ...
    def MapUsage(self) -> tuple["IfcMappedItem", ...]: ...

class IfcResourceLevelRelationship:
    """Wrapper class for IfcResourceLevelRelationship."""

    Name: Optional[str]
    Description: Optional[str]

class IfcRoot:
    """Wrapper class for IfcRoot."""

    GlobalId: str
    OwnerHistory: Optional["IfcOwnerHistory"]
    Name: Optional[str]
    Description: Optional[str]

class IfcSchedulingTime:
    """Wrapper class for IfcSchedulingTime."""

    Name: Optional[str]
    DataOrigin: Optional["IfcDataOriginEnum"]
    UserDefinedDataOrigin: Optional[str]

class IfcSectionProperties(IfcPreDefinedProperties):
    """Wrapper class for IfcSectionProperties."""

    SectionType: "IfcSectionTypeEnum"
    StartProfile: "IfcProfileDef"
    EndProfile: Optional["IfcProfileDef"]

class IfcSectionReinforcementProperties(IfcPreDefinedProperties):
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
    PartOfProductDefinitionShape: Optional[Union["IfcProductDefinitionShape", "IfcRepresentationMap"]]

class IfcStructuralConnectionCondition:
    """Wrapper class for IfcStructuralConnectionCondition."""

    Name: Optional[str]

class IfcStructuralLoad:
    """Wrapper class for IfcStructuralLoad."""

    Name: Optional[str]

class IfcSurfaceStyleLighting(IfcPresentationItem):
    """Wrapper class for IfcSurfaceStyleLighting."""

    DiffuseTransmissionColour: "IfcColourRgb"
    DiffuseReflectionColour: "IfcColourRgb"
    TransmissionColour: "IfcColourRgb"
    ReflectanceColour: "IfcColourRgb"

class IfcSurfaceStyleRefraction(IfcPresentationItem):
    """Wrapper class for IfcSurfaceStyleRefraction."""

    RefractionIndex: Optional[float]
    DispersionFactor: Optional[float]

class IfcSurfaceStyleShading(IfcPresentationItem):
    """Wrapper class for IfcSurfaceStyleShading."""

    SurfaceColour: "IfcColourRgb"
    Transparency: Optional[float]

class IfcSurfaceStyleWithTextures(IfcPresentationItem):
    """Wrapper class for IfcSurfaceStyleWithTextures."""

    Textures: list["IfcSurfaceTexture"]

class IfcSurfaceTexture(IfcPresentationItem):
    """Wrapper class for IfcSurfaceTexture."""

    RepeatS: bool
    RepeatT: bool
    Mode: Optional[str]
    TextureTransform: Optional["IfcCartesianTransformationOperator2D"]
    Parameter: Optional[list[str]]
    def IsMappedBy(self) -> tuple["IfcTextureCoordinate", ...]: ...
    def UsedInStyles(self) -> tuple["IfcSurfaceStyleWithTextures", ...]: ...

class IfcTable:
    """Wrapper class for IfcTable."""

    Name: Optional[str]
    Rows: Optional[list["IfcTableRow"]]
    Columns: Optional[list["IfcTableColumn"]]

class IfcTableColumn:
    """Wrapper class for IfcTableColumn."""

    Identifier: Optional[str]
    Name: Optional[str]
    Description: Optional[str]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    ReferencePath: Optional["IfcReference"]

class IfcTableRow:
    """Wrapper class for IfcTableRow."""

    RowCells: Optional[list[Union[float, list[int], int, list[float], str, bytes, bool]]]
    IsHeading: Optional[bool]

class IfcTextStyleForDefinedFont(IfcPresentationItem):
    """Wrapper class for IfcTextStyleForDefinedFont."""

    Colour: Union["IfcColourSpecification", "IfcPreDefinedColour"]
    BackgroundColour: Optional[Union["IfcColourSpecification", "IfcPreDefinedColour"]]

class IfcTextStyleTextModel(IfcPresentationItem):
    """Wrapper class for IfcTextStyleTextModel."""

    TextIndent: Optional[Union[str, float]]
    TextAlign: Optional[str]
    TextDecoration: Optional[str]
    LetterSpacing: Optional[Union[str, float]]
    WordSpacing: Optional[Union[str, float]]
    TextTransform: Optional[str]
    LineHeight: Optional[Union[str, float]]

class IfcTextureCoordinate(IfcPresentationItem):
    """Wrapper class for IfcTextureCoordinate."""

    Maps: list["IfcSurfaceTexture"]

class IfcTextureVertex(IfcPresentationItem):
    """Wrapper class for IfcTextureVertex."""

    Coordinates: list[float]

class IfcTimePeriod:
    """Wrapper class for IfcTimePeriod."""

    StartTime: str
    EndTime: str

class IfcTimeSeries:
    """Wrapper class for IfcTimeSeries."""

    Name: str
    Description: Optional[str]
    StartTime: str
    EndTime: str
    TimeSeriesDataType: "IfcTimeSeriesDataTypeEnum"
    DataOrigin: "IfcDataOriginEnum"
    UserDefinedDataOrigin: Optional[str]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    def HasExternalReference(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...

class IfcTimeSeriesValue:
    """Wrapper class for IfcTimeSeriesValue."""

    ListValues: list[Union[float, list[int], int, list[float], str, bytes, bool]]

class IfcUnitAssignment:
    """Wrapper class for IfcUnitAssignment."""

    Units: list[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]

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
    RasterCode: bytes

class IfcBoundaryEdgeCondition(IfcBoundaryCondition):
    """Wrapper class for IfcBoundaryEdgeCondition."""

    TranslationalStiffnessByLengthX: Optional[Union[bool, float]]
    TranslationalStiffnessByLengthY: Optional[Union[bool, float]]
    TranslationalStiffnessByLengthZ: Optional[Union[bool, float]]
    RotationalStiffnessByLengthX: Optional[Union[bool, float]]
    RotationalStiffnessByLengthY: Optional[Union[bool, float]]
    RotationalStiffnessByLengthZ: Optional[Union[bool, float]]

class IfcBoundaryFaceCondition(IfcBoundaryCondition):
    """Wrapper class for IfcBoundaryFaceCondition."""

    TranslationalStiffnessByAreaX: Optional[Union[bool, float]]
    TranslationalStiffnessByAreaY: Optional[Union[bool, float]]
    TranslationalStiffnessByAreaZ: Optional[Union[bool, float]]

class IfcBoundaryNodeCondition(IfcBoundaryCondition):
    """Wrapper class for IfcBoundaryNodeCondition."""

    TranslationalStiffnessX: Optional[Union[bool, float]]
    TranslationalStiffnessY: Optional[Union[bool, float]]
    TranslationalStiffnessZ: Optional[Union[bool, float]]
    RotationalStiffnessX: Optional[Union[bool, float]]
    RotationalStiffnessY: Optional[Union[bool, float]]
    RotationalStiffnessZ: Optional[Union[bool, float]]

class IfcClassificationReference(IfcExternalReference):
    """Wrapper class for IfcClassificationReference."""

    ReferencedSource: Optional[Union["IfcClassification", "IfcClassificationReference"]]
    Description: Optional[str]
    Sort: Optional[str]
    def ClassificationRefForObjects(self) -> tuple["IfcRelAssociatesClassification", ...]: ...
    def HasReferences(self) -> tuple["IfcClassificationReference", ...]: ...

class IfcColourRgb(IfcColourSpecification):
    """Wrapper class for IfcColourRgb."""

    Red: float
    Green: float
    Blue: float

class IfcColourRgbList(IfcPresentationItem):
    """Wrapper class for IfcColourRgbList."""

    ColourList: list[list[float]]

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

class IfcConnectionSurfaceGeometry(IfcConnectionGeometry):
    """Wrapper class for IfcConnectionSurfaceGeometry."""

    SurfaceOnRelatingElement: Union["IfcFaceBasedSurfaceModel", "IfcFaceSurface", "IfcSurface"]
    SurfaceOnRelatedElement: Optional[Union["IfcFaceBasedSurfaceModel", "IfcFaceSurface", "IfcSurface"]]

class IfcConnectionVolumeGeometry(IfcConnectionGeometry):
    """Wrapper class for IfcConnectionVolumeGeometry."""

    VolumeOnRelatingElement: Union["IfcClosedShell", "IfcSolidModel"]
    VolumeOnRelatedElement: Optional[Union["IfcClosedShell", "IfcSolidModel"]]

class IfcContextDependentUnit(IfcNamedUnit):
    """Wrapper class for IfcContextDependentUnit."""

    Name: str
    def HasExternalReference(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...

class IfcConversionBasedUnit(IfcNamedUnit):
    """Wrapper class for IfcConversionBasedUnit."""

    Name: str
    ConversionFactor: "IfcMeasureWithUnit"
    def HasExternalReference(self) -> tuple["IfcExternalReferenceRelationship", ...]: ...

class IfcCostValue(IfcAppliedValue):
    """Wrapper class for IfcCostValue."""

    ...

class IfcCurveStyle(IfcPresentationStyle):
    """Wrapper class for IfcCurveStyle."""

    CurveFont: Optional[Union["IfcCurveStyleFontAndScaling", "IfcCurveStyleFont", "IfcPreDefinedCurveFont"]]
    CurveWidth: Optional[Union[str, float]]
    CurveColour: Optional[Union["IfcColourSpecification", "IfcPreDefinedColour"]]
    ModelOrDraughting: Optional[bool]

class IfcDerivedProfileDef(IfcProfileDef):
    """Wrapper class for IfcDerivedProfileDef."""

    ParentProfile: "IfcProfileDef"
    Operator: "IfcCartesianTransformationOperator2D"
    Label: Optional[str]

class IfcDocumentReference(IfcExternalReference):
    """Wrapper class for IfcDocumentReference."""

    Description: Optional[str]
    ReferencedDocument: Optional["IfcDocumentInformation"]
    def DocumentRefForObjects(self) -> tuple["IfcRelAssociatesDocument", ...]: ...

class IfcEventTime(IfcSchedulingTime):
    """Wrapper class for IfcEventTime."""

    ActualDate: Optional[str]
    EarlyDate: Optional[str]
    LateDate: Optional[str]
    ScheduleDate: Optional[str]

class IfcExtendedProperties(IfcPropertyAbstraction):
    """Wrapper class for IfcExtendedProperties."""

    Name: Optional[str]
    Description: Optional[str]
    Properties: list["IfcProperty"]

class IfcExternalReferenceRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcExternalReferenceRelationship."""

    RelatingReference: "IfcExternalReference"
    RelatedResourceObjects: list[
        Union[
            "IfcActorRole",
            "IfcAppliedValue",
            "IfcApproval",
            "IfcConstraint",
            "IfcContextDependentUnit",
            "IfcConversionBasedUnit",
            "IfcExternalInformation",
            "IfcExternalReference",
            "IfcMaterialDefinition",
            "IfcOrganization",
            "IfcPerson",
            "IfcPersonAndOrganization",
            "IfcPhysicalQuantity",
            "IfcProfileDef",
            "IfcPropertyAbstraction",
            "IfcTimeSeries",
        ]
    ]

class IfcExternallyDefinedHatchStyle(IfcExternalReference):
    """Wrapper class for IfcExternallyDefinedHatchStyle."""

    ...

class IfcExternallyDefinedSurfaceStyle(IfcExternalReference):
    """Wrapper class for IfcExternallyDefinedSurfaceStyle."""

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
    ModelorDraughting: Optional[bool]

class IfcGeometricRepresentationContext(IfcRepresentationContext):
    """Wrapper class for IfcGeometricRepresentationContext."""

    CoordinateSpaceDimension: int
    Precision: Optional[float]
    WorldCoordinateSystem: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]
    TrueNorth: Optional["IfcDirection"]
    def HasSubContexts(self) -> tuple["IfcGeometricRepresentationSubContext", ...]: ...
    def HasCoordinateOperation(self) -> tuple["IfcCoordinateOperation", ...]: ...

class IfcGeometricRepresentationItem(IfcRepresentationItem):
    """Wrapper class for IfcGeometricRepresentationItem."""

    ...

class IfcGridPlacement(IfcObjectPlacement):
    """Wrapper class for IfcGridPlacement."""

    PlacementLocation: "IfcVirtualGridIntersection"
    PlacementRefDirection: Optional[Union["IfcDirection", "IfcVirtualGridIntersection"]]

class IfcImageTexture(IfcSurfaceTexture):
    """Wrapper class for IfcImageTexture."""

    URLReference: str

class IfcIndexedColourMap(IfcPresentationItem):
    """Wrapper class for IfcIndexedColourMap."""

    MappedTo: "IfcTessellatedFaceSet"
    Opacity: Optional[float]
    Colours: "IfcColourRgbList"
    ColourIndex: list[int]

class IfcIrregularTimeSeries(IfcTimeSeries):
    """Wrapper class for IfcIrregularTimeSeries."""

    Values: list["IfcIrregularTimeSeriesValue"]

class IfcLagTime(IfcSchedulingTime):
    """Wrapper class for IfcLagTime."""

    LagValue: Union[str, float]
    DurationType: "IfcTaskDurationEnum"

class IfcLibraryReference(IfcExternalReference):
    """Wrapper class for IfcLibraryReference."""

    Description: Optional[str]
    Language: Optional[str]
    ReferencedLibrary: Optional["IfcLibraryInformation"]
    def LibraryRefForObjects(self) -> tuple["IfcRelAssociatesLibrary", ...]: ...

class IfcLocalPlacement(IfcObjectPlacement):
    """Wrapper class for IfcLocalPlacement."""

    PlacementRelTo: Optional["IfcObjectPlacement"]
    RelativePlacement: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]

class IfcMapConversion(IfcCoordinateOperation):
    """Wrapper class for IfcMapConversion."""

    Eastings: float
    Northings: float
    OrthogonalHeight: float
    XAxisAbscissa: Optional[float]
    XAxisOrdinate: Optional[float]
    Scale: Optional[float]

class IfcMappedItem(IfcRepresentationItem):
    """Wrapper class for IfcMappedItem."""

    MappingSource: "IfcRepresentationMap"
    MappingTarget: "IfcCartesianTransformationOperator"

class IfcMaterialConstituent(IfcMaterialDefinition):
    """Wrapper class for IfcMaterialConstituent."""

    Name: Optional[str]
    Description: Optional[str]
    Material: "IfcMaterial"
    Fraction: Optional[float]
    Category: Optional[str]
    def ToMaterialConstituentSet(self) -> tuple["IfcMaterialConstituentSet", ...]: ...

class IfcMaterialConstituentSet(IfcMaterialDefinition):
    """Wrapper class for IfcMaterialConstituentSet."""

    Name: Optional[str]
    Description: Optional[str]
    MaterialConstituents: Optional[list["IfcMaterialConstituent"]]

class IfcMaterialDefinitionRepresentation(IfcProductRepresentation):
    """Wrapper class for IfcMaterialDefinitionRepresentation."""

    RepresentedMaterial: "IfcMaterial"

class IfcMaterialProfile(IfcMaterialDefinition):
    """Wrapper class for IfcMaterialProfile."""

    Name: Optional[str]
    Description: Optional[str]
    Material: Optional["IfcMaterial"]
    Profile: "IfcProfileDef"
    Priority: Optional[int]
    Category: Optional[str]
    def ToMaterialProfileSet(self) -> tuple["IfcMaterialProfileSet", ...]: ...

class IfcMaterialProfileSet(IfcMaterialDefinition):
    """Wrapper class for IfcMaterialProfileSet."""

    Name: Optional[str]
    Description: Optional[str]
    MaterialProfiles: list["IfcMaterialProfile"]
    CompositeProfile: Optional["IfcCompositeProfileDef"]

class IfcMaterialProfileSetUsage(IfcMaterialUsageDefinition):
    """Wrapper class for IfcMaterialProfileSetUsage."""

    ForProfileSet: "IfcMaterialProfileSet"
    CardinalPoint: Optional[int]
    ReferenceExtent: Optional[float]

class IfcMaterialRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcMaterialRelationship."""

    RelatingMaterial: "IfcMaterial"
    RelatedMaterials: list["IfcMaterial"]
    Expression: Optional[str]

class IfcMetric(IfcConstraint):
    """Wrapper class for IfcMetric."""

    Benchmark: "IfcBenchmarkEnum"
    ValueSource: Optional[str]
    DataValue: Optional[Union["IfcAppliedValue", "IfcMeasureWithUnit", "IfcReference", "IfcTable", "IfcTimeSeries", float, list[int], int, list[float], str, bytes, bool]]
    ReferencePath: Optional["IfcReference"]

class IfcObjectDefinition(IfcRoot):
    """Wrapper class for IfcObjectDefinition."""
    def HasAssignments(self) -> tuple["IfcRelAssigns", ...]: ...
    def Nests(self) -> tuple["IfcRelNests", ...]: ...
    def IsNestedBy(self) -> tuple["IfcRelNests", ...]: ...
    def HasContext(self) -> tuple["IfcRelDeclares", ...]: ...
    def IsDecomposedBy(self) -> tuple["IfcRelAggregates", ...]: ...
    def Decomposes(self) -> tuple["IfcRelAggregates", ...]: ...
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

    BenchmarkValues: Optional[list["IfcConstraint"]]
    LogicalAggregator: Optional["IfcLogicalOperatorEnum"]
    ObjectiveQualifier: "IfcObjectiveEnum"
    UserDefinedQualifier: Optional[str]

class IfcParameterizedProfileDef(IfcProfileDef):
    """Wrapper class for IfcParameterizedProfileDef."""

    Position: Optional["IfcAxis2Placement2D"]

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

class IfcPreDefinedProperties(IfcPropertyAbstraction):
    """Wrapper class for IfcPreDefinedProperties."""

    ...

class IfcPreDefinedTextFont(IfcPreDefinedItem):
    """Wrapper class for IfcPreDefinedTextFont."""

    ...

class IfcPresentationLayerWithStyle(IfcPresentationLayerAssignment):
    """Wrapper class for IfcPresentationLayerWithStyle."""

    LayerOn: bool
    LayerFrozen: bool
    LayerBlocked: bool
    LayerStyles: list["IfcPresentationStyle"]

class IfcProductDefinitionShape(IfcProductRepresentation):
    """Wrapper class for IfcProductDefinitionShape."""
    def ShapeOfProduct(self) -> tuple["IfcProduct", ...]: ...
    def HasShapeAspects(self) -> tuple["IfcShapeAspect", ...]: ...

class IfcProjectedCRS(IfcCoordinateReferenceSystem):
    """Wrapper class for IfcProjectedCRS."""

    MapProjection: Optional[str]
    MapZone: Optional[str]
    MapUnit: Optional["IfcNamedUnit"]

class IfcPropertyDefinition(IfcRoot):
    """Wrapper class for IfcPropertyDefinition."""
    def HasContext(self) -> tuple["IfcRelDeclares", ...]: ...
    def HasAssociations(self) -> tuple["IfcRelAssociates", ...]: ...

class IfcRegularTimeSeries(IfcTimeSeries):
    """Wrapper class for IfcRegularTimeSeries."""

    TimeStep: float
    Values: list["IfcTimeSeriesValue"]

class IfcRelationship(IfcRoot):
    """Wrapper class for IfcRelationship."""

    ...

class IfcResourceApprovalRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcResourceApprovalRelationship."""

    RelatedResourceObjects: list[
        Union[
            "IfcActorRole",
            "IfcAppliedValue",
            "IfcApproval",
            "IfcConstraint",
            "IfcContextDependentUnit",
            "IfcConversionBasedUnit",
            "IfcExternalInformation",
            "IfcExternalReference",
            "IfcMaterialDefinition",
            "IfcOrganization",
            "IfcPerson",
            "IfcPersonAndOrganization",
            "IfcPhysicalQuantity",
            "IfcProfileDef",
            "IfcPropertyAbstraction",
            "IfcTimeSeries",
        ]
    ]
    RelatingApproval: "IfcApproval"

class IfcResourceConstraintRelationship(IfcResourceLevelRelationship):
    """Wrapper class for IfcResourceConstraintRelationship."""

    RelatingConstraint: "IfcConstraint"
    RelatedResourceObjects: list[
        Union[
            "IfcActorRole",
            "IfcAppliedValue",
            "IfcApproval",
            "IfcConstraint",
            "IfcContextDependentUnit",
            "IfcConversionBasedUnit",
            "IfcExternalInformation",
            "IfcExternalReference",
            "IfcMaterialDefinition",
            "IfcOrganization",
            "IfcPerson",
            "IfcPersonAndOrganization",
            "IfcPhysicalQuantity",
            "IfcProfileDef",
            "IfcPropertyAbstraction",
            "IfcTimeSeries",
        ]
    ]

class IfcResourceTime(IfcSchedulingTime):
    """Wrapper class for IfcResourceTime."""

    ScheduleWork: Optional[str]
    ScheduleUsage: Optional[float]
    ScheduleStart: Optional[str]
    ScheduleFinish: Optional[str]
    ScheduleContour: Optional[str]
    LevelingDelay: Optional[str]
    IsOverAllocated: Optional[bool]
    StatusTime: Optional[str]
    ActualWork: Optional[str]
    ActualUsage: Optional[float]
    ActualStart: Optional[str]
    ActualFinish: Optional[str]
    RemainingWork: Optional[str]
    RemainingUsage: Optional[float]
    Completion: Optional[float]

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

class IfcStructuralLoadConfiguration(IfcStructuralLoad):
    """Wrapper class for IfcStructuralLoadConfiguration."""

    Values: list["IfcStructuralLoadOrResult"]
    Locations: Optional[list[list[float]]]

class IfcStructuralLoadOrResult(IfcStructuralLoad):
    """Wrapper class for IfcStructuralLoadOrResult."""

    ...

class IfcStructuralLoadStatic(IfcStructuralLoadOrResult):
    """Wrapper class for IfcStructuralLoadStatic."""

    ...

class IfcStyleModel(IfcRepresentation):
    """Wrapper class for IfcStyleModel."""

    ...

class IfcStyledItem(IfcRepresentationItem):
    """Wrapper class for IfcStyledItem."""

    Item: Optional["IfcRepresentationItem"]
    Styles: list[Union["IfcPresentationStyle", "IfcPresentationStyleAssignment"]]
    Name: Optional[str]

class IfcSurfaceStyle(IfcPresentationStyle):
    """Wrapper class for IfcSurfaceStyle."""

    Side: "IfcSurfaceSide"
    Styles: list[Union["IfcExternallyDefinedSurfaceStyle", "IfcSurfaceStyleLighting", "IfcSurfaceStyleRefraction", "IfcSurfaceStyleShading", "IfcSurfaceStyleWithTextures"]]

class IfcSurfaceStyleRendering(IfcSurfaceStyleShading):
    """Wrapper class for IfcSurfaceStyleRendering."""

    DiffuseColour: Optional[Union["IfcColourRgb", float]]
    TransmissionColour: Optional[Union["IfcColourRgb", float]]
    DiffuseTransmissionColour: Optional[Union["IfcColourRgb", float]]
    ReflectionColour: Optional[Union["IfcColourRgb", float]]
    SpecularColour: Optional[Union["IfcColourRgb", float]]
    SpecularHighlight: Optional[float]
    ReflectanceMethod: "IfcReflectanceMethodEnum"

class IfcTaskTime(IfcSchedulingTime):
    """Wrapper class for IfcTaskTime."""

    DurationType: Optional["IfcTaskDurationEnum"]
    ScheduleDuration: Optional[str]
    ScheduleStart: Optional[str]
    ScheduleFinish: Optional[str]
    EarlyStart: Optional[str]
    EarlyFinish: Optional[str]
    LateStart: Optional[str]
    LateFinish: Optional[str]
    FreeFloat: Optional[str]
    TotalFloat: Optional[str]
    IsCritical: Optional[bool]
    StatusTime: Optional[str]
    ActualDuration: Optional[str]
    ActualStart: Optional[str]
    ActualFinish: Optional[str]
    RemainingTime: Optional[str]
    Completion: Optional[float]

class IfcTelecomAddress(IfcAddress):
    """Wrapper class for IfcTelecomAddress."""

    TelephoneNumbers: Optional[list[str]]
    FacsimileNumbers: Optional[list[str]]
    PagerNumber: Optional[str]
    ElectronicMailAddresses: Optional[list[str]]
    WWWHomePageURL: Optional[str]
    MessagingIDs: Optional[list[str]]

class IfcTextStyle(IfcPresentationStyle):
    """Wrapper class for IfcTextStyle."""

    TextCharacterAppearance: Optional["IfcTextStyleForDefinedFont"]
    TextStyle: Optional["IfcTextStyleTextModel"]
    TextFontStyle: Union["IfcExternallyDefinedTextFont", "IfcPreDefinedTextFont"]
    ModelOrDraughting: Optional[bool]

class IfcTextureCoordinateGenerator(IfcTextureCoordinate):
    """Wrapper class for IfcTextureCoordinateGenerator."""

    Mode: str
    Parameter: Optional[list[float]]

class IfcTextureMap(IfcTextureCoordinate):
    """Wrapper class for IfcTextureMap."""

    Vertices: list["IfcTextureVertex"]
    MappedTo: "IfcFace"

class IfcTextureVertexList(IfcPresentationItem):
    """Wrapper class for IfcTextureVertexList."""

    TexCoordsList: list[list[float]]

class IfcTopologicalRepresentationItem(IfcRepresentationItem):
    """Wrapper class for IfcTopologicalRepresentationItem."""

    ...

class IfcWorkTime(IfcSchedulingTime):
    """Wrapper class for IfcWorkTime."""

    RecurrencePattern: Optional["IfcRecurrencePattern"]
    Start: Optional[str]
    Finish: Optional[str]

class IfcAnnotationFillArea(IfcGeometricRepresentationItem):
    """Wrapper class for IfcAnnotationFillArea."""

    OuterBoundary: "IfcCurve"
    InnerBoundaries: Optional[list["IfcCurve"]]

class IfcArbitraryProfileDefWithVoids(IfcArbitraryClosedProfileDef):
    """Wrapper class for IfcArbitraryProfileDefWithVoids."""

    InnerCurves: list["IfcCurve"]

class IfcBooleanResult(IfcGeometricRepresentationItem):
    """Wrapper class for IfcBooleanResult."""

    Operator: "IfcBooleanOperator"
    FirstOperand: Union["IfcBooleanResult", "IfcCsgPrimitive3D", "IfcHalfSpaceSolid", "IfcSolidModel", "IfcTessellatedFaceSet"]
    SecondOperand: Union["IfcBooleanResult", "IfcCsgPrimitive3D", "IfcHalfSpaceSolid", "IfcSolidModel", "IfcTessellatedFaceSet"]

class IfcBoundaryNodeConditionWarping(IfcBoundaryNodeCondition):
    """Wrapper class for IfcBoundaryNodeConditionWarping."""

    WarpingStiffness: Optional[Union[bool, float]]

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

class IfcCartesianPointList(IfcGeometricRepresentationItem):
    """Wrapper class for IfcCartesianPointList."""

    ...

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

class IfcContext(IfcObjectDefinition):
    """Wrapper class for IfcContext."""

    ObjectType: Optional[str]
    LongName: Optional[str]
    Phase: Optional[str]
    RepresentationContexts: Optional[list["IfcRepresentationContext"]]
    UnitsInContext: Optional["IfcUnitAssignment"]
    def IsDefinedBy(self) -> tuple["IfcRelDefinesByProperties", ...]: ...
    def Declares(self) -> tuple["IfcRelDeclares", ...]: ...
    @property
    def properties(self) -> object: ...
    @properties.setter
    def properties(self, value) -> None: ...

class IfcConversionBasedUnitWithOffset(IfcConversionBasedUnit):
    """Wrapper class for IfcConversionBasedUnitWithOffset."""

    ConversionOffset: float

class IfcCsgPrimitive3D(IfcGeometricRepresentationItem):
    """Wrapper class for IfcCsgPrimitive3D."""

    Position: "IfcAxis2Placement3D"

class IfcCurve(IfcGeometricRepresentationItem):
    """Wrapper class for IfcCurve."""

    ...

class IfcDirection(IfcGeometricRepresentationItem):
    """Wrapper class for IfcDirection."""

    DirectionRatios: list[float]

class IfcDraughtingPreDefinedColour(IfcPreDefinedColour):
    """Wrapper class for IfcDraughtingPreDefinedColour."""

    ...

class IfcDraughtingPreDefinedCurveFont(IfcPreDefinedCurveFont):
    """Wrapper class for IfcDraughtingPreDefinedCurveFont."""

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
    def HasTextureMaps(self) -> tuple["IfcTextureMap", ...]: ...

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
    StartOfNextHatchLine: Union[float, "IfcVector"]
    PointOfReferenceHatchLine: Optional["IfcCartesianPoint"]
    PatternStart: Optional["IfcCartesianPoint"]
    HatchLineAngle: float

class IfcFillAreaStyleTiles(IfcGeometricRepresentationItem):
    """Wrapper class for IfcFillAreaStyleTiles."""

    TilingPattern: list["IfcVector"]
    Tiles: list["IfcStyledItem"]
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
    FlangeEdgeRadius: Optional[float]
    FlangeSlope: Optional[float]

class IfcIndexedTextureMap(IfcTextureCoordinate):
    """Wrapper class for IfcIndexedTextureMap."""

    MappedTo: "IfcTessellatedFaceSet"
    TexCoords: "IfcTextureVertexList"

class IfcLShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcLShapeProfileDef."""

    Depth: float
    Width: Optional[float]
    Thickness: float
    FilletRadius: Optional[float]
    EdgeRadius: Optional[float]
    LegSlope: Optional[float]

class IfcLightSource(IfcGeometricRepresentationItem):
    """Wrapper class for IfcLightSource."""

    Name: Optional[str]
    LightColour: "IfcColourRgb"
    AmbientIntensity: Optional[float]
    Intensity: Optional[float]

class IfcLoop(IfcTopologicalRepresentationItem):
    """Wrapper class for IfcLoop."""

    ...

class IfcMaterialLayerWithOffsets(IfcMaterialLayer):
    """Wrapper class for IfcMaterialLayerWithOffsets."""

    OffsetDirection: "IfcLayerSetDirectionEnum"
    OffsetValues: list[float]

class IfcMaterialProfileSetUsageTapering(IfcMaterialProfileSetUsage):
    """Wrapper class for IfcMaterialProfileSetUsageTapering."""

    ForProfileEndSet: "IfcMaterialProfileSet"
    CardinalEndPoint: Optional[int]

class IfcMaterialProfileWithOffsets(IfcMaterialProfile):
    """Wrapper class for IfcMaterialProfileWithOffsets."""

    OffsetValues: list[float]

class IfcMirroredProfileDef(IfcDerivedProfileDef):
    """Wrapper class for IfcMirroredProfileDef."""

    ...

class IfcObject(IfcObjectDefinition):
    """Wrapper class for IfcObject."""

    ObjectType: Optional[str]
    def IsDeclaredBy(self) -> tuple["IfcRelDefinesByObject", ...]: ...
    def Declares(self) -> tuple["IfcRelDefinesByObject", ...]: ...
    def IsTypedBy(self) -> tuple["IfcRelDefinesByType", ...]: ...
    def IsDefinedBy(self) -> tuple["IfcRelDefinesByProperties", ...]: ...
    @property
    def psetsmap(self) -> object: ...
    @property
    def property_sets(self) -> object: ...
    @property_sets.setter
    def property_sets(self, value) -> None: ...
    @property
    def quantity_sets(self) -> object: ...

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

class IfcPropertyBoundedValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyBoundedValue."""

    UpperBoundValue: Optional[Union[float, list[int], int, list[float], str, bytes, bool]]
    LowerBoundValue: Optional[Union[float, list[int], int, list[float], str, bytes, bool]]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    SetPointValue: Optional[Union[float, list[int], int, list[float], str, bytes, bool]]

class IfcPropertyEnumeratedValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyEnumeratedValue."""

    EnumerationValues: Optional[list[Union[float, list[int], int, list[float], str, bytes, bool]]]
    EnumerationReference: Optional["IfcPropertyEnumeration"]

class IfcPropertyListValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyListValue."""

    ListValues: Optional[list[Union[float, list[int], int, list[float], str, bytes, bool]]]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]

class IfcPropertyReferenceValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyReferenceValue."""

    UsageName: Optional[str]
    PropertyReference: Optional[
        Union[
            "IfcAddress",
            "IfcAppliedValue",
            "IfcExternalReference",
            "IfcMaterialDefinition",
            "IfcOrganization",
            "IfcPerson",
            "IfcPersonAndOrganization",
            "IfcTable",
            "IfcTimeSeries",
        ]
    ]

class IfcPropertySetDefinition(IfcPropertyDefinition):
    """Wrapper class for IfcPropertySetDefinition."""
    def DefinesType(self) -> tuple["IfcTypeObject", ...]: ...
    def IsDefinedBy(self) -> tuple["IfcRelDefinesByTemplate", ...]: ...
    def DefinesOccurrence(self) -> tuple["IfcRelDefinesByProperties", ...]: ...

class IfcPropertySingleValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertySingleValue."""

    NominalValue: Optional[Union[float, list[int], int, list[float], str, bytes, bool]]
    Unit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]

class IfcPropertyTableValue(IfcSimpleProperty):
    """Wrapper class for IfcPropertyTableValue."""

    DefiningValues: Optional[list[Union[float, list[int], int, list[float], str, bytes, bool]]]
    DefinedValues: Optional[list[Union[float, list[int], int, list[float], str, bytes, bool]]]
    Expression: Optional[str]
    DefiningUnit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    DefinedUnit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    CurveInterpolation: Optional["IfcCurveInterpolationEnum"]

class IfcPropertyTemplateDefinition(IfcPropertyDefinition):
    """Wrapper class for IfcPropertyTemplateDefinition."""

    ...

class IfcQuantityArea(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityArea."""

    AreaValue: float
    Formula: Optional[str]

class IfcQuantityCount(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityCount."""

    CountValue: float
    Formula: Optional[str]

class IfcQuantityLength(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityLength."""

    LengthValue: float
    Formula: Optional[str]

class IfcQuantityTime(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityTime."""

    TimeValue: float
    Formula: Optional[str]

class IfcQuantityVolume(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityVolume."""

    VolumeValue: float
    Formula: Optional[str]

class IfcQuantityWeight(IfcPhysicalSimpleQuantity):
    """Wrapper class for IfcQuantityWeight."""

    WeightValue: float
    Formula: Optional[str]

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

    RelatedObjects: list[Union["IfcObjectDefinition", "IfcPropertyDefinition"]]

class IfcRelConnects(IfcRelationship):
    """Wrapper class for IfcRelConnects."""

    ...

class IfcRelDeclares(IfcRelationship):
    """Wrapper class for IfcRelDeclares."""

    RelatingContext: "IfcContext"
    RelatedDefinitions: list[Union["IfcObjectDefinition", "IfcPropertyDefinition"]]

class IfcRelDecomposes(IfcRelationship):
    """Wrapper class for IfcRelDecomposes."""

    ...

class IfcRelDefines(IfcRelationship):
    """Wrapper class for IfcRelDefines."""

    ...

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

    DeltaTConstant: Optional[float]
    DeltaTY: Optional[float]
    DeltaTZ: Optional[float]

class IfcStyledRepresentation(IfcStyleModel):
    """Wrapper class for IfcStyledRepresentation."""

    ...

class IfcSurface(IfcGeometricRepresentationItem):
    """Wrapper class for IfcSurface."""

    ...

class IfcSurfaceReinforcementArea(IfcStructuralLoadOrResult):
    """Wrapper class for IfcSurfaceReinforcementArea."""

    SurfaceReinforcement1: Optional[list[float]]
    SurfaceReinforcement2: Optional[list[float]]
    ShearReinforcement: Optional[float]

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

class IfcTaskTimeRecurring(IfcTaskTime):
    """Wrapper class for IfcTaskTimeRecurring."""

    Recurrence: "IfcRecurrencePattern"

class IfcTessellatedItem(IfcGeometricRepresentationItem):
    """Wrapper class for IfcTessellatedItem."""

    ...

class IfcTextLiteral(IfcGeometricRepresentationItem):
    """Wrapper class for IfcTextLiteral."""

    Literal: str
    Placement: Union["IfcAxis2Placement2D", "IfcAxis2Placement3D"]
    Path: "IfcTextPath"

class IfcTextStyleFontModel(IfcPreDefinedTextFont):
    """Wrapper class for IfcTextStyleFontModel."""

    FontFamily: list[str]
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
    def Types(self) -> tuple["IfcRelDefinesByType", ...]: ...

class IfcUShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcUShapeProfileDef."""

    Depth: float
    FlangeWidth: float
    WebThickness: float
    FlangeThickness: float
    FilletRadius: Optional[float]
    EdgeRadius: Optional[float]
    FlangeSlope: Optional[float]

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

class IfcAsymmetricIShapeProfileDef(IfcParameterizedProfileDef):
    """Wrapper class for IfcAsymmetricIShapeProfileDef."""

    BottomFlangeWidth: float
    OverallDepth: float
    WebThickness: float
    BottomFlangeThickness: float
    BottomFlangeFilletRadius: Optional[float]
    TopFlangeWidth: float
    TopFlangeThickness: Optional[float]
    TopFlangeFilletRadius: Optional[float]
    BottomFlangeEdgeRadius: Optional[float]
    BottomFlangeSlope: Optional[float]
    TopFlangeEdgeRadius: Optional[float]
    TopFlangeSlope: Optional[float]

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

class IfcCartesianPointList2D(IfcCartesianPointList):
    """Wrapper class for IfcCartesianPointList2D."""

    CoordList: list[list[float]]

class IfcCartesianPointList3D(IfcCartesianPointList):
    """Wrapper class for IfcCartesianPointList3D."""

    CoordList: list[list[float]]

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

    Identification: Optional[str]
    def Controls(self) -> tuple["IfcRelAssignsToControl", ...]: ...

class IfcCsgSolid(IfcSolidModel):
    """Wrapper class for IfcCsgSolid."""

    TreeRootExpression: Union["IfcBooleanResult", "IfcCsgPrimitive3D"]

class IfcDoorLiningProperties(IfcPreDefinedPropertySet):
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
    LiningToPanelOffsetX: Optional[float]
    LiningToPanelOffsetY: Optional[float]

class IfcDoorPanelProperties(IfcPreDefinedPropertySet):
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

class IfcElementQuantity(IfcQuantitySet):
    """Wrapper class for IfcElementQuantity."""

    MethodOfMeasurement: Optional[str]
    Quantities: list["IfcPhysicalQuantity"]

class IfcElementarySurface(IfcSurface):
    """Wrapper class for IfcElementarySurface."""

    Position: "IfcAxis2Placement3D"

class IfcFaceOuterBound(IfcFaceBound):
    """Wrapper class for IfcFaceOuterBound."""

    ...

class IfcFaceSurface(IfcFace):
    """Wrapper class for IfcFaceSurface."""

    FaceSurface: "IfcSurface"
    SameSense: bool

class IfcGeometricCurveSet(IfcGeometricSet):
    """Wrapper class for IfcGeometricCurveSet."""

    ...

class IfcGroup(IfcObject):
    """Wrapper class for IfcGroup."""
    def IsGroupedBy(self) -> tuple["IfcRelAssignsToGroup", ...]: ...

class IfcIndexedPolygonalFace(IfcTessellatedItem):
    """Wrapper class for IfcIndexedPolygonalFace."""

    CoordIndex: list[int]
    def ToFaceSet(self) -> tuple["IfcPolygonalFaceSet", ...]: ...

class IfcIndexedTriangleTextureMap(IfcIndexedTextureMap):
    """Wrapper class for IfcIndexedTriangleTextureMap."""

    TexCoordIndex: Optional[list[list[int]]]

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

class IfcPcurve(IfcCurve):
    """Wrapper class for IfcPcurve."""

    BasisSurface: "IfcSurface"
    ReferenceCurve: "IfcCurve"

class IfcPermeableCoveringProperties(IfcPreDefinedPropertySet):
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

class IfcPreDefinedPropertySet(IfcPropertySetDefinition):
    """Wrapper class for IfcPreDefinedPropertySet."""

    ...

class IfcProcess(IfcObject):
    """Wrapper class for IfcProcess."""

    Identification: Optional[str]
    LongDescription: Optional[str]
    def IsPredecessorTo(self) -> tuple["IfcRelSequence", ...]: ...
    def IsSuccessorFrom(self) -> tuple["IfcRelSequence", ...]: ...
    def OperatesOn(self) -> tuple["IfcRelAssignsToProcess", ...]: ...

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

class IfcProject(IfcContext):
    """Wrapper class for IfcProject."""
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

class IfcProjectLibrary(IfcContext):
    """Wrapper class for IfcProjectLibrary."""

    ...

class IfcPropertySet(IfcPropertySetDefinition):
    """Wrapper class for IfcPropertySet."""

    HasProperties: list["IfcProperty"]

class IfcPropertySetTemplate(IfcPropertyTemplateDefinition):
    """Wrapper class for IfcPropertySetTemplate."""

    TemplateType: Optional["IfcPropertySetTemplateTypeEnum"]
    ApplicableEntity: Optional[str]
    HasPropertyTemplates: list["IfcPropertyTemplate"]
    def Defines(self) -> tuple["IfcRelDefinesByTemplate", ...]: ...

class IfcPropertyTemplate(IfcPropertyTemplateDefinition):
    """Wrapper class for IfcPropertyTemplate."""
    def PartOfComplexTemplate(self) -> tuple["IfcComplexPropertyTemplate", ...]: ...
    def PartOfPsetTemplate(self) -> tuple["IfcPropertySetTemplate", ...]: ...

class IfcQuantitySet(IfcPropertySetDefinition):
    """Wrapper class for IfcQuantitySet."""

    ...

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

class IfcReinforcementDefinitionProperties(IfcPreDefinedPropertySet):
    """Wrapper class for IfcReinforcementDefinitionProperties."""

    DefinitionType: Optional[str]
    ReinforcementSectionDefinitions: list["IfcSectionReinforcementProperties"]

class IfcRelAggregates(IfcRelDecomposes):
    """Wrapper class for IfcRelAggregates."""

    RelatingObject: "IfcObjectDefinition"
    RelatedObjects: list["IfcObjectDefinition"]

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

    RelatingProcess: Union["IfcProcess", "IfcTypeProcess"]
    QuantityInProcess: Optional["IfcMeasureWithUnit"]

class IfcRelAssignsToProduct(IfcRelAssigns):
    """Wrapper class for IfcRelAssignsToProduct."""

    RelatingProduct: Union["IfcProduct", "IfcTypeProduct"]

class IfcRelAssignsToResource(IfcRelAssigns):
    """Wrapper class for IfcRelAssignsToResource."""

    RelatingResource: Union["IfcResource", "IfcTypeResource"]

class IfcRelAssociatesApproval(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesApproval."""

    RelatingApproval: "IfcApproval"

class IfcRelAssociatesClassification(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesClassification."""

    RelatingClassification: Union["IfcClassification", "IfcClassificationReference"]

class IfcRelAssociatesConstraint(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesConstraint."""

    Intent: Optional[str]
    RelatingConstraint: "IfcConstraint"

class IfcRelAssociatesDocument(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesDocument."""

    RelatingDocument: Union["IfcDocumentInformation", "IfcDocumentReference"]

class IfcRelAssociatesLibrary(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesLibrary."""

    RelatingLibrary: Union["IfcLibraryInformation", "IfcLibraryReference"]

class IfcRelAssociatesMaterial(IfcRelAssociates):
    """Wrapper class for IfcRelAssociatesMaterial."""

    RelatingMaterial: Union["IfcMaterialDefinition", "IfcMaterialList", "IfcMaterialUsageDefinition"]

class IfcRelConnectsElements(IfcRelConnects):
    """Wrapper class for IfcRelConnectsElements."""

    ConnectionGeometry: Optional["IfcConnectionGeometry"]
    RelatingElement: "IfcElement"
    RelatedElement: "IfcElement"

class IfcRelConnectsPortToElement(IfcRelConnects):
    """Wrapper class for IfcRelConnectsPortToElement."""

    RelatingPort: "IfcPort"
    RelatedElement: "IfcDistributionElement"

class IfcRelConnectsPorts(IfcRelConnects):
    """Wrapper class for IfcRelConnectsPorts."""

    RelatingPort: "IfcPort"
    RelatedPort: "IfcPort"
    RealizingElement: Optional["IfcElement"]

class IfcRelConnectsStructuralActivity(IfcRelConnects):
    """Wrapper class for IfcRelConnectsStructuralActivity."""

    RelatingElement: Union["IfcElement", "IfcStructuralItem"]
    RelatedStructuralActivity: "IfcStructuralActivity"

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
    RelatingStructure: "IfcSpatialElement"

class IfcRelCoversBldgElements(IfcRelConnects):
    """Wrapper class for IfcRelCoversBldgElements."""

    RelatingBuildingElement: "IfcElement"
    RelatedCoverings: list["IfcCovering"]

class IfcRelCoversSpaces(IfcRelConnects):
    """Wrapper class for IfcRelCoversSpaces."""

    RelatingSpace: "IfcSpace"
    RelatedCoverings: list["IfcCovering"]

class IfcRelDefinesByObject(IfcRelDefines):
    """Wrapper class for IfcRelDefinesByObject."""

    RelatedObjects: list["IfcObject"]
    RelatingObject: "IfcObject"

class IfcRelDefinesByProperties(IfcRelDefines):
    """Wrapper class for IfcRelDefinesByProperties."""

    RelatedObjects: list["IfcObjectDefinition"]
    RelatingPropertyDefinition: Union["IfcPropertySetDefinition", list]

class IfcRelDefinesByTemplate(IfcRelDefines):
    """Wrapper class for IfcRelDefinesByTemplate."""

    RelatedPropertySets: list["IfcPropertySetDefinition"]
    RelatingTemplate: "IfcPropertySetTemplate"

class IfcRelDefinesByType(IfcRelDefines):
    """Wrapper class for IfcRelDefinesByType."""

    RelatedObjects: list["IfcObject"]
    RelatingType: "IfcTypeObject"

class IfcRelFillsElement(IfcRelConnects):
    """Wrapper class for IfcRelFillsElement."""

    RelatingOpeningElement: "IfcOpeningElement"
    RelatedBuildingElement: "IfcElement"

class IfcRelFlowControlElements(IfcRelConnects):
    """Wrapper class for IfcRelFlowControlElements."""

    RelatedControlElements: list["IfcDistributionControlElement"]
    RelatingFlowElement: "IfcDistributionFlowElement"

class IfcRelInterferesElements(IfcRelConnects):
    """Wrapper class for IfcRelInterferesElements."""

    RelatingElement: "IfcElement"
    RelatedElement: "IfcElement"
    InterferenceGeometry: Optional["IfcConnectionGeometry"]
    InterferenceType: Optional[str]
    ImpliedOrder: bool

class IfcRelNests(IfcRelDecomposes):
    """Wrapper class for IfcRelNests."""

    RelatingObject: "IfcObjectDefinition"
    RelatedObjects: list["IfcObjectDefinition"]

class IfcRelProjectsElement(IfcRelDecomposes):
    """Wrapper class for IfcRelProjectsElement."""

    RelatingElement: "IfcElement"
    RelatedFeatureElement: "IfcFeatureElementAddition"

class IfcRelReferencedInSpatialStructure(IfcRelConnects):
    """Wrapper class for IfcRelReferencedInSpatialStructure."""

    RelatedElements: list["IfcProduct"]
    RelatingStructure: "IfcSpatialElement"

class IfcRelSequence(IfcRelConnects):
    """Wrapper class for IfcRelSequence."""

    RelatingProcess: "IfcProcess"
    RelatedProcess: "IfcProcess"
    TimeLag: Optional["IfcLagTime"]
    SequenceType: Optional["IfcSequenceEnum"]
    UserDefinedSequenceType: Optional[str]

class IfcRelServicesBuildings(IfcRelConnects):
    """Wrapper class for IfcRelServicesBuildings."""

    RelatingSystem: "IfcSystem"
    RelatedBuildings: list["IfcSpatialElement"]

class IfcRelSpaceBoundary(IfcRelConnects):
    """Wrapper class for IfcRelSpaceBoundary."""

    RelatingSpace: Union["IfcExternalSpatialElement", "IfcSpace"]
    RelatedBuildingElement: "IfcElement"
    ConnectionGeometry: Optional["IfcConnectionGeometry"]
    PhysicalOrVirtualBoundary: "IfcPhysicalOrVirtualEnum"
    InternalOrExternalBoundary: "IfcInternalOrExternalEnum"

class IfcRelVoidsElement(IfcRelDecomposes):
    """Wrapper class for IfcRelVoidsElement."""

    RelatingBuildingElement: "IfcElement"
    RelatedOpeningElement: "IfcFeatureElementSubtraction"

class IfcReparametrisedCompositeCurveSegment(IfcCompositeCurveSegment):
    """Wrapper class for IfcReparametrisedCompositeCurveSegment."""

    ParamLength: float

class IfcResource(IfcObject):
    """Wrapper class for IfcResource."""

    Identification: Optional[str]
    LongDescription: Optional[str]
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

class IfcSphere(IfcCsgPrimitive3D):
    """Wrapper class for IfcSphere."""

    Radius: float

class IfcStructuralLoadSingleDisplacementDistortion(IfcStructuralLoadSingleDisplacement):
    """Wrapper class for IfcStructuralLoadSingleDisplacementDistortion."""

    Distortion: Optional[float]

class IfcStructuralLoadSingleForceWarping(IfcStructuralLoadSingleForce):
    """Wrapper class for IfcStructuralLoadSingleForceWarping."""

    WarpingMoment: Optional[float]

class IfcSubedge(IfcEdge):
    """Wrapper class for IfcSubedge."""

    ParentEdge: "IfcEdge"

class IfcSurfaceCurve(IfcCurve):
    """Wrapper class for IfcSurfaceCurve."""

    Curve3D: "IfcCurve"
    AssociatedGeometry: list["IfcPcurve"]
    MasterRepresentation: "IfcPreferredSurfaceCurveRepresentation"

class IfcSweptAreaSolid(IfcSolidModel):
    """Wrapper class for IfcSweptAreaSolid."""

    SweptArea: "IfcProfileDef"
    Position: Optional["IfcAxis2Placement3D"]

class IfcSweptDiskSolid(IfcSolidModel):
    """Wrapper class for IfcSweptDiskSolid."""

    Directrix: "IfcCurve"
    Radius: float
    InnerRadius: Optional[float]
    StartParam: Optional[float]
    EndParam: Optional[float]

class IfcSweptSurface(IfcSurface):
    """Wrapper class for IfcSweptSurface."""

    SweptCurve: "IfcProfileDef"
    Position: Optional["IfcAxis2Placement3D"]

class IfcTessellatedFaceSet(IfcTessellatedItem):
    """Wrapper class for IfcTessellatedFaceSet."""

    Coordinates: "IfcCartesianPointList3D"
    def HasColours(self) -> tuple["IfcIndexedColourMap", ...]: ...
    def HasTextures(self) -> tuple["IfcIndexedTextureMap", ...]: ...

class IfcTextLiteralWithExtent(IfcTextLiteral):
    """Wrapper class for IfcTextLiteralWithExtent."""

    Extent: "IfcPlanarExtent"
    BoxAlignment: str

class IfcTypeProcess(IfcTypeObject):
    """Wrapper class for IfcTypeProcess."""

    Identification: Optional[str]
    LongDescription: Optional[str]
    ProcessType: Optional[str]
    def OperatesOn(self) -> tuple["IfcRelAssignsToProcess", ...]: ...

class IfcTypeProduct(IfcTypeObject):
    """Wrapper class for IfcTypeProduct."""

    RepresentationMaps: Optional[list["IfcRepresentationMap"]]
    Tag: Optional[str]
    def ReferencedBy(self) -> tuple["IfcRelAssignsToProduct", ...]: ...

class IfcTypeResource(IfcTypeObject):
    """Wrapper class for IfcTypeResource."""

    Identification: Optional[str]
    LongDescription: Optional[str]
    ResourceType: Optional[str]
    def ResourceOf(self) -> tuple["IfcRelAssignsToResource", ...]: ...

class IfcVertexLoop(IfcLoop):
    """Wrapper class for IfcVertexLoop."""

    LoopVertex: "IfcVertex"

class IfcVertexPoint(IfcVertex):
    """Wrapper class for IfcVertexPoint."""

    VertexGeometry: "IfcPoint"

class IfcWindowLiningProperties(IfcPreDefinedPropertySet):
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
    LiningOffset: Optional[float]
    LiningToPanelOffsetX: Optional[float]
    LiningToPanelOffsetY: Optional[float]

class IfcWindowPanelProperties(IfcPreDefinedPropertySet):
    """Wrapper class for IfcWindowPanelProperties."""

    OperationType: "IfcWindowPanelOperationEnum"
    PanelPosition: "IfcWindowPanelPositionEnum"
    FrameDepth: Optional[float]
    FrameThickness: Optional[float]
    ShapeAspectStyle: Optional["IfcShapeAspect"]

class IfcActionRequest(IfcControl):
    """Wrapper class for IfcActionRequest."""

    PredefinedType: Optional["IfcActionRequestTypeEnum"]
    Status: Optional[str]
    LongDescription: Optional[str]

class IfcAdvancedBrep(IfcManifoldSolidBrep):
    """Wrapper class for IfcAdvancedBrep."""

    ...

class IfcAdvancedFace(IfcFaceSurface):
    """Wrapper class for IfcAdvancedFace."""

    ...

class IfcAnnotation(IfcProduct):
    """Wrapper class for IfcAnnotation."""
    def ContainedInStructure(self) -> tuple["IfcRelContainedInSpatialStructure", ...]: ...

class IfcAsset(IfcGroup):
    """Wrapper class for IfcAsset."""

    Identification: Optional[str]
    OriginalValue: Optional["IfcCostValue"]
    CurrentValue: Optional["IfcCostValue"]
    TotalReplacementCost: Optional["IfcCostValue"]
    Owner: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    User: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    ResponsiblePerson: Optional["IfcPerson"]
    IncorporationDate: Optional[str]
    DepreciatedValue: Optional["IfcCostValue"]

class IfcBSplineCurve(IfcBoundedCurve):
    """Wrapper class for IfcBSplineCurve."""

    Degree: int
    ControlPointsList: list["IfcCartesianPoint"]
    CurveForm: "IfcBSplineCurveForm"
    ClosedCurve: bool
    SelfIntersect: bool

class IfcBSplineSurface(IfcBoundedSurface):
    """Wrapper class for IfcBSplineSurface."""

    UDegree: int
    VDegree: int
    ControlPointsList: list[list["IfcCartesianPoint"]]
    SurfaceForm: "IfcBSplineSurfaceForm"
    UClosed: bool
    VClosed: bool
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

class IfcComplexPropertyTemplate(IfcPropertyTemplate):
    """Wrapper class for IfcComplexPropertyTemplate."""

    UsageName: Optional[str]
    TemplateType: Optional["IfcComplexPropertyTemplateTypeEnum"]
    HasPropertyTemplates: Optional[list["IfcPropertyTemplate"]]

class IfcCompositeCurve(IfcBoundedCurve):
    """Wrapper class for IfcCompositeCurve."""

    Segments: list["IfcCompositeCurveSegment"]
    SelfIntersect: bool

class IfcConstructionResource(IfcResource):
    """Wrapper class for IfcConstructionResource."""

    Usage: Optional["IfcResourceTime"]
    BaseCosts: Optional[list["IfcAppliedValue"]]
    BaseQuantity: Optional["IfcPhysicalQuantity"]

class IfcConstructionResourceType(IfcTypeResource):
    """Wrapper class for IfcConstructionResourceType."""

    BaseCosts: Optional[list["IfcAppliedValue"]]
    BaseQuantity: Optional["IfcPhysicalQuantity"]

class IfcCostItem(IfcControl):
    """Wrapper class for IfcCostItem."""

    PredefinedType: Optional["IfcCostItemTypeEnum"]
    CostValues: Optional[list["IfcCostValue"]]
    CostQuantities: Optional[list["IfcPhysicalQuantity"]]

class IfcCostSchedule(IfcControl):
    """Wrapper class for IfcCostSchedule."""

    PredefinedType: Optional["IfcCostScheduleTypeEnum"]
    Status: Optional[str]
    SubmittedOn: Optional[str]
    UpdateDate: Optional[str]

class IfcCurveBoundedPlane(IfcBoundedSurface):
    """Wrapper class for IfcCurveBoundedPlane."""

    BasisSurface: "IfcPlane"
    OuterBoundary: "IfcCurve"
    InnerBoundaries: list["IfcCurve"]

class IfcCurveBoundedSurface(IfcBoundedSurface):
    """Wrapper class for IfcCurveBoundedSurface."""

    BasisSurface: "IfcSurface"
    Boundaries: list["IfcBoundaryCurve"]
    ImplicitOuter: bool

class IfcCylindricalSurface(IfcElementarySurface):
    """Wrapper class for IfcCylindricalSurface."""

    Radius: float

class IfcDoorStyle(IfcTypeProduct):
    """Wrapper class for IfcDoorStyle."""

    OperationType: "IfcDoorStyleOperationEnum"
    ConstructionType: "IfcDoorStyleConstructionEnum"
    ParameterTakesPrecedence: bool
    Sizeable: bool

class IfcElement(IfcProduct):
    """Wrapper class for IfcElement."""

    Tag: Optional[str]
    def FillsVoids(self) -> tuple["IfcRelFillsElement", ...]: ...
    def ConnectedTo(self) -> tuple["IfcRelConnectsElements", ...]: ...
    def IsInterferedByElements(self) -> tuple["IfcRelInterferesElements", ...]: ...
    def InterferesElements(self) -> tuple["IfcRelInterferesElements", ...]: ...
    def HasProjections(self) -> tuple["IfcRelProjectsElement", ...]: ...
    def ReferencedInStructures(self) -> tuple["IfcRelReferencedInSpatialStructure", ...]: ...
    def HasOpenings(self) -> tuple["IfcRelVoidsElement", ...]: ...
    def IsConnectionRealization(self) -> tuple["IfcRelConnectsWithRealizingElements", ...]: ...
    def ProvidesBoundaries(self) -> tuple["IfcRelSpaceBoundary", ...]: ...
    def ConnectedFrom(self) -> tuple["IfcRelConnectsElements", ...]: ...
    def ContainedInStructure(self) -> tuple["IfcRelContainedInSpatialStructure", ...]: ...
    def HasCoverings(self) -> tuple["IfcRelCoversBldgElements", ...]: ...
    @property
    def parent(self) -> object: ...

class IfcElementType(IfcTypeProduct):
    """Wrapper class for IfcElementType."""

    ElementType: Optional[str]

class IfcEllipse(IfcConic):
    """Wrapper class for IfcEllipse."""

    SemiAxis1: float
    SemiAxis2: float

class IfcEvent(IfcProcess):
    """Wrapper class for IfcEvent."""

    PredefinedType: Optional["IfcEventTypeEnum"]
    EventTriggerType: Optional["IfcEventTriggerTypeEnum"]
    UserDefinedEventTriggerType: Optional[str]
    EventOccurenceTime: Optional["IfcEventTime"]

class IfcEventType(IfcTypeProcess):
    """Wrapper class for IfcEventType."""

    PredefinedType: "IfcEventTypeEnum"
    EventTriggerType: "IfcEventTriggerTypeEnum"
    UserDefinedEventTriggerType: Optional[str]

class IfcExtrudedAreaSolid(IfcSweptAreaSolid):
    """Wrapper class for IfcExtrudedAreaSolid."""

    ExtrudedDirection: "IfcDirection"
    Depth: float

class IfcFacetedBrep(IfcManifoldSolidBrep):
    """Wrapper class for IfcFacetedBrep."""

    ...

class IfcFacetedBrepWithVoids(IfcFacetedBrep):
    """Wrapper class for IfcFacetedBrepWithVoids."""

    Voids: list["IfcClosedShell"]

class IfcFixedReferenceSweptAreaSolid(IfcSweptAreaSolid):
    """Wrapper class for IfcFixedReferenceSweptAreaSolid."""

    Directrix: "IfcCurve"
    StartParam: Optional[float]
    EndParam: Optional[float]
    FixedReference: "IfcDirection"

class IfcGrid(IfcProduct):
    """Wrapper class for IfcGrid."""

    UAxes: list["IfcGridAxis"]
    VAxes: list["IfcGridAxis"]
    WAxes: Optional[list["IfcGridAxis"]]
    PredefinedType: Optional["IfcGridTypeEnum"]
    def ContainedInStructure(self) -> tuple["IfcRelContainedInSpatialStructure", ...]: ...

class IfcIndexedPolyCurve(IfcBoundedCurve):
    """Wrapper class for IfcIndexedPolyCurve."""

    Points: "IfcCartesianPointList"
    Segments: Optional[list[list[int]]]
    SelfIntersect: Optional[bool]

class IfcIndexedPolygonalFaceWithVoids(IfcIndexedPolygonalFace):
    """Wrapper class for IfcIndexedPolygonalFaceWithVoids."""

    InnerCoordIndices: list[list[int]]

class IfcIntersectionCurve(IfcSurfaceCurve):
    """Wrapper class for IfcIntersectionCurve."""

    ...

class IfcInventory(IfcGroup):
    """Wrapper class for IfcInventory."""

    PredefinedType: Optional["IfcInventoryTypeEnum"]
    Jurisdiction: Optional[Union["IfcOrganization", "IfcPerson", "IfcPersonAndOrganization"]]
    ResponsiblePersons: Optional[list["IfcPerson"]]
    LastUpdateDate: Optional[str]
    CurrentValue: Optional["IfcCostValue"]
    OriginalValue: Optional["IfcCostValue"]

class IfcLightSourceSpot(IfcLightSourcePositional):
    """Wrapper class for IfcLightSourceSpot."""

    Orientation: "IfcDirection"
    ConcentrationExponent: Optional[float]
    SpreadAngle: float
    BeamWidthAngle: float

class IfcOccupant(IfcActor):
    """Wrapper class for IfcOccupant."""

    PredefinedType: Optional["IfcOccupantTypeEnum"]

class IfcPerformanceHistory(IfcControl):
    """Wrapper class for IfcPerformanceHistory."""

    LifeCyclePhase: str
    PredefinedType: Optional["IfcPerformanceHistoryTypeEnum"]

class IfcPermit(IfcControl):
    """Wrapper class for IfcPermit."""

    PredefinedType: Optional["IfcPermitTypeEnum"]
    Status: Optional[str]
    LongDescription: Optional[str]

class IfcPlane(IfcElementarySurface):
    """Wrapper class for IfcPlane."""

    ...

class IfcPolygonalFaceSet(IfcTessellatedFaceSet):
    """Wrapper class for IfcPolygonalFaceSet."""

    Closed: Optional[bool]
    Faces: list["IfcIndexedPolygonalFace"]
    PnIndex: Optional[list[int]]

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

    PredefinedType: Optional["IfcProcedureTypeEnum"]

class IfcProcedureType(IfcTypeProcess):
    """Wrapper class for IfcProcedureType."""

    PredefinedType: "IfcProcedureTypeEnum"

class IfcProjectOrder(IfcControl):
    """Wrapper class for IfcProjectOrder."""

    PredefinedType: Optional["IfcProjectOrderTypeEnum"]
    Status: Optional[str]
    LongDescription: Optional[str]

class IfcProxy(IfcProduct):
    """Wrapper class for IfcProxy."""

    ProxyType: "IfcObjectTypeEnum"
    Tag: Optional[str]

class IfcRectangularTrimmedSurface(IfcBoundedSurface):
    """Wrapper class for IfcRectangularTrimmedSurface."""

    BasisSurface: "IfcSurface"
    U1: float
    V1: float
    U2: float
    V2: float
    Usense: bool
    Vsense: bool

class IfcRelAssignsToGroupByFactor(IfcRelAssignsToGroup):
    """Wrapper class for IfcRelAssignsToGroupByFactor."""

    Factor: float

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

class IfcRelSpaceBoundary1stLevel(IfcRelSpaceBoundary):
    """Wrapper class for IfcRelSpaceBoundary1stLevel."""

    ParentBoundary: Optional["IfcRelSpaceBoundary1stLevel"]
    def InnerBoundaries(self) -> tuple["IfcRelSpaceBoundary1stLevel", ...]: ...

class IfcRevolvedAreaSolid(IfcSweptAreaSolid):
    """Wrapper class for IfcRevolvedAreaSolid."""

    Axis: "IfcAxis1Placement"
    Angle: float

class IfcSeamCurve(IfcSurfaceCurve):
    """Wrapper class for IfcSeamCurve."""

    ...

class IfcSimplePropertyTemplate(IfcPropertyTemplate):
    """Wrapper class for IfcSimplePropertyTemplate."""

    TemplateType: Optional["IfcSimplePropertyTemplateTypeEnum"]
    PrimaryMeasureType: Optional[str]
    SecondaryMeasureType: Optional[str]
    Enumerators: Optional["IfcPropertyEnumeration"]
    PrimaryUnit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    SecondaryUnit: Optional[Union["IfcDerivedUnit", "IfcMonetaryUnit", "IfcNamedUnit"]]
    Expression: Optional[str]
    AccessState: Optional["IfcStateEnum"]

class IfcSpatialElement(IfcProduct):
    """Wrapper class for IfcSpatialElement."""

    LongName: Optional[str]
    def ContainsElements(self) -> tuple["IfcRelContainedInSpatialStructure", ...]: ...
    def ServicedBySystems(self) -> tuple["IfcRelServicesBuildings", ...]: ...
    def ReferencesElements(self) -> tuple["IfcRelReferencedInSpatialStructure", ...]: ...
    @property
    def children(self) -> object: ...

class IfcSpatialElementType(IfcTypeProduct):
    """Wrapper class for IfcSpatialElementType."""

    ElementType: Optional[str]

class IfcSpatialStructureElement(IfcSpatialElement):
    """Wrapper class for IfcSpatialStructureElement."""

    CompositionType: Optional["IfcElementCompositionEnum"]

class IfcSphericalSurface(IfcElementarySurface):
    """Wrapper class for IfcSphericalSurface."""

    Radius: float

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
    StartParam: Optional[float]
    EndParam: Optional[float]
    ReferenceSurface: "IfcSurface"

class IfcSurfaceOfLinearExtrusion(IfcSweptSurface):
    """Wrapper class for IfcSurfaceOfLinearExtrusion."""

    ExtrudedDirection: "IfcDirection"
    Depth: float

class IfcSurfaceOfRevolution(IfcSweptSurface):
    """Wrapper class for IfcSurfaceOfRevolution."""

    AxisPosition: "IfcAxis1Placement"

class IfcSweptDiskSolidPolygonal(IfcSweptDiskSolid):
    """Wrapper class for IfcSweptDiskSolidPolygonal."""

    FilletRadius: Optional[float]

class IfcSystem(IfcGroup):
    """Wrapper class for IfcSystem."""
    def ServicesBuildings(self) -> tuple["IfcRelServicesBuildings", ...]: ...

class IfcTask(IfcProcess):
    """Wrapper class for IfcTask."""

    Status: Optional[str]
    WorkMethod: Optional[str]
    IsMilestone: bool
    Priority: Optional[int]
    TaskTime: Optional["IfcTaskTime"]
    PredefinedType: Optional["IfcTaskTypeEnum"]

class IfcTaskType(IfcTypeProcess):
    """Wrapper class for IfcTaskType."""

    PredefinedType: "IfcTaskTypeEnum"
    WorkMethod: Optional[str]

class IfcToroidalSurface(IfcElementarySurface):
    """Wrapper class for IfcToroidalSurface."""

    MajorRadius: float
    MinorRadius: float

class IfcTriangulatedFaceSet(IfcTessellatedFaceSet):
    """Wrapper class for IfcTriangulatedFaceSet."""

    Normals: Optional[list[list[float]]]
    Closed: Optional[bool]
    CoordIndex: list[list[int]]
    PnIndex: Optional[list[int]]

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

class IfcWorkCalendar(IfcControl):
    """Wrapper class for IfcWorkCalendar."""

    WorkingTimes: Optional[list["IfcWorkTime"]]
    ExceptionTimes: Optional[list["IfcWorkTime"]]
    PredefinedType: Optional["IfcWorkCalendarTypeEnum"]

class IfcWorkControl(IfcControl):
    """Wrapper class for IfcWorkControl."""

    CreationDate: str
    Creators: Optional[list["IfcPerson"]]
    Purpose: Optional[str]
    Duration: Optional[str]
    TotalFloat: Optional[str]
    StartTime: str
    FinishTime: Optional[str]

class IfcZone(IfcSystem):
    """Wrapper class for IfcZone."""

    LongName: Optional[str]

class IfcAdvancedBrepWithVoids(IfcAdvancedBrep):
    """Wrapper class for IfcAdvancedBrepWithVoids."""

    Voids: list["IfcClosedShell"]

class IfcBSplineCurveWithKnots(IfcBSplineCurve):
    """Wrapper class for IfcBSplineCurveWithKnots."""

    KnotMultiplicities: list[int]
    Knots: list[float]
    KnotSpec: "IfcKnotType"

class IfcBSplineSurfaceWithKnots(IfcBSplineSurface):
    """Wrapper class for IfcBSplineSurfaceWithKnots."""

    UMultiplicities: list[int]
    VMultiplicities: list[int]
    UKnots: list[float]
    VKnots: list[float]
    KnotSpec: "IfcKnotType"

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

class IfcBuildingSystem(IfcSystem):
    """Wrapper class for IfcBuildingSystem."""

    PredefinedType: Optional["IfcBuildingSystemTypeEnum"]
    LongName: Optional[str]

class IfcCivilElement(IfcElement):
    """Wrapper class for IfcCivilElement."""

    ...

class IfcCivilElementType(IfcElementType):
    """Wrapper class for IfcCivilElementType."""

    ...

class IfcCompositeCurveOnSurface(IfcCompositeCurve):
    """Wrapper class for IfcCompositeCurveOnSurface."""

    ...

class IfcConstructionEquipmentResource(IfcConstructionResource):
    """Wrapper class for IfcConstructionEquipmentResource."""

    PredefinedType: Optional["IfcConstructionEquipmentResourceTypeEnum"]

class IfcConstructionEquipmentResourceType(IfcConstructionResourceType):
    """Wrapper class for IfcConstructionEquipmentResourceType."""

    PredefinedType: "IfcConstructionEquipmentResourceTypeEnum"

class IfcConstructionMaterialResource(IfcConstructionResource):
    """Wrapper class for IfcConstructionMaterialResource."""

    PredefinedType: Optional["IfcConstructionMaterialResourceTypeEnum"]

class IfcConstructionMaterialResourceType(IfcConstructionResourceType):
    """Wrapper class for IfcConstructionMaterialResourceType."""

    PredefinedType: "IfcConstructionMaterialResourceTypeEnum"

class IfcConstructionProductResource(IfcConstructionResource):
    """Wrapper class for IfcConstructionProductResource."""

    PredefinedType: Optional["IfcConstructionProductResourceTypeEnum"]

class IfcConstructionProductResourceType(IfcConstructionResourceType):
    """Wrapper class for IfcConstructionProductResourceType."""

    PredefinedType: "IfcConstructionProductResourceTypeEnum"

class IfcCrewResource(IfcConstructionResource):
    """Wrapper class for IfcCrewResource."""

    PredefinedType: Optional["IfcCrewResourceTypeEnum"]

class IfcCrewResourceType(IfcConstructionResourceType):
    """Wrapper class for IfcCrewResourceType."""

    PredefinedType: "IfcCrewResourceTypeEnum"

class IfcDistributionElement(IfcElement):
    """Wrapper class for IfcDistributionElement."""
    def HasPorts(self) -> tuple["IfcRelConnectsPortToElement", ...]: ...

class IfcDistributionElementType(IfcElementType):
    """Wrapper class for IfcDistributionElementType."""

    ...

class IfcDistributionPort(IfcPort):
    """Wrapper class for IfcDistributionPort."""

    FlowDirection: Optional["IfcFlowDirectionEnum"]
    PredefinedType: Optional["IfcDistributionPortTypeEnum"]
    SystemType: Optional["IfcDistributionSystemEnum"]

class IfcDistributionSystem(IfcSystem):
    """Wrapper class for IfcDistributionSystem."""

    LongName: Optional[str]
    PredefinedType: Optional["IfcDistributionSystemEnum"]

class IfcElementAssembly(IfcElement):
    """Wrapper class for IfcElementAssembly."""

    AssemblyPlace: Optional["IfcAssemblyPlaceEnum"]
    PredefinedType: Optional["IfcElementAssemblyTypeEnum"]

class IfcElementAssemblyType(IfcElementType):
    """Wrapper class for IfcElementAssemblyType."""

    PredefinedType: "IfcElementAssemblyTypeEnum"

class IfcElementComponent(IfcElement):
    """Wrapper class for IfcElementComponent."""

    ...

class IfcElementComponentType(IfcElementType):
    """Wrapper class for IfcElementComponentType."""

    ...

class IfcExternalSpatialStructureElement(IfcSpatialElement):
    """Wrapper class for IfcExternalSpatialStructureElement."""

    ...

class IfcExtrudedAreaSolidTapered(IfcExtrudedAreaSolid):
    """Wrapper class for IfcExtrudedAreaSolidTapered."""

    EndSweptArea: "IfcProfileDef"

class IfcFeatureElement(IfcElement):
    """Wrapper class for IfcFeatureElement."""

    ...

class IfcFurnishingElement(IfcElement):
    """Wrapper class for IfcFurnishingElement."""

    ...

class IfcFurnishingElementType(IfcElementType):
    """Wrapper class for IfcFurnishingElementType."""

    ...

class IfcGeographicElement(IfcElement):
    """Wrapper class for IfcGeographicElement."""

    PredefinedType: Optional["IfcGeographicElementTypeEnum"]

class IfcGeographicElementType(IfcElementType):
    """Wrapper class for IfcGeographicElementType."""

    PredefinedType: "IfcGeographicElementTypeEnum"

class IfcLaborResource(IfcConstructionResource):
    """Wrapper class for IfcLaborResource."""

    PredefinedType: Optional["IfcLaborResourceTypeEnum"]

class IfcLaborResourceType(IfcConstructionResourceType):
    """Wrapper class for IfcLaborResourceType."""

    PredefinedType: "IfcLaborResourceTypeEnum"

class IfcRelSpaceBoundary2ndLevel(IfcRelSpaceBoundary1stLevel):
    """Wrapper class for IfcRelSpaceBoundary2ndLevel."""

    CorrespondingBoundary: Optional["IfcRelSpaceBoundary2ndLevel"]
    def Corresponds(self) -> tuple["IfcRelSpaceBoundary2ndLevel", ...]: ...

class IfcRevolvedAreaSolidTapered(IfcRevolvedAreaSolid):
    """Wrapper class for IfcRevolvedAreaSolidTapered."""

    EndSweptArea: "IfcProfileDef"

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

    PredefinedType: Optional["IfcSpaceTypeEnum"]
    ElevationWithFlooring: Optional[float]
    def HasCoverings(self) -> tuple["IfcRelCoversSpaces", ...]: ...
    def BoundedBy(self) -> tuple["IfcRelSpaceBoundary", ...]: ...

class IfcSpatialStructureElementType(IfcSpatialElementType):
    """Wrapper class for IfcSpatialStructureElementType."""

    ...

class IfcSpatialZone(IfcSpatialElement):
    """Wrapper class for IfcSpatialZone."""

    PredefinedType: Optional["IfcSpatialZoneTypeEnum"]

class IfcSpatialZoneType(IfcSpatialElementType):
    """Wrapper class for IfcSpatialZoneType."""

    PredefinedType: "IfcSpatialZoneTypeEnum"
    LongName: Optional[str]

class IfcStructuralAction(IfcStructuralActivity):
    """Wrapper class for IfcStructuralAction."""

    DestabilizingLoad: Optional[bool]

class IfcStructuralAnalysisModel(IfcSystem):
    """Wrapper class for IfcStructuralAnalysisModel."""

    PredefinedType: "IfcAnalysisModelTypeEnum"
    OrientationOf2DPlane: Optional["IfcAxis2Placement3D"]
    LoadedBy: Optional[list["IfcStructuralLoadGroup"]]
    HasResults: Optional[list["IfcStructuralResultGroup"]]
    SharedPlacement: Optional["IfcObjectPlacement"]

class IfcStructuralConnection(IfcStructuralItem):
    """Wrapper class for IfcStructuralConnection."""

    AppliedCondition: Optional["IfcBoundaryCondition"]
    def ConnectsStructuralMembers(self) -> tuple["IfcRelConnectsStructuralMember", ...]: ...

class IfcStructuralLoadCase(IfcStructuralLoadGroup):
    """Wrapper class for IfcStructuralLoadCase."""

    SelfWeightCoefficients: Optional[list[float]]

class IfcStructuralMember(IfcStructuralItem):
    """Wrapper class for IfcStructuralMember."""
    def ConnectedBy(self) -> tuple["IfcRelConnectsStructuralMember", ...]: ...

class IfcStructuralReaction(IfcStructuralActivity):
    """Wrapper class for IfcStructuralReaction."""

    ...

class IfcSubContractResource(IfcConstructionResource):
    """Wrapper class for IfcSubContractResource."""

    PredefinedType: Optional["IfcSubContractResourceTypeEnum"]

class IfcSubContractResourceType(IfcConstructionResourceType):
    """Wrapper class for IfcSubContractResourceType."""

    PredefinedType: "IfcSubContractResourceTypeEnum"

class IfcTransportElement(IfcElement):
    """Wrapper class for IfcTransportElement."""

    PredefinedType: Optional["IfcTransportElementTypeEnum"]

class IfcTransportElementType(IfcElementType):
    """Wrapper class for IfcTransportElementType."""

    PredefinedType: "IfcTransportElementTypeEnum"

class IfcVirtualElement(IfcElement):
    """Wrapper class for IfcVirtualElement."""

    ...

class IfcWorkPlan(IfcWorkControl):
    """Wrapper class for IfcWorkPlan."""

    PredefinedType: Optional["IfcWorkPlanTypeEnum"]

class IfcWorkSchedule(IfcWorkControl):
    """Wrapper class for IfcWorkSchedule."""

    PredefinedType: Optional["IfcWorkScheduleTypeEnum"]

class IfcBeam(IfcBuildingElement):
    """Wrapper class for IfcBeam."""

    PredefinedType: Optional["IfcBeamTypeEnum"]

class IfcBeamType(IfcBuildingElementType):
    """Wrapper class for IfcBeamType."""

    PredefinedType: "IfcBeamTypeEnum"

class IfcBoundaryCurve(IfcCompositeCurveOnSurface):
    """Wrapper class for IfcBoundaryCurve."""

    ...

class IfcBuildingElementPartType(IfcElementComponentType):
    """Wrapper class for IfcBuildingElementPartType."""

    PredefinedType: "IfcBuildingElementPartTypeEnum"

class IfcBuildingElementProxy(IfcBuildingElement):
    """Wrapper class for IfcBuildingElementProxy."""

    PredefinedType: Optional["IfcBuildingElementProxyTypeEnum"]

class IfcBuildingElementProxyType(IfcBuildingElementType):
    """Wrapper class for IfcBuildingElementProxyType."""

    PredefinedType: "IfcBuildingElementProxyTypeEnum"

class IfcChimney(IfcBuildingElement):
    """Wrapper class for IfcChimney."""

    PredefinedType: Optional["IfcChimneyTypeEnum"]

class IfcChimneyType(IfcBuildingElementType):
    """Wrapper class for IfcChimneyType."""

    PredefinedType: "IfcChimneyTypeEnum"

class IfcColumn(IfcBuildingElement):
    """Wrapper class for IfcColumn."""

    PredefinedType: Optional["IfcColumnTypeEnum"]

class IfcColumnType(IfcBuildingElementType):
    """Wrapper class for IfcColumnType."""

    PredefinedType: "IfcColumnTypeEnum"

class IfcCovering(IfcBuildingElement):
    """Wrapper class for IfcCovering."""

    PredefinedType: Optional["IfcCoveringTypeEnum"]
    def CoversSpaces(self) -> tuple["IfcRelCoversSpaces", ...]: ...
    def CoversElements(self) -> tuple["IfcRelCoversBldgElements", ...]: ...

class IfcCoveringType(IfcBuildingElementType):
    """Wrapper class for IfcCoveringType."""

    PredefinedType: "IfcCoveringTypeEnum"

class IfcCurtainWall(IfcBuildingElement):
    """Wrapper class for IfcCurtainWall."""

    PredefinedType: Optional["IfcCurtainWallTypeEnum"]

class IfcCurtainWallType(IfcBuildingElementType):
    """Wrapper class for IfcCurtainWallType."""

    PredefinedType: "IfcCurtainWallTypeEnum"

class IfcDiscreteAccessory(IfcElementComponent):
    """Wrapper class for IfcDiscreteAccessory."""

    PredefinedType: Optional["IfcDiscreteAccessoryTypeEnum"]

class IfcDiscreteAccessoryType(IfcElementComponentType):
    """Wrapper class for IfcDiscreteAccessoryType."""

    PredefinedType: "IfcDiscreteAccessoryTypeEnum"

class IfcDistributionCircuit(IfcDistributionSystem):
    """Wrapper class for IfcDistributionCircuit."""

    ...

class IfcDistributionControlElement(IfcDistributionElement):
    """Wrapper class for IfcDistributionControlElement."""
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
    PredefinedType: Optional["IfcDoorTypeEnum"]
    OperationType: Optional["IfcDoorTypeOperationEnum"]
    UserDefinedOperationType: Optional[str]

class IfcDoorType(IfcBuildingElementType):
    """Wrapper class for IfcDoorType."""

    PredefinedType: "IfcDoorTypeEnum"
    OperationType: "IfcDoorTypeOperationEnum"
    ParameterTakesPrecedence: Optional[bool]
    UserDefinedOperationType: Optional[str]

class IfcExternalSpatialElement(IfcExternalSpatialStructureElement):
    """Wrapper class for IfcExternalSpatialElement."""

    PredefinedType: Optional["IfcExternalSpatialElementTypeEnum"]
    def BoundedBy(self) -> tuple["IfcRelSpaceBoundary", ...]: ...

class IfcFastener(IfcElementComponent):
    """Wrapper class for IfcFastener."""

    PredefinedType: Optional["IfcFastenerTypeEnum"]

class IfcFastenerType(IfcElementComponentType):
    """Wrapper class for IfcFastenerType."""

    PredefinedType: "IfcFastenerTypeEnum"

class IfcFeatureElementAddition(IfcFeatureElement):
    """Wrapper class for IfcFeatureElementAddition."""
    def ProjectsElements(self) -> tuple["IfcRelProjectsElement", ...]: ...

class IfcFeatureElementSubtraction(IfcFeatureElement):
    """Wrapper class for IfcFeatureElementSubtraction."""
    def VoidsElements(self) -> tuple["IfcRelVoidsElement", ...]: ...

class IfcFooting(IfcBuildingElement):
    """Wrapper class for IfcFooting."""

    PredefinedType: Optional["IfcFootingTypeEnum"]

class IfcFootingType(IfcBuildingElementType):
    """Wrapper class for IfcFootingType."""

    PredefinedType: "IfcFootingTypeEnum"

class IfcFurniture(IfcFurnishingElement):
    """Wrapper class for IfcFurniture."""

    PredefinedType: Optional["IfcFurnitureTypeEnum"]

class IfcFurnitureType(IfcFurnishingElementType):
    """Wrapper class for IfcFurnitureType."""

    AssemblyPlace: "IfcAssemblyPlaceEnum"
    PredefinedType: Optional["IfcFurnitureTypeEnum"]

class IfcMember(IfcBuildingElement):
    """Wrapper class for IfcMember."""

    PredefinedType: Optional["IfcMemberTypeEnum"]

class IfcMemberType(IfcBuildingElementType):
    """Wrapper class for IfcMemberType."""

    PredefinedType: "IfcMemberTypeEnum"

class IfcPile(IfcBuildingElement):
    """Wrapper class for IfcPile."""

    PredefinedType: Optional["IfcPileTypeEnum"]
    ConstructionType: Optional["IfcPileConstructionEnum"]

class IfcPileType(IfcBuildingElementType):
    """Wrapper class for IfcPileType."""

    PredefinedType: "IfcPileTypeEnum"

class IfcPlate(IfcBuildingElement):
    """Wrapper class for IfcPlate."""

    PredefinedType: Optional["IfcPlateTypeEnum"]

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

    PredefinedType: Optional["IfcRampTypeEnum"]

class IfcRampFlight(IfcBuildingElement):
    """Wrapper class for IfcRampFlight."""

    PredefinedType: Optional["IfcRampFlightTypeEnum"]

class IfcRampFlightType(IfcBuildingElementType):
    """Wrapper class for IfcRampFlightType."""

    PredefinedType: "IfcRampFlightTypeEnum"

class IfcRampType(IfcBuildingElementType):
    """Wrapper class for IfcRampType."""

    PredefinedType: "IfcRampTypeEnum"

class IfcRationalBSplineCurveWithKnots(IfcBSplineCurveWithKnots):
    """Wrapper class for IfcRationalBSplineCurveWithKnots."""

    WeightsData: list[float]

class IfcRationalBSplineSurfaceWithKnots(IfcBSplineSurfaceWithKnots):
    """Wrapper class for IfcRationalBSplineSurfaceWithKnots."""

    WeightsData: list[list[float]]

class IfcReinforcingElementType(IfcElementComponentType):
    """Wrapper class for IfcReinforcingElementType."""

    ...

class IfcRoof(IfcBuildingElement):
    """Wrapper class for IfcRoof."""

    PredefinedType: Optional["IfcRoofTypeEnum"]

class IfcRoofType(IfcBuildingElementType):
    """Wrapper class for IfcRoofType."""

    PredefinedType: "IfcRoofTypeEnum"

class IfcShadingDevice(IfcBuildingElement):
    """Wrapper class for IfcShadingDevice."""

    PredefinedType: Optional["IfcShadingDeviceTypeEnum"]

class IfcShadingDeviceType(IfcBuildingElementType):
    """Wrapper class for IfcShadingDeviceType."""

    PredefinedType: "IfcShadingDeviceTypeEnum"

class IfcSlab(IfcBuildingElement):
    """Wrapper class for IfcSlab."""

    PredefinedType: Optional["IfcSlabTypeEnum"]

class IfcSlabType(IfcBuildingElementType):
    """Wrapper class for IfcSlabType."""

    PredefinedType: "IfcSlabTypeEnum"

class IfcSpaceType(IfcSpatialStructureElementType):
    """Wrapper class for IfcSpaceType."""

    PredefinedType: "IfcSpaceTypeEnum"
    LongName: Optional[str]

class IfcStair(IfcBuildingElement):
    """Wrapper class for IfcStair."""

    PredefinedType: Optional["IfcStairTypeEnum"]

class IfcStairFlight(IfcBuildingElement):
    """Wrapper class for IfcStairFlight."""

    NumberOfRisers: Optional[int]
    NumberOfTreads: Optional[int]
    RiserHeight: Optional[float]
    TreadLength: Optional[float]
    PredefinedType: Optional["IfcStairFlightTypeEnum"]

class IfcStairFlightType(IfcBuildingElementType):
    """Wrapper class for IfcStairFlightType."""

    PredefinedType: "IfcStairFlightTypeEnum"

class IfcStairType(IfcBuildingElementType):
    """Wrapper class for IfcStairType."""

    PredefinedType: "IfcStairTypeEnum"

class IfcStructuralCurveAction(IfcStructuralAction):
    """Wrapper class for IfcStructuralCurveAction."""

    ProjectedOrTrue: Optional["IfcProjectedOrTrueLengthEnum"]
    PredefinedType: "IfcStructuralCurveActivityTypeEnum"

class IfcStructuralCurveConnection(IfcStructuralConnection):
    """Wrapper class for IfcStructuralCurveConnection."""

    Axis: "IfcDirection"

class IfcStructuralCurveMember(IfcStructuralMember):
    """Wrapper class for IfcStructuralCurveMember."""

    PredefinedType: "IfcStructuralCurveMemberTypeEnum"
    Axis: "IfcDirection"

class IfcStructuralCurveReaction(IfcStructuralReaction):
    """Wrapper class for IfcStructuralCurveReaction."""

    PredefinedType: "IfcStructuralCurveActivityTypeEnum"

class IfcStructuralLinearAction(IfcStructuralCurveAction):
    """Wrapper class for IfcStructuralLinearAction."""

    ...

class IfcStructuralPlanarAction(IfcStructuralSurfaceAction):
    """Wrapper class for IfcStructuralPlanarAction."""

    ...

class IfcStructuralPointAction(IfcStructuralAction):
    """Wrapper class for IfcStructuralPointAction."""

    ...

class IfcStructuralPointConnection(IfcStructuralConnection):
    """Wrapper class for IfcStructuralPointConnection."""

    ConditionCoordinateSystem: Optional["IfcAxis2Placement3D"]

class IfcStructuralPointReaction(IfcStructuralReaction):
    """Wrapper class for IfcStructuralPointReaction."""

    ...

class IfcStructuralSurfaceAction(IfcStructuralAction):
    """Wrapper class for IfcStructuralSurfaceAction."""

    ProjectedOrTrue: Optional["IfcProjectedOrTrueLengthEnum"]
    PredefinedType: "IfcStructuralSurfaceActivityTypeEnum"

class IfcStructuralSurfaceConnection(IfcStructuralConnection):
    """Wrapper class for IfcStructuralSurfaceConnection."""

    ...

class IfcStructuralSurfaceMember(IfcStructuralMember):
    """Wrapper class for IfcStructuralSurfaceMember."""

    PredefinedType: "IfcStructuralSurfaceMemberTypeEnum"
    Thickness: Optional[float]

class IfcStructuralSurfaceReaction(IfcStructuralReaction):
    """Wrapper class for IfcStructuralSurfaceReaction."""

    PredefinedType: "IfcStructuralSurfaceActivityTypeEnum"

class IfcSurfaceFeature(IfcFeatureElement):
    """Wrapper class for IfcSurfaceFeature."""

    PredefinedType: Optional["IfcSurfaceFeatureTypeEnum"]

class IfcSystemFurnitureElement(IfcFurnishingElement):
    """Wrapper class for IfcSystemFurnitureElement."""

    PredefinedType: Optional["IfcSystemFurnitureElementTypeEnum"]

class IfcSystemFurnitureElementType(IfcFurnishingElementType):
    """Wrapper class for IfcSystemFurnitureElementType."""

    PredefinedType: Optional["IfcSystemFurnitureElementTypeEnum"]

class IfcVibrationIsolator(IfcElementComponent):
    """Wrapper class for IfcVibrationIsolator."""

    PredefinedType: Optional["IfcVibrationIsolatorTypeEnum"]

class IfcWall(IfcBuildingElement):
    """Wrapper class for IfcWall."""

    PredefinedType: Optional["IfcWallTypeEnum"]

class IfcWallType(IfcBuildingElementType):
    """Wrapper class for IfcWallType."""

    PredefinedType: "IfcWallTypeEnum"

class IfcWindow(IfcBuildingElement):
    """Wrapper class for IfcWindow."""

    OverallHeight: Optional[float]
    OverallWidth: Optional[float]
    PredefinedType: Optional["IfcWindowTypeEnum"]
    PartitioningType: Optional["IfcWindowTypePartitioningEnum"]
    UserDefinedPartitioningType: Optional[str]

class IfcWindowType(IfcBuildingElementType):
    """Wrapper class for IfcWindowType."""

    PredefinedType: "IfcWindowTypeEnum"
    PartitioningType: "IfcWindowTypePartitioningEnum"
    ParameterTakesPrecedence: Optional[bool]
    UserDefinedPartitioningType: Optional[str]

class IfcActuator(IfcDistributionControlElement):
    """Wrapper class for IfcActuator."""

    PredefinedType: Optional["IfcActuatorTypeEnum"]

class IfcActuatorType(IfcDistributionControlElementType):
    """Wrapper class for IfcActuatorType."""

    PredefinedType: "IfcActuatorTypeEnum"

class IfcAlarm(IfcDistributionControlElement):
    """Wrapper class for IfcAlarm."""

    PredefinedType: Optional["IfcAlarmTypeEnum"]

class IfcAlarmType(IfcDistributionControlElementType):
    """Wrapper class for IfcAlarmType."""

    PredefinedType: "IfcAlarmTypeEnum"

class IfcBeamStandardCase(IfcBeam):
    """Wrapper class for IfcBeamStandardCase."""

    ...

class IfcBuildingElementPart(IfcElementComponent):
    """Wrapper class for IfcBuildingElementPart."""

    PredefinedType: Optional["IfcBuildingElementPartTypeEnum"]

class IfcColumnStandardCase(IfcColumn):
    """Wrapper class for IfcColumnStandardCase."""

    ...

class IfcController(IfcDistributionControlElement):
    """Wrapper class for IfcController."""

    PredefinedType: Optional["IfcControllerTypeEnum"]

class IfcControllerType(IfcDistributionControlElementType):
    """Wrapper class for IfcControllerType."""

    PredefinedType: "IfcControllerTypeEnum"

class IfcDistributionChamberElement(IfcDistributionFlowElement):
    """Wrapper class for IfcDistributionChamberElement."""

    PredefinedType: Optional["IfcDistributionChamberElementTypeEnum"]

class IfcDistributionChamberElementType(IfcDistributionFlowElementType):
    """Wrapper class for IfcDistributionChamberElementType."""

    PredefinedType: "IfcDistributionChamberElementTypeEnum"

class IfcDoorStandardCase(IfcDoor):
    """Wrapper class for IfcDoorStandardCase."""

    ...

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

class IfcFlowInstrument(IfcDistributionControlElement):
    """Wrapper class for IfcFlowInstrument."""

    PredefinedType: Optional["IfcFlowInstrumentTypeEnum"]

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

class IfcMechanicalFastener(IfcElementComponent):
    """Wrapper class for IfcMechanicalFastener."""

    NominalDiameter: Optional[float]
    NominalLength: Optional[float]
    PredefinedType: Optional["IfcMechanicalFastenerTypeEnum"]

class IfcMechanicalFastenerType(IfcElementComponentType):
    """Wrapper class for IfcMechanicalFastenerType."""

    PredefinedType: "IfcMechanicalFastenerTypeEnum"
    NominalDiameter: Optional[float]
    NominalLength: Optional[float]

class IfcMemberStandardCase(IfcMember):
    """Wrapper class for IfcMemberStandardCase."""

    ...

class IfcOpeningElement(IfcFeatureElementSubtraction):
    """Wrapper class for IfcOpeningElement."""

    PredefinedType: Optional["IfcOpeningElementTypeEnum"]
    def HasFillings(self) -> tuple["IfcRelFillsElement", ...]: ...

class IfcOuterBoundaryCurve(IfcBoundaryCurve):
    """Wrapper class for IfcOuterBoundaryCurve."""

    ...

class IfcPlateStandardCase(IfcPlate):
    """Wrapper class for IfcPlateStandardCase."""

    ...

class IfcProjectionElement(IfcFeatureElementAddition):
    """Wrapper class for IfcProjectionElement."""

    PredefinedType: Optional["IfcProjectionElementTypeEnum"]

class IfcProtectiveDeviceTrippingUnit(IfcDistributionControlElement):
    """Wrapper class for IfcProtectiveDeviceTrippingUnit."""

    PredefinedType: Optional["IfcProtectiveDeviceTrippingUnitTypeEnum"]

class IfcProtectiveDeviceTrippingUnitType(IfcDistributionControlElementType):
    """Wrapper class for IfcProtectiveDeviceTrippingUnitType."""

    PredefinedType: "IfcProtectiveDeviceTrippingUnitTypeEnum"

class IfcReinforcingBarType(IfcReinforcingElementType):
    """Wrapper class for IfcReinforcingBarType."""

    PredefinedType: "IfcReinforcingBarTypeEnum"
    NominalDiameter: Optional[float]
    CrossSectionArea: Optional[float]
    BarLength: Optional[float]
    BarSurface: Optional["IfcReinforcingBarSurfaceEnum"]
    BendingShapeCode: Optional[str]
    BendingParameters: Optional[list[float]]

class IfcReinforcingElement(IfcElementComponent):
    """Wrapper class for IfcReinforcingElement."""

    SteelGrade: Optional[str]

class IfcReinforcingMeshType(IfcReinforcingElementType):
    """Wrapper class for IfcReinforcingMeshType."""

    PredefinedType: "IfcReinforcingMeshTypeEnum"
    MeshLength: Optional[float]
    MeshWidth: Optional[float]
    LongitudinalBarNominalDiameter: Optional[float]
    TransverseBarNominalDiameter: Optional[float]
    LongitudinalBarCrossSectionArea: Optional[float]
    TransverseBarCrossSectionArea: Optional[float]
    LongitudinalBarSpacing: Optional[float]
    TransverseBarSpacing: Optional[float]
    BendingShapeCode: Optional[str]
    BendingParameters: Optional[list[float]]

class IfcSensor(IfcDistributionControlElement):
    """Wrapper class for IfcSensor."""

    PredefinedType: Optional["IfcSensorTypeEnum"]

class IfcSensorType(IfcDistributionControlElementType):
    """Wrapper class for IfcSensorType."""

    PredefinedType: "IfcSensorTypeEnum"

class IfcSlabElementedCase(IfcSlab):
    """Wrapper class for IfcSlabElementedCase."""

    ...

class IfcSlabStandardCase(IfcSlab):
    """Wrapper class for IfcSlabStandardCase."""

    ...

class IfcStructuralCurveMemberVarying(IfcStructuralCurveMember):
    """Wrapper class for IfcStructuralCurveMemberVarying."""

    ...

class IfcStructuralSurfaceMemberVarying(IfcStructuralSurfaceMember):
    """Wrapper class for IfcStructuralSurfaceMemberVarying."""

    ...

class IfcTendonAnchorType(IfcReinforcingElementType):
    """Wrapper class for IfcTendonAnchorType."""

    PredefinedType: "IfcTendonAnchorTypeEnum"

class IfcTendonType(IfcReinforcingElementType):
    """Wrapper class for IfcTendonType."""

    PredefinedType: "IfcTendonTypeEnum"
    NominalDiameter: Optional[float]
    CrossSectionArea: Optional[float]
    SheathDiameter: Optional[float]

class IfcUnitaryControlElement(IfcDistributionControlElement):
    """Wrapper class for IfcUnitaryControlElement."""

    PredefinedType: Optional["IfcUnitaryControlElementTypeEnum"]

class IfcUnitaryControlElementType(IfcDistributionControlElementType):
    """Wrapper class for IfcUnitaryControlElementType."""

    PredefinedType: "IfcUnitaryControlElementTypeEnum"

class IfcVibrationIsolatorType(IfcElementComponentType):
    """Wrapper class for IfcVibrationIsolatorType."""

    PredefinedType: "IfcVibrationIsolatorTypeEnum"

class IfcVoidingFeature(IfcFeatureElementSubtraction):
    """Wrapper class for IfcVoidingFeature."""

    PredefinedType: Optional["IfcVoidingFeatureTypeEnum"]

class IfcWallElementedCase(IfcWall):
    """Wrapper class for IfcWallElementedCase."""

    ...

class IfcWallStandardCase(IfcWall):
    """Wrapper class for IfcWallStandardCase."""

    ...

class IfcWindowStandardCase(IfcWindow):
    """Wrapper class for IfcWindowStandardCase."""

    ...

class IfcAirTerminal(IfcFlowTerminal):
    """Wrapper class for IfcAirTerminal."""

    PredefinedType: Optional["IfcAirTerminalTypeEnum"]

class IfcAirTerminalBox(IfcFlowController):
    """Wrapper class for IfcAirTerminalBox."""

    PredefinedType: Optional["IfcAirTerminalBoxTypeEnum"]

class IfcAirTerminalBoxType(IfcFlowControllerType):
    """Wrapper class for IfcAirTerminalBoxType."""

    PredefinedType: "IfcAirTerminalBoxTypeEnum"

class IfcAirTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcAirTerminalType."""

    PredefinedType: "IfcAirTerminalTypeEnum"

class IfcAirToAirHeatRecovery(IfcEnergyConversionDevice):
    """Wrapper class for IfcAirToAirHeatRecovery."""

    PredefinedType: Optional["IfcAirToAirHeatRecoveryTypeEnum"]

class IfcAirToAirHeatRecoveryType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcAirToAirHeatRecoveryType."""

    PredefinedType: "IfcAirToAirHeatRecoveryTypeEnum"

class IfcAudioVisualAppliance(IfcFlowTerminal):
    """Wrapper class for IfcAudioVisualAppliance."""

    PredefinedType: Optional["IfcAudioVisualApplianceTypeEnum"]

class IfcAudioVisualApplianceType(IfcFlowTerminalType):
    """Wrapper class for IfcAudioVisualApplianceType."""

    PredefinedType: "IfcAudioVisualApplianceTypeEnum"

class IfcBoiler(IfcEnergyConversionDevice):
    """Wrapper class for IfcBoiler."""

    PredefinedType: Optional["IfcBoilerTypeEnum"]

class IfcBoilerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcBoilerType."""

    PredefinedType: "IfcBoilerTypeEnum"

class IfcBurner(IfcEnergyConversionDevice):
    """Wrapper class for IfcBurner."""

    PredefinedType: Optional["IfcBurnerTypeEnum"]

class IfcBurnerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcBurnerType."""

    PredefinedType: "IfcBurnerTypeEnum"

class IfcCableCarrierFitting(IfcFlowFitting):
    """Wrapper class for IfcCableCarrierFitting."""

    PredefinedType: Optional["IfcCableCarrierFittingTypeEnum"]

class IfcCableCarrierFittingType(IfcFlowFittingType):
    """Wrapper class for IfcCableCarrierFittingType."""

    PredefinedType: "IfcCableCarrierFittingTypeEnum"

class IfcCableCarrierSegment(IfcFlowSegment):
    """Wrapper class for IfcCableCarrierSegment."""

    PredefinedType: Optional["IfcCableCarrierSegmentTypeEnum"]

class IfcCableCarrierSegmentType(IfcFlowSegmentType):
    """Wrapper class for IfcCableCarrierSegmentType."""

    PredefinedType: "IfcCableCarrierSegmentTypeEnum"

class IfcCableFitting(IfcFlowFitting):
    """Wrapper class for IfcCableFitting."""

    PredefinedType: Optional["IfcCableFittingTypeEnum"]

class IfcCableFittingType(IfcFlowFittingType):
    """Wrapper class for IfcCableFittingType."""

    PredefinedType: "IfcCableFittingTypeEnum"

class IfcCableSegment(IfcFlowSegment):
    """Wrapper class for IfcCableSegment."""

    PredefinedType: Optional["IfcCableSegmentTypeEnum"]

class IfcCableSegmentType(IfcFlowSegmentType):
    """Wrapper class for IfcCableSegmentType."""

    PredefinedType: "IfcCableSegmentTypeEnum"

class IfcChiller(IfcEnergyConversionDevice):
    """Wrapper class for IfcChiller."""

    PredefinedType: Optional["IfcChillerTypeEnum"]

class IfcChillerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcChillerType."""

    PredefinedType: "IfcChillerTypeEnum"

class IfcCoil(IfcEnergyConversionDevice):
    """Wrapper class for IfcCoil."""

    PredefinedType: Optional["IfcCoilTypeEnum"]

class IfcCoilType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcCoilType."""

    PredefinedType: "IfcCoilTypeEnum"

class IfcCommunicationsAppliance(IfcFlowTerminal):
    """Wrapper class for IfcCommunicationsAppliance."""

    PredefinedType: Optional["IfcCommunicationsApplianceTypeEnum"]

class IfcCommunicationsApplianceType(IfcFlowTerminalType):
    """Wrapper class for IfcCommunicationsApplianceType."""

    PredefinedType: "IfcCommunicationsApplianceTypeEnum"

class IfcCompressor(IfcFlowMovingDevice):
    """Wrapper class for IfcCompressor."""

    PredefinedType: Optional["IfcCompressorTypeEnum"]

class IfcCompressorType(IfcFlowMovingDeviceType):
    """Wrapper class for IfcCompressorType."""

    PredefinedType: "IfcCompressorTypeEnum"

class IfcCondenser(IfcEnergyConversionDevice):
    """Wrapper class for IfcCondenser."""

    PredefinedType: Optional["IfcCondenserTypeEnum"]

class IfcCondenserType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcCondenserType."""

    PredefinedType: "IfcCondenserTypeEnum"

class IfcCooledBeam(IfcEnergyConversionDevice):
    """Wrapper class for IfcCooledBeam."""

    PredefinedType: Optional["IfcCooledBeamTypeEnum"]

class IfcCooledBeamType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcCooledBeamType."""

    PredefinedType: "IfcCooledBeamTypeEnum"

class IfcCoolingTower(IfcEnergyConversionDevice):
    """Wrapper class for IfcCoolingTower."""

    PredefinedType: Optional["IfcCoolingTowerTypeEnum"]

class IfcCoolingTowerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcCoolingTowerType."""

    PredefinedType: "IfcCoolingTowerTypeEnum"

class IfcDamper(IfcFlowController):
    """Wrapper class for IfcDamper."""

    PredefinedType: Optional["IfcDamperTypeEnum"]

class IfcDamperType(IfcFlowControllerType):
    """Wrapper class for IfcDamperType."""

    PredefinedType: "IfcDamperTypeEnum"

class IfcDuctFitting(IfcFlowFitting):
    """Wrapper class for IfcDuctFitting."""

    PredefinedType: Optional["IfcDuctFittingTypeEnum"]

class IfcDuctFittingType(IfcFlowFittingType):
    """Wrapper class for IfcDuctFittingType."""

    PredefinedType: "IfcDuctFittingTypeEnum"

class IfcDuctSegment(IfcFlowSegment):
    """Wrapper class for IfcDuctSegment."""

    PredefinedType: Optional["IfcDuctSegmentTypeEnum"]

class IfcDuctSegmentType(IfcFlowSegmentType):
    """Wrapper class for IfcDuctSegmentType."""

    PredefinedType: "IfcDuctSegmentTypeEnum"

class IfcDuctSilencer(IfcFlowTreatmentDevice):
    """Wrapper class for IfcDuctSilencer."""

    PredefinedType: Optional["IfcDuctSilencerTypeEnum"]

class IfcDuctSilencerType(IfcFlowTreatmentDeviceType):
    """Wrapper class for IfcDuctSilencerType."""

    PredefinedType: "IfcDuctSilencerTypeEnum"

class IfcElectricAppliance(IfcFlowTerminal):
    """Wrapper class for IfcElectricAppliance."""

    PredefinedType: Optional["IfcElectricApplianceTypeEnum"]

class IfcElectricApplianceType(IfcFlowTerminalType):
    """Wrapper class for IfcElectricApplianceType."""

    PredefinedType: "IfcElectricApplianceTypeEnum"

class IfcElectricDistributionBoard(IfcFlowController):
    """Wrapper class for IfcElectricDistributionBoard."""

    PredefinedType: Optional["IfcElectricDistributionBoardTypeEnum"]

class IfcElectricDistributionBoardType(IfcFlowControllerType):
    """Wrapper class for IfcElectricDistributionBoardType."""

    PredefinedType: "IfcElectricDistributionBoardTypeEnum"

class IfcElectricFlowStorageDevice(IfcFlowStorageDevice):
    """Wrapper class for IfcElectricFlowStorageDevice."""

    PredefinedType: Optional["IfcElectricFlowStorageDeviceTypeEnum"]

class IfcElectricFlowStorageDeviceType(IfcFlowStorageDeviceType):
    """Wrapper class for IfcElectricFlowStorageDeviceType."""

    PredefinedType: "IfcElectricFlowStorageDeviceTypeEnum"

class IfcElectricGenerator(IfcEnergyConversionDevice):
    """Wrapper class for IfcElectricGenerator."""

    PredefinedType: Optional["IfcElectricGeneratorTypeEnum"]

class IfcElectricGeneratorType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcElectricGeneratorType."""

    PredefinedType: "IfcElectricGeneratorTypeEnum"

class IfcElectricMotor(IfcEnergyConversionDevice):
    """Wrapper class for IfcElectricMotor."""

    PredefinedType: Optional["IfcElectricMotorTypeEnum"]

class IfcElectricMotorType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcElectricMotorType."""

    PredefinedType: "IfcElectricMotorTypeEnum"

class IfcElectricTimeControl(IfcFlowController):
    """Wrapper class for IfcElectricTimeControl."""

    PredefinedType: Optional["IfcElectricTimeControlTypeEnum"]

class IfcElectricTimeControlType(IfcFlowControllerType):
    """Wrapper class for IfcElectricTimeControlType."""

    PredefinedType: "IfcElectricTimeControlTypeEnum"

class IfcEngine(IfcEnergyConversionDevice):
    """Wrapper class for IfcEngine."""

    PredefinedType: Optional["IfcEngineTypeEnum"]

class IfcEngineType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcEngineType."""

    PredefinedType: "IfcEngineTypeEnum"

class IfcEvaporativeCooler(IfcEnergyConversionDevice):
    """Wrapper class for IfcEvaporativeCooler."""

    PredefinedType: Optional["IfcEvaporativeCoolerTypeEnum"]

class IfcEvaporativeCoolerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcEvaporativeCoolerType."""

    PredefinedType: "IfcEvaporativeCoolerTypeEnum"

class IfcEvaporator(IfcEnergyConversionDevice):
    """Wrapper class for IfcEvaporator."""

    PredefinedType: Optional["IfcEvaporatorTypeEnum"]

class IfcEvaporatorType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcEvaporatorType."""

    PredefinedType: "IfcEvaporatorTypeEnum"

class IfcFan(IfcFlowMovingDevice):
    """Wrapper class for IfcFan."""

    PredefinedType: Optional["IfcFanTypeEnum"]

class IfcFanType(IfcFlowMovingDeviceType):
    """Wrapper class for IfcFanType."""

    PredefinedType: "IfcFanTypeEnum"

class IfcFilter(IfcFlowTreatmentDevice):
    """Wrapper class for IfcFilter."""

    PredefinedType: Optional["IfcFilterTypeEnum"]

class IfcFilterType(IfcFlowTreatmentDeviceType):
    """Wrapper class for IfcFilterType."""

    PredefinedType: "IfcFilterTypeEnum"

class IfcFireSuppressionTerminal(IfcFlowTerminal):
    """Wrapper class for IfcFireSuppressionTerminal."""

    PredefinedType: Optional["IfcFireSuppressionTerminalTypeEnum"]

class IfcFireSuppressionTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcFireSuppressionTerminalType."""

    PredefinedType: "IfcFireSuppressionTerminalTypeEnum"

class IfcFlowMeter(IfcFlowController):
    """Wrapper class for IfcFlowMeter."""

    PredefinedType: Optional["IfcFlowMeterTypeEnum"]

class IfcFlowMeterType(IfcFlowControllerType):
    """Wrapper class for IfcFlowMeterType."""

    PredefinedType: "IfcFlowMeterTypeEnum"

class IfcHeatExchanger(IfcEnergyConversionDevice):
    """Wrapper class for IfcHeatExchanger."""

    PredefinedType: Optional["IfcHeatExchangerTypeEnum"]

class IfcHeatExchangerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcHeatExchangerType."""

    PredefinedType: "IfcHeatExchangerTypeEnum"

class IfcHumidifier(IfcEnergyConversionDevice):
    """Wrapper class for IfcHumidifier."""

    PredefinedType: Optional["IfcHumidifierTypeEnum"]

class IfcHumidifierType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcHumidifierType."""

    PredefinedType: "IfcHumidifierTypeEnum"

class IfcInterceptor(IfcFlowTreatmentDevice):
    """Wrapper class for IfcInterceptor."""

    PredefinedType: Optional["IfcInterceptorTypeEnum"]

class IfcInterceptorType(IfcFlowTreatmentDeviceType):
    """Wrapper class for IfcInterceptorType."""

    PredefinedType: "IfcInterceptorTypeEnum"

class IfcJunctionBox(IfcFlowFitting):
    """Wrapper class for IfcJunctionBox."""

    PredefinedType: Optional["IfcJunctionBoxTypeEnum"]

class IfcJunctionBoxType(IfcFlowFittingType):
    """Wrapper class for IfcJunctionBoxType."""

    PredefinedType: "IfcJunctionBoxTypeEnum"

class IfcLamp(IfcFlowTerminal):
    """Wrapper class for IfcLamp."""

    PredefinedType: Optional["IfcLampTypeEnum"]

class IfcLampType(IfcFlowTerminalType):
    """Wrapper class for IfcLampType."""

    PredefinedType: "IfcLampTypeEnum"

class IfcLightFixture(IfcFlowTerminal):
    """Wrapper class for IfcLightFixture."""

    PredefinedType: Optional["IfcLightFixtureTypeEnum"]

class IfcLightFixtureType(IfcFlowTerminalType):
    """Wrapper class for IfcLightFixtureType."""

    PredefinedType: "IfcLightFixtureTypeEnum"

class IfcMedicalDevice(IfcFlowTerminal):
    """Wrapper class for IfcMedicalDevice."""

    PredefinedType: Optional["IfcMedicalDeviceTypeEnum"]

class IfcMedicalDeviceType(IfcFlowTerminalType):
    """Wrapper class for IfcMedicalDeviceType."""

    PredefinedType: "IfcMedicalDeviceTypeEnum"

class IfcMotorConnection(IfcEnergyConversionDevice):
    """Wrapper class for IfcMotorConnection."""

    PredefinedType: Optional["IfcMotorConnectionTypeEnum"]

class IfcMotorConnectionType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcMotorConnectionType."""

    PredefinedType: "IfcMotorConnectionTypeEnum"

class IfcOpeningStandardCase(IfcOpeningElement):
    """Wrapper class for IfcOpeningStandardCase."""

    ...

class IfcOutlet(IfcFlowTerminal):
    """Wrapper class for IfcOutlet."""

    PredefinedType: Optional["IfcOutletTypeEnum"]

class IfcOutletType(IfcFlowTerminalType):
    """Wrapper class for IfcOutletType."""

    PredefinedType: "IfcOutletTypeEnum"

class IfcPipeFitting(IfcFlowFitting):
    """Wrapper class for IfcPipeFitting."""

    PredefinedType: Optional["IfcPipeFittingTypeEnum"]

class IfcPipeFittingType(IfcFlowFittingType):
    """Wrapper class for IfcPipeFittingType."""

    PredefinedType: "IfcPipeFittingTypeEnum"

class IfcPipeSegment(IfcFlowSegment):
    """Wrapper class for IfcPipeSegment."""

    PredefinedType: Optional["IfcPipeSegmentTypeEnum"]

class IfcPipeSegmentType(IfcFlowSegmentType):
    """Wrapper class for IfcPipeSegmentType."""

    PredefinedType: "IfcPipeSegmentTypeEnum"

class IfcProtectiveDevice(IfcFlowController):
    """Wrapper class for IfcProtectiveDevice."""

    PredefinedType: Optional["IfcProtectiveDeviceTypeEnum"]

class IfcProtectiveDeviceType(IfcFlowControllerType):
    """Wrapper class for IfcProtectiveDeviceType."""

    PredefinedType: "IfcProtectiveDeviceTypeEnum"

class IfcPump(IfcFlowMovingDevice):
    """Wrapper class for IfcPump."""

    PredefinedType: Optional["IfcPumpTypeEnum"]

class IfcPumpType(IfcFlowMovingDeviceType):
    """Wrapper class for IfcPumpType."""

    PredefinedType: "IfcPumpTypeEnum"

class IfcReinforcingBar(IfcReinforcingElement):
    """Wrapper class for IfcReinforcingBar."""

    NominalDiameter: Optional[float]
    CrossSectionArea: Optional[float]
    BarLength: Optional[float]
    PredefinedType: Optional["IfcReinforcingBarTypeEnum"]
    BarSurface: Optional["IfcReinforcingBarSurfaceEnum"]

class IfcReinforcingMesh(IfcReinforcingElement):
    """Wrapper class for IfcReinforcingMesh."""

    MeshLength: Optional[float]
    MeshWidth: Optional[float]
    LongitudinalBarNominalDiameter: Optional[float]
    TransverseBarNominalDiameter: Optional[float]
    LongitudinalBarCrossSectionArea: Optional[float]
    TransverseBarCrossSectionArea: Optional[float]
    LongitudinalBarSpacing: Optional[float]
    TransverseBarSpacing: Optional[float]
    PredefinedType: Optional["IfcReinforcingMeshTypeEnum"]

class IfcSanitaryTerminal(IfcFlowTerminal):
    """Wrapper class for IfcSanitaryTerminal."""

    PredefinedType: Optional["IfcSanitaryTerminalTypeEnum"]

class IfcSanitaryTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcSanitaryTerminalType."""

    PredefinedType: "IfcSanitaryTerminalTypeEnum"

class IfcSolarDevice(IfcEnergyConversionDevice):
    """Wrapper class for IfcSolarDevice."""

    PredefinedType: Optional["IfcSolarDeviceTypeEnum"]

class IfcSolarDeviceType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcSolarDeviceType."""

    PredefinedType: "IfcSolarDeviceTypeEnum"

class IfcSpaceHeater(IfcFlowTerminal):
    """Wrapper class for IfcSpaceHeater."""

    PredefinedType: Optional["IfcSpaceHeaterTypeEnum"]

class IfcSpaceHeaterType(IfcFlowTerminalType):
    """Wrapper class for IfcSpaceHeaterType."""

    PredefinedType: "IfcSpaceHeaterTypeEnum"

class IfcStackTerminal(IfcFlowTerminal):
    """Wrapper class for IfcStackTerminal."""

    PredefinedType: Optional["IfcStackTerminalTypeEnum"]

class IfcStackTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcStackTerminalType."""

    PredefinedType: "IfcStackTerminalTypeEnum"

class IfcSwitchingDevice(IfcFlowController):
    """Wrapper class for IfcSwitchingDevice."""

    PredefinedType: Optional["IfcSwitchingDeviceTypeEnum"]

class IfcSwitchingDeviceType(IfcFlowControllerType):
    """Wrapper class for IfcSwitchingDeviceType."""

    PredefinedType: "IfcSwitchingDeviceTypeEnum"

class IfcTank(IfcFlowStorageDevice):
    """Wrapper class for IfcTank."""

    PredefinedType: Optional["IfcTankTypeEnum"]

class IfcTankType(IfcFlowStorageDeviceType):
    """Wrapper class for IfcTankType."""

    PredefinedType: "IfcTankTypeEnum"

class IfcTendon(IfcReinforcingElement):
    """Wrapper class for IfcTendon."""

    PredefinedType: Optional["IfcTendonTypeEnum"]
    NominalDiameter: Optional[float]
    CrossSectionArea: Optional[float]
    TensionForce: Optional[float]
    PreStress: Optional[float]
    FrictionCoefficient: Optional[float]
    AnchorageSlip: Optional[float]
    MinCurvatureRadius: Optional[float]

class IfcTendonAnchor(IfcReinforcingElement):
    """Wrapper class for IfcTendonAnchor."""

    PredefinedType: Optional["IfcTendonAnchorTypeEnum"]

class IfcTransformer(IfcEnergyConversionDevice):
    """Wrapper class for IfcTransformer."""

    PredefinedType: Optional["IfcTransformerTypeEnum"]

class IfcTransformerType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcTransformerType."""

    PredefinedType: "IfcTransformerTypeEnum"

class IfcTubeBundle(IfcEnergyConversionDevice):
    """Wrapper class for IfcTubeBundle."""

    PredefinedType: Optional["IfcTubeBundleTypeEnum"]

class IfcTubeBundleType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcTubeBundleType."""

    PredefinedType: "IfcTubeBundleTypeEnum"

class IfcUnitaryEquipment(IfcEnergyConversionDevice):
    """Wrapper class for IfcUnitaryEquipment."""

    PredefinedType: Optional["IfcUnitaryEquipmentTypeEnum"]

class IfcUnitaryEquipmentType(IfcEnergyConversionDeviceType):
    """Wrapper class for IfcUnitaryEquipmentType."""

    PredefinedType: "IfcUnitaryEquipmentTypeEnum"

class IfcValve(IfcFlowController):
    """Wrapper class for IfcValve."""

    PredefinedType: Optional["IfcValveTypeEnum"]

class IfcValveType(IfcFlowControllerType):
    """Wrapper class for IfcValveType."""

    PredefinedType: "IfcValveTypeEnum"

class IfcWasteTerminal(IfcFlowTerminal):
    """Wrapper class for IfcWasteTerminal."""

    PredefinedType: Optional["IfcWasteTerminalTypeEnum"]

class IfcWasteTerminalType(IfcFlowTerminalType):
    """Wrapper class for IfcWasteTerminalType."""

    PredefinedType: "IfcWasteTerminalTypeEnum"

__all__ = [
    "IfcActionRequest",
    "IfcActionRequestTypeEnum",
    "IfcActionSourceTypeEnum",
    "IfcActionTypeEnum",
    "IfcActor",
    "IfcActorRole",
    "IfcActuator",
    "IfcActuatorType",
    "IfcActuatorTypeEnum",
    "IfcAddress",
    "IfcAddressTypeEnum",
    "IfcAdvancedBrep",
    "IfcAdvancedBrepWithVoids",
    "IfcAdvancedFace",
    "IfcAirTerminal",
    "IfcAirTerminalBox",
    "IfcAirTerminalBoxType",
    "IfcAirTerminalBoxTypeEnum",
    "IfcAirTerminalType",
    "IfcAirTerminalTypeEnum",
    "IfcAirToAirHeatRecovery",
    "IfcAirToAirHeatRecoveryType",
    "IfcAirToAirHeatRecoveryTypeEnum",
    "IfcAlarm",
    "IfcAlarmType",
    "IfcAlarmTypeEnum",
    "IfcAnalysisModelTypeEnum",
    "IfcAnalysisTheoryTypeEnum",
    "IfcAnnotation",
    "IfcAnnotationFillArea",
    "IfcApplication",
    "IfcAppliedValue",
    "IfcApproval",
    "IfcApprovalRelationship",
    "IfcArbitraryClosedProfileDef",
    "IfcArbitraryOpenProfileDef",
    "IfcArbitraryProfileDefWithVoids",
    "IfcArithmeticOperatorEnum",
    "IfcAssemblyPlaceEnum",
    "IfcAsset",
    "IfcAsymmetricIShapeProfileDef",
    "IfcAudioVisualAppliance",
    "IfcAudioVisualApplianceType",
    "IfcAudioVisualApplianceTypeEnum",
    "IfcAxis1Placement",
    "IfcAxis2Placement2D",
    "IfcAxis2Placement3D",
    "IfcBSplineCurve",
    "IfcBSplineCurveForm",
    "IfcBSplineCurveWithKnots",
    "IfcBSplineSurface",
    "IfcBSplineSurfaceForm",
    "IfcBSplineSurfaceWithKnots",
    "IfcBeam",
    "IfcBeamStandardCase",
    "IfcBeamType",
    "IfcBeamTypeEnum",
    "IfcBenchmarkEnum",
    "IfcBlobTexture",
    "IfcBlock",
    "IfcBoiler",
    "IfcBoilerType",
    "IfcBoilerTypeEnum",
    "IfcBooleanClippingResult",
    "IfcBooleanOperator",
    "IfcBooleanResult",
    "IfcBoundaryCondition",
    "IfcBoundaryCurve",
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
    "IfcBuildingElementPart",
    "IfcBuildingElementPartType",
    "IfcBuildingElementPartTypeEnum",
    "IfcBuildingElementProxy",
    "IfcBuildingElementProxyType",
    "IfcBuildingElementProxyTypeEnum",
    "IfcBuildingElementType",
    "IfcBuildingStorey",
    "IfcBuildingSystem",
    "IfcBuildingSystemTypeEnum",
    "IfcBurner",
    "IfcBurnerType",
    "IfcBurnerTypeEnum",
    "IfcCShapeProfileDef",
    "IfcCableCarrierFitting",
    "IfcCableCarrierFittingType",
    "IfcCableCarrierFittingTypeEnum",
    "IfcCableCarrierSegment",
    "IfcCableCarrierSegmentType",
    "IfcCableCarrierSegmentTypeEnum",
    "IfcCableFitting",
    "IfcCableFittingType",
    "IfcCableFittingTypeEnum",
    "IfcCableSegment",
    "IfcCableSegmentType",
    "IfcCableSegmentTypeEnum",
    "IfcCartesianPoint",
    "IfcCartesianPointList",
    "IfcCartesianPointList2D",
    "IfcCartesianPointList3D",
    "IfcCartesianTransformationOperator",
    "IfcCartesianTransformationOperator2D",
    "IfcCartesianTransformationOperator2DnonUniform",
    "IfcCartesianTransformationOperator3D",
    "IfcCartesianTransformationOperator3DnonUniform",
    "IfcCenterLineProfileDef",
    "IfcChangeActionEnum",
    "IfcChiller",
    "IfcChillerType",
    "IfcChillerTypeEnum",
    "IfcChimney",
    "IfcChimneyType",
    "IfcChimneyTypeEnum",
    "IfcCircle",
    "IfcCircleHollowProfileDef",
    "IfcCircleProfileDef",
    "IfcCivilElement",
    "IfcCivilElementType",
    "IfcClassification",
    "IfcClassificationReference",
    "IfcClosedShell",
    "IfcCoil",
    "IfcCoilType",
    "IfcCoilTypeEnum",
    "IfcColourRgb",
    "IfcColourRgbList",
    "IfcColourSpecification",
    "IfcColumn",
    "IfcColumnStandardCase",
    "IfcColumnType",
    "IfcColumnTypeEnum",
    "IfcCommunicationsAppliance",
    "IfcCommunicationsApplianceType",
    "IfcCommunicationsApplianceTypeEnum",
    "IfcComplexProperty",
    "IfcComplexPropertyTemplate",
    "IfcComplexPropertyTemplateTypeEnum",
    "IfcCompositeCurve",
    "IfcCompositeCurveOnSurface",
    "IfcCompositeCurveSegment",
    "IfcCompositeProfileDef",
    "IfcCompressor",
    "IfcCompressorType",
    "IfcCompressorTypeEnum",
    "IfcCondenser",
    "IfcCondenserType",
    "IfcCondenserTypeEnum",
    "IfcConic",
    "IfcConnectedFaceSet",
    "IfcConnectionCurveGeometry",
    "IfcConnectionGeometry",
    "IfcConnectionPointEccentricity",
    "IfcConnectionPointGeometry",
    "IfcConnectionSurfaceGeometry",
    "IfcConnectionTypeEnum",
    "IfcConnectionVolumeGeometry",
    "IfcConstraint",
    "IfcConstraintEnum",
    "IfcConstructionEquipmentResource",
    "IfcConstructionEquipmentResourceType",
    "IfcConstructionEquipmentResourceTypeEnum",
    "IfcConstructionMaterialResource",
    "IfcConstructionMaterialResourceType",
    "IfcConstructionMaterialResourceTypeEnum",
    "IfcConstructionProductResource",
    "IfcConstructionProductResourceType",
    "IfcConstructionProductResourceTypeEnum",
    "IfcConstructionResource",
    "IfcConstructionResourceType",
    "IfcContext",
    "IfcContextDependentUnit",
    "IfcControl",
    "IfcController",
    "IfcControllerType",
    "IfcControllerTypeEnum",
    "IfcConversionBasedUnit",
    "IfcConversionBasedUnitWithOffset",
    "IfcCooledBeam",
    "IfcCooledBeamType",
    "IfcCooledBeamTypeEnum",
    "IfcCoolingTower",
    "IfcCoolingTowerType",
    "IfcCoolingTowerTypeEnum",
    "IfcCoordinateOperation",
    "IfcCoordinateReferenceSystem",
    "IfcCostItem",
    "IfcCostItemTypeEnum",
    "IfcCostSchedule",
    "IfcCostScheduleTypeEnum",
    "IfcCostValue",
    "IfcCovering",
    "IfcCoveringType",
    "IfcCoveringTypeEnum",
    "IfcCrewResource",
    "IfcCrewResourceType",
    "IfcCrewResourceTypeEnum",
    "IfcCsgPrimitive3D",
    "IfcCsgSolid",
    "IfcCurrencyRelationship",
    "IfcCurtainWall",
    "IfcCurtainWallType",
    "IfcCurtainWallTypeEnum",
    "IfcCurve",
    "IfcCurveBoundedPlane",
    "IfcCurveBoundedSurface",
    "IfcCurveInterpolationEnum",
    "IfcCurveStyle",
    "IfcCurveStyleFont",
    "IfcCurveStyleFontAndScaling",
    "IfcCurveStyleFontPattern",
    "IfcCylindricalSurface",
    "IfcDamper",
    "IfcDamperType",
    "IfcDamperTypeEnum",
    "IfcDataOriginEnum",
    "IfcDerivedProfileDef",
    "IfcDerivedUnit",
    "IfcDerivedUnitElement",
    "IfcDerivedUnitEnum",
    "IfcDimensionalExponents",
    "IfcDirection",
    "IfcDirectionSenseEnum",
    "IfcDiscreteAccessory",
    "IfcDiscreteAccessoryType",
    "IfcDiscreteAccessoryTypeEnum",
    "IfcDistributionChamberElement",
    "IfcDistributionChamberElementType",
    "IfcDistributionChamberElementTypeEnum",
    "IfcDistributionCircuit",
    "IfcDistributionControlElement",
    "IfcDistributionControlElementType",
    "IfcDistributionElement",
    "IfcDistributionElementType",
    "IfcDistributionFlowElement",
    "IfcDistributionFlowElementType",
    "IfcDistributionPort",
    "IfcDistributionPortTypeEnum",
    "IfcDistributionSystem",
    "IfcDistributionSystemEnum",
    "IfcDocumentConfidentialityEnum",
    "IfcDocumentInformation",
    "IfcDocumentInformationRelationship",
    "IfcDocumentReference",
    "IfcDocumentStatusEnum",
    "IfcDoor",
    "IfcDoorLiningProperties",
    "IfcDoorPanelOperationEnum",
    "IfcDoorPanelPositionEnum",
    "IfcDoorPanelProperties",
    "IfcDoorStandardCase",
    "IfcDoorStyle",
    "IfcDoorStyleConstructionEnum",
    "IfcDoorStyleOperationEnum",
    "IfcDoorType",
    "IfcDoorTypeEnum",
    "IfcDoorTypeOperationEnum",
    "IfcDraughtingPreDefinedColour",
    "IfcDraughtingPreDefinedCurveFont",
    "IfcDuctFitting",
    "IfcDuctFittingType",
    "IfcDuctFittingTypeEnum",
    "IfcDuctSegment",
    "IfcDuctSegmentType",
    "IfcDuctSegmentTypeEnum",
    "IfcDuctSilencer",
    "IfcDuctSilencerType",
    "IfcDuctSilencerTypeEnum",
    "IfcEdge",
    "IfcEdgeCurve",
    "IfcEdgeLoop",
    "IfcElectricAppliance",
    "IfcElectricApplianceType",
    "IfcElectricApplianceTypeEnum",
    "IfcElectricDistributionBoard",
    "IfcElectricDistributionBoardType",
    "IfcElectricDistributionBoardTypeEnum",
    "IfcElectricFlowStorageDevice",
    "IfcElectricFlowStorageDeviceType",
    "IfcElectricFlowStorageDeviceTypeEnum",
    "IfcElectricGenerator",
    "IfcElectricGeneratorType",
    "IfcElectricGeneratorTypeEnum",
    "IfcElectricMotor",
    "IfcElectricMotorType",
    "IfcElectricMotorTypeEnum",
    "IfcElectricTimeControl",
    "IfcElectricTimeControlType",
    "IfcElectricTimeControlTypeEnum",
    "IfcElement",
    "IfcElementAssembly",
    "IfcElementAssemblyType",
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
    "IfcEngine",
    "IfcEngineType",
    "IfcEngineTypeEnum",
    "IfcEvaporativeCooler",
    "IfcEvaporativeCoolerType",
    "IfcEvaporativeCoolerTypeEnum",
    "IfcEvaporator",
    "IfcEvaporatorType",
    "IfcEvaporatorTypeEnum",
    "IfcEvent",
    "IfcEventTime",
    "IfcEventTriggerTypeEnum",
    "IfcEventType",
    "IfcEventTypeEnum",
    "IfcExtendedProperties",
    "IfcExternalInformation",
    "IfcExternalReference",
    "IfcExternalReferenceRelationship",
    "IfcExternalSpatialElement",
    "IfcExternalSpatialElementTypeEnum",
    "IfcExternalSpatialStructureElement",
    "IfcExternallyDefinedHatchStyle",
    "IfcExternallyDefinedSurfaceStyle",
    "IfcExternallyDefinedTextFont",
    "IfcExtrudedAreaSolid",
    "IfcExtrudedAreaSolidTapered",
    "IfcFace",
    "IfcFaceBasedSurfaceModel",
    "IfcFaceBound",
    "IfcFaceOuterBound",
    "IfcFaceSurface",
    "IfcFacetedBrep",
    "IfcFacetedBrepWithVoids",
    "IfcFailureConnectionCondition",
    "IfcFan",
    "IfcFanType",
    "IfcFanTypeEnum",
    "IfcFastener",
    "IfcFastenerType",
    "IfcFastenerTypeEnum",
    "IfcFeatureElement",
    "IfcFeatureElementAddition",
    "IfcFeatureElementSubtraction",
    "IfcFillAreaStyle",
    "IfcFillAreaStyleHatching",
    "IfcFillAreaStyleTiles",
    "IfcFilter",
    "IfcFilterType",
    "IfcFilterTypeEnum",
    "IfcFireSuppressionTerminal",
    "IfcFireSuppressionTerminalType",
    "IfcFireSuppressionTerminalTypeEnum",
    "IfcFixedReferenceSweptAreaSolid",
    "IfcFlowController",
    "IfcFlowControllerType",
    "IfcFlowDirectionEnum",
    "IfcFlowFitting",
    "IfcFlowFittingType",
    "IfcFlowInstrument",
    "IfcFlowInstrumentType",
    "IfcFlowInstrumentTypeEnum",
    "IfcFlowMeter",
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
    "IfcFooting",
    "IfcFootingType",
    "IfcFootingTypeEnum",
    "IfcFurnishingElement",
    "IfcFurnishingElementType",
    "IfcFurniture",
    "IfcFurnitureType",
    "IfcFurnitureTypeEnum",
    "IfcGeographicElement",
    "IfcGeographicElementType",
    "IfcGeographicElementTypeEnum",
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
    "IfcGridTypeEnum",
    "IfcGroup",
    "IfcHalfSpaceSolid",
    "IfcHeatExchanger",
    "IfcHeatExchangerType",
    "IfcHeatExchangerTypeEnum",
    "IfcHumidifier",
    "IfcHumidifierType",
    "IfcHumidifierTypeEnum",
    "IfcIShapeProfileDef",
    "IfcImageTexture",
    "IfcIndexedColourMap",
    "IfcIndexedPolyCurve",
    "IfcIndexedPolygonalFace",
    "IfcIndexedPolygonalFaceWithVoids",
    "IfcIndexedTextureMap",
    "IfcIndexedTriangleTextureMap",
    "IfcInterceptor",
    "IfcInterceptorType",
    "IfcInterceptorTypeEnum",
    "IfcInternalOrExternalEnum",
    "IfcIntersectionCurve",
    "IfcInventory",
    "IfcInventoryTypeEnum",
    "IfcIrregularTimeSeries",
    "IfcIrregularTimeSeriesValue",
    "IfcJunctionBox",
    "IfcJunctionBoxType",
    "IfcJunctionBoxTypeEnum",
    "IfcKnotType",
    "IfcLShapeProfileDef",
    "IfcLaborResource",
    "IfcLaborResourceType",
    "IfcLaborResourceTypeEnum",
    "IfcLagTime",
    "IfcLamp",
    "IfcLampType",
    "IfcLampTypeEnum",
    "IfcLayerSetDirectionEnum",
    "IfcLibraryInformation",
    "IfcLibraryReference",
    "IfcLightDistributionCurveEnum",
    "IfcLightDistributionData",
    "IfcLightEmissionSourceEnum",
    "IfcLightFixture",
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
    "IfcLoadGroupTypeEnum",
    "IfcLocalPlacement",
    "IfcLogicalOperatorEnum",
    "IfcLoop",
    "IfcManifoldSolidBrep",
    "IfcMapConversion",
    "IfcMappedItem",
    "IfcMaterial",
    "IfcMaterialClassificationRelationship",
    "IfcMaterialConstituent",
    "IfcMaterialConstituentSet",
    "IfcMaterialDefinition",
    "IfcMaterialDefinitionRepresentation",
    "IfcMaterialLayer",
    "IfcMaterialLayerSet",
    "IfcMaterialLayerSetUsage",
    "IfcMaterialLayerWithOffsets",
    "IfcMaterialList",
    "IfcMaterialProfile",
    "IfcMaterialProfileSet",
    "IfcMaterialProfileSetUsage",
    "IfcMaterialProfileSetUsageTapering",
    "IfcMaterialProfileWithOffsets",
    "IfcMaterialProperties",
    "IfcMaterialRelationship",
    "IfcMaterialUsageDefinition",
    "IfcMeasureWithUnit",
    "IfcMechanicalFastener",
    "IfcMechanicalFastenerType",
    "IfcMechanicalFastenerTypeEnum",
    "IfcMedicalDevice",
    "IfcMedicalDeviceType",
    "IfcMedicalDeviceTypeEnum",
    "IfcMember",
    "IfcMemberStandardCase",
    "IfcMemberType",
    "IfcMemberTypeEnum",
    "IfcMetric",
    "IfcMirroredProfileDef",
    "IfcMonetaryUnit",
    "IfcMotorConnection",
    "IfcMotorConnectionType",
    "IfcMotorConnectionTypeEnum",
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
    "IfcOpenShell",
    "IfcOpeningElement",
    "IfcOpeningElementTypeEnum",
    "IfcOpeningStandardCase",
    "IfcOrganization",
    "IfcOrganizationRelationship",
    "IfcOrientedEdge",
    "IfcOuterBoundaryCurve",
    "IfcOutlet",
    "IfcOutletType",
    "IfcOutletTypeEnum",
    "IfcOwnerHistory",
    "IfcParameterizedProfileDef",
    "IfcPath",
    "IfcPcurve",
    "IfcPerformanceHistory",
    "IfcPerformanceHistoryTypeEnum",
    "IfcPermeableCoveringOperationEnum",
    "IfcPermeableCoveringProperties",
    "IfcPermit",
    "IfcPermitTypeEnum",
    "IfcPerson",
    "IfcPersonAndOrganization",
    "IfcPhysicalComplexQuantity",
    "IfcPhysicalOrVirtualEnum",
    "IfcPhysicalQuantity",
    "IfcPhysicalSimpleQuantity",
    "IfcPile",
    "IfcPileConstructionEnum",
    "IfcPileType",
    "IfcPileTypeEnum",
    "IfcPipeFitting",
    "IfcPipeFittingType",
    "IfcPipeFittingTypeEnum",
    "IfcPipeSegment",
    "IfcPipeSegmentType",
    "IfcPipeSegmentTypeEnum",
    "IfcPixelTexture",
    "IfcPlacement",
    "IfcPlanarBox",
    "IfcPlanarExtent",
    "IfcPlane",
    "IfcPlate",
    "IfcPlateStandardCase",
    "IfcPlateType",
    "IfcPlateTypeEnum",
    "IfcPoint",
    "IfcPointOnCurve",
    "IfcPointOnSurface",
    "IfcPolyLoop",
    "IfcPolygonalBoundedHalfSpace",
    "IfcPolygonalFaceSet",
    "IfcPolyline",
    "IfcPort",
    "IfcPostalAddress",
    "IfcPreDefinedColour",
    "IfcPreDefinedCurveFont",
    "IfcPreDefinedItem",
    "IfcPreDefinedProperties",
    "IfcPreDefinedPropertySet",
    "IfcPreDefinedTextFont",
    "IfcPreferredSurfaceCurveRepresentation",
    "IfcPresentationItem",
    "IfcPresentationLayerAssignment",
    "IfcPresentationLayerWithStyle",
    "IfcPresentationStyle",
    "IfcPresentationStyleAssignment",
    "IfcProcedure",
    "IfcProcedureType",
    "IfcProcedureTypeEnum",
    "IfcProcess",
    "IfcProduct",
    "IfcProductDefinitionShape",
    "IfcProductRepresentation",
    "IfcProfileDef",
    "IfcProfileProperties",
    "IfcProfileTypeEnum",
    "IfcProject",
    "IfcProjectLibrary",
    "IfcProjectOrder",
    "IfcProjectOrderTypeEnum",
    "IfcProjectedCRS",
    "IfcProjectedOrTrueLengthEnum",
    "IfcProjectionElement",
    "IfcProjectionElementTypeEnum",
    "IfcProperty",
    "IfcPropertyAbstraction",
    "IfcPropertyBoundedValue",
    "IfcPropertyDefinition",
    "IfcPropertyDependencyRelationship",
    "IfcPropertyEnumeratedValue",
    "IfcPropertyEnumeration",
    "IfcPropertyListValue",
    "IfcPropertyReferenceValue",
    "IfcPropertySet",
    "IfcPropertySetDefinition",
    "IfcPropertySetTemplate",
    "IfcPropertySetTemplateTypeEnum",
    "IfcPropertySingleValue",
    "IfcPropertyTableValue",
    "IfcPropertyTemplate",
    "IfcPropertyTemplateDefinition",
    "IfcProtectiveDevice",
    "IfcProtectiveDeviceTrippingUnit",
    "IfcProtectiveDeviceTrippingUnitType",
    "IfcProtectiveDeviceTrippingUnitTypeEnum",
    "IfcProtectiveDeviceType",
    "IfcProtectiveDeviceTypeEnum",
    "IfcProxy",
    "IfcPump",
    "IfcPumpType",
    "IfcPumpTypeEnum",
    "IfcQuantityArea",
    "IfcQuantityCount",
    "IfcQuantityLength",
    "IfcQuantitySet",
    "IfcQuantityTime",
    "IfcQuantityVolume",
    "IfcQuantityWeight",
    "IfcRailing",
    "IfcRailingType",
    "IfcRailingTypeEnum",
    "IfcRamp",
    "IfcRampFlight",
    "IfcRampFlightType",
    "IfcRampFlightTypeEnum",
    "IfcRampType",
    "IfcRampTypeEnum",
    "IfcRationalBSplineCurveWithKnots",
    "IfcRationalBSplineSurfaceWithKnots",
    "IfcRectangleHollowProfileDef",
    "IfcRectangleProfileDef",
    "IfcRectangularPyramid",
    "IfcRectangularTrimmedSurface",
    "IfcRecurrencePattern",
    "IfcRecurrenceTypeEnum",
    "IfcReference",
    "IfcReflectanceMethodEnum",
    "IfcRegularTimeSeries",
    "IfcReinforcementBarProperties",
    "IfcReinforcementDefinitionProperties",
    "IfcReinforcingBar",
    "IfcReinforcingBarRoleEnum",
    "IfcReinforcingBarSurfaceEnum",
    "IfcReinforcingBarType",
    "IfcReinforcingBarTypeEnum",
    "IfcReinforcingElement",
    "IfcReinforcingElementType",
    "IfcReinforcingMesh",
    "IfcReinforcingMeshType",
    "IfcReinforcingMeshTypeEnum",
    "IfcRelAggregates",
    "IfcRelAssigns",
    "IfcRelAssignsToActor",
    "IfcRelAssignsToControl",
    "IfcRelAssignsToGroup",
    "IfcRelAssignsToGroupByFactor",
    "IfcRelAssignsToProcess",
    "IfcRelAssignsToProduct",
    "IfcRelAssignsToResource",
    "IfcRelAssociates",
    "IfcRelAssociatesApproval",
    "IfcRelAssociatesClassification",
    "IfcRelAssociatesConstraint",
    "IfcRelAssociatesDocument",
    "IfcRelAssociatesLibrary",
    "IfcRelAssociatesMaterial",
    "IfcRelConnects",
    "IfcRelConnectsElements",
    "IfcRelConnectsPathElements",
    "IfcRelConnectsPortToElement",
    "IfcRelConnectsPorts",
    "IfcRelConnectsStructuralActivity",
    "IfcRelConnectsStructuralMember",
    "IfcRelConnectsWithEccentricity",
    "IfcRelConnectsWithRealizingElements",
    "IfcRelContainedInSpatialStructure",
    "IfcRelCoversBldgElements",
    "IfcRelCoversSpaces",
    "IfcRelDeclares",
    "IfcRelDecomposes",
    "IfcRelDefines",
    "IfcRelDefinesByObject",
    "IfcRelDefinesByProperties",
    "IfcRelDefinesByTemplate",
    "IfcRelDefinesByType",
    "IfcRelFillsElement",
    "IfcRelFlowControlElements",
    "IfcRelInterferesElements",
    "IfcRelNests",
    "IfcRelProjectsElement",
    "IfcRelReferencedInSpatialStructure",
    "IfcRelSequence",
    "IfcRelServicesBuildings",
    "IfcRelSpaceBoundary",
    "IfcRelSpaceBoundary1stLevel",
    "IfcRelSpaceBoundary2ndLevel",
    "IfcRelVoidsElement",
    "IfcRelationship",
    "IfcReparametrisedCompositeCurveSegment",
    "IfcRepresentation",
    "IfcRepresentationContext",
    "IfcRepresentationItem",
    "IfcRepresentationMap",
    "IfcResource",
    "IfcResourceApprovalRelationship",
    "IfcResourceConstraintRelationship",
    "IfcResourceLevelRelationship",
    "IfcResourceTime",
    "IfcRevolvedAreaSolid",
    "IfcRevolvedAreaSolidTapered",
    "IfcRightCircularCone",
    "IfcRightCircularCylinder",
    "IfcRoleEnum",
    "IfcRoof",
    "IfcRoofType",
    "IfcRoofTypeEnum",
    "IfcRoot",
    "IfcRoundedRectangleProfileDef",
    "IfcSIPrefix",
    "IfcSIUnit",
    "IfcSIUnitName",
    "IfcSanitaryTerminal",
    "IfcSanitaryTerminalType",
    "IfcSanitaryTerminalTypeEnum",
    "IfcSchedulingTime",
    "IfcSeamCurve",
    "IfcSectionProperties",
    "IfcSectionReinforcementProperties",
    "IfcSectionTypeEnum",
    "IfcSectionedSpine",
    "IfcSensor",
    "IfcSensorType",
    "IfcSensorTypeEnum",
    "IfcSequenceEnum",
    "IfcShadingDevice",
    "IfcShadingDeviceType",
    "IfcShadingDeviceTypeEnum",
    "IfcShapeAspect",
    "IfcShapeModel",
    "IfcShapeRepresentation",
    "IfcShellBasedSurfaceModel",
    "IfcSimpleProperty",
    "IfcSimplePropertyTemplate",
    "IfcSimplePropertyTemplateTypeEnum",
    "IfcSite",
    "IfcSlab",
    "IfcSlabElementedCase",
    "IfcSlabStandardCase",
    "IfcSlabType",
    "IfcSlabTypeEnum",
    "IfcSlippageConnectionCondition",
    "IfcSolarDevice",
    "IfcSolarDeviceType",
    "IfcSolarDeviceTypeEnum",
    "IfcSolidModel",
    "IfcSpace",
    "IfcSpaceHeater",
    "IfcSpaceHeaterType",
    "IfcSpaceHeaterTypeEnum",
    "IfcSpaceType",
    "IfcSpaceTypeEnum",
    "IfcSpatialElement",
    "IfcSpatialElementType",
    "IfcSpatialStructureElement",
    "IfcSpatialStructureElementType",
    "IfcSpatialZone",
    "IfcSpatialZoneType",
    "IfcSpatialZoneTypeEnum",
    "IfcSphere",
    "IfcSphericalSurface",
    "IfcStackTerminal",
    "IfcStackTerminalType",
    "IfcStackTerminalTypeEnum",
    "IfcStair",
    "IfcStairFlight",
    "IfcStairFlightType",
    "IfcStairFlightTypeEnum",
    "IfcStairType",
    "IfcStairTypeEnum",
    "IfcStateEnum",
    "IfcStructuralAction",
    "IfcStructuralActivity",
    "IfcStructuralAnalysisModel",
    "IfcStructuralConnection",
    "IfcStructuralConnectionCondition",
    "IfcStructuralCurveAction",
    "IfcStructuralCurveActivityTypeEnum",
    "IfcStructuralCurveConnection",
    "IfcStructuralCurveMember",
    "IfcStructuralCurveMemberTypeEnum",
    "IfcStructuralCurveMemberVarying",
    "IfcStructuralCurveReaction",
    "IfcStructuralItem",
    "IfcStructuralLinearAction",
    "IfcStructuralLoad",
    "IfcStructuralLoadCase",
    "IfcStructuralLoadConfiguration",
    "IfcStructuralLoadGroup",
    "IfcStructuralLoadLinearForce",
    "IfcStructuralLoadOrResult",
    "IfcStructuralLoadPlanarForce",
    "IfcStructuralLoadSingleDisplacement",
    "IfcStructuralLoadSingleDisplacementDistortion",
    "IfcStructuralLoadSingleForce",
    "IfcStructuralLoadSingleForceWarping",
    "IfcStructuralLoadStatic",
    "IfcStructuralLoadTemperature",
    "IfcStructuralMember",
    "IfcStructuralPlanarAction",
    "IfcStructuralPointAction",
    "IfcStructuralPointConnection",
    "IfcStructuralPointReaction",
    "IfcStructuralReaction",
    "IfcStructuralResultGroup",
    "IfcStructuralSurfaceAction",
    "IfcStructuralSurfaceActivityTypeEnum",
    "IfcStructuralSurfaceConnection",
    "IfcStructuralSurfaceMember",
    "IfcStructuralSurfaceMemberTypeEnum",
    "IfcStructuralSurfaceMemberVarying",
    "IfcStructuralSurfaceReaction",
    "IfcStyleModel",
    "IfcStyledItem",
    "IfcStyledRepresentation",
    "IfcSubContractResource",
    "IfcSubContractResourceType",
    "IfcSubContractResourceTypeEnum",
    "IfcSubedge",
    "IfcSurface",
    "IfcSurfaceCurve",
    "IfcSurfaceCurveSweptAreaSolid",
    "IfcSurfaceFeature",
    "IfcSurfaceFeatureTypeEnum",
    "IfcSurfaceOfLinearExtrusion",
    "IfcSurfaceOfRevolution",
    "IfcSurfaceReinforcementArea",
    "IfcSurfaceSide",
    "IfcSurfaceStyle",
    "IfcSurfaceStyleLighting",
    "IfcSurfaceStyleRefraction",
    "IfcSurfaceStyleRendering",
    "IfcSurfaceStyleShading",
    "IfcSurfaceStyleWithTextures",
    "IfcSurfaceTexture",
    "IfcSweptAreaSolid",
    "IfcSweptDiskSolid",
    "IfcSweptDiskSolidPolygonal",
    "IfcSweptSurface",
    "IfcSwitchingDevice",
    "IfcSwitchingDeviceType",
    "IfcSwitchingDeviceTypeEnum",
    "IfcSystem",
    "IfcSystemFurnitureElement",
    "IfcSystemFurnitureElementType",
    "IfcSystemFurnitureElementTypeEnum",
    "IfcTShapeProfileDef",
    "IfcTable",
    "IfcTableColumn",
    "IfcTableRow",
    "IfcTank",
    "IfcTankType",
    "IfcTankTypeEnum",
    "IfcTask",
    "IfcTaskDurationEnum",
    "IfcTaskTime",
    "IfcTaskTimeRecurring",
    "IfcTaskType",
    "IfcTaskTypeEnum",
    "IfcTelecomAddress",
    "IfcTendon",
    "IfcTendonAnchor",
    "IfcTendonAnchorType",
    "IfcTendonAnchorTypeEnum",
    "IfcTendonType",
    "IfcTendonTypeEnum",
    "IfcTessellatedFaceSet",
    "IfcTessellatedItem",
    "IfcTextLiteral",
    "IfcTextLiteralWithExtent",
    "IfcTextPath",
    "IfcTextStyle",
    "IfcTextStyleFontModel",
    "IfcTextStyleForDefinedFont",
    "IfcTextStyleTextModel",
    "IfcTextureCoordinate",
    "IfcTextureCoordinateGenerator",
    "IfcTextureMap",
    "IfcTextureVertex",
    "IfcTextureVertexList",
    "IfcTimePeriod",
    "IfcTimeSeries",
    "IfcTimeSeriesDataTypeEnum",
    "IfcTimeSeriesValue",
    "IfcTopologicalRepresentationItem",
    "IfcTopologyRepresentation",
    "IfcToroidalSurface",
    "IfcTransformer",
    "IfcTransformerType",
    "IfcTransformerTypeEnum",
    "IfcTransitionCode",
    "IfcTransportElement",
    "IfcTransportElementType",
    "IfcTransportElementTypeEnum",
    "IfcTrapeziumProfileDef",
    "IfcTriangulatedFaceSet",
    "IfcTrimmedCurve",
    "IfcTrimmingPreference",
    "IfcTubeBundle",
    "IfcTubeBundleType",
    "IfcTubeBundleTypeEnum",
    "IfcTypeObject",
    "IfcTypeProcess",
    "IfcTypeProduct",
    "IfcTypeResource",
    "IfcUShapeProfileDef",
    "IfcUnitAssignment",
    "IfcUnitEnum",
    "IfcUnitaryControlElement",
    "IfcUnitaryControlElementType",
    "IfcUnitaryControlElementTypeEnum",
    "IfcUnitaryEquipment",
    "IfcUnitaryEquipmentType",
    "IfcUnitaryEquipmentTypeEnum",
    "IfcValve",
    "IfcValveType",
    "IfcValveTypeEnum",
    "IfcVector",
    "IfcVertex",
    "IfcVertexLoop",
    "IfcVertexPoint",
    "IfcVibrationIsolator",
    "IfcVibrationIsolatorType",
    "IfcVibrationIsolatorTypeEnum",
    "IfcVirtualElement",
    "IfcVirtualGridIntersection",
    "IfcVoidingFeature",
    "IfcVoidingFeatureTypeEnum",
    "IfcWall",
    "IfcWallElementedCase",
    "IfcWallStandardCase",
    "IfcWallType",
    "IfcWallTypeEnum",
    "IfcWasteTerminal",
    "IfcWasteTerminalType",
    "IfcWasteTerminalTypeEnum",
    "IfcWindow",
    "IfcWindowLiningProperties",
    "IfcWindowPanelOperationEnum",
    "IfcWindowPanelPositionEnum",
    "IfcWindowPanelProperties",
    "IfcWindowStandardCase",
    "IfcWindowStyle",
    "IfcWindowStyleConstructionEnum",
    "IfcWindowStyleOperationEnum",
    "IfcWindowType",
    "IfcWindowTypeEnum",
    "IfcWindowTypePartitioningEnum",
    "IfcWorkCalendar",
    "IfcWorkCalendarTypeEnum",
    "IfcWorkControl",
    "IfcWorkPlan",
    "IfcWorkPlanTypeEnum",
    "IfcWorkSchedule",
    "IfcWorkScheduleTypeEnum",
    "IfcWorkTime",
    "IfcZShapeProfileDef",
    "IfcZone",
]
