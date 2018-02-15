from flask.ext.wtf import Form
from wtforms import SelectField, HiddenField, TextField, DateField, IntegerField, FloatField, TextAreaField, \
    BooleanField, RadioField
from wtforms.validators import Required, Length, Optional
from app.diagnostic.models import *
from app import db
from app.users.models import User

# myChoices = [ ('' , '...') ] + [ (page.translations[page.get_locale()].title , page.translations[get_locale()].title) for page in Pages.query.order_by(Pages.updated_on.desc()).all() ]
myChoices = []


class MenuViewForm(Form):
    page_view = SelectField(u'Select Page', choices=myChoices, validators=[Required()])
    node_id = HiddenField("node_id", validators=[Required()])


# front page forms
# TODO choises must be filled from db,  not hardcode
stage_choice = [(x.id, x.name ) for x in db.session.query(TestStatus).all()]
order_status_choice = [('Paid', 'Paid'), ]
initials_choice = [(x.id, x.name ) for x in db.session.query(User).all()]
lab_choice = [(x.id, x.name ) for x in db.session.query(Lab).all()]
point_choice = [(x.id, x.name) for x in db.session.query(SamplingPoint).all()]
testing_choice = [(x.id, x.name) for x in db.session.query(TestReason).all()]
profile_choice = [(x.name, x.name) for x in db.session.query(ElectricalProfile).all()]
fluid_choice = [(x.name, x.name) for x in db.session.query(FluidProfile).all()]
equipment_sel_choice = [('all', 'All sites'), ('selected', 'Equipment under selected site')]
winding_choice = [('TODO', 'TODO'), ]
wire_choice = [('TODO', 'TODO'), ]
insulating_choice = [('Oil', 'Oil'), ]
rise_choice = [(55, 55), (65, 65), ]
site_report_choices = [('todo', 'TODO')]
list_choices = [('today', 'Starting as of today'), ('from', 'Starting as of'), ('list', 'Tests list')]
type_choice = [('Transformer', 'Transformer'), ('Switcher', 'Switcher2')]
manufacturer_choice = [('TODO', 'TODO'), ]

class IdentificationViewForm(Form):
    analysis_type = TextField('Analysis Type', validators=[Required()])
    initials = SelectField('Initials', choices=initials_choice, validators=[Required()])
    acq_date = DateField('Acquisition date', validators=[Optional()], format='%m/%d/%Y %H:%M A')
    reason = SelectField('Reason for analysis', choices=testing_choice, validators=[Required()])
    stage = SelectField('Analysis stage', choices=stage_choice, validators=[Required()])
    temp = IntegerField('Fluid temp.(*C)', validators=[Required()])
    insulating = IntegerField('Insulating fluid', validators=[Required()])
    contract = TextField('Contract No.', validators=[Required()])
    grouping = TextField('Test grouping', validators=[Required()])
    sampling = SelectField('Sampling point', choices=point_choice, validators=[Required()])
    syringe = TextField('Syringe No. / jar No. ', validators=[Required()])
    analysis_no = IntegerField('Analysis No.', validators=[Required()])
    lab_date = DateField('Lab analysis date', validators=[Optional()], format='%m/%d/%Y %H:%M:%S')
    load_mva = FloatField('Load(Mva)', validators=[Required()])
    equipment = TextField('Test equipment', validators=[Required()])
    order_status = SelectField('Lad order status', choices=order_status_choice, validators=[Required()])
    lab_no = TextField('Lab P.O. No.', validators=[Required()])
    laboratory = SelectField('Laboratory', choices=lab_choice, validators=[Required()])


class TestRepairViewForm(Form):
    comments = TextAreaField('Test or sampling comments', validators=[Required()])
    notes = TextAreaField('Notes on equipment: repairs, additions, etc.', validators=[Required()])
    sampled = TextField('Sampled by', validators=[Required()])
    date = DateField('Date of repairs or degassing', validators=[Optional()], format='%m/%d/%Y %H:%M A')


