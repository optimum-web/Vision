#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Index, ForeignKey, Column, Integer, String, Text, Unicode, DateTime, Boolean, Float
import sqlalchemy as sqla
from sqlalchemy_i18n import (
    make_translatable
, translation_base
, Translatable
)
from app import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

BaseManager = declarative_base()

###############################
# acording to schematic


class TestParam(BaseManager):
    """
    TestParam. Contains parameters of tests.
    """
    __tablename__ = 'test_params'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class TestType(BaseManager):
    """
    TestType. Contains types of tests.
    """
    __tablename__ = 'test_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class TestTypesParams(BaseManager):
    """
    TestTypesParams. Contains connection between test type and test parameters.
    """
    __tablename__ = 'test_types_params'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("test_types.id"))
    param_id = Column(Integer, ForeignKey("test_params.id"))


class EquipmentType(BaseManager):
    """
    EquipmentType. Contains types of equipment.
    """
    __tablename__ = u'equipment_types'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))
    code = Column(String(50))


class Equipment(BaseManager):
    """
    Equipment.  records all information about the equipment.
    """
    __tablename__ = u'equipment'

    id = Column(Integer, primary_key=True, nullable=False)

    # EquipmentNumber: Equipment ID given by equipment owner.
    # Equipment number to uniquely identify equipment
    Code = Column(Integer, nullable=False, index=True)

    # EquipmentType. Define equipment by a single letter code. T:transformer, D; breaker etc...
    Type = Column(
        'equipment_type_id',
        ForeignKey("equipment_type.id"),
        nullable=False
    )

    # Location. Indicate the named placed where the equipement is.
    # Example, a main transformer is at site Budapest, and at localisation Church street.
    # Its the equivalent of the substation name.
    Location = Column(
        'location_id',
        ForeignKey("location.id"),
        nullable=False
    )

    # EditedInfo. False no changes.  True Indicates the equipment info have changed and should update information
    # while importing data from Lab.
    Modifier = Column(Boolean)

    Comments = Column(Text)  # Comments relation

    # these fields should be related to every components test , it's not a preperty of the device its a test
    VisualDate = Column(DateTime)  # VisualDate.  Date where was done the last visual inspection.
    VisualInspectionBy = Column(String(30))  # VisualInspectionBy. Who made the visual inspection. user relation
    VisualInspectionComments = Column(Text)  # VisualInspectionComments. Visual inspection comments,

    # test inspection of tap changer or characteristic ?
    NbrOfTapChangeLTC = Column(Integer)  # NbrTapChange.  Number of tap change on LTC

    # its a separate norms table for all devices
    Norm = Column(
        'norm_id',
        ForeignKey("norm.id"),
        nullable=False
    )

    # its a state of a transformer / breaker /switch /motor / cable  not
    Upstream1 = Column(String(100))  # Upstream1. Upstream device name
    Upstream2 = Column(String(100))  # Upstream2. Upstream device name
    Upstream3 = Column(String(100))  # Upstream3. Upstream device name
    Upstream4 = Column(String(100))  # Upstream4. Upstream device name
    Upstream5 = Column(String(100))  # Upstream5. Upstream device name

    Downstream1 = Column(String(100))  # Downstream1. Downstream device name
    Downstream2 = Column(String(100))  # Downstream2. Downstream device name
    Downstream3 = Column(String(100))  # Downstream3. Downstream device name
    Downstream4 = Column(String(100))  # Downstream4. Downstream device name
    Downstream5 = Column(String(100))  # Downstream5. Downstream device name

    TieLocation = Column(Boolean)          # TieLocation. Tie device location
    TieMaintenanceState = Column(Integer)  # TieMaintenanceState. Tie is open or closed during maintenance
    TieStatus = Column(Integer)     # TieAnalysisState.

    PhysPosition = Column(Integer)

    # device property for all equipment
    Tension4 = Column(Float(53))  # Voltage4

    # Validated. Indicate equipment info has been validated and can be imported.
    Validated = Column(Boolean)

    # InValidation. If true, equipment information from lab must be updated before get imported into the main DB
    InValidation = Column(Boolean)

    # PrevSerielNum. If InValidation is true, indicate what was the previous value to retreive the correct equipment
    # information from Lab
    PrevSerialNumber = Column(String(50))

    # PrevEquipmentNum. If InValidation is true, indicate what was the previous value to retreive the correct equipment information from Lab
    PrevEquipmentNumber = Column(String(50))

    # Sibling. Unique Common Index with the other siblings.  If 0 then no sibling
    # id of a similar equipment
    Sibling = Column(Integer)


class ContractsStatuses(BaseManager):
    """
    ContractsStatuses. Contains types of tests.
    """
    __tablename__ = 'contracts_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class Contract(BaseManager):
    """
    Contract
    """
    __tablename__ = u'contracts'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    contract_num = Column(String(25))  # ContractNum: What is the contract number within the company
    status_id = Column(Integer, ForeignKey("contracts_statuses.id"))


class Lab(BaseManager):
    __tablename__ = 'lab'

    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    analyser = Column(Unicode(256))

    def __init__(self, code=0, analyser=''):
        self.code = code
        self.analyser = analyser

    def dump(self, _indent=0):
        return "   " * _indent + repr(self) + \
               "\n" + \
               "".join(
                   [c.dump(_indent + 1) for c in self.children.values()]
               )

    def __repr__(self):
        return "Lab(id=%r, code=%r, analyser=%r)" % (
            self.id,
            self.code,
            self.analyser
        )


