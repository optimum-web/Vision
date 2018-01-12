from flask import flash, g, session
import sqlalchemy_utils
from .models import *
from app import db
from sqlalchemy.orm import joinedload_all
from app import app
from sqlalchemy.orm.session import make_transient
import json
from flask import jsonify
from app.diagnostic.models import EquipmentType, Location, Transformer, AirCircuitBreaker, Bushing, \
    Capacitor, Breaker, PowerSource, Cable, SwitchGear, InductionMachine, SynchronousMachine, \
    LoadTapChanger, Rectifier, Tank, Switch, Inductance, NeutralResistance, GasSensor, Graph
from flask.ext import admin, login

import datetime

def set_locale():
    sqlalchemy_utils.i18n.get_locale = get_locale


def get_locale():
    if 'locale' in session:
        if session['locale'] is not None:
            return session['locale']

    return 'en'


# return all tree
def get_tree():
    # try:
    #     # .options(joinedload_all("children", "children", "children", "children"))
    #     tree = db.session.query(TreeNode).options(joinedload_all("children", "children", "children", "children")) \
    #         .filter(TreeNode.text == u'Vision Diagnostic').first()
    #     res = None
    #     if tree is not None:
    #         res = "<ul>"
    #         res += create_tree(tree)
    #         res += "</ul>"
    # except Exception as e:
    #     import logging
    #     logging.error(e)
    #     res = None

    # try:
    #     tree = db.session.query(TreeNode).options(joinedload_all("children", "children", "children", "children")) \
    #         .filter(TreeNode.text == u'Vision Diagnostic').first()
    # tree = db.session.query(TreeNode)\
    #     .options(joinedload_all("children", "children", "children", "children"))\
    #     .filter(TreeNode.text == u'Vision Diagnostic').first()

    tree = db.session.query(TreeNode).options(joinedload_all("children", "children", "children", "children")).get(1) # get root

    res = []
    # res.insert(0,tree.serialize())
    if tree:
        res.append(tree.serialize())

        if tree.children:
            res = serialize(tree.children, res)
            # for item in tree.children:
            #     res.append(item.serialize())
            #     if item.children:
        # print res

    response = json.dumps(res)
    return response

    # except Exception as e:
    #     import logging
    #     logging.error(e)


def get_owner_tree():
    """ Get tree which lists owners and equipment which belong to them """
    locations = db.session.query(Location).filter(Location.group_id==g.user.group_id).options(joinedload_all('children')).all()
    tree_nodes, generic_tree_nodes = get_tree_nodes()
    res = []
    for location in locations:
        serialized_location = location.serialize(True)
        serialized_location = add_tree_data(
            location=serialized_location,
            tree_nodes=tree_nodes,
            tree_root=generic_tree_nodes['default'],
            tree_main=generic_tree_nodes['main'],
        )
        res.append(serialized_location)
    response = json.dumps(res)
    return response


def get_tree_nodes():
    """ Get tree nodes which correspond to the loaded equipment """
    # Get tree nodes
    tree_nodes = db.session.query(TreeNode).all()
    # Map tree nodes
    mapped_tree_nodes = {}
    generic_tree_nodes = {}
    for tree_node in tree_nodes:
        mapped_tree_nodes[tree_node.equipment_id] = tree_node
        if tree_node.type in ('default', 'main'):
            generic_tree_nodes[tree_node.type] = tree_node
    return mapped_tree_nodes, generic_tree_nodes


def add_tree_data(location, tree_nodes, tree_root, tree_main):
    """ Add tree data to the location and equipment """
    location = add_equipment_tree_data(location=location, tree_nodes=tree_nodes)
    location = add_owner_tree_data(location=location, tree_root=tree_root, tree_main=tree_main)
    return location


def add_equipment_tree_data(location, tree_nodes):
    """ Add tree data to the equipment """
    if location['children']:
        for equipment in location['children']:
            tree_node = tree_nodes.get(int(equipment['id']))
            if tree_node:
                equipment['id'] = tree_node.id
                equipment['text'] = tree_node.text
                equipment['icon'] = tree_node.icon
                equipment['disabled'] = tree_node.disabled
                equipment['selected'] = tree_node.selected
                equipment['type'] = tree_node.type
                equipment['view'] = tree_node.view
                equipment['location_id'] = location['id']
                equipment['parent_id'] = tree_node.parent_id
        location['children'] = make_equipment_tree(location['children'])
    return location


def make_equipment_tree(equipments):
    for equipment in equipments[:]:
        equipment_id = equipment['id']
        for child in equipments:
            if child.get('parent_id') == equipment_id:
                if not equipment.get('children'):
                    equipment['children'] = []
                equipment['children'].append(child)
                equipments.remove(child)
    return equipments


def add_owner_tree_data(location, tree_root, tree_main):
    """ Add tree data to the location (owner) """
    if tree_root:
        location['location_id'] = location['id']
        location['icon'] = tree_root.icon
        location['id'] = location['id'] #tree_main.id
    return location


def serialize_equipment(tree):
    children = []
    for item in tree:
        children.append(item.serialize())
    return children