class RecordsDiagnosticViewForm(Form):
    diagnosis = TextAreaField('Diagnosis', validators=[Required()])
    recommendations = TextAreaField('Recommendations', validators=[Required()])
    predefined_diag = TextField('Predefined diagnosis', validators=[Required()])
    predefined_rec = TextField('Predefined Recommendations', validators=[Required()])
    date = DateField('Date of recommendation', validators=[Optional()], format='%m/%d/%Y')


class EquipmentDiagnosisViewForm(Form):
    diagnosis = TextAreaField('Equipment diagnosis', validators=[Required()])
    indicator = TextField('Condition indicator', validators=[Required()])
    condition = BooleanField('Equipment in questionable condition or out of service', validators=[Optional()])

# Create new test
class NewTestDescription(Form):
    equipment = TextField('Equipment No.', validators=[Required()])
    position = TextField('Position No.', validators=[Required()])
    fluid = TextField('Insulating fluid.', validators=[Required()])
    lab = SelectField('Lab./On-line analyser', choices=lab_choice, validators=[Required()])
    contract = TextField('Contract No.', validators=[Required()])
    lab_no = TextField('Lab P.O No.', validators=[Required()])
    date = DateField('Acquisition date', validators=[Optional()], format='%m/%d/%Y %H:%M:%S')
    testing = SelectField('Reason for testing', choices=testing_choice, validators=[Required()])
    initials = SelectField('Initials', choices=initials_choice, validators=[Required()])


class NewTestElectrical(Form):
    bushing = BooleanField('Bushing Cap. and PF', validators=[Optional()])
    winding = BooleanField('Winding Cap. and PF', validators=[Optional()])
    winding_double = BooleanField('Winding Cap. and PF Doble', validators=[Optional()])
    insulation = BooleanField('Insulation resistance', validators=[Optional()])
    visual = BooleanField('Visual inspection', validators=[Optional()])
    resistance = BooleanField('Resistance; winding/contact', validators=[Optional()])
    degree = BooleanField('Degree of Polymerization (DP)', validators=[Optional()])
    turns = BooleanField('Turns ratio test (TTR)', validators=[Optional()])


class NewTestFluid(Form):
    # syringe
    gas = BooleanField('Dissolved gas', validators=[Optional()])
    water = BooleanField('Water', validators=[Optional()])
    furans = BooleanField('Furans', validators=[Optional()])
    inhibitor = BooleanField('Inhibitor', validators=[Optional()])
    pcb = BooleanField('PCB', validators=[Optional()])
    qty_ser = IntegerField('Qty', validators=[Optional()])
    sampling = SelectField('Sampling point', choices=point_choice, validators=[Required()])
    # jar
    dielec = BooleanField('Dielec.D1816(1mm)(kV)', validators=[Optional()])
    acidity = BooleanField('Acidity(D974)', validators=[Optional()])
    density = BooleanField('Density(D1298)', validators=[Optional()])
    pcb_jar = BooleanField('PCB', validators=[Optional()])
    inhibitor_jar = BooleanField('Inhibitor', validators=[Optional()])
    point = BooleanField('Pour point', validators=[Optional()])
    dielec_2 = BooleanField('Dielec.D1816(2mm)(kV)', validators=[Optional()])
    color = BooleanField('Color(D1500)', validators=[Optional()])
    pf = BooleanField('PF 25C(D924)', validators=[Optional()])
    particles = BooleanField('Particles', validators=[Optional()])
    metals = BooleanField('Metals in oil', validators=[Optional()])
    viscosity = BooleanField('Viscosity', validators=[Optional()])
    dielec_d = BooleanField('Dielec. D877(kV)', validators=[Optional()])
    ift = BooleanField('IFT (D971)', validators=[Optional()])
    pf_100 = BooleanField('PF 100C (D924)', validators=[Optional()])
    furans_f = BooleanField('Furans', validators=[Optional()])
    water_w = BooleanField('Water', validators=[Optional()])
    corr = BooleanField('Corr. sulfur', validators=[Optional()])
    dielec_i = BooleanField('Dielec. IEC-156(kV)', validators=[Optional()])
    visual = BooleanField('Visual (D1524)', validators=[Optional()])
    qty_jar = IntegerField('Qty', validators=[Optional()])
    sampling_jar = SelectField('Sampling point', choices=point_choice, validators=[Required()])
    # vial
    pcb_vial = BooleanField('PCB', validators=[Optional()])
    antioxidant = BooleanField('Antioxidant', validators=[Optional()])
    qty_vial = IntegerField('Qty', validators=[Optional()])
    sampling_vial = SelectField('Sampling point', choices=point_choice, validators=[Required()])