class CampaignStatuses(BaseManager):
    """
    TestTypes. Contains types of tests.
    """
    __tablename__ = 'campaign_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class Campaign(BaseManager):
    """
    Campaign: Contain current analysis results, who did it and why. It also contain analysis management and statuses
    If a test is done on the equipment, then an Analysis record is created
    """
    __tablename__ = u'campaign'
    __table_args__ = (
        # will be reviewed
        #db.Index(u'campaign_DatePrelevement_NoEquipement_NoSerieEquipe_TypeAnal_key', u'DatePrelevement', u'NoEquipement', u'NoSerieEquipe', u'TypeAnalyse', u'ClefAnalyse', unique=True),
        #db.Index(u'campaign_NoEquipement_NoSerieEquipe_DatePrelevement_ClefAnal_key', u'NoEquipement', u'NoSerieEquipe', u'DatePrelevement', u'ClefAnalyse', u'TypeAnalyse', unique=True),
        #db.Index(u'campaign_SerieDate', u'NoSerieEquipe', u'DatePrelevement', u'ClefAnalyse', u'TypeAnalyse'),
        #db.Index(u'campaign_TypeAnalyse_NoEquipement_NoSerieEquipe_DatePrelevem_key', u'TypeAnalyse', u'NoEquipement', u'NoSerieEquipe', u'DatePrelevement', u'ClefAnalyse', unique=True),
        #db.Index(u'campaign_NoEquipement_NoSerieEquipe_TypeAnalyse_DatePrelevem_key', u'NoEquipement', u'NoSerieEquipe', u'TypeAnalyse', u'DatePrelevement', u'ClefAnalyse', unique=True),
        #db.Index(u'campaign_DateSerie', u'DatePrelevement', u'NoSerieEquipe', u'TypeAnalyse', u'ClefAnalyse'),
        #db.Index(u'campaign_Condition_douteuse', u'NoEquipement', u'NoSerieEquipe', u'If_OK', u'DatePrelevement'),
        #db.Index(u'campaign_NoEquipement', u'NoEquipement', u'NoSerieEquipe')
    )

    id = Column(db.Integer(), primary_key=True, nullable=False)

    ########## Foreign keys
    # Laboratory: Company that perform the analysis.  Used with Laboratory table
    # Laboratoire = Column(db.String(20), index=True)  # shou be a relation to lab table
    lab_id = Column(Integer, ForeignKey("lab.id"))

    # # user 1 enters manually
    # # ContractNum: What is the contract number within the company
    # ContratNumber = Column(db.String(25))
    #
    # # ContractStatus: What is the status of the contract
    # #
    # ContractStatus = Column(db.Integer)
    contract_id = Column(Integer, ForeignKey("contracts.id"))

    # # relation
    # # EquipmentSerialNum: Equipment ID given by manufacturer. Index key, along with Equipment number to uniquely identify equipment
    # NoSerieEquipe = Column(db.String(50), index=True)
    # # EquipmentNumber: Equipment ID given by equipment owner. Index key, along with Equipment number to uniquely identify equipment
    # NoEquipement = Column(db.String(50))
    # #TestEquipNum: What is the serial number of the test equipement.  Sometimes it is mandatory to enter the test equipment information so same one can be used next time
    # TestEquipNum = Column(db.String(25))	# it s going to be a relation to equipment table
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    created_by = ''  # user_id - relation to user table  #user one  (manager group)

    # # AnalysisType: Analysis type performed on equipment: (insulating fluid  material from equipment , it should be a relation )
    # Type = Column(db.String(4), index=True)
    test_type_id = Column(Integer, ForeignKey("test_types.id"))

    # # AnalysisStateCode: Code indicating the Analysis status.
    # # Analysis is a process with several steps and each one has a code.
    # Status = Column(db.Integer)  #
    status_id = Column(Integer, ForeignKey("campaign_statuses.id"))


    code = Column(db.String(50), index=True) 	#AnalysisKey: Index key for all tests results

    # date filled by labratory when analysis was done
    DateAnalyse = Column(db.DateTime, index=True)   # AnalysisDate: Date the analysis was performed
    CodeMatiere = Column(db.Integer)                # MaterialCode: Define the type of material analysed: copper, sand, paper, etc..

    #AnalysisNo: a number that comes from laboratory generated by themself, user #3 (at the beggining)
    NoAnalyse = Column(db.String(15), index=True)

    # This is moved to TestResults
    # # Reason: Code indicating why the analysis was performed. Mainly use for oil sampling. We should add a table that defines these code.
    # Reason = Column(db.Integer, server_default=db.text("0"))	# the list is defined in the campagn

    # comes from  "Fluid as per user"   dropdown  list  when add new test in perception
    # PointCode: Code indicating where the oil sample was done
    CodeLieu = Column(db.Integer, server_default=db.text("0"))


    # comes from equipment
    # PercentRatio: Indicate if the TTR was done using Percent ratio or Ratio. Used with TTR table
    # specific electrical test on winding.  TTR - tranformer term ...
    # true when user decided to use percent ratio for ttr
    PourcentRatio = Column(db.Boolean)

    # OilType: What type of insulating material is used: Mineral oil, Silicone, Vegetable oil, etc..
    #  comes from equipment
    TypeHuile = Column(db.Integer, server_default=db.text("0"))

    #Load: what was the equipment loading at the time of sampling
    # MW MVR (Equipment can sustain), charge is the actual MVA MW
    Charge = Column(db.Float(53))

    # user 1 create the sampling,  date when user 2( guy in the field) starts the work
    # SamplingDate: Date of sampling
    # User 1 adds this value and user 2 has oprtunity to change it (he has access to database)
    DatePrelevement = Column(db.DateTime, index=True)

    # Remark: Any pertiment remark related to sampling or equipment status  (can be entered by user1 2 or 3)
    Remarque = Column(db.Text)

    # SampledBy: Who did the sampling  user 2 relation to users table
    Executor = Column(db.String(50))

    # Modify: Bolean field to indicate record has changed, and foreign database need updates
    Modifier = Column(db.Boolean)

    # Transmission: Sampled information and material has been sent to the laboratory
    # Toggled by user 2, and sends to lab  (normally it's done buy user 1)
    # user 2 completes the sampling compaign and reassigns record to user 1, transmision is toggled
    # check the screenshot,  it's a file that exported to a laboratory and then received back by email compared checked and
    # user 1 updates data
    Transmission = Column(db.Boolean)


    # DateRepair: entered by user1 and indicated when repair is done.  What date was repair done last time
    # It's not a part of the campaign, it should be a kind  of type of campaign
    DateReparation = Column(db.DateTime)
    # RepairDescription: Describe what was doen during repair, part of repair compaign
    Desc_Reparation = Column(db.Text)

    # # Bolean field that may no longer be required
    # If_REM = Column(db.String(5))
    # # Bolean field that may no longer be required
    # If_OK = Column(db.String(5))


    # generated by user1   uses predefined list of recommandations
    # RecommendationCode: Used with Recommendation Table, where a list of recomended action are suggested
    CodeRecommandation = Column(db.Integer) # it's going to be a relation to reccomandations

    # RecommendationWritten: The analyser gather all his though in this field to explain what should be done in plain that
    RecommandationEcrite = Column(db.Text)	# Text are field Reccommandation
    ReccomenderPerson = '' # relation to user who does the reccomndation

    #DateApplication: When recommendation was written
    DateApplication = Column(db.DateTime)
    Commentaire = Column(db.Text)										#Comments: Any comments other than recommendations.


    # Same like load, actual MW of the equipment
    #MWs: Equipment loading in MWatt
    MWs = Column(db.Float(53), server_default=db.text("0"))

    # Temperature: Equipement temperature at sampling time
    Temperature = Column(db.Float(53))

    # SamplingcardPrint: Indicate if the sampling cart need to be printed to fill in the field information
    # user 2 has to print small form
    CartEchantImp = Column(db.Boolean)

    # ContainerNbr: How many containers are required
    NbrContenant = Column(db.Float(53), server_default=db.text("1"))

    # SamplingCardGathered: Used for printing the card in batch
    CartEchantRassembler = Column(db.Integer)

    RegroupEssaiType = Column(db.String(50))					#GatheredTestType: Indicates the tests that are grouped for each equipment that need work on
    NoContratLab = Column(db.String(50))						#ContractLabNum: What is the contract number with laboratory
    SeringueNum = Column(db.String(50))						#SeringeNum: Seringe number as printed
    DataValid = Column(db.Integer, server_default=db.text("0"))			#DataValid: Need to look into
    Status1 = Column(db.Integer, server_default=db.text("0"))				#Status1: Need to look into
    Status2 = Column(db.Integer, server_default=db.text("0"))				#Status2:	 Need to look into
    ErrorState = Column(db.Integer, server_default=db.text("0"))			#ErrorState: Need to look into
    ErrorCode = Column(db.Integer, server_default=db.text("0"))			#ErrorCode: Need to look into
    Ambient_Air_Temperature = Column(db.Float(53), server_default=db.text("0"))	#AmbientAirTemperature: Ambient air temperature at sampling time


