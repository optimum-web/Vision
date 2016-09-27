from flask import Flask, Blueprint, jsonify, abort, make_response, request
from flask.ext.sqlalchemy import SQLAlchemy
from api_utility import MyValidator as Validator
from api_utility import model_dict, eq_type_dict
from app.diagnostic.models import EquipmentType, TestResult, Campaign, FluidProfile, Country
from app.diagnostic.models import ElectricalProfile
from app.users.models import User, Role
from collections import Iterable
from sqlalchemy import create_engine, MetaData, or_, and_
from flask.ext.blogging import SQLAStorage
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.security.utils import encrypt_password
from flask.ext import login
from sqlalchemy.orm.session import make_transient

api = Flask(__name__, static_url_path='/app/static')
api.config.from_object('config')
engine = create_engine(api.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(api, session_options={'autoflush': False})
api_blueprint = Blueprint('api_v1_0', __name__, url_prefix='/api/v1.0')
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(api, user_datastore)


# Accessory functions
def return_json(items_name, items_list):
    return jsonify({items_name: items_list})


def set_attrs_to_item(item, attr_dict):
    for k, v in attr_dict.items():
        try:
            setattr(item, k, v)
        except AttributeError:
            abort(500, "can't set attribute - {}: {}".format(k, v))


def get_model_by_path(path):
    return model_dict[path].get('model') or abort(500, 'Model missing')


def get_schema_by_path(path):
    return model_dict[path].get('schema') or abort(500, 'Validation schema missing')


# Returns dict with data for Tree model based on item information
def prepare_data_for_tree(equipment):
    short_name = eq_type_dict.get(equipment.equipment_type_id, '')
    return {
        'equipment_id': equipment.id,
        'parent_id': 32,
        'icon': '../app/static/img/icons/{0}_b.ico'.format(short_name),
        'type': '{0}'.format(short_name)
    }


def prepare_data_for_tree_translation(tree_item_id, equipment_name):
    return {
        'id': tree_item_id,
        'locale': 'en',
        'text': equipment_name,
        'tooltip': equipment_name
        # 'text': param_dict['name'],
        # 'tooltip': param_dict['name']
    }


# Verifications
def validate_or_abort(path, data_to_validate=None, update=False, context=None):
    if not data_to_validate:
        data_to_validate = request.json
    v = Validator(ignore_none_values=True)
    if not v.validate(data_to_validate, get_schema_by_path(path), update, context):
        abort(400, v.errors)
    return v.document


def abort_if_json_missing():
    if not request.json:
        abort(400, 'JSON not found')


def abort_if_wrong_path(path):
    if path not in model_dict:
        abort(404)


def abort_if_wrong_id(item_id):
    if not item_id:
        abort(404)


# Standard CRUD functions
# Create
def add_item(path, data):
    items_model = get_model_by_path(path)
    item = items_model()
    set_attrs_to_item(item, data)
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        abort(500, e.args)

    return item


# Read
def get_item(path, item_id):
    items_model = get_model_by_path(path)
    item = db.session.query(items_model).get(item_id) or abort(404)
    return item.serialize()


def get_items(path, args):
    items_model = get_model_by_path(path)
    if args:
        kwargs = {
            k: v for k,v in args.items() if hasattr(items_model, k)
                 or abort(400, 'Wrong attribute: {}'.format(k))
        }
        if items_model == Campaign and 'equipment_id' in kwargs:
            campaing_ids = {item.campaign_id for item in db.session.query(TestResult).filter_by(**kwargs)}
            return [item.serialize() for item in db.session.query(Campaign).filter(Campaign.id.in_(campaing_ids))]

        return [item.serialize() for item in db.session.query(items_model).filter_by(**kwargs)]
    return [item.serialize() for item in db.session.query(items_model).all()]


# Update
def update_item(path, item_id, data):
    item = db.session.query(get_model_by_path(path)).get(item_id)
    set_attrs_to_item(item, data)
    try:
        db.session.commit()
    except Exception as e:
        abort(500, e.args)

    return item


# Delete
def delete_item(path, item_id):
    items_model = get_model_by_path(path)
    try:
        rows = db.session.query(items_model).filter(items_model.id == item_id).delete(synchronize_session=False)
    except:
        return False
    else:
        db.session.commit()
        return rows > 0


# Custom CRUD functions
# Add equipment and add related objects automaticaly
def add_equipment(path, data):
    extra_fields_dict = data.pop('extra_fields', {})
    item = add_item(path, data)

    tree_data = prepare_data_for_tree(item)
    # validate_or_abort('tree', tree_data)
    item_tree = add_item('tree', tree_data)

    tree_trans_data = prepare_data_for_tree_translation(item_tree.id, item.name)
    # validate_or_abort('tree_translation', tree_trans_data)
    add_item('tree_translation', tree_trans_data)

    if extra_fields_dict:
        extra_table_name = item.equipment_type and item.equipment_type.table_name
        extra_fields_dict['equipment_id'] = item.id
        # validate_or_abort(extra_table_name, extra_fields_dict)
        add_item(extra_table_name, extra_fields_dict)
    return item


def add_fluid_profile(path, data):
    if data.get("shared") is False:
        # Save id of the current user
        data["user_id"] = login.current_user.id if login.current_user else None
    item = add_item(path, data)
    return item


def add_electrical_profile(path, data):
    if data.get("shared") is False:
        # Save id of the current user
        data["user_id"] = login.current_user.id if login.current_user else None
    item = add_item(path, data)
    return item


# Get equipment upstreams and downstreams
def get_up_down_stream_of_equipment(item_id):
    path = 'equipment_connection'
    model = get_model_by_path(path)
    kwargs = {'equipment_id': item_id}
    upstream = [item.parent_id for item in db.session.query(model).filter_by(**kwargs)]
    kwargs = {'parent_id': item_id}
    downstream = [item.equipment_id for item in db.session.query(model).filter_by(**kwargs)]
    return {'upstream': upstream, 'downstream': downstream}


def add_up_down_stream_to_equipment(item_id, data):
    path = 'equipment_connection'
    upstream_list = data.get('upstream', [])
    for upstream_id in upstream_list:
        add_item(path, {'equipment_id': item_id, 'parent_id': upstream_id})

    downstream_list = data.get('downstream', [])
    for downstream_id in downstream_list:
        add_item(path, {'equipment_id': downstream_id, 'parent_id': item_id})

    return get_up_down_stream_of_equipment(item_id)


# Remove connection between equipment and its upstreams and downstreams
def delete_up_down_stream_of_equipment(item_id):
    path = 'equipment_connection'
    model = get_model_by_path(path)
    upstream = request.json.get('upstream', [])
    downstream = request.json.get('downstream', [])
    try:
        db.session.query(model)\
            .filter(model.parent_id.in_(upstream), model.equipment_id == item_id)\
            .delete(synchronize_session=False)
        db.session.query(model)\
            .filter(model.equipment_id.in_(downstream), model.parent_id == item_id)\
            .delete(synchronize_session=False)
    except:
        return False
    else:
        db.session.commit()
        return True


# Add a lot of test results
def add_items(path, data):
    items_model = get_model_by_path(path)
    campaign_id = data.get('campaign_id')
    # TODO - deleting of all related test results IMHO isn't the best way
    # because of related to test results objects like tests
    try:
        db.session.query(items_model).filter(items_model.campaign_id == campaign_id).delete(synchronize_session=False)
    except:
        db.session.rollback()
    else:
        db.session.commit()

    equipment_ids = data.get('equipment_id')
    if not isinstance(equipment_ids, Iterable):
        equipment_ids = [equipment_ids]
    return [add_item(path, {'campaign_id':campaign_id, 'equipment_id':id}).id for id in equipment_ids]


def add_or_update_tests(path):
    items_model = get_model_by_path(path)
    items = []
    for test in request.json:
        if 'id' in test:
            item = db.session.query(items_model).get(test['id'])
        else:
            validated_data = validate_or_abort(path, test)
            item = add_item(path, validated_data)

        items.append(item)
        set_attrs_to_item(item, test)

    try:
        db.session.commit()
    except Exception as e:
        abort(500, e.args)

    return [item.serialize() for item in items]


# Create user
def add_user(path, data):
    items_model = get_model_by_path(path)
    item = items_model()
    role_id = data.pop("roles", None)
    if role_id:
        role = db.session.query(Role).filter(Role.id == role_id).first()
        item.roles = [role] if role else abort(400, {"roles": "invalid value"})

    item.password = encrypt_password(data["password"])
    country_id = data.get("country_id")
    if country_id:
        country_exists = db.session.query(db.exists().where(Country.id == country_id)).scalar()
        if not country_exists:
            abort(400, {"country_id": "invalid value"})

    set_attrs_to_item(item, data)
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        abort(500, e.args)

    return item


# Duplicate test result and related fluid or electrical profile
def duplicate_test_result(test_result_id):
    user = login.current_user
    test_result_model = get_model_by_path('test_result')
    electrical_profile_model = get_model_by_path('electrical_profile')
    fluid_profile_model = get_model_by_path('fluid_profile')
    test_result = db.session\
        .query(test_result_model)\
        .outerjoin(test_result_model.electrical_profile)\
        .outerjoin(test_result_model.fluid_profile)\
        .filter(
            and_(
                # get only profiles with user_id NULL or the ones which belong to the current user
                or_(electrical_profile_model.user_id == None, electrical_profile_model.user_id == user.id),
                or_(fluid_profile_model.user_id == None, fluid_profile_model.user_id == user.id)
            ),
            test_result_model.id == test_result_id
        ).first()
    if test_result:
        test_result = handle_profile_and_test_result_duplication(test_result, user.id)
    return test_result.id if test_result else None


def handle_profile_and_test_result_duplication(test_result, user_id):
    profile = None
    profile_type = None
    if test_result.electrical_profile and test_result.electrical_profile.user_id == user_id:
        # Electrical profile belongs to the current user
        profile = duplicate_instance(test_result.electrical_profile)
        profile_type = "electrical"
    elif test_result.fluid_profile and test_result.fluid_profile.user_id == user_id:
        # Fluid profile belongs to the current user
        profile = duplicate_instance(test_result.fluid_profile)
        profile_type = "fluid"

    try:
        if profile:
            db.session.flush()
            if profile_type == "electrical":
                test_result.electrical_profile_id = profile.id
            elif profile_type == "fluid":
                test_result.fluid_profile_id = profile.id
        # Test result
        duplicate_instance(test_result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, e.args)
    return test_result


def duplicate_instance(item):
    db.session.expunge(item)
    make_transient(item)
    item.id = None
    db.session.add(item)
    return item


# Get fields from corresponding table of specified equipment type
def get_equipment_type_fields(item_id):
    item = db.session.query(EquipmentType).get(item_id) or abort(404)
    return {str(c.name): str(c.type) for c in meta.tables[item.table_name].columns}


@api.errorhandler(404)
def not_found(error):
    return make_response(return_json('error', 'Not found'), 404)


@api.errorhandler(400)
def bad_request(error):
    return make_response(return_json('error', error.description), 400)


@api.errorhandler(500)
def internal_server_error(error):
    return make_response(return_json('error', error.description), 500)


# Standard routes
# Create
@api_blueprint.route('/<path>/', methods=['POST'])
def create_item_handler(path):
    abort_if_wrong_path(path)
    abort_if_json_missing()
    validated_data = validate_or_abort(path)
    new_item = add_item(path, validated_data)
    return return_json('result', new_item.id)


# Read
@api_blueprint.route('/<path>/', methods=['GET'])
def read_items_handler(path):
    abort_if_wrong_path(path)
    return return_json('result', get_items(path, request.args))


@api_blueprint.route('/<path>/<int:item_id>', methods=['GET'])
def read_item_handler(path, item_id):
    abort_if_wrong_path(path)
    abort_if_wrong_id(item_id)
    return return_json('result', get_item(path, item_id))


# Update
@api_blueprint.route('/<path>/<int:item_id>', methods=['PUT', 'POST'])
def update_item_handler(path, item_id):
    abort_if_wrong_path(path)
    abort_if_wrong_id(item_id)
    abort_if_json_missing()
    validated_data = validate_or_abort(path, update=True)
    updated_item = update_item(path, item_id, validated_data)
    return return_json('result', updated_item.serialize())


# Delete
@api_blueprint.route('/<path>/<int:item_id>', methods=['DELETE'])
def delete_item_handler(path, item_id):
    abort_if_wrong_path(path)
    abort_if_wrong_id(item_id)
    return return_json('result', delete_item(path, item_id))


# Custom routes
# Get fields from corresponding table of specified equipment type
@api_blueprint.route('/equipment_type/<int:item_id>/fields', methods=['GET'])
def handler_equipment_type_fields(item_id):
    abort_if_wrong_id(item_id)
    return return_json('result', get_equipment_type_fields(item_id))


# Get fluid and electrical profiles in one responce
@api_blueprint.route('/test_profile/', methods=['GET'])
def get_test_profile():
    rows_fluid = db.session.query(FluidProfile).all()
    rows_electrical = db.session.query(ElectricalProfile).all()
    return return_json('result', [item.serialize() for rows in (rows_fluid, rows_electrical) for item in rows])


# Create equipment
@api_blueprint.route('/equipment/', methods=['POST'])
def create_equipment_handler():
    path = 'equipment'
    abort_if_json_missing()
    validated_data = validate_or_abort(path)
    new_item = add_equipment(path, validated_data)
    return return_json('result', new_item.id)


# Create equipment upstreams and downstreams
@api_blueprint.route('/equipment/<int:item_id>/up_down_stream/', methods=['POST'])
def create_equipment_up_down_stream_handler(item_id):
    abort_if_json_missing()
    # validated_data = validate_or_abort('equipment_up_down_stream')
    return return_json('result', add_up_down_stream_to_equipment(item_id, request.json))


# Get equipment upstreams and downstreams
@api_blueprint.route('/equipment/<int:item_id>/up_down_stream/', methods=['GET'])
def read_equipment_up_down_stream_handler(item_id):
    return return_json('result', get_up_down_stream_of_equipment(item_id))


# Remove connection between equipment and its upstreams and downstreams
@api_blueprint.route('/equipment/<int:item_id>/up_down_stream/', methods=['DELETE'])
def delete_equipment_up_down_stream_handler(item_id):
    abort_if_json_missing()
    return return_json('result', delete_up_down_stream_of_equipment(item_id))


# Create a lot of test_results with equipment using one query
@api_blueprint.route('/test_result/equipment', methods=['POST'])
def handler_items():
    path = 'test_result_equipment'
    abort_if_json_missing()
    validated_data = validate_or_abort(path)
    return return_json('result', add_items(path, validated_data))


# Create or update a lot of tests
@api_blueprint.route('/test_result/multi/<path>', methods=['POST'])
def handler_tests(path):
    if path not in ('transformer_turn_ratio_test',
                    'winding_resistance_test',
                    'winding_test'):
        abort(404)
    abort_if_json_missing()
    return return_json('result', add_or_update_tests(path))


# Duplicate test result and related electrical or fluid profile
@api_blueprint.route('/test_result/<int:test_result_id>/duplicate', methods=['POST'])
def duplicate_test_result_handler(test_result_id):
    abort_if_wrong_id(test_result_id)
    return return_json('result', duplicate_test_result(test_result_id))


# Create user
@api_blueprint.route('/user/', methods=['POST'])
def create_user_handler():
    path = 'user'
    abort_if_json_missing()
    validated_data = validate_or_abort(path)
    new_user = add_user(path, validated_data)
    return return_json('result', new_user.id)


# Create fluid_profile
@api_blueprint.route('/fluid_profile/', methods=['POST'])
def create_fluid_profile_handler():
    path = 'fluid_profile'
    abort_if_json_missing()
    validated_data = validate_or_abort(path)
    new_item = add_fluid_profile(path, validated_data)
    return return_json('result', new_item.id)


# Create electrical_profile
@api_blueprint.route('/electrical_profile/', methods=['POST'])
def create_electrical_profile_handler():
    path = 'electrical_profile'
    abort_if_json_missing()
    validated_data = validate_or_abort(path)
    new_item = add_electrical_profile(path, validated_data)
    return return_json('result', new_item.id)


api.register_blueprint(api_blueprint)