class NewTestProfile(Form):
    # electrical
    enable_elc = BooleanField('Enable the selection of test according to profile', validators=[Optional()])
    profile_elc = SelectField('Profile selection', choices = profile_choice , validators=[Required()])
    description_elc = TextField('Description', validators=[Required()])
    # fluid
    enable_fl = BooleanField('Enable the selection of test according to profile', validators=[Optional()])
    profile_fl = SelectField('Profile selection', choices = fluid_choice , validators=[Required()])
    description_fl = TextField('Description', validators=[Required()])


class BatchViewForm(Form):
    # equipment selection
    equipment_sel = RadioField('Equipment Selection', choices=equipment_sel_choice)
    # data selection
    months = TextField(
        'Number of months in analysis period,starting from date selected.Select "0" to include all dates',
        validators=[Required()])
    gasses = BooleanField('Dissolved gasses.', validators=[Optional()])
    acquisition = BooleanField('Acquisition.', validators=[Optional()])
    oil = BooleanField('Oil quality.', validators=[Optional()])
    lab = BooleanField('Lab./On-line analyser.', validators=[Optional()])
    water = BooleanField('Dissolved water.', validators=[Optional()])
    diagnosis = BooleanField('Diagnosis', validators=[Optional()])
    oxidation = BooleanField('Oxidation Inhibitor.', validators=[Optional()])
    recommendation = BooleanField('Recommendation', validators=[Optional()])
    furans = BooleanField('Furan coumpounds.', validators=[Optional()])
    completed = BooleanField('Completed', validators=[Optional()])
    electrical = BooleanField('Electrical tests.', validators=[Optional()])
    # selection of cases for the report
    rush = BooleanField('Rush.', validators=[Optional()])
    follow = BooleanField('To follow up.', validators=[Optional()])
    # validation of selections
    # recording of results
    abnormal = BooleanField('If condition is abnormal, set "Doubtful Condition(DC)" flag', validators=[Optional()])
    normal = BooleanField('If condition is normal, set the analysis status to "Completed"', validators=[Optional()])