class TestReasons(BaseManager):
    """
    TestReasons. Contains test reasons.
    """
    __tablename__ = 'test_reasons'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class TestResults(BaseManager):
    """
    TestResults. Contains test results. It is a "tablepart" of campaign
    """
    __tablename__ = 'test_results'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    reason_id = Column(Integer, ForeignKey("test_reasons.id"))


###############################
# old tables
# class SamplingCampaign(BaseManager):
#     """SamplingCampaign:
#     Contain current analysis results, who did it and why.
#     It also contain analysis management and statuses
#     If a test is done on the equipment, then an Analysis record is created
#     """
#
#     __tablename__ = u'SamplingCampaign'
#     __table_args__ = (
#         Index(u'SamplingDate_EquipmentID_TypeAnal_key'    , u'SamplingDate', u'EquipmentID', u'Type', u'Key', unique=True),
#         Index(u'EquipmentID_SamplingDate_ClefAnal_key'    , u'EquipmentID', u'SamplingDate', u'Key', u'Type', unique=True),
#         Index(u'SerieDate',                                 u'EquipmentID', u'SamplingDate', u'Key', u'Type'),
#         Index(u'Type_EquipmentID_DatePrelevem_key',         u'Type', u'EquipmentID', u'SamplingDate', u'Key', unique=True),
#         Index(u'EquipmentID_AnalysisType_DatePrelevem_key', u'EquipmentID', u'Type', u'SamplingDate', u'Key', unique=True),
#         Index(u'DateSerie'                                , u'SamplingDate', u'EquipmentID', u'Type', u'Key'),
#         # Index(u'Condition_douteuse'                       , u'EquipmentID', u'If_OK', u'SamplingDate'),
#         Index(u'Condition_douteuse'                       , u'EquipmentID', u'SamplingDate')
#     )
#
#     Key                   = Column(String(50), primary_key=True, index=True)  # Index key for all tests results
#     Date                  = Column(DateTime, index=True)                      # Date the analysis was performed
#     Type                  = Column(String(4),index=True)                      # Analysis type performed on equipment: chemical , electrical etc...
#     Number                = Column(String(15), index=True)                    # Auto increment number assigne when record is created
#     MaterialCode          = Column(Integer)                                   # Define the type of material analysed: copper, sand, paper, etc..
#     MotiveCode            = Column(Integer, server_default=sqla.text("0"))    # Code indicating why the analysis was performed. Mainly use for oil sampling. We should add a table that defines these code.
#     PointCode             = Column(Integer, server_default=sqla.text("0"))    # Code indicating where the oil sample was done
#     PercentRatio          = Column(Boolean)                                   # Indicate if the TTR was done using Percent ratio or Ratio. Used with TTR table
#     OilType               = Column(Integer, server_default=sqla.text("0"))    # What type of insulating material is used: Mineral oil, Silicone, Vegetable oil, etc..
#     Load                  = Column(Float(53))                                 # Load: what was the equipment loading at the time of sampling
#     SamplingDate          = Column(DateTime, index=True)                      # SamplingDate: Date of sampling
#     Remark                = Column(Text)                                      # Remark: Any pertiment remark related to sampling or equipment status
#     SampledBy             = Column(String(50))                                # SampledBy: Who did the sampling
#     Modify                = Column(Boolean)                                   # Modify: Bolean field to indicate record has changed, and foreign database need updates
#     Transmission          = Column(Boolean)                                   # Transmission: Sampled information and material has been sent to the laboratory
#     Laboratory            = Column(String(20), index=True)                    # Laboratory: Company that perform the analysis.  Used with Laboratory table
#     DateRepair            = Column(DateTime)                                  # DateRepair: What date was repair done last time
#     RepairDescription     = Column(Text)                                      # RepairDescription: Describe what was doen during repair
#     # If_REM                = Column(String(5))                                 # Bolean field that may no longer be required
#     # If_OK                 = Column(String(5))                                 # Bolean field that may no longer be required
#     RecommendationCode    = Column(Integer)                                   # RecommendationCode: Used with Recommendation Table, where a list of recomended action are suggested
#     RecommendationWritten = Column(Text)                                      # RecommendationWritten: The analyser gather all his though in this field to explain what should be done in plain that
#     DateApplication       = Column(DateTime)                                  # DateApplication: When recommendation was written
#     Comments              = Column(Text)                                      # Comments: Any comments other than recommendations.
#     AnalysisStateCode     = Column(Integer)                                   # AnalysisStateCode: Code indicating the Analysis status.  Analysis is a process with several steps and each one has a code.
#     MWs                   = Column(Float(53), server_default=sqla.text("0"))  # MWs: Equipment loading in MWatt
#     Temperature           = Column(Float(53))                                 # Temperature: Equipement temperature at sampling time
#     TestEquipNum          = Column(String(25))                                # TestEquipNum: What is the serial number of the test equipement.  Sometimes it is mandatory to enter the test equipment information so same one can be used next time
#     SamplingCardPrint     = Column(Boolean)                                   # SamplingcardPrint: Indicate if the sampling cart need to be printed to fill in the field information
#     ContainerNbr          = Column(Float(53), server_default=sqla.text("1"))  # ContainerNbr: How many containers are required
#     SamplingCardGathered  = Column(Integer)                                   # SamplingCardGathered: Used for printing the card in batch
#     GatheredTestType      = Column(String(50))                                # GatheredTestType: Indicates the tests that are grouped for each equipment that need work on
#     ContractLabNum        = Column(String(50))                                # ContractLabNum: What is the contract number with laboratory
#     SeringeNum            = Column(String(50))                                # SeringeNum: Seringe number as printed
#     DataValid             = Column(Integer, server_default=sqla.text("0"))    # DataValid: Need to look into
#     Status1               = Column(Integer, server_default=sqla.text("0"))    # Status1: Need to look into
#     Status2               = Column(Integer, server_default=sqla.text("0"))    # Status2:	 Need to look into
#     ErrorState            = Column(Integer, server_default=sqla.text("0"))    # ErrorState: Need to look into
#     ErrorCode             = Column(Integer, server_default=sqla.text("0"))    # ErrorCode: Need to look into
#     AmbientAirTemperature = Column(Float(53), server_default=sqla.text("0"))  # AmbientAirTemperature: Ambient air temperature at sampling time
#     ContractID            = Column(Integer, ForeignKey("contracts.id"))
#     EquipmentID           = Column(Integer, ForeignKey("equipment.id"))
#
#     contract  = relationship("Contract", foreign_keys=[ContractID])
#     equipment = relationship("Equipment", foreign_keys=[EquipmentID])
#     user_id = Column(Integer, db.ForeignKey("users_user.id"))


