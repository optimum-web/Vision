from functools import wraps
import os
from datetime import datetime, timedelta
from flask import Flask, Blueprint, jsonify, abort, make_response, request, g
from flask.ext.sqlalchemy import SQLAlchemy
from api_utility import MyValidator as Validator
from api_utility import model_dict, eq_type_dict
from app.diagnostic.models import EquipmentType, TestResult, Campaign, FluidProfile, \
    Country, TestReason, TestType, TestStatus, Equipment, Norm
from app.diagnostic.models import ElectricalProfile
from app.users.models import User, Role
from collections import Iterable
from sqlalchemy import create_engine, MetaData, or_, and_, String
from sqlalchemy.sql.expression import cast
from sqlalchemy.sql.functions import concat
from sqlalchemy import func
from flask.ext.blogging import SQLAStorage
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.security.utils import encrypt_password
from flask.ext import login
from sqlalchemy.orm.session import make_transient
from .mail_utility import send_email, generate_message
from tasks import apply_send_email_task, setup_periodic_email_task
from flask import Response


api = Flask(__name__, static_url_path='/app/static')
api.config.from_object('config')
engine = create_engine(api.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(api, session_options={'autoflush': False})
api_blueprint = Blueprint('api_v1_0', __name__, url_prefix='/api/v1.0')
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(api, user_datastore)


# Authentication functions
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        # if not auth:
        #     abort(401)
        if auth:
            if not verify_password(auth['username'], unicode(auth['password'], 'utf-8')):
                pass
                # abort(401)
        return f(*args, **kwargs)
    return decorated_function


def admin_role_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.has_role(Role.query.get(1)):
            abort(403, 'Admin role needed!')
        return f(*args, **kwargs)
    return decorated_function


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
def validate_or_abort(path, data_to_validate=None, update=False, abort_request=True):
    if not data_to_validate:
        data_to_validate = request.json
    v = Validator(ignore_none_values=True)
    if not v.validate(data_to_validate, get_schema_by_path(path), update):
        if abort_request:
            abort(400, v.errors)
        else:
            return {'errors': v.errors}
    return v.document


def json_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.json:
            abort(400, 'JSON not found')
        return f(*args, **kwargs)
    return decorated_function


def abort_if_wrong_path(path):
    if path not in model_dict:
        abort(404)


def abort_if_wrong_id(item_id):
    if not item_id:
        abort(404)


def abort_if_not_owner_or_admin(path, item_id, check_owner_field='user_id'):
    if not g.user.has_role(Role.query.get(1)):
        items_model = get_model_by_path(path)
        item = db.session.query(items_model).get(item_id) or abort(404)
        if getattr(item, check_owner_field) != g.user.id:
            abort(404)


def add_user_id_and_save_item(path, data):
    # Save id of the current user
    data["user_id"] = login.current_user.id if login.current_user else None
    item = add_item(path, data)
    return item


def get_items_by_role(path, args, check_owner_field='user_id'):
    if not g.user.has_role(Role.query.get(1)):
        # If not admin, get only user's records
        args = args.copy()
        args.add(check_owner_field, g.user.id)
    return get_items(path, args)


# Standard CRUD functions
# Create
def add_item(path, data):
    items_model = get_model_by_path(path)
    item = items_model()
    set_attrs_to_item(item, data)
    if path == "equipment" or path == "contract" or path == "campaign":
        item.group_id = login.current_user.group_id
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

def get_item_by_item_id(path, item_id):
    items_model = get_model_by_path(path)
    item = db.session.query(items_model).filter(items_model.equipment_id == item_id).first() or abort(404)
    return item.serialize()

def get_items_by_item_id(path, item_id):
    items_model = get_model_by_path(path)
    items = [item.serialize() for item in db.session.query(items_model).filter(items_model.equipment_id == item_id).all() or abort(404)]
    return items

def get_items(path, args):
    items_model = get_model_by_path(path)
    if args:
        kwargs = {
            k: v for k, v in args.items() if hasattr(items_model, k)
                 or (k == 'campaign__created_by_id' and items_model == TestResult)
                 or (k == 'search_all' and items_model == TestResult)
                 or abort(400, 'Wrong attribute: {}'.format(k))
        }
        if items_model == Campaign and 'equipment_id' in kwargs:
            campaign_ids = {item.campaign_id for item in db.session.query(TestResult).filter_by(**kwargs)}
            return [item.serialize() for item in db.session.query(Campaign).filter(Campaign.id.in_(campaign_ids))]

        if 'campaign__created_by_id' in kwargs:
            created_by_id = kwargs.pop('campaign__created_by_id')
            return [item.serialize() for item in db.session.query(items_model)
                                                           .filter_by(**kwargs)
                                                           .outerjoin(items_model.campaign)
                                                           .filter(Campaign.created_by_id == created_by_id)]
        if 'search_all' in kwargs:
            search_value = kwargs.pop('search_all')
            return [item.serialize() for item in build_seach_equipment_query(items_model, search_value)]
        
        return [item.serialize() for item in db.session.query(items_model).filter_by(**kwargs)]
    
    if path == "location" or path == "assigned_to" or path == "user" or path == "contract" or path == "equipment":
        return [item.serialize() for item in db.session.query(items_model).filter(items_model.group_id==login.current_user.group_id).all()]

    return [item.serialize() for item in db.session.query(items_model).all()]


def build_seach_equipment_query(items_model, search_value):
    # Probably it is better to make filters like in Django: date_analyse__icontains="value"
    return db.session\
        .query(items_model)\
        .outerjoin(items_model.test_reason)\
        .outerjoin(items_model.test_type)\
        .outerjoin(items_model.test_status)\
        .outerjoin(items_model.equipment)\
        .outerjoin(items_model.campaign)\
        .outerjoin(Campaign.created_by)\
        .filter(Campaign.group_id == login.current_user.group_id)\
        .filter(or_(
            cast(TestResult.date_analyse, String).ilike("%{}%".format(search_value)),
            cast(TestResult.id, String).ilike("%{}%".format(search_value)),
            concat(cast(TestResult.id, String),
                   func.substring(User.name, r'^([a-zA-Z]{1})'),
                   func.substring(User.name, r'\s([a-zA-Z]){1}'))
                .ilike("%{}%".format(search_value)),
            TestReason.name.ilike("%{}%".format(search_value)),
            TestType.name.ilike("%{}%".format(search_value)),
            TestStatus.name.ilike("%{}%".format(search_value)),
            Equipment.serial.ilike("%{}%".format(search_value)),
            Equipment.equipment_number.ilike("%{}%".format(search_value)),
            ))\
        .all()


def validate_multi(path, group_by_field):
    validation_errors = {}
    validated_norms = []

    # Validate all items at once
    for item in request.json:
        if 'id' not in item:
            validated_data = validate_or_abort(path, item, abort_request=False)
            if validated_data.get('errors'):
                # Save errors
                if not validation_errors.get(item[group_by_field]):
                    validation_errors[item[group_by_field]] = {}
                validation_errors[item[group_by_field]].update(validated_data['errors'])
            else:
                # Save validated document
                validated_norms.append(validated_data)
    return validation_errors, validated_norms


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
    try:
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

    except:
        return {}




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


# Remove connection between equipment and its upstream
def delete_upstream_of_equipment(item_id, upstream_id):
    path = 'equipment_connection'
    model = get_model_by_path(path)
    try:
        db.session.query(model)\
            .filter(model.parent_id == upstream_id, model.equipment_id == item_id)\
            .delete(synchronize_session=False)
    except:
        return False
    else:
        db.session.commit()
        return True


# Remove connection between equipment and its downstream
def delete_downstream_of_equipment(item_id, downstream_id):
    return delete_upstream_of_equipment(downstream_id, item_id)


# Add standard norms to an equipment
def add_standard_norms_to_equipment(item_id):
    available_norms = get_available_norms()
    if available_norms:
        equipment = db.session.query(Equipment).filter_by(id=item_id).first()
        if equipment:
            equipment_type_id = equipment.equipment_type_id
            add_equipment_norms_to_session(available_norms, equipment_type_id, item_id)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                abort(500, e.args)
    return True


# Get all currently available norms
def get_available_norms():
    norms = db.session.query(Norm).all()
    available_norms = {}
    for norm in norms:
        norm_model = model_dict.get(norm.table_name, {}).get('model')
        if norm_model:
            available_norms[norm_model] = norm.table_name
    return available_norms


def add_equipment_norms_to_session(available_norms, equipment_type_id, item_id):
    for norm_model, norm_table_name in available_norms.items():
        # Get standard norm
        equipment_norm = db.session.query(norm_model) \
            .filter_by(equipment_type_id=equipment_type_id) \
            .order_by(norm_model.date_created.desc()) \
            .first()
        if equipment_norm:
            equipment_norm = prepare_equipment_norm_data(equipment_norm, norm_table_name, item_id)
            if equipment_norm:
                db.session.add(equipment_norm)


# Pre-process standard norm to save it to norm data table
def prepare_equipment_norm_data(equipment_norm, norm_table_name, item_id):
    equipment_norm = equipment_norm.serialize()
    equipment_norm_model = model_dict.get("{}_data".format(norm_table_name), {}).get('model')
    if equipment_norm_model:
        equipment_norm['norm_id'] = equipment_norm.pop('id')
        equipment_norm['equipment_id'] = item_id
        equipment_norm['user_id'] = login.current_user.id
        del equipment_norm['equipment_type_id']
        del equipment_norm['equipment_type']
        del equipment_norm['date_created']
        equipment_norm = equipment_norm_model(**equipment_norm)
        return equipment_norm
    return {}


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


def add_or_update_items(path):
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


@api.errorhandler(403)
def forbidden(error):
    return make_response(return_json('error', error.description), 403)


@api.errorhandler(401)
def unauthorized(error):
    return make_response(return_json('error', error.description), 401)


@api.errorhandler(400)
def bad_request(error):
    return make_response(return_json('error', error.description), 400)


@api.errorhandler(500)
def internal_server_error(error):
    return make_response(return_json('error', error.description), 500)


# Standard routes
# Create
@api_blueprint.route('/<path>/', methods=['POST'])
@login_required
@json_required
def create_item_handler(path):
    abort_if_wrong_path(path)
    validated_data = validate_or_abort(path)
    new_item = add_item(path, validated_data)
    return return_json('result', new_item.id)


# Read
@api_blueprint.route('/<path>/', methods=['GET'])
@login_required
def read_items_handler(path):
    abort_if_wrong_path(path)
    return return_json('result', get_items(path, request.args))


@api_blueprint.route('/<path>/<int:item_id>', methods=['GET'])
@login_required
def read_item_handler(path, item_id):
    abort_if_wrong_path(path)
    abort_if_wrong_id(item_id)
    return return_json('result', get_item(path, item_id))


@api_blueprint.route('/<path>/item_id/<int:item_id>', methods=['GET'])
@login_required
def read_item_handler_equipment_id(path, item_id):
    abort_if_wrong_path(path)
    abort_if_wrong_id(item_id)
    return return_json('result', get_item_by_item_id(path, item_id))

@api_blueprint.route('/<path>/item_id/<int:item_id>/all', methods=['GET'])
@login_required
def read_items_handler_equipment_id(path, item_id):
    abort_if_wrong_path(path)
    abort_if_wrong_id(item_id)
    return return_json('result', get_items_by_item_id(path, item_id))

# Update
@api_blueprint.route('/<path>/<int:item_id>', methods=['PUT', 'POST'])
@login_required
@json_required
def update_item_handler(path, item_id):
    abort_if_wrong_path(path)
    abort_if_wrong_id(item_id)
    validated_data = validate_or_abort(path, update=True)
    updated_item = update_item(path, item_id, validated_data)
    return return_json('result', updated_item.serialize())


# Delete
@api_blueprint.route('/<path>/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item_handler(path, item_id):
    abort_if_wrong_path(path)
    abort_if_wrong_id(item_id)
    return return_json('result', delete_item(path, item_id))


# Custom routes
# Get token
@api_blueprint.route('/token/')
@login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii'), 'user_id': g.user.get_id()})


# Get fields from corresponding table of specified equipment type
@api_blueprint.route('/equipment_type/<int:item_id>/fields', methods=['GET'])
@login_required
def handler_equipment_type_fields(item_id):
    abort_if_wrong_id(item_id)
    return return_json('result', get_equipment_type_fields(item_id))


# Get fluid and electrical profiles in one responce
@api_blueprint.route('/test_profile/', methods=['GET'])
@login_required
def get_test_profile():
    rows_fluid = db.session.query(FluidProfile).all()
    rows_electrical = db.session.query(ElectricalProfile).all()
    return return_json('result', [item.serialize() for rows in (rows_fluid, rows_electrical) for item in rows])


# Create equipment
@api_blueprint.route('/equipment/', methods=['POST'])
@login_required
@json_required
def create_equipment_handler():
    path = 'equipment'
    validated_data = validate_or_abort(path)
    new_item = add_equipment(path, validated_data)
    return return_json('result', new_item.id)


# Update equipment
@api_blueprint.route('/equipment/<int:item_id>', methods=['PUT', 'POST'])
@login_required
@json_required
def update_equipment_handler(item_id):
    path = 'equipment'
    abort_if_wrong_id(item_id)
    validated_data = validate_or_abort(path, update=True)
    updated_item = update_item(path, item_id, validated_data)

    # Send notifications if only status field is updated
    if len(validated_data) == 1 and validated_data.get('status'):
        email_recipients = [updated_item.assigned_to.email,
                            updated_item.visual_inspection_by.email,
                            g.user.email]
        send_email(email_recipients,
                   generate_message(path, updated_item),
                   'Vision - Equipment health state of {} updated'.format(updated_item.name))
    return return_json('result', updated_item.serialize())


# Create equipment upstreams and downstreams
@api_blueprint.route('/equipment/<int:item_id>/up_down_stream/', methods=['POST'])
@login_required
@json_required
def create_equipment_up_down_stream_handler(item_id):
    # validated_data = validate_or_abort('equipment_up_down_stream')
    return return_json('result', add_up_down_stream_to_equipment(item_id, request.json))


# Get equipment upstreams and downstreams
@api_blueprint.route('/equipment/<int:item_id>/up_down_stream/', methods=['GET'])
@login_required
def read_equipment_up_down_stream_handler(item_id):
    return return_json('result', get_up_down_stream_of_equipment(item_id))


# Remove connection between equipment and its upstreams and downstreams
@api_blueprint.route('/equipment/<int:item_id>/up_down_stream/', methods=['DELETE'])
@login_required
@json_required
def delete_equipment_up_down_stream_handler(item_id):
    return return_json('result', delete_up_down_stream_of_equipment(item_id))


# Remove connection between equipment and its upstream
@api_blueprint.route('/equipment/<int:item_id>/upstream/<int:upstream_id>', methods=['DELETE'])
def delete_equipment_upstream_handler(item_id, upstream_id):
    return return_json('result', delete_upstream_of_equipment(item_id, upstream_id))


# Remove connection between equipment and its downstream
@api_blueprint.route('/equipment/<int:item_id>/downstream/<int:downstream_id>', methods=['DELETE'])
def delete_equipment_downstream_handler(item_id, downstream_id):
    return return_json('result', delete_downstream_of_equipment(item_id, downstream_id))


# Add standard norms to the equipment
@api_blueprint.route('/equipment/<int:item_id>/norm/', methods=['POST'])
@login_required
def create_equipment_standard_norms_handler(item_id):
    abort_if_wrong_id(item_id)
    return return_json('result', add_standard_norms_to_equipment(item_id))


# Create a lot of test_results with equipment using one query
@api_blueprint.route('/test_result/equipment/', methods=['POST'])
@login_required
@json_required
def handler_items():
    path = 'test_result_equipment'
    validated_data = validate_or_abort(path)
    return return_json('result', add_items(path, validated_data))


# Create or update a lot of tests
@api_blueprint.route('/test_result/multi/<path>', methods=['POST'])
@login_required
@json_required
def handler_tests(path):
    if path not in ('transformer_turn_ratio_test',
                    'winding_resistance_test',
                    'winding_test'):
        abort(404)
    return return_json('result', add_or_update_items(path))


# Duplicate test result and related electrical or fluid profile
@api_blueprint.route('/test_result/<int:test_result_id>/duplicate', methods=['POST'])
@login_required
def duplicate_test_result_handler(test_result_id):
    abort_if_wrong_id(test_result_id)
    return return_json('result', duplicate_test_result(test_result_id))


# Create user
@api_blueprint.route('/user/', methods=['POST'])
@login_required
@admin_role_required
@json_required
def create_user_handler():
    path = 'user'
    validated_data = validate_or_abort(path)
    new_user = add_user(path, validated_data)
    return return_json('result', new_user.id)


# Create fluid_profile
@api_blueprint.route('/fluid_profile/', methods=['POST'])
@login_required
@json_required
def create_fluid_profile_handler():
    path = 'fluid_profile'
    validated_data = validate_or_abort(path)
    new_item = add_fluid_profile(path, validated_data)
    return return_json('result', new_item.id)


# Create electrical_profile
@api_blueprint.route('/electrical_profile/', methods=['POST'])
@login_required
@json_required
def create_electrical_profile_handler():
    path = 'electrical_profile'
    validated_data = validate_or_abort(path)
    new_item = add_electrical_profile(path, validated_data)
    return return_json('result', new_item.id)


# Create test recommendation
@api_blueprint.route('/test_recommendation/', methods=['POST'])
@login_required
@json_required
def create_test_recommendation_handler():
    path = 'test_recommendation'
    validated_data = validate_or_abort(path)
    new_item = add_user_id_and_save_item(path, validated_data)
    return return_json('result', new_item.id)


# Create test diagnosis
@api_blueprint.route('/test_diagnosis/', methods=['POST'])
@login_required
@json_required
def create_test_diagnosis_handler():
    path = 'test_diagnosis'
    validated_data = validate_or_abort(path)
    new_item = add_user_id_and_save_item(path, validated_data)
    return return_json('result', new_item.id)


# Create test repair note
@api_blueprint.route('/test_repair_note/', methods=['POST'])
@login_required
@json_required
def create_test_repair_note_handler():
    path = 'test_repair_note'
    validated_data = validate_or_abort(path)
    new_item = add_user_id_and_save_item(path, validated_data)
    return return_json('result', new_item.id)


# Read schedules filtered by role
@api_blueprint.route('/schedule/', methods=['GET'])
@login_required
def read_tasks_handler():
    path = 'schedule'
    return return_json('result', get_items_by_role(path, request.args, check_owner_field="assigned_to_id"))


# Read schedule filtered by role
@api_blueprint.route('/schedule/<int:item_id>', methods=['GET'])
@login_required
def read_task_handler(item_id):
    path = 'schedule'
    abort_if_wrong_id(item_id)
    abort_if_not_owner_or_admin(path, item_id, check_owner_field='assigned_to_id')
    return return_json('result', get_item(path, item_id))


# Anyone can create a schedule
@api_blueprint.route('/schedule/', methods=['POST'])
@login_required
@json_required
def create_task_handler():
    path = 'schedule'
    validated_data = validate_or_abort(path)
    new_item = add_item(path, validated_data)

    email_recipients = [new_item.assigned_to.email, g.user.email]
    email_message = generate_message(path, new_item)
    send_email(email_recipients, email_message, 'Vision - Task Created #{}'.format(new_item.id))
    send_task_emails_to_queue(email_recipients, email_message, new_item, validated_data)

    return return_json('result', new_item.id)


def send_task_emails_to_queue(email_recipients, email_message, new_item, validated_data):
    kwargs = {}
    date_start = datetime.strptime(validated_data.get('date_start'), '%Y-%m-%dT%H:%M')
    notify_before_in_days = validated_data.get('notify_before_in_days')
    recurring = validated_data.get('recurring')
    if date_start:
        if recurring:
            period_data = prepare_period_data(validated_data)
            if period_data:
                setup_periodic_email_task(email_recipients,
                                          email_message,
                                          'Vision - Periodic Task #{} Reminder'.format(new_item.id),
                                          period_data,
                                          date_start)
        if notify_before_in_days:
            kwargs['eta'] = date_start - timedelta(days=notify_before_in_days)
            apply_send_email_task(email_recipients,
                                  email_message,
                                  'Vision - Notification of Created Task #{}'.format(new_item.id),
                                  kwargs)


def prepare_period_data(data):
    period_data = {}
    if data.get('period_days'):
        period_data = {'period_days': data.get('period_days')}
    elif data.get('period_months'):
        period_data = {'period_months': data.get('period_months')}
    elif data.get('period_years'):
        period_data = {'period_years': data.get('period_years')}
    return period_data


# Update schedule
@api_blueprint.route('/schedule/<int:item_id>', methods=['PUT', 'POST'])
@login_required
@json_required
def update_task_handler(item_id):
    path = 'schedule'
    abort_if_wrong_id(item_id)
    abort_if_not_owner_or_admin(path, item_id, check_owner_field='assigned_to_id')

    previous_assigned_to = get_item(path, item_id)['assigned_to']['email']
    validated_data = validate_or_abort(path, update=True)
    updated_item = update_item(path, item_id, validated_data)

    email_recipients = [previous_assigned_to, updated_item.assigned_to.email, g.user.email]
    send_email(email_recipients, generate_message(path, updated_item), 'Vision - Task Updated #{}'.format(updated_item.id))
    return return_json('result', updated_item.serialize())


# Delete schedule
@api_blueprint.route('/schedule/<int:item_id>', methods=['DELETE'])
@login_required
def delete_task_handler(item_id):
    path = 'schedule'
    abort_if_wrong_id(item_id)
    abort_if_not_owner_or_admin(path, item_id, check_owner_field='assigned_to_id')
    return return_json('result', delete_item(path, item_id))


@api_blueprint.route('/campaign/<int:item_id>/finish/', methods=['GET'])
@login_required
def finish_campaign_handler(item_id):
    path = 'campaign'
    abort_if_wrong_id(item_id)
    item = db.session.query(Campaign).get(item_id)
    test_results = db.session.query(TestResult).filter(Campaign.id == item_id).all()
    email_recipients = [test_result.performed_by.email for test_result in test_results if test_result.performed_by]
    email_recipients.extend([item.created_by.email, g.user.email]) # to_check
    send_email(email_recipients,
               generate_message(path, item),
               'Vision - Campaign setup finished #{:%m/%d/%Y %I:%M %p}'.format(item.date_created))
    return return_json('result', item.id)


@api_blueprint.route('/campaign/', methods=['GET'])
@login_required
def get_campaigns_handler():
    last_id = request.args.get('last_id')
    if last_id and not last_id.isnumeric():
        abort(400, {'last_id': 'Invalid value'})

    path = 'campaign'
    items_model = get_model_by_path(path)
    filter_clause = None
    page_len = 20
    search_val = request.args.get('q')
    args = request.args

    if args:
        kwargs = {k: v for k, v in args.items() if hasattr(items_model, k)}
        if search_val:
            filter_clause = func.concat(items_model.date_created, ' ', items_model.description).like('%{}%'.format(search_val))
            if last_id:
                filter_clause = and_(filter_clause, items_model.id > last_id)
        query = db.session.query(items_model).filter(items_model.group_id == login.current_user.group_id)
        if filter_clause is not None:
            query = query.filter(filter_clause)
        total_count = query.filter_by(**kwargs).count()
        return return_json('result', {
            'items': [item.serialize() for item in query
                           .filter_by(**kwargs)
                           .order_by(items_model.date_created.asc())
                           .limit(page_len)],
            'total_count': total_count})
    return return_json('result', get_items(path, args))


# Get release version
@api_blueprint.route('/release_version/', methods=['GET'])
@login_required
def get_release_version_handler():
    answer = os.popen('git tag -l "v*"').read()
    current_version = answer.rstrip().split('\n')[-1:]
    return return_json('result', current_version)

import requests
from flask import request

# Get release version
@api_blueprint.route('/download/<id>', methods=['GET'])
@login_required
def generate_pdf(id):
    url = api.config['EQUIPMENT_REPORT_URL'] + id + "?" + request.query_string
    auth = request.headers.get('Authorization')
    r = requests.post('http://wkhtml:5001/', data = {'html' : url ,'auth' : auth, 'pdfId' : request.args.get('pdfId')})
    return return_json('result', 1)

# Check if PDF is generated
@api_blueprint.route('/check_pdf/<pdfId>', methods=['GET'])
@login_required
def check_pdf(pdfId):
    if os.path.isfile(api.config['EQUIPMENT_REPORT_DIR'] + pdfId + ".pdf"):
        return return_json('result', 1)
    return return_json('result', 0)

import base64
# Invite one user
@api_blueprint.route('/invite_user/', methods=['POST'])
@login_required
def invite_user():

    group_id = base64.b64encode("group|{}".format(g.user.group_id))
    link = "http://{}/group/register?group={}".format(api.config['HOST'], group_id)

    email_message = "Dear {}. You have been invited to join Vision. Please follow this link to complete registration {}".format(request.json['name'], link)
    print email_message
    send_email([request.json['email']], email_message, 'Vision - invitation')
    return return_json('result', 0)


api.register_blueprint(api_blueprint)