class EquipmentTestReportViewForm(Form):
    # Equipment
    site = SelectField('Site', choices=site_report_choices, validators=[Required()])
    generate = BooleanField('Generate reports on all equipment with the following contract number.',
                            validators=[Optional()])
    contact = TextField('Description', validators=[Required()])
    contract_list = TextField('List of equipment with same contract number listed above', validators=[Required()])
    above = TextAreaField('List', validators=[Required()])
    # Reports
    bushing = BooleanField('Bushing Cap. and PF', validators=[Optional()])
    color = BooleanField('Color', validators=[Optional()])
    cap = BooleanField('Winding Cap. and PF', validators=[Optional()])
    double = BooleanField('Double', validators=[Optional()])
    dissolved = BooleanField('Dissolved gas', validators=[Optional()])
    resistance = BooleanField('Insulation resistance', validators=[Optional()])
    fluid = BooleanField('Insulation resistance', validators=[Optional()])
    inspection = BooleanField('Visual inspection', validators=[Optional()])
    water = BooleanField('Water', validators=[Optional()])
    winding = BooleanField('Resistance;winding/contact', validators=[Optional()])
    inhibitor = BooleanField('Inhibitor', validators=[Optional()])
    ratio = BooleanField('Turns ration test(TTR)', validators=[Optional()])
    furans = BooleanField('Furans', validators=[Optional()])
    sampling = BooleanField('Sampling sheet', validators=[Optional()])
    metals = BooleanField('Metals in oil', validators=[Optional()])
    evaluation = BooleanField('Global evaluation', validators=[Optional()])
    pcb = BooleanField('PCB', validators=[Optional()])
    particles = BooleanField('Particles', validators=[Optional()])
    degree = BooleanField('Degree of Polymerization(DP)', validators=[Optional()])
    log_1 = BooleanField('Log', validators=[Optional()])
    log_2 = BooleanField('Log', validators=[Optional()])
    log_3 = BooleanField('Log', validators=[Optional()])
    log_4 = BooleanField('Log', validators=[Optional()])
    log_5 = BooleanField('Log', validators=[Optional()])
    log_6 = BooleanField('Log', validators=[Optional()])
    log_7 = BooleanField('Log', validators=[Optional()])
    percent_1 = BooleanField('Percent', validators=[Optional()])
    percent_2 = BooleanField('Percent', validators=[Optional()])
    percent_3 = BooleanField('Percent', validators=[Optional()])
    percent_4 = BooleanField('Percent', validators=[Optional()])
    percent_5 = BooleanField('Percent', validators=[Optional()])
    percent_6 = BooleanField('Percent', validators=[Optional()])
    percent_7 = BooleanField('Percent', validators=[Optional()])
    alignment_1 = BooleanField('Alignment', validators=[Optional()])
    alignment_2 = BooleanField('Alignment', validators=[Optional()])
    alignment_3 = BooleanField('Alignment', validators=[Optional()])
    alignment_4 = BooleanField('Alignment', validators=[Optional()])
    alignment_5 = BooleanField('Alignment', validators=[Optional()])
    alignment_6 = BooleanField('Alignment', validators=[Optional()])
    alignment_7 = BooleanField('Alignment', validators=[Optional()])
    border_1 = BooleanField('Borders', validators=[Optional()])
    border_2 = BooleanField('Borders', validators=[Optional()])
    border_3 = BooleanField('Borders', validators=[Optional()])
    border_4 = BooleanField('Borders', validators=[Optional()])
    border_5 = BooleanField('Borders', validators=[Optional()])
    border_6 = BooleanField('Borders', validators=[Optional()])
    border_7 = BooleanField('Borders', validators=[Optional()])
    # test records (max. - 7)
    list = RadioField('Starting', choices=list_choices)
    list_date = DateField('Date', validators=[Optional()], format='%m/%d/%Y')
    period = TextField('Analysis period(months)', validators=[Required()])
    ascending = BooleanField('Sort ascending', validators=[Optional()])
    # generation of reports
    pdf = BooleanField('PDF', validators=[Optional()])
    paper = BooleanField('Paper format', validators=[Optional()])
    preview = BooleanField('Preview', validators=[Optional()])
    numbering = TextField('Start of page numbering', validators=[Required()])
    rtf = BooleanField('RTF', validators=[Optional()])


class ManageCustomersViewForm(Form):
    cust_no = TextField('Cust. No.', validators=[Required()])
    customer = TextField('Customer', validators=[Optional()])
    contact = TextField('Contact', validators=[Optional()])
    street = TextField('Street', validators=[Optional()])
    city = TextField('City', validators=[Optional()])
    state = TextField('Prov./State', validators=[Optional()])
    tel = TextField('Tel.', validators=[Optional()])
    ext = TextField('Ext.', validators=[Optional()])
    fax = TextField('Fax', validators=[Optional()])
    email = TextField('E-mail', validators=[Optional()])
    zip = TextField('E-mail', validators=[Optional()])
    pdf = BooleanField('PDF', validators=[Optional()])
    paper = BooleanField('Paper format', validators=[Optional()])
    preview = BooleanField('Preview', validators=[Optional()])
    numbering = TextField('Start of page numbering', validators=[Required()])
    rtf = BooleanField('RTF', validators=[Optional()])


class SearchViewForm(Form):
    equipment = TextField('Search', validators=[Required()])