class ElectricalProfile(BaseManager):
    __tablename__ = 'electrical_profile'

    id = sqla.Column(sqla.Integer, primary_key=True)

    selection = sqla.Column(sqla.Unicode(256))
    description = sqla.Column(sqla.Unicode(1024))
    bushing = sqla.Column(sqla.Boolean(False))
    winding = sqla.Column(sqla.Boolean(False))
    winding_double = sqla.Column(sqla.Boolean(False))
    insulation = sqla.Column(sqla.Boolean(False))
    visual = sqla.Column(sqla.Boolean(False))
    resistance = sqla.Column(sqla.Boolean(False))
    degree = sqla.Column(sqla.Boolean(False))
    turns = sqla.Column(sqla.Boolean(False))

    def dump(self, _indent=0):
        return "   " * _indent + repr(self) + \
               "\n" + \
               "".join(
                   [c.dump(_indent + 1) for c in self.children.values()]
               )

    def parsedata(self, data):
        if data:
            for key in data.keys():
                # print key + ' ' + data[key]
                if hasattr(self, key):
                    if key == 'selection' or key == 'description':
                        if data[key]:
                            setattr(self, key, data[key])
                    else:
                        setattr(self, key, True if data[key] == 'y' else False)

    def __init__(self, data=None):
        self.parsedata(data)
        # print getattr(self, key)

    def clear_data(self):
        for attr in self.__dict__:
            if attr not in ['id', '_sa_instance_state']:
                # print attr
                if attr == 'selection' or attr == 'description':
                    setattr(self, attr, '')
                else:
                    setattr(self, attr, False)

    def add_data(self, data):
        self.parsedata(data)