def get_switch_ids():
    switch_names = ("Air circuit breaker", "Breaker", "Switch")
    switches = db.session.query(EquipmentType).filter(EquipmentType.name.in_(switch_names)).values("id")
    switches = [switch[0] for switch in switches]
    return json.dumps(switches)


def serialize(tree, res):
    if type(tree) == list:
        for item in tree:
            res.append(item.serialize())
            if item.children:
                return serialize(item.children, res)

    # item = tree.serialize()
    # res.append(item)
    return res


# create generate tree
def create_node(parent, text, icon, type, tooltip):
    try:
        # options(joinedload_all("children", "children", "children", "children")).
        parent = db.session.query(TreeNode).filter(TreeNode.id == parent).first()
        node = TreeNode(icon=icon, parent=parent, type=type)
        # think of a different solution how to extract node.id
        db.session.commit()

        node.text = text + str(node.id)
        node.tooltip = tooltip + str(node.id)

        if get_locale() is not node.get_locale():
            node.translations[node.get_locale()].text = text + str(node.id)
            node.translations[node.get_locale()].tooltip = tooltip + str(node.id)

        # parent.append(node)
        # parent.children[text + str(node.id)] = node
        db.session.commit()
        res = node.id
    except Exception as e:
        import logging
        logging.error(e)
        res = None

    return res


# rename tree element
def rename_node(id, text):
    try:
        node = db.session.query(TreeNode).filter(TreeNode.id == id).first()
        node.text = text
        db.session.commit()
        res = True
    except Exception as e:
        import logging
        logging.error(e)
        res = False
    return res


# delete node element
def delete_node(id):
    try:
        node = db.session.query(TreeNode).filter(TreeNode.id == id).first()
        db.session.delete(node)
        db.session.commit()
        res = node.id
    except Exception as e:
        import logging
        logging.error(e)
        res = None

    return res


# get view by id
def get_view_by_id(id):
    try:
        node = db.session.query(TreeNode).filter(TreeNode.id == id).first()
        res = (node.view, node.tooltip)
    except Exception as e:
        import logging
        logging.error(e)
        res = None

    return res


# update node tree
def update_node(node_id, view, tooltip):
    try:
        node = db.session.query(TreeNode).filter(TreeNode.id == node_id).first()
        node.view = view
        node.tooltip = tooltip
        db.session.commit()
        res = True
    except Exception as e:
        import logging
        logging.error(e)
        res = None

    return res


# move node tree
def move_node(node_id, parent_id):
    try:
        db.session.query(TreeNode).filter(TreeNode.id == node_id).update({'parent_id': parent_id})
        db.session.commit()
        res = True
    except Exception as e:
        import logging
        logging.error(e)
        res = None

    return res


# move node tree to another location
def move_node_to_location(node_id, location_id):
    res = None
    tree_node = db.session.query(TreeNode).filter(TreeNode.id == node_id).first()
    if tree_node and tree_node.equipment_id:
        try:
            tree_node.equipment.location_id = location_id
            db.session.commit()
            res = True
        except Exception as e:
            import logging
            logging.error(e)

    return res


def change_status(node_id, status):
    try:
        node = db.session.query(TreeNode).filter(TreeNode.id == node_id).first()

        if int(status) == 0:
            node.status = 0
            to_rep = '_b.ico'
            if '_y.ico' in node.icon:
                to_rep = '_y.ico'
            node.icon = node.icon.replace(to_rep, '_r.ico')
        elif int(status) == 2:
            node.status = 0
            to_rep = '_b.ico'
            if '_r.ico' in node.icon:
                to_rep = '_r.ico'
            node.icon = node.icon.replace(to_rep, '_y.ico')
        elif int(status) == 1:
            node.status = 1
            to_rep = '_r.ico'
            if '_y.ico' in node.icon:
                to_rep = '_y.ico'
            node.icon = node.icon.replace(to_rep, '_b.ico')

        db.session.commit()
        res = node.icon
    except Exception as e:
        import logging
        logging.error(e)
        res = None

    return res


def join_node(node_id, to_join):
    try:
        res = []
        ids = json.loads(to_join)

        for id in ids:
            node = db.session.query(TreeNode).filter(TreeNode.id == id).first()
            db.session.delete(node)
            db.session.commit()
            res.append(id)

    except Exception as e:
        import logging
        logging.error(e)
        res = None

    return res


# copy node tree
def copy_node(node_id, parent_id):
    try:
        node = db.session.query(TreeNode).filter(TreeNode.id == node_id).first()
        db.session.expunge(node)

        make_transient(node)
        node.id = None
        node.parent_id = parent_id
        # print(node.text)
        node.text = node.text + 'Copy'
        if get_locale() is not node.get_locale():
            node.translations[node.get_locale()].text = node.text + 'Copy'

        db.session.add(node)
        db.session.commit()
        db.session.flush()

        res = node.id
    except Exception as e:
        import logging
        logging.error(e)
        res = None

    return res