class DataViewForm(Form):
    hydrogen_check = BooleanField('Hydrogen', validators=[Optional()])
    hydrogen_h2 = IntegerField('Hydrogen-H2', validators=[Required()])
    oxygen_check = BooleanField('Oxygen', validators=[Optional()])
    oxygen_o2 = IntegerField('Oxygen-O2', validators=[Required()])
    nitrogen_check = BooleanField('Nitrogen', validators=[Optional()])
    nitrogen = IntegerField('Nitrogen-N2', validators=[Required()])
    co_check = BooleanField('CO', validators=[Optional()])
    co = IntegerField('CO', validators=[Required()])
    methane_check = BooleanField('Methane', validators=[Optional()])
    methane = IntegerField('Methane-CH4', validators=[Required()])
    co2_check = BooleanField('CO2', validators=[Optional()])
    co2 = IntegerField('C02', validators=[Required()])
    ethylene_check = BooleanField('Ethylene', validators=[Optional()])
    ethylene = IntegerField('Ethylene-C2H4', validators=[Required()])
    ethylene_c2_check = BooleanField('Ethylene', validators=[Optional()])
    ethylene_c2 = IntegerField('Ethylene-C2H6', validators=[Required()])
    acethylene_check = BooleanField('Acethylene', validators=[Optional()])
    acethylene = IntegerField('Acethylene-C2H2', validators=[Required()])
    status_1 = TextField('Status 1', validators=[Required()])
    status_2 = TextField('Status 2', validators=[Required()])
    measured = IntegerField('Measured', validators=[Required()])
    calculated_minus = TextField('-Calculated', validators=[Required()])
    calculated_plus = TextField('+Calculated', validators=[Required()])
    tdcg = IntegerField('TDCG', validators=[Required()])
    total = IntegerField('Total hydrocarbons', validators=[Required()])
    gas_1 = FloatField('Gas content(%)', validators=[Required()])
    gas_2 = FloatField('Gas content(%)', validators=[Required()])


class IdentificationInfoViewForm(Form):
    # Designation
    equipment = TextField('Equipment No.', validators=[Required()])
    serial = TextField('Serial No.', validators=[Required()])
    type = SelectField('Type', choices=type_choice, validators=[Required()])
    # information for printed reports
    site = TextField('Site', validators=[Required()])
    substation = TextField('Substation', validators=[Required()])
    manufacturer = SelectField('Manufacturer', choices=manufacturer_choice, validators=[Required()])
    year = IntegerField('Year', validators=[Required()])
    position = TextField('Position No.', validators=[Required()])
    description = TextField('Description', validators=[Required()])
    analyzer = TextField('Dissolved gas analyzed', validators=[Required()])
    cust = TextField('Cust. No', validators=[Required()])
    cus_ds = TextField('Cust. No1', validators=[Required()])


class ValidationInfoViewForm(Form):
    transformer = TextAreaField('Mobile transformer', validators=[Required()])
    # information validated with the laboratory
    validated = BooleanField('Information validated', validators=[Optional()])
    validated_info = BooleanField('Information being validated', validators=[Optional()])
    equipment = TextField('Previous equipment No.', validators=[Required()])
    serial = TextField('Previous serial No.', validators=[Required()])