class FluidProfile(BaseManager):
    __tablename__ = 'fluid_profile'

    id = sqla.Column(sqla.Integer, primary_key=True)

    selection = sqla.Column(sqla.Unicode(256))
    description = sqla.Column(sqla.Unicode(1024))

    # syringe
    gas = sqla.Column(sqla.Boolean(False))
    water = sqla.Column(sqla.Boolean(False))
    furans = sqla.Column(sqla.Boolean(False))
    inhibitor = sqla.Column(sqla.Boolean(False))
    pcb = sqla.Column(sqla.Boolean(False))
    qty = sqla.Column(sqla.Integer)
    sampling = sqla.Column(sqla.Integer)
    # jar
    dielec = sqla.Column(sqla.Boolean(False))
    acidity = sqla.Column(sqla.Boolean(False))
    density = sqla.Column(sqla.Boolean(False))
    pcb_jar = sqla.Column(sqla.Boolean(False))
    inhibitor_jar = sqla.Column(sqla.Boolean(False))
    point = sqla.Column(sqla.Boolean(False))
    dielec_2 = sqla.Column(sqla.Boolean(False))
    color = sqla.Column(sqla.Boolean(False))
    pf = sqla.Column(sqla.Boolean(False))
    particles = sqla.Column(sqla.Boolean(False))
    metals = sqla.Column(sqla.Boolean(False))
    viscosity = sqla.Column(sqla.Boolean(False))
    dielec_d = sqla.Column(sqla.Boolean(False))
    ift = sqla.Column(sqla.Boolean(False))
    pf_100 = sqla.Column(sqla.Boolean(False))
    furans_f = sqla.Column(sqla.Boolean(False))
    water_w = sqla.Column(sqla.Boolean(False))
    corr = sqla.Column(sqla.Boolean(False))
    dielec_i = sqla.Column(sqla.Boolean(False))
    visual = sqla.Column(sqla.Boolean(False))
    qty_jar = sqla.Column(sqla.Integer)
    sampling_jar = sqla.Column(sqla.Integer)
    # vial
    pcb_vial = sqla.Column(sqla.Boolean(False))
    antioxidant = sqla.Column(sqla.Boolean(False))
    qty_vial = sqla.Column(sqla.Integer)
    sampling_vial = sqla.Column(sqla.Integer)

    def parsedata(self, data):
        if data:
            for key in data.keys():
                if hasattr(self, key):
                    if key in ['selection', 'description', 'qty', 'sampling', 'qty_jar', 'sampling_jar', 'qty_vial',
                               'sampling_vial', 'sampling_vial']:
                        if data[key]:
                            setattr(self, key, data[key])
                    else:
                        setattr(self, key, True if data[key] == 'y' else False)

    def __init__(self, data=None):
        self.parsedata(data)

    def clear_data(self):
        for attr in self.__dict__:
            if attr not in ['id', '_sa_instance_state']:
                # print attr
                if attr == 'selection' and attr == 'description':
                    setattr(self, attr, '')
                if attr in ['qty', 'sampling', 'qty_jar', 'sampling_jar', 'qty_vial', 'sampling_vial', 'sampling_vial']:
                    setattr(self, attr, 0)
                else:
                    setattr(self, attr, False)

    def add_data(self, data):
        self.parsedata(data)


class Location(BaseManager):
    # PhyPosition GPS location
    __tablename__ = u'location'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    # Site. What is the name of the site.
    # Example. A company may have a assembly plants in several cities,
    # therefore each site is named after each city where the plant is.
    Name = sqla.Column(db.String(50), index=True)  # should be relation


class Manufacturer(BaseManager):
    __tablename__ = u'manufacturer'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    Name = sqla.Column(db.String(50))


class GasSensor(BaseManager):
    """
    GasSensor. List gas sensor with their respective sensitivity to each measured gas
     """
    __tablename__ = u'gas_sensor'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Sensor. Sensor commercial name
    Name = sqla.Column(db.String(50))
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    H2 = sqla.Column(db.Float(53), server_default=db.text("0"))  # Remaining are equivalent
    CH4 = sqla.Column(db.Float(53), server_default=db.text("0"))
    C2H2 = sqla.Column(db.Float(53), server_default=db.text("0"))
    C2H4 = sqla.Column(db.Float(53), server_default=db.text("0"))
    C2H6 = sqla.Column(db.Float(53), server_default=db.text("0"))
    CO = sqla.Column(db.Float(53), server_default=db.text("0"))
    CO2 = sqla.Column(db.Float(53), server_default=db.text("0"))
    O2 = sqla.Column(db.Float(53), server_default=db.text("0"))
    N2 = sqla.Column(db.Float(53), server_default=db.text("0"))

    # ppmError. Calculated ppm error by comparing lab ppm from sample with sensor reading at sampling time
    ppmError = sqla.Column(db.Integer, server_default=db.text("0"))

    # percentError. Calculated error in percent
    percentError = sqla.Column(db.Float(53), server_default=db.text("0"))

    def __repr__(self):
        return self.__tablename__


