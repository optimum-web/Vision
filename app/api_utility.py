import math
from app.diagnostic.models import *
from app.users.models import User, Role
from datetime import datetime
from cerberus import Validator
from sqlalchemy import desc



class Tree(db.Model):
    __tablename__ = 'tree'

    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    parent_id = db.Column('parent_id', db.ForeignKey("tree.id"), nullable=True)
    equipment_id = db.Column('equipment_id', db.ForeignKey(Equipment.id), nullable=False)
    equipment = db.relationship(Equipment, foreign_keys='Tree.equipment_id')
    icon = db.Column(db.String(126))
    opened = db.Column(db.Boolean)
    disabled = db.Column(db.Boolean)
    selected = db.Column(db.Boolean)
    type = db.Column(db.String(58))
    view = db.Column(db.String(126))
    status = db.Column(db.SMALLINT)

    def __repr__(self):
        return "{}".format(self.id)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'equipment_id': self.equipment_id,
            'icon': self.icon,
            'opened': self.opened,
            'disabled': self.disabled,
            'selected': self.selected,
            'type': self.type,
            'view': self.view,
            'status': self.status,
        }


class TreeTranslation(db.Model):
    __tablename__ = 'tree_translation'

    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    locale = db.Column(db.String(10))
    text = db.Column(db.String(250))
    tooltip = db.Column(db.String(250))

    def __repr__(self):
        return "{}".format(self.id)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'locale': self.locale,
            'text': self.text,
            'tooltip': self.tooltip,
        }


class MyValidator(Validator):
    def _validate_fluid_tests_qty(self, fluid_tests_qty, field, value):
        quantity_ml_syringe = 0

        # Syringe
        if self.document.get('gas'): quantity_ml_syringe += 15
        if self.document.get('water'): quantity_ml_syringe += 10
        if self.document.get('pcb'): quantity_ml_syringe += 5
        if self.document.get('furans'): quantity_ml_syringe += 20

        quantity = math.ceil(quantity_ml_syringe / 30.0)

        if not quantity_ml_syringe and self.document.get('inhibitor'):  # chkDBPCSer.Item(0).value?
            quantity = 1

        if quantity != value:
            self._error(field, "Wrong quantity, must be {}".format(quantity))

    def _validate_fluid_tests_qty_jar(self, fluid_tests_qty, field, value):
        quantity_ml_jar = 0
        # POTS. Jar
        if self.document.get('dielec'): quantity_ml_jar += 500
        if self.document.get('dielec_2'): quantity_ml_jar += 500
        if self.document.get('dielec_d'): quantity_ml_jar += 450
        if self.document.get('dielec_i'): quantity_ml_jar += 500
        if self.document.get('ift'): quantity_ml_jar += 25
        if self.document.get('pf'): quantity_ml_jar += 100
        if self.document.get('pf_100'): quantity_ml_jar += 100
        if self.document.get('point'): quantity_ml_jar += 50
        if self.document.get('viscosity'): quantity_ml_jar += 50
        if self.document.get('corr'): quantity_ml_jar += 200
        if self.document.get('pcb_jar'): quantity_ml_jar += 5
        if self.document.get('particles'): quantity_ml_jar += 500
        if self.document.get('metals'): quantity_ml_jar += 50
        if self.document.get('water_w'): quantity_ml_jar += 10
        if self.document.get('furans_f'): quantity_ml_jar += 20

        quantity = math.ceil(quantity_ml_jar / 750.0)

        if(not quantity_ml_jar) and (self.document.get('acidity') or
                                     self.document.get('color') or
                                     self.document.get('density') or
                                     self.document.get('visual') or
                                     self.document.get('inhibitor_jar')):
            quantity = 1

        if quantity != value:
            self._error(field, "Wrong quantity, must be {}".format(quantity))

    def _validate_fluid_tests_qty_vial(self, fluid_tests_qty, field, value):
        # FIOLES. vial
        quantite_ml_vial = 0

        if self.document.get('pcb_vial'):
            quantite_ml_vial += 5
        quantity = math.ceil(quantite_ml_vial / 5.0)

        if not quantite_ml_vial and self.document.get('antioxidant'):
            quantity = 1

        if quantity != value:
            self._error(field, "Wrong quantity, must be {}".format(quantity))
    # testcheckedtemp = 0
    # if (self.document.get('point') or
    #     self.document.get('viscosity') or
    #     self.document.get('corr')):
    #     testcheckedtemp = 1

    def _validate_norm_gas_fluid_level(self, norm_gas_fluid_level, field, value):
        last_norm = db.session.query(NormGas).order_by(desc(NormGas.fluid_level)).first()

        if last_norm and last_norm.fluid_level >= value:
            msg = "Wrong fluid level, must be more than {}".format(last_norm.fluid_level)
            self._error(field, msg)

    def _validate_more_then(self, field_compare, field, value):
        lower_value = self.document.get(field_compare)
        if lower_value is None:
            self._error(field, "Value of {} must be indicated".format(field_compare))
        if lower_value >= value:
            msg = "Wrong {} value, must be more than {}".format(field, field_compare)
            self._error(field, msg)


def dict_copy_union(dict1, *kargs):
    dict3 = dict1.copy()
    for dict_item in kargs:
        dict3.update(dict_item)
    return dict3


def coerce_to_bool(value):
    if value is None:
        return None
    return bool(value)


def coerce_to_int(value):
    try:
        return int(value)
    except TypeError:
        return None


def coerce_to_float(value):
    try:
        return float(value)
    except TypeError:
        return None


def coerce_to_str(value):
    if value is None:
        return None
    return str(value.encode('utf-8'))


def coerce_to_date_str(value):
    if value is None:
        return None
    return value


# Schemas for creation
readonly_dict = {'readonly': True}
required_dict = {'required': True, 'nullable': False}
type_string_dict = {'type': 'string', 'coerce': coerce_to_str}
type_datetime_dict = {'type': 'string', 'coerce': coerce_to_date_str}
type_boolean_coerce_dict = {'type': 'boolean', 'coerce': coerce_to_bool}
type_float_coerce_dict = {'type': 'float', 'coerce': coerce_to_float}
type_datetime_required_dict = dict_copy_union(type_datetime_dict, required_dict)
type_integer_coerce_dict = {'type': 'integer', 'coerce': coerce_to_int}
type_integer_coerce_4_digits_dict = dict_copy_union(type_integer_coerce_dict, {'max': 9999})
type_integer_coerce_6_digits_dict = dict_copy_union(type_integer_coerce_dict, {'max': 999999})
type_integer_coerce_8_digits_dict = dict_copy_union(type_integer_coerce_dict, {'max': 99999999})
type_integer_coerce_required_dict = dict_copy_union(type_integer_coerce_dict, required_dict)
type_string_maxlength_5_dict = dict_copy_union(type_string_dict, {'maxlength': 5})
type_string_maxlength_10_dict = dict_copy_union(type_string_dict, {'maxlength': 10})
type_string_maxlength_20_dict = dict_copy_union(type_string_dict, {'maxlength': 20})
type_string_maxlength_25_dict = dict_copy_union(type_string_dict, {'maxlength': 25})
type_string_maxlength_50_dict = dict_copy_union(type_string_dict, {'maxlength': 50})
type_string_maxlength_80_dict = dict_copy_union(type_string_dict, {'maxlength': 80})
type_string_maxlength_100_dict = dict_copy_union(type_string_dict, {'maxlength': 100})
type_string_maxlength_126_dict = dict_copy_union(type_string_dict, {'maxlength': 126})
type_string_maxlength_250_dict = dict_copy_union(type_string_dict, {'maxlength': 250})
type_string_maxlength_255_dict = dict_copy_union(type_string_dict, {'maxlength': 255})
type_string_maxlength_256_dict = dict_copy_union(type_string_dict, {'maxlength': 256})
type_string_maxlength_1024_dict = dict_copy_union(type_string_dict, {'maxlength': 1024})
type_string_maxlength_50_required_dict = dict_copy_union(type_string_maxlength_50_dict, required_dict)
type_string_frequency_dict = dict_copy_union(type_string_dict, {'allowed': ['25', '50', '60', 'DC']})

fluid_type_schema = sampling_point_schema = contract_status_schema = interrupting_medium_schema = \
    gas_level_schema = breaker_mechanism_schema = insulation_schema = test_reason_schema = \
    location_schema = {'id': readonly_dict, 'name': type_string_maxlength_50_dict}