class NameplateInfoViewForm(Form):
    winding = SelectField('Winding', choices=winding_choice, validators=[Required()])
    phase = BooleanField('Three-phase', validators=[Optional()])
    transf = BooleanField('Auto-transf.', validators=[Optional()])
    sealed = BooleanField('Sealed', validators=[Optional()])
    cover = BooleanField('Welded cover', validators=[Optional()])
    pri_1 = IntegerField('Pri.', validators=[Required()])
    pri_2 = IntegerField('Pri.', validators=[Required()])
    pri_3 = IntegerField('Pri.', validators=[Required()])
    pri_4 = IntegerField('Pri.', validators=[Required()])
    pri_5 = IntegerField('Pri.', validators=[Required()])
    sec_1 = IntegerField('Sec.', validators=[Required()])
    sec_2 = IntegerField('Sec.', validators=[Required()])
    sec_3 = IntegerField('Sec.', validators=[Required()])
    sec_4 = IntegerField('Sec.', validators=[Required()])
    sec_5 = IntegerField('Sec.', validators=[Required()])
    tert_1 = IntegerField('Tert.', validators=[Required()])
    tert_2 = IntegerField('Tert.', validators=[Required()])
    tert_3 = IntegerField('Tert.', validators=[Required()])
    tert_4 = IntegerField('Tert.', validators=[Required()])
    tert_5 = IntegerField('Tert.', validators=[Required()])
    shield_1 = BooleanField('Eelect. shield', validators=[Optional()])
    shield_2 = BooleanField('Eelect. shield', validators=[Optional()])
    shield_3 = BooleanField('Eelect. shield', validators=[Optional()])
    taps_1 = IntegerField('No. of taps', validators=[Optional()])
    taps_2 = IntegerField('No. of taps', validators=[Optional()])
    taps_3 = IntegerField('No. of taps', validators=[Optional()])
    conn_1 = TextField('Winding conn.', validators=[Required()])
    conn_2 = TextField('Winding conn.', validators=[Required()])
    conn_3 = TextField('Winding conn.', validators=[Required()])
    bushing = BooleanField('Neutral Bushing.', validators=[Required()])
    insulating = SelectField('Insulating fluid', choices=insulating_choice, validators=[Required()])
    mva = IntegerField('Base Mva', validators=[Required()])
    mva_1 = IntegerField('Base Mva', validators=[Required()])
    mva_pro = IntegerField('%', validators=[Required()])
    mva_pro_1 = IntegerField('%', validators=[Required()])
    qty = IntegerField('Oil qty. (liters)', validators=[Optional()])
    rise = RadioField('Temp. rise(C)', choices=rise_choice, validators=[Optional()])
    wire = SelectField('Winding wire.', choices=winding_choice, validators=[Required()])
    maint = IntegerField('No. of op. between maint', validators=[Required()])
    freq = IntegerField('Freq. (Hz)', validators=[Required()])


class BushingInfoViewForm(Form):
    primary_1 = IntegerField('Primary (H)', validators=[Optional()])
    primary_2 = IntegerField('Primary (H)', validators=[Optional()])
    primary_3 = IntegerField('Primary (H)', validators=[Optional()])
    manufacturer = TextField('Manufacturer', validators=[Required()])
    type = TextField('Type', validators=[Required()])
    secondary_1 = IntegerField('Secondary (X)', validators=[Optional()])
    secondary_2 = IntegerField('Secondary (X)', validators=[Optional()])
    secondary_3 = IntegerField('Secondary (X)', validators=[Optional()])
    manufacturer_1 = TextField('Manufacturer', validators=[Required()])
    type_1 = TextField('Type', validators=[Required()])
    tertiary_1 = IntegerField('Tertiary (T)', validators=[Optional()])
    tertiary_2 = IntegerField('Tertiary (T)', validators=[Optional()])
    tertiary_3 = IntegerField('Tertiary (T)', validators=[Optional()])
    manufacturer_2 = TextField('Manufacturer', validators=[Required()])
    type_2 = TextField('Type', validators=[Required()])


class TapsInfoViewForm(Form):
    phase_x_1 = TextField('Phase 1', validators=[Required()])
    phase_x_2 = TextField('Phase 2', validators=[Required()])
    phase_x_3 = TextField('Phase 3', validators=[Required()])
    phase_t_1 = TextField('Phase 1', validators=[Required()])
    phase_t_2 = TextField('Phase 2', validators=[Required()])
    phase_t_3 = TextField('Phase 3', validators=[Required()])


class NormsInfoViewForm(Form):
    oil = TextField('Oil Quality', validators=[Required()])
    gas = TextField('Dissolved Gases', validators=[Required()])
    furnas = TextField('Furans', validators=[Required()])


class LoadInfoViewForm(Form):
    mw_actual = IntegerField('MW', validators=[Optional()])
    mvar_actual = IntegerField('MVAR', validators=[Optional()])
    mw_reserved = IntegerField('MW', validators=[Optional()])
    mvar_reserved = IntegerField('MVAR', validators=[Optional()])
    mw_maximum = IntegerField('MW', validators=[Optional()])
    mvar_maximum = IntegerField('MVAR', validators=[Optional()])
    data = TextAreaField('Design and tests data', validators=[Optional()])


class DocInfoViewForm(Form):
    from_1 = TextField('From:', validators=[Required()])
    from_2 = TextField('From:', validators=[Required()])
    to_1 = TextField('To:', validators=[Required()])
    to_2 = TextField('To:', validators=[Required()])