class Transformer(BaseManager):
    __tablename__ = u'transformer'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    GasSensor = db.Column(
        'gas_sensor_id',
        db.ForeignKey("gas_sensor.id"),
        nullable=False
    )

    Frequency = sqla.Column(db.Integer)  # Frequency. Operating frequency
    Windings = sqla.Column(db.Integer)  # Windings. Number of windings in transformer
    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    PhaseNumber = sqla.Column(db.Boolean)  # PhaseNum. 1=single phase, 3=triphase, 6=hexaphase

    # FluidVolume. Quantity of insulating fluid in equipment in litre
    FluidVolume = sqla.Column(db.Float(53))

    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    PrimaryTension = sqla.Column(db.Float(53))  # Volt1. Primary voltage in kV
    SecondaryTension = sqla.Column(db.Float(53))  # Volt2. Secondary voltage in kV
    TertiaryTension = sqla.Column(db.Float(53))  # Volt3. Tertiary voltage in kV

    BasedTransformerPower = sqla.Column(db.Float(53))  # MVA1. Based transformer power
    FirstCoolingStagePower = sqla.Column(db.Float(53))  # MVA2. First cooling stage power
    SecondCoolingStagePower = sqla.Column(db.Float(53))  # MVA3. second cooling stage power

    AutoTransformer = sqla.Column(db.Boolean)  # Autotransformer. True if it is

    # is a separate device
    PrimaryWindingConnection = sqla.Column(
        db.Integer)  # PrimConnection. Primary windings connection on a multi phase transformer
    SecondaryWindingConnection = sqla.Column(
        db.Integer)  # SecConnection. Secondary windings connection on a multi phase transformer
    TertiaryWindingConnection = sqla.Column(
        db.Integer)  # TertConnection. Tertiary windings connection on a multi phase transformer

    # winding metal is a property of winding
    WindindMetal = sqla.Column(db.Integer)  # WindingMetal. Copper or aluminium

    BIL1 = sqla.Column(db.Float(53))  # BIL1. Primary Insulation level in kV
    BIL2 = sqla.Column(db.Float(53))  # BIL2. Secondary Insulation level in kV
    BIL3 = sqla.Column(db.Float(53))  # BIL3. Tertiary Insulation level in kV

    StaticShield1 = sqla.Column(db.Boolean)  # StaticShield1. true with primary electrostatic shield is present
    StaticShield2 = sqla.Column(db.Boolean)  # StaticShield2. true with secondary electrostatic shield is present
    StaticShield3 = sqla.Column(db.Boolean)  # StaticShield3. true with tertiary electrostatic shield is present

    # it's tranformer property
    BushingNeutral1 = sqla.Column(db.Float(53))
    BushingNeutral2 = sqla.Column(db.Float(53))
    BushingNeutral3 = sqla.Column(db.Float(53))
    BushingNeutral4 = sqla.Column(db.Float(53))

    LTC1 = sqla.Column(db.Float(53))  # LTC1.
    LTC2 = sqla.Column(db.Float(53))  # LTC2
    LTC3 = sqla.Column(db.Float(53))  # LTC3

    TemperatureRise = sqla.Column(db.Integer)  # TemperatureRise. Transformer temperature rise

    # it can be a property and also can be tested
    Impedance1 = sqla.Column(db.Float(53))  # Impedance1. Impedance at base MVA
    Imp_Base1 = sqla.Column(db.Float(53))  # ImpBasedMVA1

    Impedance2 = sqla.Column(db.Float(53))  # Impedance2. Impedance at first forced cooling MVA
    Imp_Base2 = sqla.Column(db.Float(53))  # ImpBasedMVA2

    MVAForced11 = sqla.Column(db.Float(53))  # MVAForced11
    MVAForced12 = sqla.Column(db.Float(53))  # MVAForced12
    MVAForced13 = sqla.Column(db.Float(53))  # MVAForced13
    MVAForced14 = sqla.Column(db.Float(53))  # MVAForced14
    MVAForced21 = sqla.Column(db.Float(53))  # MVAForced21
    MVAForced22 = sqla.Column(db.Float(53))  # MVAForced22
    MVAForced23 = sqla.Column(db.Float(53))  # MVAForced23
    MVAForced24 = sqla.Column(db.Float(53))  # MVAForced24

    Impedance3 = sqla.Column(db.Float(53))  # Impedance3. Impedance at third forced cooling MVA
    ImpBasedMVA3 = sqla.Column(db.Float(53))  # ImpBasedMVA3

    # it belongs to transformer , tap voltage, it s a part of the test process
    FormulaRatio2 = sqla.Column(db.Integer)  # RatioFormula2. Formula used for TTR

    # it belongs to transformer , tap voltage, it s a part of the test process
    FormulaRatio = sqla.Column(db.Integer)  # RatioFormula. Formula used for TTR
    RatioTag1 = sqla.Column(db.String(20))  # RatioTag1. Tag use for TTR
    RatioTag2 = sqla.Column(db.String(20))  # RatioTag2. Tag use for TTR
    RatioTag3 = sqla.Column(db.String(20))  # RatioTag3. Tag use for TTR
    RatioTag4 = sqla.Column(db.String(20))  # RatioTag4. Tag use for TTR
    RatioTag5 = sqla.Column(db.String(20))  # RatioTag5. Tag use for TTR
    RatioTag6 = sqla.Column(db.String(20))  # RatioTag6. Tag use for TTR
    FluidType = sqla.Column(db.Integer)  # FluidType. Insulating fluid used in equipment


    # it's a relation to bushing table column "serial number"
    BushingSerial1 = sqla.Column(db.String(15))  # BushingSerial1.
    BushingSerial2 = sqla.Column(db.String(15))  # BushingSerial2.
    BushingSerial3 = sqla.Column(db.String(15))  # BushingSerial3.
    BushingSerial4 = sqla.Column(db.String(15))  # BushingSerial4.
    BushingSerial5 = sqla.Column(db.String(15))  # BushingSerial5.
    BushingSerial6 = sqla.Column(db.String(15))  # BushingSerial6.
    BushingSerial7 = sqla.Column(db.String(15))  # BushingSerial7.
    BushingSerial8 = sqla.Column(db.String(15))  # BushingSerial8.
    BushingSerial9 = sqla.Column(db.String(15))  # BushingSerial9.
    BushingSerial10 = sqla.Column(db.String(15))  # BushingSerial10.
    BushingSerial11 = sqla.Column(db.String(15))  # BushingSerial11.
    BushingSerial12 = sqla.Column(db.String(15))  # BushingSerial12.

    # device property ,  for  transformer
    MVAActual = sqla.Column(db.Float(53))  # MVAActual. Actual MVA used
    MVARActual = sqla.Column(db.Float(53))  # MVARActual. Actual MVA used
    MWReserve = sqla.Column(db.Float(53))  # MWReserve. How much MW in reserve for backup
    MVARReserve = sqla.Column(db.Float(53))  # MVARReserve. How much MVAR in reserve for backup
    MWUltime = sqla.Column(db.Float(53))  # MWUltima. How much MW can ultimately be used in emergency
    MVARUltime = sqla.Column(db.Float(53))  # MVARUltima. How much MVAR can ultimately be used in emergency

    # transformer device property
    MVA4 = sqla.Column(db.Float(53))  # MVA4

    # it transformer property
    # QuatConnection. Quaternary windings connection on a multi phase transformer
    QuaternaryWindingConnection = sqla.Column(db.Float(53))

    # tranformer property
    BIL4 = sqla.Column(db.Float(53))  # BIL4. Tertiary Insulation level in kV
    # tranformer property
    StaticShield4 = sqla.Column(db.Float(53))  # StaticShield4. true with tertiary electrostatic shield is present

    # tranformer property
    RatioTag7 = sqla.Column(db.Float(53))  # RatioTag7. Tag use for TTR
    RatioTag8 = sqla.Column(db.Float(53))  # RatioTag8. Tag use for TTR
    FormulaRatio3 = sqla.Column(db.Float(53))  # RatioFormula3

    def __repr__(self):
        return self.__tablename__