def render_tree_li(tree):
    data = "<li data-jstree='"
    opened = "true" if tree.opened else "false"
    data += "\"openend\" : " + opened
    selected = "true" if tree.selected else "false"
    data += ",\"selected\" : " + selected
    disabled = "true" if tree.disabled else "false"
    data += ",\"disabled\" : " + disabled
    data += ",\"type\" : \"" + tree.type + "\""
    data += ",\"icon\" : \"" + tree.icon + "\"}'"
    if tree.tooltip is not None:
        data += " title=\"" + tree.tooltip + "\""
    data += " id=\"" + str(tree.id) + "\">" + tree.text

    return data


def create_tree(tree):
    data = render_tree_li(tree)
    if tree.children:
        data += "<ul>"
        for chd in tree.children:
            if tree.children[chd].children:
                data += create_tree(tree.children[chd])
            else:
                data += render_tree_li(tree.children[chd])
                data += "</li>"
        data += "</ul>"
    data += "</li>"
    return data


@app.template_filter('render_tree')
def render_tree_filter(tree):
    data = "<ul>"
    data += create_tree(tree)
    data += "</ul>"

    return data


def get_equipment_type_to_url():
    return json.dumps({
        'air_breaker': AirCircuitBreaker.__name__.lower(),
        'bushing': Bushing.__name__.lower(),
        'capacitor': Capacitor.__name__.lower(),
        'breaker': Breaker.__name__.lower(),
        'powersource': PowerSource.__name__.lower(),
        'cable': Cable.__name__.lower(),
        'switchgear': SwitchGear.__name__.lower(),
        'induction_machine': InductionMachine.__name__.lower(),
        'synchronous_machine': SynchronousMachine.__name__.lower(),
        'tap_changer': LoadTapChanger.__name__.lower(),
        'rectifier': Rectifier.__name__.lower(),
        'transformer': Transformer.__name__.lower(),
        'tank': Tank.__name__.lower(),
        'switch': Switch.__name__.lower(),
        'inductance': Inductance.__name__.lower(),
        'resistance': NeutralResistance.__name__.lower(),
        'gas_sensor': GasSensor.__name__.lower(),
    })

class GraphData:
    def __init__(self, equipment_id = 0):
        self.gases = {'h2', 'o2', 'n2', 'co', 'ch4', 'co2', 'c2h2', 'c2h4', 'c2h6', 'cap_gaz', 'content_gaz','dielectric_1816', 'dielectric_1816_2', 'dielectric_877',
        'dielectric_iec_156', 'acidity', 'color', 'ift', 'density', 'pf20c', 'pf100c', 'sludge', 'aniline_point', 'viscosity', 'flash_point', 'pour_point', 'inhibitor',
        'water', 'aroclor_1242', 'aroclor_1254', 'aroclor_1260', 'hmf', 'fol', 'fal', 'acf', 'mef'}

        self.equipment_id = equipment_id
        self.graph_data = []

    def load_from_db(self):
        db.session.execute("SET datestyle = dmy;")
        self.query = db.session.query(Graph)
        if self.equipment_id > 0:
            self.query = self.query.filter(Graph.equipment_id.in_(self.equipment_id))
        self.query = self.query.order_by(Graph.date_analyse.asc(), Graph.equipment_id.asc())
    
    def group_by_equipment(self):
        tests = {}
        for record in self.query:
            equipment = record.equipment
            if equipment.id not in tests:
                tests[equipment.id] = {
                    'obj': [],
                    'equipment': equipment.equipment_number.encode('utf-8')
                }
            tests[equipment.id]['obj'].append(record)
        return tests

    def group_by_gases(self, tests):
        for equipment_id, data in tests.items():
            test_objs = data['obj']
            equipment = data['equipment']
            for gas in self.gases:
                records = []
                test_name = ""
                for record in test_objs:
                    if isinstance(record.date_analyse, datetime.datetime) and getattr(record, gas):
                        records.append({"day":record.date_analyse.strftime('%Y.%m.%d'), "count":getattr(record, gas)})
                        test_name = record.test_name

                if len(records) > 0:
                    self.graph_data.append({"data": records, "label": "{} {}".format(gas.upper(), equipment), "test_name" : test_name})


    def group_by_test(self,data):
        final = {}
        for record in data:
            if record['test_name'] not in final:
                final[record['test_name']] = []
            final[record['test_name']].append(record)    
        return final  

    def fetch(self):
        self.load_from_db()
        tests = self.group_by_equipment()
        self.group_by_gases(tests=tests)
        self.graph_data = sorted(self.graph_data, key=lambda k: k['label']) 
        graph_data = self.group_by_test(self.graph_data)
        return graph_data

    def search(self, params):
        self.load_from_db()
        for key, param in params.viewitems():
            if key == 'date':
                self.query = self.query.filter(Graph.date_analyse==param)
            # need to change DB view for searching
            #if key == 'campaignId':
            #    self.query = self.query.filter(TestResult.campaign_id==param)
            #if key == 'testId':
            #    self.query = self.query.filter(TestResult.id==param)
        tests = self.group_by_equipment()
        self.group_by_gases(tests=tests)
        return self.graph_data