gasket_condition_schema = gas_relay_schema = fluid_level_schema = pressure_unit_schema = valve_condition_schema = \
    pump_condition_schema = overall_condition_schema = paint_types_schema = tap_counter_status_schema = \
    tap_filter_condition_schema = fan_condition_schema = connection_condition_schema = foundation_condition_schema = \
    heating_condition_schema = {
        'id': readonly_dict,
        'name': type_string_maxlength_25_dict
    }
equipment_connection_schema = {
    'id': readonly_dict,
    'equipment_id': type_integer_coerce_dict,
    'parent_id': type_integer_coerce_dict,
}
sibling_schema = {
    'id': readonly_dict,
    'equipment_id': type_integer_coerce_dict,
    'sibling_id': type_integer_coerce_dict,
}
# sampling_card_schema = {
#     'id': readonly_dict,
#     'card_gathered': type_integer_coerce_dict,
#     'card_print': type_boolean_coerce_dict,
# }
equipment_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_required_dict,
    'equipment_number': type_string_maxlength_50_required_dict,
    'equipment_type_id': type_integer_coerce_required_dict,
    'location_id': type_integer_coerce_required_dict,
    #'assigned_to_id': type_integer_coerce_required_dict,
    'manufacturer_id': type_integer_coerce_dict,
    'serial': type_string_maxlength_50_dict,
    'manufactured': dict_copy_union(type_integer_coerce_dict, {'min': 1900, 'max': datetime.now().year}),
    'frequency': type_string_frequency_dict,
    'description': type_string_dict,
    'modifier':  type_boolean_coerce_dict,
    'comments':  type_string_dict,
    'nbr_of_tap_change_ltc': type_integer_coerce_dict,
    'tie_status':    type_integer_coerce_dict,
    'status':    type_integer_coerce_dict,
    'phys_position': type_integer_coerce_dict,
    'tension4':  type_float_coerce_dict,
    'validated': type_boolean_coerce_dict,
    'invalidation':  type_boolean_coerce_dict,
    'prev_serial_number':    type_string_maxlength_50_dict,
    'prev_equipment_number': type_string_maxlength_50_dict,
    'sibling':   type_integer_coerce_dict,
    'extra_fields': {'type': 'dict'},
}
equipment_type_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'code': type_string_maxlength_50_dict,
    'table_name': type_string_maxlength_50_dict,
}
campaign_schema = {
    'id': readonly_dict,
    'date_created': type_datetime_required_dict,
    'created_by_id': type_integer_coerce_required_dict,
    'contract_id': type_integer_coerce_required_dict,
    'date_sampling': type_datetime_dict,
    'description': type_string_dict,
    'status_id': type_integer_coerce_dict,
}
contract_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_required_dict,
    'code': type_string_maxlength_50_required_dict,
    'contract_status_id': type_integer_coerce_required_dict,
}
norm_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'table_name': type_string_maxlength_50_dict,
}
manufacturer_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_required_dict,
    'markings': type_string_dict,
    'location': type_string_maxlength_256_dict,
    'description': type_string_dict,
}
user_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'alias': type_string_maxlength_50_required_dict,
    'email': dict_copy_union(type_string_dict, required_dict, {'maxlength': 120}),
    'password': type_string_maxlength_50_required_dict,
    'roles': type_integer_coerce_required_dict,
    'status': type_integer_coerce_dict,
    'address': type_string_maxlength_255_dict,
    'mobile': type_string_maxlength_50_dict,
    'website': type_string_maxlength_255_dict,
    # 'country': type_string_maxlength_255_dict,
    'country_id': type_integer_coerce_dict,
    'photo': type_string_maxlength_255_dict,
    'description': type_string_dict,
    'active': type_boolean_coerce_dict,
    'confirmed': type_boolean_coerce_dict,
    # 'confirmed_at': type_datetime_dict,
    'created': type_datetime_dict,
    'updated': type_datetime_dict,
}
electrical_profile_schema = {
    'id': readonly_dict,
    'user_id': type_integer_coerce_dict,
    'name': type_string_maxlength_256_dict,
    'description': type_string_maxlength_1024_dict,
    'shared': type_boolean_coerce_dict,
    'bushing': type_boolean_coerce_dict,
    'winding': type_boolean_coerce_dict,
    'insulation_pf': type_boolean_coerce_dict,
    'insulation': type_boolean_coerce_dict,
    'visual': type_boolean_coerce_dict,
    'resistance': type_boolean_coerce_dict,
    'degree': type_boolean_coerce_dict,
    'turns': type_boolean_coerce_dict,
}
country_schema = {
    'id': readonly_dict,
    'name': readonly_dict,
    'iso_name': readonly_dict,
}
fluid_profile_schema = {
    'id': readonly_dict,
    'user_id': type_integer_coerce_dict,
    'name': type_string_maxlength_256_dict,
    'description': type_string_maxlength_1024_dict,
    'shared': type_boolean_coerce_dict,
    'gas': type_boolean_coerce_dict,
    'water': type_boolean_coerce_dict,
    'furans': type_boolean_coerce_dict,
    'inhibitor': type_boolean_coerce_dict,
    'pcb': type_boolean_coerce_dict,
    'qty_ser': dict_copy_union(type_integer_coerce_dict, {'fluid_tests_qty': True}),
    'sampling': type_integer_coerce_dict,
    'dielec': type_boolean_coerce_dict,
    'acidity': type_boolean_coerce_dict,
    'density': type_boolean_coerce_dict,
    'pcb_jar': type_boolean_coerce_dict,
    'inhibitor_jar': type_boolean_coerce_dict,
    'point': type_boolean_coerce_dict,
    'dielec_2': type_boolean_coerce_dict,
    'color': type_boolean_coerce_dict,
    'pf': type_boolean_coerce_dict,
    'particles': type_boolean_coerce_dict,
    'metals': type_boolean_coerce_dict,
    'viscosity': type_boolean_coerce_dict,
    'dielec_d': type_boolean_coerce_dict,
    'ift': type_boolean_coerce_dict,
    'pf_100': type_boolean_coerce_dict,
    'furans_f': type_boolean_coerce_dict,
    'water_w': type_boolean_coerce_dict,
    'corr': type_boolean_coerce_dict,
    'dielec_i': type_boolean_coerce_dict,
    'visual': type_boolean_coerce_dict,
    'qty_jar': dict_copy_union(type_integer_coerce_dict, {'fluid_tests_qty_jar': True}),
    'sampling_jar': type_integer_coerce_dict,
    'pcb_vial': type_boolean_coerce_dict,
    'antioxidant': type_boolean_coerce_dict,
    'qty_vial': dict_copy_union(type_integer_coerce_dict, {'fluid_tests_qty_vial': True}),
    'sampling_vial': type_integer_coerce_dict,
}
test_result_schema = {
    'id': readonly_dict,
    'campaign_id': type_integer_coerce_required_dict,
    'test_reason_id': type_integer_coerce_dict,
    'date_analyse': type_datetime_dict,
    'test_type_id': type_integer_coerce_dict,
    'sampling_point_id': type_integer_coerce_dict,
    'test_status_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_dict,
    'fluid_profile_id': type_integer_coerce_dict,
    'electrical_profile_id': type_integer_coerce_dict,
    'test_recommendation_id': type_integer_coerce_dict,
    'percent_ratio': type_boolean_coerce_dict,
    'analysis_number': readonly_dict,
    'performed_by_id': type_integer_coerce_dict,
    'lab_id': type_integer_coerce_dict,
    'material_id': type_integer_coerce_dict,
    'fluid_type_id': type_integer_coerce_dict,
    'lab_contract_id': type_integer_coerce_dict,
    'seringe_num': type_string_maxlength_50_dict,
    'mws': type_float_coerce_dict,
    'temperature': type_float_coerce_dict,
    'containers': type_float_coerce_dict,
    'transmission': type_boolean_coerce_dict,
    'charge': type_float_coerce_dict,
    'remark': type_string_dict,
    'modifier': type_boolean_coerce_dict,
    'repair_date': type_datetime_dict,
    'repair_description': type_string_dict,
    'ambient_air_temperature': type_float_coerce_dict,
    'bushing': type_boolean_coerce_dict,
    'winding': type_boolean_coerce_dict,
    'insulation_pf': type_boolean_coerce_dict,
    'insulation': type_boolean_coerce_dict,
    'visual_inspection': type_boolean_coerce_dict,
    'resistance': type_boolean_coerce_dict,
    'degree': type_boolean_coerce_dict,
    'turns': type_boolean_coerce_dict,
    'gas': type_boolean_coerce_dict,
    'water': type_boolean_coerce_dict,
    'furans': type_boolean_coerce_dict,
    'inhibitor': type_boolean_coerce_dict,
    'pcb': type_boolean_coerce_dict,
    'qty_ser': dict_copy_union(type_integer_coerce_dict, {'fluid_tests_qty': True}),
    'sampling': type_integer_coerce_dict,
    'dielec': type_boolean_coerce_dict,
    'acidity': type_boolean_coerce_dict,
    'density': type_boolean_coerce_dict,
    'pcb_jar': type_boolean_coerce_dict,
    'inhibitor_jar': type_boolean_coerce_dict,
    'point': type_boolean_coerce_dict,
    'dielec_2': type_boolean_coerce_dict,
    'color': type_boolean_coerce_dict,
    'pf': type_boolean_coerce_dict,
    'particles': type_boolean_coerce_dict,
    'metals': type_boolean_coerce_dict,
    'viscosity': type_boolean_coerce_dict,
    'dielec_d': type_boolean_coerce_dict,
    'ift': type_boolean_coerce_dict,
    'pf_100': type_boolean_coerce_dict,
    'furans_f': type_boolean_coerce_dict,
    'water_w': type_boolean_coerce_dict,
    'corr': type_boolean_coerce_dict,
    'dielec_i': type_boolean_coerce_dict,
    'visual': type_boolean_coerce_dict,
    'qty_jar': dict_copy_union(type_integer_coerce_dict, {'fluid_tests_qty_jar': True}),
    'sampling_jar': type_integer_coerce_dict,
    'pcb_vial': type_boolean_coerce_dict,
    'antioxidant': type_boolean_coerce_dict,
    'qty_vial': dict_copy_union(type_integer_coerce_dict, {'fluid_tests_qty_vial': True}),
    'sampling_vial': type_integer_coerce_dict,
}
test_result_equipment_schema = {
    'campaign_id': type_integer_coerce_required_dict,
    'equipment_id': {'type': ['integer', 'list'], 'schema': type_integer_coerce_dict},
}
role_schema = {
    'id': readonly_dict,
    'name': dict_copy_union(type_string_dict, {'maxlength': 80}),
    'description': type_string_maxlength_255_dict,
}
lab_schema = {
    'id': readonly_dict,
    'code': type_integer_coerce_dict,
    'name': type_string_maxlength_256_dict,
    'analyser': type_string_maxlength_256_dict,
}
material_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'code': type_string_maxlength_50_dict,
}
gas_sensor_schema = {
    'id': readonly_dict,
    'model': type_string_maxlength_50_dict,
    'h2': type_float_coerce_dict,
    'ch4': type_float_coerce_dict,
    'c2h2': type_float_coerce_dict,
    'c2h4': type_float_coerce_dict,
    'c2h6': type_float_coerce_dict,
    'co': type_float_coerce_dict,
    'co2': type_float_coerce_dict,
    'o2': type_float_coerce_dict,
    'n2': type_float_coerce_dict,
    'percent_error': type_float_coerce_dict,
    'ppm_error': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
transformer_schema = {
    'id': readonly_dict,
    'equipment_id': type_integer_coerce_required_dict,
    "windings": type_integer_coerce_dict,
    "phase_number": dict_copy_union(type_string_dict, {'allowed': ['1', '3', '6']}),
    "static_shield1": type_boolean_coerce_dict,
    "static_shield2": type_boolean_coerce_dict,
    "autotransformer": type_boolean_coerce_dict,
    "cooling_type": type_string_maxlength_20_dict,
    "cooling_stages": type_integer_coerce_dict,
    "fluid_volume": type_float_coerce_dict,
    "temperature_rise": type_float_coerce_dict,
    "conservator_type": type_string_maxlength_50_dict,
    "welded_cover": type_boolean_coerce_dict,
    "primary_tension": type_float_coerce_dict,
    "secondary_tension": type_float_coerce_dict,
    "tertiary_tension": type_float_coerce_dict,
    "fourth_tension": type_float_coerce_dict,
    "mvaforced11": type_float_coerce_dict,
    "mvaforced12": type_float_coerce_dict,
    "mvaforced13": type_float_coerce_dict,
    "mvaforced14": type_float_coerce_dict,
    "imp_base1": type_float_coerce_dict,
    "imp_base2": type_float_coerce_dict,
    "imp_base3": type_float_coerce_dict,
    "imp_base4": type_float_coerce_dict,
    "bil1": type_float_coerce_dict,
    "bil2": type_float_coerce_dict,
    "bil3": type_float_coerce_dict,
    "bil4": type_float_coerce_dict,
    "winding_metal1": type_string_maxlength_20_dict,
    "winding_metal2": type_string_maxlength_20_dict,
    "winding_metal3": type_string_maxlength_20_dict,
    "winding_metal4": type_string_maxlength_20_dict,
    "primary_winding_connection": type_integer_coerce_dict,
    "secondary_winding_connection": type_integer_coerce_dict,
    "tertiary_winding_connection": type_integer_coerce_dict,
    "quaternary_winding_connection": type_integer_coerce_dict,
    "bushing_neutral1": type_float_coerce_dict,
    "bushing_neutral2": type_float_coerce_dict,
    "bushing_neutral3": type_float_coerce_dict,
    "bushing_neutral4": type_float_coerce_dict,
    "ltc2": type_float_coerce_dict,
    "ltc3": type_float_coerce_dict,
    "ltc1": type_float_coerce_dict,

}
breaker_schema = {
    'id': readonly_dict,
    'current_rating': type_integer_coerce_6_digits_dict,
    'open': type_boolean_coerce_dict,
    'fluid_type_id': type_integer_coerce_dict,
    'fluid_level_id': type_integer_coerce_dict,
    'interrupting_medium_id': type_integer_coerce_dict,
    'breaker_mechanism_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
tap_changer_schema = {
    'id': readonly_dict,
    'model': type_string_maxlength_50_dict,
    'filter': dict_copy_union(type_string_dict, {'maxlength': 30}),
    'counter': type_integer_coerce_dict,
    'number_of_taps': type_integer_coerce_dict,
    'fluid_type_id': type_integer_coerce_dict,
    'fluid_level_id': type_integer_coerce_dict,
    'interrupting_medium_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
    'tap_set': type_integer_coerce_dict,
}
bushing_schema = {
    'id': readonly_dict,
    'model': type_string_maxlength_50_dict,
    'type': dict_copy_union(type_string_dict, {'allowed': ['phase', 'Neutral']}),
    'kv': type_float_coerce_dict,
    'sealed': type_boolean_coerce_dict,
    'current_rating': type_integer_coerce_dict,
    'fluid_volume': type_float_coerce_dict,
    'bil': type_integer_coerce_8_digits_dict,
    'c1': type_float_coerce_dict,
    'c1pf': type_float_coerce_dict,
    'c2': type_float_coerce_dict,
    'c2pf': type_float_coerce_dict,
    'fluid_type_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
resistance_schema = {
    'id': readonly_dict,
    'neutral_resistance': type_float_coerce_dict,
    'neutral_resistance1': type_float_coerce_dict,
    'neutral_resistance0': type_boolean_coerce_dict,
    'neutral_resistance2': type_float_coerce_dict,
    'neutral_resistance3': type_float_coerce_dict,
    'neutral_resistance_open1': type_boolean_coerce_dict,
    'neutral_resistance_open2': type_boolean_coerce_dict,
    'neutral_resistance_open3': type_float_coerce_dict,
    'kv': type_float_coerce_dict,
    'bil': type_integer_coerce_8_digits_dict,
    'open': type_boolean_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
air_breaker_schema = {
    'id': readonly_dict,
    'current_rating': type_integer_coerce_6_digits_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
capacitor_schema = {
    'id': readonly_dict,
    'kv': type_float_coerce_dict,
    'kvar': type_float_coerce_dict,
    'bil': type_integer_coerce_8_digits_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
powersource_schema = {
    'id': readonly_dict,
    'kv': type_float_coerce_dict,
    'threephase': type_boolean_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
switchgear_schema = {
    'id': readonly_dict,
    'current_rating': type_integer_coerce_6_digits_dict,
    'insulation_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
induction_machine_schema = {
    'id': readonly_dict,
    'current_rating': type_integer_coerce_6_digits_dict,
    'hp': type_string_maxlength_50_dict,
    'kva': type_string_maxlength_50_dict,
    'pf': type_string_maxlength_50_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
synchronous_machine_schema = {
    'id': readonly_dict,
    'current_rating': type_integer_coerce_6_digits_dict,
    'hp': type_string_maxlength_50_dict,
    'kw': type_string_maxlength_50_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
rectifier_schema = {
    'id': readonly_dict,
    'fluid_volume': type_float_coerce_dict,
    'sealed': type_boolean_coerce_dict,
    'windings': type_integer_coerce_dict,
    'welded_cover': type_boolean_coerce_dict,
    'cooling_rating': type_integer_coerce_dict,
    'fluid_type_id': type_integer_coerce_dict,
    'fluid_level_id': type_integer_coerce_dict,
    'gas_sensor_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
inductance_schema = {
    'id': readonly_dict,
    'fluid_volume': type_float_coerce_dict,
    'sealed': type_boolean_coerce_dict,
    'welded_cover': type_boolean_coerce_dict,
    'cooling_rating': type_integer_coerce_dict,
    'fluid_type_id': type_integer_coerce_dict,
    'fluid_level_id': type_integer_coerce_dict,
    'gas_sensor_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
tank_schema = {
    'id': readonly_dict,
    'welded_cover': type_boolean_coerce_dict,
    'fluid_type_id': type_integer_coerce_dict,
    'fluid_level_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
switch_schema = {
    'id': readonly_dict,
    'current_rating': type_integer_coerce_6_digits_dict,
    'threephase': type_boolean_coerce_dict,
    'interrupting_medium_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
    'open': type_boolean_coerce_dict,
}
cable_schema = {
    'id': readonly_dict,
    'model': type_string_maxlength_50_dict,
    'sealed': type_boolean_coerce_dict,
    'threephase': type_boolean_coerce_dict,
    'insulation_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
recommendation_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_required_dict,
    'code': type_string_maxlength_50_dict,
    'description': type_string_dict,
    'test_type_id': type_integer_coerce_required_dict,
}
test_recommendation_schema = {
    'id': readonly_dict,
    'recommendation_id': type_integer_coerce_dict,
    'recommendation_notes': type_string_dict,
    'user_id': type_integer_coerce_dict,
    'date_created': type_integer_coerce_dict,
    'date_updated': type_integer_coerce_dict,
    'test_result_id': type_integer_coerce_dict,
    'test_type_id': type_integer_coerce_dict,
}
syringe_schema = {
    'id': readonly_dict,
    'serial': type_string_maxlength_50_required_dict,
    'lab_id': type_integer_coerce_dict,
}
test_status_schema = campaign_status_schema = {
    'id': readonly_dict,
    'code': type_string_maxlength_50_dict,
    'name': type_string_maxlength_50_dict,
}
schedule_schema = {
    'id': readonly_dict,
    'date_start': type_datetime_required_dict,
    'period_years': type_integer_coerce_dict,
    'period_months': type_integer_coerce_dict,
    'period_days': type_integer_coerce_dict,
    'assigned_to_id': type_integer_coerce_required_dict,
    'recurring': type_boolean_coerce_dict,
    'notify_before_in_days': type_integer_coerce_dict,
    'description': type_string_dict,
    'test_recommendation_id': type_integer_coerce_required_dict,
    'priority': type_integer_coerce_required_dict,
    'date_updated': type_datetime_dict,
    'date_created': type_datetime_dict,
    'status_id': type_integer_coerce_dict,
    'parent_id': type_integer_coerce_dict,
}
test_type_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_required_dict,
    'group_id': type_integer_coerce_dict,
    'is_group': dict_copy_union(type_boolean_coerce_dict, required_dict),
    'test_table_name': type_string_maxlength_100_dict,
}
bushing_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'h1': type_float_coerce_dict,
    'h2': type_float_coerce_dict,
    'h3': type_float_coerce_dict,
    'hn': type_float_coerce_dict,
    'h1c1': type_float_coerce_dict,
    'h2c1': type_float_coerce_dict,
    'h3c1': type_float_coerce_dict,
    'hnc1': type_float_coerce_dict,
    'h1c2': type_float_coerce_dict,
    'h2c2': type_float_coerce_dict,
    'h3c2': type_float_coerce_dict,
    'hnc2': type_float_coerce_dict,
    'x1': type_float_coerce_dict,
    'x2': type_float_coerce_dict,
    'x3': type_float_coerce_dict,
    'xn': type_float_coerce_dict,
    'x1c1': type_float_coerce_dict,
    'x2c1': type_float_coerce_dict,
    'x3c1': type_float_coerce_dict,
    'xnc1': type_float_coerce_dict,
    'x1c2': type_float_coerce_dict,
    'x2c2': type_float_coerce_dict,
    'x3c2': type_float_coerce_dict,
    'xnc2': type_float_coerce_dict,
    't1': type_float_coerce_dict,
    't2': type_float_coerce_dict,
    't3': type_float_coerce_dict,
    'tn': type_float_coerce_dict,
    't1c1': type_float_coerce_dict,
    't2c1': type_float_coerce_dict,
    't3c1': type_float_coerce_dict,
    'tnc1': type_float_coerce_dict,
    't1c2': type_float_coerce_dict,
    't2c2': type_float_coerce_dict,
    't3c2': type_float_coerce_dict,
    'tnc2': type_float_coerce_dict,
    'temperature': type_float_coerce_dict,
    'facteur': type_float_coerce_dict,
    'facteur1': type_float_coerce_dict,
    'facteur2': type_float_coerce_dict,
    'q1': type_float_coerce_dict,
    'q2': type_float_coerce_dict,
    'q3': type_float_coerce_dict,
    'qn': type_float_coerce_dict,
    'q1c1': type_float_coerce_dict,
    'q2c1': type_float_coerce_dict,
    'q3c1': type_float_coerce_dict,
    'qnc1': type_float_coerce_dict,
    'q1c2': type_float_coerce_dict,
    'q2c2': type_float_coerce_dict,
    'q3c2': type_float_coerce_dict,
    'qnc2': type_float_coerce_dict,
    'facteur3': type_float_coerce_dict,
    'humidity': type_float_coerce_dict,
    'test_kv_h1': type_float_coerce_dict,
    'test_kv_h2': type_float_coerce_dict,
    'test_kv_h3': type_float_coerce_dict,
    'test_kv_hn': type_float_coerce_dict,
    'test_kv_x1': type_float_coerce_dict,
    'test_kv_x2': type_float_coerce_dict,
    'test_kv_x3': type_float_coerce_dict,
    'test_kv_xn': type_float_coerce_dict,
    'test_kv_t1': type_float_coerce_dict,
    'test_kv_t2': type_float_coerce_dict,
    'test_kv_t3': type_float_coerce_dict,
    'test_kv_tn': type_float_coerce_dict,
    'test_kv_q1': type_float_coerce_dict,
    'test_kv_q2': type_float_coerce_dict,
    'test_kv_q3': type_float_coerce_dict,
    'test_kv_qn': type_float_coerce_dict,
    'test_pfc2_h1': type_float_coerce_dict,
    'test_pfc2_h2': type_float_coerce_dict,
    'test_pfc2_h3': type_float_coerce_dict,
    'test_pfc2_hn': type_float_coerce_dict,
    'test_pfc2_x1': type_float_coerce_dict,
    'test_pfc2_x2': type_float_coerce_dict,
    'test_pfc2_x3': type_float_coerce_dict,
    'test_pfc2_xn': type_float_coerce_dict,
    'test_pfc2_t1': type_float_coerce_dict,
    'test_pfc2_t2': type_float_coerce_dict,
    'test_pfc2_t3': type_float_coerce_dict,
    'test_pfc2_tn': type_float_coerce_dict,
    'test_pfc2_q1': type_float_coerce_dict,
    'test_pfc2_q2': type_float_coerce_dict,
    'test_pfc2_q3': type_float_coerce_dict,
    'test_pfc2_qn': type_float_coerce_dict,
    'facteurn': type_float_coerce_dict,
    'facteurn1': type_float_coerce_dict,
    'facteurn2': type_float_coerce_dict,
    'facteurn3': type_float_coerce_dict,
}
winding_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'test_kv1': type_float_coerce_dict,
    'test_kv2': type_float_coerce_dict,
    'test_kv3': type_float_coerce_dict,
    'test_kv4': type_float_coerce_dict,
    'test_kv5': type_float_coerce_dict,
    'test_kv6': type_float_coerce_dict,
    'test_kv7': type_float_coerce_dict,
    'test_kv8': type_float_coerce_dict,
    'test_kv9': type_float_coerce_dict,
    'test_kv10': type_float_coerce_dict,
    'm_meter1': type_float_coerce_dict,
    'm_meter2': type_float_coerce_dict,
    'm_meter3': type_float_coerce_dict,
    'm_meter4': type_float_coerce_dict,
    'm_meter5': type_float_coerce_dict,
    'm_meter6': type_float_coerce_dict,
    'm_meter7': type_float_coerce_dict,
    'm_meter8': type_float_coerce_dict,
    'm_meter9': type_float_coerce_dict,
    'm_meter10': type_float_coerce_dict,
    'm_multiplier1': type_float_coerce_dict,
    'm_multiplier2': type_float_coerce_dict,
    'm_multiplier3': type_float_coerce_dict,
    'm_multiplier4': type_float_coerce_dict,
    'm_multiplier5': type_float_coerce_dict,
    'm_multiplier6': type_float_coerce_dict,
    'm_multiplier7': type_float_coerce_dict,
    'm_multiplier8': type_float_coerce_dict,
    'm_multiplier9': type_float_coerce_dict,
    'm_multiplier10': type_float_coerce_dict,
    'w_meter1': type_float_coerce_dict,
    'w_meter2': type_float_coerce_dict,
    'w_meter3': type_float_coerce_dict,
    'w_meter4': type_float_coerce_dict,
    'w_meter5': type_float_coerce_dict,
    'w_meter6': type_float_coerce_dict,
    'w_meter7': type_float_coerce_dict,
    'w_meter8': type_float_coerce_dict,
    'w_meter9': type_float_coerce_dict,
    'w_meter10': type_float_coerce_dict,
    'w_multiplier1': type_float_coerce_dict,
    'w_multiplier2': type_float_coerce_dict,
    'w_multiplier3': type_float_coerce_dict,
    'w_multiplier4': type_float_coerce_dict,
    'w_multiplier5': type_float_coerce_dict,
    'w_multiplier6': type_float_coerce_dict,
    'w_multiplier7': type_float_coerce_dict,
    'w_multiplier8': type_float_coerce_dict,
    'w_multiplier9': type_float_coerce_dict,
    'w_multiplier10': type_float_coerce_dict,
    'type_doble': type_boolean_coerce_dict,
    'humidity': type_float_coerce_dict,
}
visual_inspection_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'notes': dict_copy_union(type_string_dict, {'maxlength': 1000}),
    'tank_cover_gasket_id': type_integer_coerce_dict,
    'tank_manhole_gasket_id': type_integer_coerce_dict,
    'tank_gas_relay_id': type_integer_coerce_dict,
    'tank_oil_level_id': type_integer_coerce_dict,
    'tank_winding_temp_max': type_float_coerce_dict,
    'tank_winding_temp_actual': type_float_coerce_dict,
    'tank_oil_temp_max': type_float_coerce_dict,
    'tank_oil_temp_actual': type_float_coerce_dict,
    'tank_winding_flag': type_boolean_coerce_dict,
    'tank_oil_flag': type_boolean_coerce_dict,
    'tank_pressure_unit_id': type_integer_coerce_dict,
    'tank_pressure': type_float_coerce_dict,
    'tank_overpressure_valve_id': type_integer_coerce_dict,
    'tank_sampling_valve_id': type_integer_coerce_dict,
    'tank_oil_pump_id': type_integer_coerce_dict,
    'tank_gas_analyser': type_float_coerce_dict,
    'tank_overall_condition_id': type_integer_coerce_dict,
    'exp_tank_pipe_gasket_id': type_integer_coerce_dict,
    'exp_tank_oil_level_id': type_integer_coerce_dict,
    'exp_tank_paint_id': type_integer_coerce_dict,
    'exp_tank_overall_condition_id': type_integer_coerce_dict,
    'bushing_gasket_id': type_integer_coerce_dict,
    'bushing_oil_level_id': type_integer_coerce_dict,
    'bushing_overall_condition_id': type_integer_coerce_dict,
    'tap_changer_gasket_id': type_integer_coerce_dict,
    'tap_changer_oil_level_id': type_integer_coerce_dict,
    'tap_changer_temp_max': type_float_coerce_dict,
    'tap_changer_temp_actual': type_float_coerce_dict,
    'tap_changer_pressure_max': type_float_coerce_dict,
    'tap_changer_pressure_actual': type_float_coerce_dict,
    'tap_changer_pressure_unit_id': type_integer_coerce_dict,
    'tap_changer_tap_position': type_float_coerce_dict,
    'tap_changer_overpressure_valve_id': type_integer_coerce_dict,
    'tap_changer_sampling_valve_id': type_integer_coerce_dict,
    'tap_changer_operation_counter': type_integer_coerce_dict,
    'tap_changer_counter_id': type_integer_coerce_dict,
    'tap_changer_filter_id': type_integer_coerce_dict,
    'tap_changer_overall_condition_id': type_integer_coerce_dict,
    'radiator_fan_id': type_integer_coerce_dict,
    'radiator_gasket_id': type_integer_coerce_dict,
    'radiator_overall_condition_id': type_integer_coerce_dict,
    'control_cab_connection_id': type_integer_coerce_dict,
    'control_cab_heating_id': type_integer_coerce_dict,
    'control_cab_overall_condition_id': type_integer_coerce_dict,
    'grounding_value': type_float_coerce_dict,
    'grounding_connection_id': type_integer_coerce_dict,
    'misc_foundation_id': type_integer_coerce_dict,
    'misc_temp_ambiant': type_float_coerce_dict,
    'misc_load': type_float_coerce_dict,
}
insulation_resistance_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'test_kv1': type_float_coerce_dict,
    'resistance1': type_float_coerce_dict,
    'multiplier1': type_float_coerce_dict,
    'test_kv2': type_float_coerce_dict,
    'resistance2': type_float_coerce_dict,
    'multiplier2': type_float_coerce_dict,
    'test_kv3': type_float_coerce_dict,
    'resistance3': type_float_coerce_dict,
    'multiplier3': type_float_coerce_dict,
    'test_kv4': type_float_coerce_dict,
    'resistance4': type_float_coerce_dict,
    'multiplier4': type_float_coerce_dict,
    'test_kv5': type_float_coerce_dict,
    'resistance5': type_float_coerce_dict,
    'multiplier5': type_float_coerce_dict,
}
polymerisation_degree_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'phase_a1': type_float_coerce_dict,
    'phase_a2': type_float_coerce_dict,
    'phase_a3': type_float_coerce_dict,
    'phase_b1': type_float_coerce_dict,
    'phase_b2': type_float_coerce_dict,
    'phase_b3': type_float_coerce_dict,
    'phase_c1': type_float_coerce_dict,
    'phase_c2': type_float_coerce_dict,
    'phase_c3': type_float_coerce_dict,
    'lead_a': type_integer_coerce_4_digits_dict,
    'lead_b': type_integer_coerce_4_digits_dict,
    'lead_c': type_integer_coerce_4_digits_dict,
    'lead_n': type_integer_coerce_4_digits_dict,
    'winding': type_integer_coerce_4_digits_dict,
}
transformer_turn_ratio_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'winding': type_integer_coerce_required_dict,
    'tap_position': type_integer_coerce_dict,
    'measured_current1': type_float_coerce_dict,
    'measured_current2': type_float_coerce_dict,
    'measured_current3': type_float_coerce_dict,
    'calculated_current1': type_float_coerce_dict,
    'calculated_current2': type_float_coerce_dict,
    'calculated_current3': type_float_coerce_dict,
    'error1': type_float_coerce_dict,
    'error2': type_float_coerce_dict,
    'error3': type_float_coerce_dict,
    'ratio': type_float_coerce_dict,
    'select': type_boolean_coerce_dict,
}
winding_resistance_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'winding': type_integer_coerce_required_dict,
    'tap_position': type_integer_coerce_dict,
    'mesure1': type_float_coerce_dict,
    'temp1': type_float_coerce_dict,
    'corr1': type_float_coerce_dict,
    'mesure2': type_float_coerce_dict,
    'temp2': type_float_coerce_dict,
    'corr2': type_float_coerce_dict,
    'mesure3': type_float_coerce_dict,
    'temp3': type_float_coerce_dict,
    'corr3': type_float_coerce_dict,
}
dissolved_gas_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'h2': type_float_coerce_dict,
    'o2': type_float_coerce_dict,
    'n2': type_float_coerce_dict,
    'co': type_float_coerce_dict,
    'ch4': type_float_coerce_dict,
    'co2': type_float_coerce_dict,
    'c2h2': type_float_coerce_dict,
    'c2h4': type_float_coerce_dict,
    'c2h6': type_float_coerce_dict,
    'h2_flag': type_boolean_coerce_dict,
    'o2_flag': type_boolean_coerce_dict,
    'n2_flag': type_boolean_coerce_dict,
    'co_flag': type_boolean_coerce_dict,
    'ch4_flag': type_boolean_coerce_dict,
    'co2_flag': type_boolean_coerce_dict,
    'c2h2_flag': type_boolean_coerce_dict,
    'c2h4_flag': type_boolean_coerce_dict,
    'c2h6_flag': type_boolean_coerce_dict,
    'cap_gaz': type_float_coerce_dict,
    'content_gaz': type_float_coerce_dict,
}
water_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'water_flag': type_boolean_coerce_dict,
    'water': type_float_coerce_dict,
    'remark': type_string_maxlength_80_dict,
}
furan_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'hmf': type_float_coerce_dict,
    'fol': type_float_coerce_dict,
    'fal': type_float_coerce_dict,
    'acf': type_float_coerce_dict,
    'mef': type_float_coerce_dict,
    'hmf_flag': type_boolean_coerce_dict,
    'fol_flag': type_boolean_coerce_dict,
    'fal_flag': type_boolean_coerce_dict,
    'acf_flag': type_boolean_coerce_dict,
    'mef_flag': type_boolean_coerce_dict,
}
inhibitor_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'inhibitor_type_id': type_integer_coerce_dict,
    'inhibitor': type_float_coerce_dict,
    'remark': type_string_maxlength_80_dict,
    'inhibitor_flag': type_boolean_coerce_dict,
}
inhibitor_type_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_10_dict,
}
pcb_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'aroclor_1242': type_float_coerce_dict,
    'aroclor_1254': type_float_coerce_dict,
    'aroclor_1260': type_float_coerce_dict,
    'aroclor_1242_flag': type_boolean_coerce_dict,
    'aroclor_1254_flag': type_boolean_coerce_dict,
    'aroclor_1260_flag': type_boolean_coerce_dict,
    'pcb_total': type_float_coerce_dict,
    'total_flag': type_boolean_coerce_dict,
}
particle_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    '_2um': type_float_coerce_dict,
    '_5um': type_float_coerce_dict,
    '_10um': type_float_coerce_dict,
    '_15um': type_float_coerce_dict,
    '_25um': type_float_coerce_dict,
    '_50um': type_float_coerce_dict,
    '_100um': type_float_coerce_dict,
    'nas1638': type_float_coerce_dict,
    'iso4406_1': type_float_coerce_dict,
    'iso4406_2': type_float_coerce_dict,
    'iso4406_3': type_float_coerce_dict,
}
metals_in_oil_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'iron': type_float_coerce_dict,
    'nickel': type_float_coerce_dict,
    'aluminium': type_float_coerce_dict,
    'copper': type_float_coerce_dict,
    'tin': type_float_coerce_dict,
    'silver': type_float_coerce_dict,
    'lead': type_float_coerce_dict,
    'zinc': type_float_coerce_dict,
    'arsenic': type_float_coerce_dict,
    'cadmium': type_float_coerce_dict,
    'chrome': type_float_coerce_dict,
    'iron_flag': type_boolean_coerce_dict,
    'nickel_flag': type_boolean_coerce_dict,
    'aluminium_flag': type_boolean_coerce_dict,
    'copper_flag': type_boolean_coerce_dict,
    'tin_flag': type_boolean_coerce_dict,
    'silver_flag': type_boolean_coerce_dict,
    'lead_flag': type_boolean_coerce_dict,
    'zinc_flag': type_boolean_coerce_dict,
    'arsenic_flag': type_boolean_coerce_dict,
    'cadmium_flag': type_boolean_coerce_dict,
    'chrome_flag': type_boolean_coerce_dict,
}
fluid_test_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'dielectric_1816': type_float_coerce_dict,
    'dielectric_1816_2': type_float_coerce_dict,
    'dielectric_877': type_float_coerce_dict,
    'dielectric_iec_156': type_float_coerce_dict,
    'acidity': type_float_coerce_dict,
    'color': type_float_coerce_dict,
    'ift': type_float_coerce_dict,
    'visual': type_string_maxlength_25_dict,
    'density': type_float_coerce_dict,
    'pf20c': type_float_coerce_dict,
    'pf100c': type_float_coerce_dict,
    'sludge': type_float_coerce_dict,
    'aniline_point': type_float_coerce_dict,
    'corrosive_sulfur': type_string_maxlength_25_dict,
    'viscosity': type_float_coerce_dict,
    'flash_point': type_float_coerce_dict,
    'pour_point': type_float_coerce_dict,
    'dielectric_1816_flag': type_boolean_coerce_dict,
    'dielectric_1816_2_flag': type_boolean_coerce_dict,
    'dielectric_877_flag': type_boolean_coerce_dict,
    'dielectric_iec_156_flag': type_boolean_coerce_dict,
}
# test_result_transformer_turn_ratio_test_schema = {
#     'type': 'list', 'schema': {'type': 'dict', 'schema': transformer_turn_ratio_test_schema},
# }
# test_result_winding_test_schema = {
#     'type': 'list', 'schema': {'type': 'dict', 'schema': winding_test_schema},
# }
# test_result_winding_resistance_test_schema = {
#     'type': 'list', 'schema': {'type': 'dict', 'schema': winding_resistance_test_schema},
# }
norm_physic_schema = {
    'id': readonly_dict,
    'name': dict_copy_union(type_string_maxlength_20_dict, required_dict),
    'equipment_id': type_integer_coerce_required_dict,
    'acid_min': type_float_coerce_dict,
    'acid_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'acid_min'}),
    'ift_min': type_float_coerce_dict,
    'ift_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'ift_min'}),
    'd1816_min': type_float_coerce_dict,
    'd1816_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'd1816_min'}),
    'd877_min': type_float_coerce_dict,
    'd877_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'd877_min'}),
    'color_min': type_float_coerce_dict,
    'color_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'color_min'}),
    'density_min': type_float_coerce_dict,
    'density_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'density_min'}),
    'pf20_min': type_float_coerce_dict,
    'pf20_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'pf20_min'}),
    'water_min': type_float_coerce_dict,
    'water_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'water_min'}),
    'flashpoint_min': type_float_coerce_dict,
    'flashpoint_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'flashpoint_min'}),
    'pourpoint_min': type_float_coerce_dict,
    'pourpoint_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'pourpoint_min'}),
    'viscosity_min': type_float_coerce_dict,
    'viscosity_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'viscosity_min'}),
    'd1816_2_min': type_float_coerce_dict,
    'd1816_2_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'd1816_2_min'}),
    'p100_min': type_float_coerce_dict,
    'p100_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'p100_min'}),
    'fluid_type_id': type_integer_coerce_dict,
    'cei156_min': type_integer_coerce_dict,
    'cei156_max': dict_copy_union(type_integer_coerce_dict, {'more_then': 'cei156_min'}),
}
norm_gas_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'condition': type_integer_coerce_dict,
    'h2': type_float_coerce_dict,
    'ch4': type_float_coerce_dict,
    'c2h2': type_float_coerce_dict,
    'c2h4': type_float_coerce_dict,
    'c2h6': type_float_coerce_dict,
    'co': type_float_coerce_dict,
    'co2': type_float_coerce_dict,
    'tdcg': type_float_coerce_dict,
    'fluid_level': dict_copy_union(type_integer_coerce_dict, {'norm_gas_fluid_level': True}),
}
particles_schema = {
    'id': readonly_dict,
    'equipment_id': type_integer_coerce_dict,
    '_2um': type_float_coerce_dict,
    '_5um': type_float_coerce_dict,
    '_10um': type_float_coerce_dict,
    '_15um': type_float_coerce_dict,
    '_25um': type_float_coerce_dict,
    '_50um': type_float_coerce_dict,
    '_100um': type_float_coerce_dict,
    'nas1638': type_float_coerce_dict,
    'iso4406_1': type_float_coerce_dict,
    'iso4406_2': type_float_coerce_dict,
    'iso4406_3': type_float_coerce_dict,
}
norm_isolation_schema = {
    'id': readonly_dict,
    'c': type_float_coerce_dict,
    'f': type_float_coerce_dict,
    'notseal': type_float_coerce_dict,
    'seal': type_float_coerce_dict,
}
norm_furan_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'c1': type_float_coerce_dict,
    'c2': type_float_coerce_dict,
    'c3': type_float_coerce_dict,
    'c4': type_float_coerce_dict,
}
test_sampling_card_schema = {
    'id': readonly_dict,
    'test_result_id': type_integer_coerce_dict,
    'date_created': type_datetime_dict,
    'printed': type_boolean_coerce_dict,
}
tree_schema = {
    'id': readonly_dict,
    'parent_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
    'icon': type_string_maxlength_126_dict,
    'opened': type_boolean_coerce_dict,
    'disabled': type_boolean_coerce_dict,
    'selected': type_boolean_coerce_dict,
    'type': dict_copy_union(type_string_dict, {'maxlength': 58}),
    'view': type_string_maxlength_126_dict,
    'status': type_integer_coerce_dict,
}
tree_translation_schema = {
    'id': readonly_dict,
    'locale': type_string_maxlength_10_dict,
    'text': type_string_maxlength_250_dict,
    'tooltip': type_string_maxlength_250_dict,
}
test_repair_note_schema = {
    'id': readonly_dict,
    'description': type_string_dict,
    'remark': type_string_dict,
    'sample': type_string_dict,
    'date_created': type_datetime_dict,
    'user_id': type_integer_coerce_dict,
    'test_result_id': type_integer_coerce_dict,
    'test_type_id': type_integer_coerce_dict
}
diagnosis_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'code': type_string_maxlength_50_dict,
    'description': type_string_dict,
    'test_type_id': type_integer_coerce_dict
}
test_diagnosis_schema = {
    'id': readonly_dict,
    'diagnosis_notes': type_string_dict,
    'date_created': type_datetime_dict,
    'date_updated': type_datetime_dict,
    'diagnosis_id': type_integer_coerce_dict,
    'user_id': type_integer_coerce_dict,
    'test_result_id': type_integer_coerce_dict,
    'test_type_id': type_integer_coerce_dict
}
task_status_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_20_dict
}
norm_physic_data_schema = {
    'id': readonly_dict,
    'name': dict_copy_union(type_string_maxlength_20_dict, required_dict),
    'acid_min': type_float_coerce_dict,
    'acid_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'acid_min'}),
    'ift_min': type_float_coerce_dict,
    'ift_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'ift_min'}),
    'd1816_min': type_float_coerce_dict,
    'd1816_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'd1816_min'}),
    'd877_min': type_float_coerce_dict,
    'd877_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'd877_min'}),
    'color_min': type_float_coerce_dict,
    'color_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'color_min'}),
    'density_min': type_float_coerce_dict,
    'density_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'density_min'}),
    'pf20_min': type_float_coerce_dict,
    'pf20_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'pf20_min'}),
    'water_min': type_float_coerce_dict,
    'water_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'water_min'}),
    'flashpoint_min': type_float_coerce_dict,
    'flashpoint_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'flashpoint_min'}),
    'pourpoint_min': type_float_coerce_dict,
    'pourpoint_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'pourpoint_min'}),
    'viscosity_min': type_float_coerce_dict,
    'viscosity_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'viscosity_min'}),
    'd1816_2_min': type_float_coerce_dict,
    'd1816_2_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'd1816_2_min'}),
    'p100_min': type_float_coerce_dict,
    'p100_max': dict_copy_union(type_float_coerce_dict, {'more_then': 'p100_min'}),
    'fluid_type_id': type_integer_coerce_dict,
    'cei156_min': type_integer_coerce_dict,
    'cei156_max': dict_copy_union(type_integer_coerce_dict, {'more_then': 'cei156_min'}),
    'norm_id': type_integer_coerce_dict,
    'campaign_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
norm_gas_data_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'condition': type_integer_coerce_dict,
    'h2': type_float_coerce_dict,
    'ch4': type_float_coerce_dict,
    'c2h2': type_float_coerce_dict,
    'c2h4': type_float_coerce_dict,
    'c2h6': type_float_coerce_dict,
    'co': type_float_coerce_dict,
    'co2': type_float_coerce_dict,
    'tdcg': type_float_coerce_dict,
    'fluid_level': dict_copy_union(type_integer_coerce_dict, {'norm_gas_fluid_level': True}),
    'norm_id': type_integer_coerce_dict,
    'campaign_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
norm_particles_data_schema = {
    'id': readonly_dict,
    '_2um': type_float_coerce_dict,
    '_5um': type_float_coerce_dict,
    '_10um': type_float_coerce_dict,
    '_15um': type_float_coerce_dict,
    '_25um': type_float_coerce_dict,
    '_50um': type_float_coerce_dict,
    '_100um': type_float_coerce_dict,
    'nas1638': type_float_coerce_dict,
    'iso4406_1': type_float_coerce_dict,
    'iso4406_2': type_float_coerce_dict,
    'iso4406_3': type_float_coerce_dict,
    'name': type_string_maxlength_50_dict,
    'norm_id': type_string_maxlength_50_dict,
    'campaign_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
norm_isolation_data_schema = {
    'id': readonly_dict,
    'c': type_float_coerce_dict,
    'f': type_float_coerce_dict,
    'notseal': type_float_coerce_dict,
    'seal': type_float_coerce_dict,
    'name': type_string_maxlength_50_dict,
    'norm_id': type_integer_coerce_dict,
    'campaign_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
norm_furan_data_schema = {
    'id': readonly_dict,
    'name': type_string_maxlength_50_dict,
    'c1': type_float_coerce_dict,
    'c2': type_float_coerce_dict,
    'c3': type_float_coerce_dict,
    'c4': type_float_coerce_dict,
    'norm_id': type_integer_coerce_dict,
    'campaign_id': type_integer_coerce_dict,
    'equipment_id': type_integer_coerce_required_dict,
}
model_dict = {
    'equipment': {
        'model': Equipment,
        'schema': equipment_schema,
    },
    'equipment_type': {
        'model': EquipmentType,
        'schema': equipment_type_schema
    },
    'campaign': {
        'model': Campaign,
        'schema': campaign_schema,
    },
    'contract': {
        'model': Contract,
        'schema': contract_schema,
    },
    'norm': {
        'model': Norm,
        'schema': norm_schema
    },
    'location': {
        'model': Location,
        'schema': location_schema
    },
    'manufacturer': {
        'model': Manufacturer,
        'schema': manufacturer_schema,
    },
    'user': {
        'model': User,
        'schema': user_schema,
    },
    'assigned_to': {
        'model': User,
        'schema': user_schema
    },
    'visual_inspection_by': {
        'model': User,
        'schema': user_schema
    },
    'electrical_profile': {
        'model': ElectricalProfile,
        'schema': electrical_profile_schema
    },
    'fluid_profile': {
        'model': FluidProfile,
        'schema': fluid_profile_schema
    },
    'test_result': {
        'model': TestResult,
        'schema': test_result_schema,
    },
    'test_result_equipment': {
        'model': TestResult,
        'schema': test_result_equipment_schema
    },
    'role': {
        'model': Role,
        'schema': role_schema
    },
    'lab': {
        'model': Lab,
        'schema': lab_schema
    },
    'contract_status': {
        'model': ContractStatus,
        'schema': contract_status_schema
    },
    'sampling_point': {
        'model': SamplingPoint,
        'schema': sampling_point_schema
    },
    'material': {
        'model': Material,
        'schema': material_schema
    },
    'fluid_type': {
        'model': FluidType,
        'schema': fluid_type_schema
    },
    'gas_sensor': {
        'model': GasSensor,
        'schema': gas_sensor_schema,
    },
    'transformer': {
        'model': Transformer,
        'schema': transformer_schema,
    },
    'breaker': {
        'model': Breaker,
        'schema': breaker_schema,
    },
    'tap_changer': {
        'model': LoadTapChanger,
        'schema': tap_changer_schema
    },
    'bushing': {
        'model': Bushing,
        'schema': bushing_schema,
    },
    'equipment_connection': {
        'model': EquipmentConnection,
        'schema': equipment_connection_schema
    },
    'sibling': {
        'model': Sibling,
        'schema': sibling_schema
    },
    'resistance': {
        'model': NeutralResistance,
        'schema': resistance_schema,
    },
    'air_breaker': {
        'model': AirCircuitBreaker,
        'schema': air_breaker_schema,
    },
    'capacitor': {
        'model': Capacitor,
        'schema': capacitor_schema,
    },
    'powersource': {
        'model': PowerSource,
        'schema': powersource_schema,
    },
    'switchgear': {
        'model': SwitchGear,
        'schema': switchgear_schema,
    },
    'induction_machine': {
        'model': InductionMachine,
        'schema': induction_machine_schema,
    },
    'synchronous_machine': {
        'model': SynchronousMachine,
        'schema': synchronous_machine_schema,
    },
    'rectifier': {
        'model': Rectifier,
        'schema': rectifier_schema,
    },
    'inductance': {
        'model': Inductance,
        'schema': inductance_schema,
    },
    'tank': {
        'model': Tank,
        'schema': tank_schema,
    },
    'switch': {
        'model': Switch,
        'schema': switch_schema,
    },
    'cable': {
        'model': Cable,
        'schema': cable_schema,
    },
    'recommendation': {
        'model': Recommendation,
        'schema': recommendation_schema,
    },
    'test_recommendation': {
        'model': TestRecommendation,
        'schema': test_recommendation_schema
    },
    'gas_level': {
        'model': GasLevel,
        'schema': gas_level_schema
    },
    'interrupting_medium': {
        'model': InterruptingMedium,
        'schema': interrupting_medium_schema
    },
    'breaker_mechanism': {
        'model': BreakerMechanism,
        'schema': breaker_mechanism_schema
    },
    'insulation': {
        'model': Insulation,
        'schema': insulation_schema
    },
    'syringe': {
        'model': Syringe,
        'schema': syringe_schema,
    },
    'test_reason': {
        'model': TestReason,
        'schema': test_reason_schema
    },
    'test_status': {
        'model': TestStatus,
        'schema': test_status_schema
    },
    'campaign_status': {
        'model': CampaignStatus,
        'schema': campaign_status_schema
    },
    'schedule': {
        'model': TestSchedule,
        'schema': schedule_schema,
    },
    'test_type': {
        'model': TestType,
        'schema': test_type_schema,
    },
    'gasket_condition': {
        'model': GasketCondition,
        'schema': gasket_condition_schema
    },
    'gas_relay': {
        'model': GasRelay,
        'schema': gas_relay_schema
    },
    'fluid_level': {
        'model': FluidLevel,
        'schema': fluid_level_schema
    },
    'pressure_unit': {
        'model': PressureUnit,
        'schema': pressure_unit_schema
    },
    'valve_condition': {
        'model': ValveCondition,
        'schema': valve_condition_schema
    },
    'pump_condition': {
        'model': PumpCondition,
        'schema': pump_condition_schema
    },
    'overall_condition': {
        'model': OverallCondition,
        'schema': overall_condition_schema
    },
    'paint_types': {
        'model': PaintTypes,
        'schema': paint_types_schema
    },
    'tap_counter_status': {
        'model': TapCounterStatus,
        'schema': tap_counter_status_schema
    },
    'tap_filter_condition': {
        'model': TapFilterCondition,
        'schema': tap_filter_condition_schema
    },
    'fan_condition': {
        'model': FanCondition,
        'schema': fan_condition_schema
    },
    'connection_condition': {
        'model': ConnectionCondition,
        'schema': connection_condition_schema
    },
    'foundation_condition': {
        'model': FoundationCondition,
        'schema': foundation_condition_schema
    },
    'heating_condition': {
        'model': HeatingCondition,
        'schema': heating_condition_schema
    },
    'bushing_test': {
        'model': BushingTest,
        'schema': bushing_test_schema
    },
    'winding_test': {
        'model': WindingTest,
        'schema': winding_test_schema
    },
    'visual_inspection_test': {
        'model': VisualInspectionTest,
        'schema': visual_inspection_test_schema
    },
    'insulation_resistance_test': {
        'model': InsulationResistanceTest,
        'schema': insulation_resistance_test_schema
    },
    'polymerisation_degree_test': {
        'model': PolymerisationDegreeTest,
        'schema': polymerisation_degree_test_schema
    },
    'transformer_turn_ratio_test': {
        'model': TransformerTurnRatioTest,
        'schema': transformer_turn_ratio_test_schema,
    },
    'winding_resistance_test': {
        'model': WindingResistanceTest,
        'schema': winding_resistance_test_schema,
    },
    'dissolved_gas_test': {
        'model': DissolvedGasTest,
        'schema': dissolved_gas_test_schema
    },
    'water_test': {
        'model': WaterTest,
        'schema': water_test_schema
    },
    'furan_test': {
        'model': FuranTest,
        'schema': furan_test_schema
    },
    'inhibitor_test': {
        'model': InhibitorTest,
        'schema': inhibitor_test_schema
    },
    'inhibitor_type': {
        'model': InhibitorType,
        'schema': inhibitor_type_schema
    },
    'pcb_test': {
        'model': PCBTest,
        'schema': pcb_test_schema
    },
    'particle_test': {
        'model': ParticleTest,
        'schema': particle_test_schema
    },
    'metals_in_oil_test': {
        'model': MetalsInOilTest,
        'schema': metals_in_oil_test_schema
    },
    'fluid_test': {
        'model': FluidTest,
        'schema': fluid_test_schema
    },
    'norm_physic': {
        'model': NormPhysic,
        'schema': norm_physic_schema,
    },
    'norm_gas': {
        'model': NormGas,
        'schema': norm_gas_schema
    },
    'particles': {
        'model': NormParticles,
        'schema': particles_schema
    },
    'norm_isolation': {
        'model': NormIsolation,
        'schema': norm_isolation_schema
    },
    'norm_furan': {
        'model': NormFuran,
        'schema': norm_furan_schema
    },
    # 'sampling_card': {
    #     'model': SamplingCard,
    #     'schema': sampling_card_schema,
    # },
    'test_sampling_card': {
        'model': TestSamplingCard,
        'schema': test_sampling_card_schema
    },
    'country': {
        'model': Country,
        'schema': country_schema
    },
    'tree': {
        'model': Tree,
        'schema': tree_schema,
    },
    'tree_translation': {
        'model': TreeTranslation,
        'schema': tree_translation_schema
    },
    'test_repair_note': {
        'model': TestRepairNote,
        'schema': test_repair_note_schema
    },
    'diagnosis': {
        'model': Diagnosis,
        'schema': diagnosis_schema
    },
    'test_diagnosis': {
        'model': TestDiagnosis,
        'schema': test_diagnosis_schema
    },
    'task_status': {
        'model': TaskStatus,
        'schema': task_status_schema
    },
    # 'test_result_winding_test': {
    #     'model': WindingTest,
    #     'schema': test_result_winding_test_schema
    # },
    # 'test_result_transformer_turn_ratio_test': {
    #     'model': TransformerTurnRatioTest,
    #     'schema': test_result_transformer_turn_ratio_test_schema
    # },
    # 'test_result_winding_resistance_test': {
    #     'model': WindingResistanceTest,
    #     'schema': test_result_winding_resistance_test_schema
    # },
    'norm_physic_data': {
        'model': NormPhysicData,
        'schema': norm_physic_data_schema,
    },
    'norm_gas_data': {
        'model': NormGasData,
        'schema': norm_gas_data_schema
    },
    'norm_particles_data': {
        'model': NormParticlesData,
        'schema': norm_particles_data_schema
    },
    'norm_isolation_data': {
        'model': NormIsolationData,
        'schema': norm_isolation_data_schema
    },
    'norm_furan_data': {
        'model': NormFuranData,
        'schema': norm_furan_data_schema
    },
}

eq_type_dict = {
    1: 'air_bkr',
    2: 'bushing',
    3: 'capacitor',
    4: 'bkr',
    5: 'source',
    6: 'cable',
    # 7: 'Switchgear',
    # 8: 'Induction machine',
    9: 'synch',
    # 10: 'localization'
    11: 'tc',  # tap changer
    12: 'rect',
    # 13: 'site',
    14: 'transfo',
    15: 'tank',
    16: 'switch',
    17: 'induc',
    # 18: 'neutral resistance',
    # 19: 'gas sensor',
}