class Breaker(BaseManager):
    __tablename__ = u'breaker'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    PhaseNumber = sqla.Column(db.Boolean)  # PhaseNum. 1=single phase, 3=triphase, 6=hexaphase
    Frequency = sqla.Column(db.Integer)  # Frequency. Operating frequency
    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class LoadTapChanger(BaseManager):
    __tablename__ = u'tap_changer'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Frequency = sqla.Column(db.Integer)  # Frequency. Operating frequency
    PhaseNumber = sqla.Column(db.Boolean)  # PhaseNum. 1=single phase, 3=triphase, 6=hexaphase
    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function
    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    # it should be a test value
    # Filter. What condition is the filter. We must make this field a selection choice such Good, bad, replace etc..
    Filter = sqla.Column(db.String(30))

    # so this is test value (inspection)
    Counter = sqla.Column(db.Integer)  # Counter. Used for load tap changer or arrester (ligthning)

    # tap changer property property
    LTC4 = sqla.Column(db.Float(53))  # LTC4

    def __repr__(self):
        return self.__tablename__


class Bushing(BaseManager):
    __tablename__ = u'bushing'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    Type = ['phase', 'Neutral']
    Name = sqla.Column(db.String(50))
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Frequency = sqla.Column(db.Integer)  # Frequency. Operating frequency
    PhaseNumber = sqla.Column(db.Boolean)  # PhaseNum. 1=single phase, 3=triphase, 6=hexaphase
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function
    BushingManufacturerH1 = sqla.Column(db.String(25))  # Bushing manufacturer for H1
    BushingManufacturerH2 = sqla.Column(db.String(25))  # Bushing manufacturer for H2
    BushingManufacturerH3 = sqla.Column(db.String(25))  # Bushing manufacturer for H3
    BushingManufacturerHN = sqla.Column(db.String(25))  # Bushing manufacturer for HN
    BushingManufacturerX1 = sqla.Column(db.String(25))  # Bushing manufacturer for X1
    BushingManufacturerX2 = sqla.Column(db.String(25))  # Bushing manufacturer for X2
    BushingManufacturerX3 = sqla.Column(db.String(25))  # Bushing manufacturer for X3
    BushingManufacturerXN = sqla.Column(db.String(25))  # Bushing manufacturer for XN
    BushingManufacturerT1 = sqla.Column(db.String(25))  # Bushing manufacturer for T1
    BushingManufacturerT2 = sqla.Column(db.String(25))  # Bushing manufacturer for T2
    BushingManufacturerT3 = sqla.Column(db.String(25))  # Bushing manufacturer for T3
    BushingManufacturerTN = sqla.Column(db.String(25))  # Bushing manufacturer for TN
    BushingManufacturerQ1 = sqla.Column(db.String(25))  # Bushing manufacturer for Q1
    BushingManufacturerQ2 = sqla.Column(db.String(25))  # Bushing manufacturer for Q2
    BushingManufacturerQ3 = sqla.Column(db.String(25))  # Bushing manufacturer for Q3
    BushingManufacturerQN = sqla.Column(db.String(25))  # Bushing manufacturer for QN
    BushingType_H = sqla.Column(db.String(25))  # Bushing type for H
    BushingType_HN = sqla.Column(db.String(25))  # Bushing type for HN
    BushingType_X = sqla.Column(db.String(25))  # Bushing type for X
    BushingType_XN = sqla.Column(db.String(25))  # Bushing type for XN
    BushingType_T = sqla.Column(db.String(25))  # Bushing type for T
    BushingType_TN = sqla.Column(db.String(25))  # Bushing type for TN
    BushingType_Q = sqla.Column(db.String(25))  # Bushing type for Q
    BushingType_QN = sqla.Column(db.String(25))  # Bushing type for QN

    def __repr__(self):
        return self.__tablename__


class Upstream(BaseManager):
    __tablename__ = u'upstream'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    Name = sqla.Column(db.String(50), index=True)


class Downstream(BaseManager):
    __tablename__ = u'downstream'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    Name = sqla.Column(db.String(50), index=True)


class NeutralResistance(BaseManager):

    __tablename__ = u'resistance'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    Name = sqla.Column(db.String(50))
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )
    # its a separate device should be splitted into another table
    NeutralResistance = sqla.Column(db.Float(53))   # NeutralResistance1.
    NeutralResistance1 = sqla.Column(db.Float(53))  # NeutralResistance1.
    NeutralResistance0 = sqla.Column(db.Boolean)    # NeutralResistance0
    NeutralResistance2 = sqla.Column(db.Float(53))  # NeutralResistance2
    NeutralResistance3 = sqla.Column(db.Float(53))  # NeutralResistance3

    # it's status or mode  of a resistance
    NeutralResistanceOpen1 = sqla.Column(db.Boolean)  # NeutralResistanceOpen1
    NeutralResistanceOpen2 = sqla.Column(db.Boolean)  # NeutralResistanceOpen2
    # property of resistence, it's status
    NeutralResistanceOpen3 = sqla.Column(db.Float(53))  # NeutralResistanceOpen3

    def __repr__(self):
        return self.__tablename__


class AirCircuitBreaker(BaseManager):

    __tablename__ = u'air_breaker'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    PhaseNumber = sqla.Column(db.Boolean)  # PhaseNum. 1=single phase, 3=triphase, 6=hexaphase
    Frequency = sqla.Column(db.Integer)  # Frequency. Operating frequency
    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class Capacitor(BaseManager):

    __tablename__ = u'capacitor'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    PhaseNumber = sqla.Column(db.Boolean)  # PhaseNum. 1=single phase, 3=triphase, 6=hexaphase
    Frequency = sqla.Column(db.Integer)  # Frequency. Operating frequency
    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class PowerSource(BaseManager):
    __tablename__ = u'powersource'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    PhaseNumber = sqla.Column(db.Boolean)  # PhaseNum. 1=single phase, 3=triphase, 6=hexaphase
    Frequency = sqla.Column(db.Integer)  # Frequency. Operating frequency
    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class SwitchGear(BaseManager):
    __tablename__ = u'switchgear'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class InductionMachine(BaseManager):
    __tablename__ = u'induction_machine'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class SynchronousMachine(BaseManager):
    __tablename__ = u'synchronous_machine'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class Rectifier(BaseManager):
    __tablename__ = u'rectifier'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class Tank(BaseManager):
    __tablename__ = u'tank'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class Switch(BaseManager):
    __tablename__ = u'switch'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    # WeldedCover. Is cover welded. Important to planned work as it is much longer to remove cover
    WeldedCover = sqla.Column(db.Boolean)

    def __repr__(self):
        return self.__tablename__


class Cable(BaseManager):

    __tablename__ = u'cable'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)

    # Assigned name given by production.
    # Production name never change but equipment may moved around. Must be careful applying a diagnostic related to a
    # Production because equipment can changed over the years and associate wrong diagnostic
    Name = sqla.Column(db.String(50))

    # EquipmentSerialNum: Equipment ID given by manufacturer.
    # Index key, along with Equipment number to uniquely identify equipment
    Serial = sqla.Column(db.String(50), nullable=False, index=True, unique=True)

    Manufacturer = db.Column(
        'manufacturer_id',
        db.ForeignKey("manufacturer.id"),
        nullable=False
    )

    Sealed = sqla.Column(db.Boolean)  # Sealed. Is equipment sealed.
    Manufactured = sqla.Column(db.Integer)  # ManuYear. Year manufactured
    Description = sqla.Column(db.String(50))  # Description. Describe the equipment function

    def __repr__(self):
        return self.__tablename__


class NormType(BaseManager):
    __tablename__ = u'norm_type'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    Name = sqla.Column(db.String(50), index=True)

    # NormPHY.  Fluid physical properties norms
    # NormDissolvedGas. Fluid dissolved gas norms
    # NormFluid# NormFur. Fluid furan norms


class Norm(BaseManager):
    __tablename__ = u'norm'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    Name = sqla.Column(db.String(50), index=True)
    NormType = db.Column(
        'norm_type_id',
        db.ForeignKey("norm_type.id"),
        nullable=False
    )

    # NormPHY.  Fluid physical properties norms
    # NormDissolvedGas. Fluid dissolved gas norms
    # NormFluid# NormFur. Fluid furan norms


class NormParameter(BaseManager):
    __tablename__ = u'norm_parameter'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    Name = sqla.Column(db.String(50), index=True)


class NormParameterValue(BaseManager):

    __tablename__ = u'norm_parameter_value'

    id = sqla.Column(db.Integer(), primary_key=True, nullable=False)
    parameter = db.Column(
        'param_id',
        db.ForeignKey('norm_parameter.id'),
        nullable=False
    )

    Norm = db.Column(
        'norm_id',
        db.ForeignKey("norm.id"),
        nullable=False
    )

    equipment_type_id = db.Column(
        'equipment_type_id',
        db.ForeignKey('equipment_type.id'),
        nullable=False
    )

    value_type = sqla.Column(db.String(50), index=True)
    value = sqla.Column(db.String(50), index=True)