#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from .forms import *
from app.admin.views import MyModelView
from flask.ext import login
from .models import *
from app.users.models import User
from flask.ext.admin.contrib.sqla.view import func
from wtforms import HiddenField
from wtforms.fields import TextField
from flask_admin.form import Select2Field
from flask import g
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import class_mapper
from flask_admin.actions import action
from flask import flash
from flask.ext.babel import gettext

from flask.ext.admin.contrib.sqla.ajax import QueryAjaxModelLoader

class myQueryAjaxLoader(QueryAjaxModelLoader):
    def get_list(self, term, offset=0, limit=10):
        filters = list(
            field.ilike(u'%%%s%%' % term) for field in self._cached_fields
        )
        filters.append(Campaign.group_id == g.user.group_id)
        query = db.session.query(self.model).join(Campaign).filter(*filters).offset(offset).limit(limit)
        return query.all()

class equipmentAjaxLoader(QueryAjaxModelLoader):
    def get_list(self, term, offset=0, limit=10):
        filters = list(
            field.ilike(u'%%%s%%' % term) for field in self._cached_fields
        )
        filters.append(Equipment.group_id == g.user.group_id)
        query = db.session.query(self.model).filter(*filters).offset(offset).limit(limit)
        return query.all()

class userAjaxLoader(QueryAjaxModelLoader):
    def get_list(self, term, offset=0, limit=10):
        filters = list(
            field.ilike(u'%%%s%%' % term) for field in self._cached_fields
        )
        filters.append(User.group_id == g.user.group_id)
        query = db.session.query(self.model).filter(*filters).offset(offset).limit(limit)
        return query.all()


class EquipmentView(MyModelView):
    """
    Equipment management view
    """
    # Visible columns in the list view
    column_list = (
        'equipment_number', 'equipment_type', 'location',
    )
    # List of columns that can be sorted.
    column_sortable_list = (
        'id', 'equipment_number', 'equipment_type', 'location_id',
        'status', 'tie_status'
    )

    column_searchable_list = ('equipment_number',)

    column_hide_backrefs = False

    form_excluded_columns = (
        # 'id',
        # 'location_id',
        'sibling',
        'modifier',
        'status',
    )
    column_exclude_list = [
        'sibling',
        'modifier'
    ]

    form_widget_args = {
        'frequency': {
            'style': 'width: 100px'
        },
        'manufactured': {
            'style': 'width: 100px'
        },
    }

    form_choices = {
        'manufactured': [(int(x), x) for x in range(1900, datetime.now().year + 1)]
    }
    form_args = {
        'manufactured': {'coerce': int}
    }

    form_ajax_refs = {
        'manufacturer': {'fields': (Manufacturer.name,)},
        'location': {'fields': (Location.name,)},
        'norm_isolation_data': {'fields': (NormIsolationData.name,)},
        'norm_furan_data': {'fields': (NormFuranData.name,)},
        'norm_particles_data': {'fields': (NormParticlesData.name,)},
        'norm_physic_data': {'fields': (NormPhysicData.name,)},
        'norm_gas_data': {'fields': (NormGasData.name,)},
    }
    
    column_exclude_list = ('group_id')
    form_overrides = dict(
        group_id=HiddenField
    )

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(self.model).filter(self.model.group_id==g.user.group_id)
        else:
            return super(EquipmentView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(func.count('*')).filter(self.model.group_id==g.user.group_id)
        else:
            return super(EquipmentView, self).get_count_query()
    
    def create_form(self):
        form = super(MyModelView, self).create_form()
        form.group_id.data = g.user.group_id
        return form

    def scaffold_form(self):
        form_class = super(EquipmentView, self).scaffold_form()
        form_class.prev_serial_number = TextField('Prev Serial Number')
        form_class.serial = TextField('Serial')
        return form_class
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False
    def __init__(self, dbsession):
        super(EquipmentView, self).__init__(Equipment, dbsession, name="Equipment", category="Equipment")
#


class NormFuranView(MyModelView):
    """
    NormFuran management view
    """
    # Visible columns in the list view
    column_hide_backrefs = False
    # form_excluded_columns = (
    # )
    # column_exclude_list = [
    # ]

    # # List of columns that can be sorted.
    column_sortable_list = ('name',)
    column_searchable_list = ('name',)

    def is_accessible(self):
        """ Can create and edit norm tables """
        if login.current_user.is_authenticated():
            return login.current_user.has_role('expert')

        return False

    def __init__(self, dbsession):
        super(NormFuranView, self).__init__(
            NormFuran, dbsession, name="Norms furan", category="Norms"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class NormIsolationView(MyModelView):
    """
    NormIsolation management view
    """
    # Visible columns in the list view
    column_hide_backrefs = False
    # form_excluded_columns = (
    # )
    # column_exclude_list = [
    # ]

    # # List of columns that can be sorted.
    column_sortable_list = ('c', 'f', 'notseal', 'seal')
    column_searchable_list = ('c', 'f')

    def is_accessible(self):
        """ Can create and edit norm tables """
        if login.current_user.is_authenticated():
            return login.current_user.has_role('expert')

        return False

    def __init__(self, dbsession):
        super(NormIsolationView, self).__init__(
            NormIsolation, dbsession, name="Norms isolation", category='Norms'
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class NormPhysicView(MyModelView):
    """
    NormPhysic management view
    """
    # Visible columns in the list view
    column_hide_backrefs = False
    # form_excluded_columns = (
    # )
    # column_exclude_list = [
    # ]

    # # List of columns that can be sorted.
    column_sortable_list = ('name',)
    column_searchable_list = ('name',)

    def is_accessible(self):
        """ Can create and edit norm tables """
        if login.current_user.is_authenticated():
            return login.current_user.has_role('expert')

        return False

    def __init__(self, dbsession):
        super(NormPhysicView, self).__init__(
            NormPhysic, dbsession, name="Norms physic", category='Norms'
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class NormGasView(MyModelView):
    """
    NormGasView management view
    """
    # Visible columns in the list view
    column_hide_backrefs = False
    # form_excluded_columns = (
    # )
    # column_exclude_list = [
    # ]

    # # List of columns that can be sorted.
    column_sortable_list = ('name',)
    column_searchable_list = ('name',)

    def is_accessible(self):
        """ Can create and edit norm tables """
        if login.current_user.is_authenticated():
            return login.current_user.has_role('expert')

        return False

    def __init__(self, dbsession):
        super(NormGasView, self).__init__(
            NormGas, dbsession, name="Norms gas", category="Norms"
        )


class NormParticlesView(MyModelView):
    column_searchable_list = ('name',)

    def __init__(self, dbsession):
        super(NormParticlesView, self).__init__(
            NormParticles, dbsession, name="Norms gas", category="Norms"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class ManufacturerView(MyModelView):
    """
    Manufacturer management view
    """
    # Visible columns in the list view
    column_hide_backrefs = True

    # # List of columns that can be sorted.
    column_sortable_list = ('name',)
    column_searchable_list = ('name',)

    # inline_models = (GasSensor, Transformer, Breaker, AirCircuitBreaker, Capacitor, PowerSource, SwitchGear, Tank,
    #                  InductionMachine, SynchronousMachine, Rectifier, LoadTapChanger, Bushing, NeutralResistance,
    #                  Switch, Cable,
    #                  )

    def __init__(self, dbsession):
        super(ManufacturerView, self).__init__(
            Manufacturer, dbsession, name="Manufacturer", category="Options"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class FluidTypeView(MyModelView):
    """
    Manufacturer management view
    """
    # Visible columns in the list view
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    column_sortable_list = ('name',)
    column_searchable_list = ('name',)

    # inline_models = (Transformer, Campaign)

    def __init__(self, dbsession):
        super(FluidTypeView, self).__init__(
            FluidType, dbsession, name="Fluid type", category="Types"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class AirCircuitBreakerView(MyModelView):
    """
    Airbreaker management view
    """
    # Visible columns in the list view
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(AirCircuitBreakerView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(AirCircuitBreakerView, self).get_count_query()

    def __init__(self, dbsession):
        super(AirCircuitBreakerView, self).__init__(
            AirCircuitBreaker, dbsession,
            name="Air circuit breaker", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class BushingView(MyModelView):
    column_hide_backrefs = False
    column_list = ('id')
    form_ajax_refs = {
        'mfr_h1': {'fields': (Manufacturer.name,)},
        'mfr_h2': {'fields': (Manufacturer.name,)},
        'mfr_h3': {'fields': (Manufacturer.name,)},
        'mfr_hn': {'fields': (Manufacturer.name,)},
        'mfr_x1': {'fields': (Manufacturer.name,)},
        'mfr_x2': {'fields': (Manufacturer.name,)},
        'mfr_x3': {'fields': (Manufacturer.name,)},
        'mfr_xn': {'fields': (Manufacturer.name,)},
        'mfr_t1': {'fields': (Manufacturer.name,)},
        'mfr_t2': {'fields': (Manufacturer.name,)},
        'mfr_t3': {'fields': (Manufacturer.name,)},
        'mfr_tn': {'fields': (Manufacturer.name,)},
        'mfr_q1': {'fields': (Manufacturer.name,)},
        'mfr_q2': {'fields': (Manufacturer.name,)},
        'mfr_q3': {'fields': (Manufacturer.name,)},
        'mfr_qn': {'fields': (Manufacturer.name,)},
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(BushingView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(BushingView, self).get_count_query()

    def __init__(self, dbsession):
        super(BushingView, self).__init__(
            Bushing, dbsession, name="Bushing", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class CableView(MyModelView):
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(CableView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(CableView, self).get_count_query()

    def __init__(self, dbsession):
        super(CableView, self).__init__(
            Cable, dbsession, name="Cable", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class CapacitorView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(CapacitorView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(CapacitorView, self).get_count_query()

    def __init__(self, dbsession):
        super(CapacitorView, self).__init__(
            Capacitor, dbsession, name="Capacitor", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class RectifierView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    # form_widget_args = {
    #     'phase_number': {
    #         'style': 'width: 50px'
    #     },
    # }

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(RectifierView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(RectifierView, self).get_count_query()

    def __init__(self, dbsession):
        super(RectifierView, self).__init__(
            Rectifier, dbsession, name="Rectifier", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class InductanceView(MyModelView):
    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(InductanceView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(InductanceView, self).get_count_query()

    def __init__(self, dbsession):
        super(InductanceView, self).__init__(
            Inductance, dbsession, name="Inductance", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class NeutralResistanceView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(NeutralResistanceView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(NeutralResistanceView, self).get_count_query()
          

    def __init__(self, dbsession):
        super(NeutralResistanceView, self).__init__(
            NeutralResistance, dbsession, name="Neutral resistance", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class TankView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(TankView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(TankView, self).get_count_query()

    def __init__(self, dbsession):
        super(TankView, self).__init__(
            Tank, dbsession, name="Tank", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class LoadTapChangerView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(LoadTapChangerView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(LoadTapChangerView, self).get_count_query()

    def __init__(self, dbsession):
        super(LoadTapChangerView, self).__init__(
            LoadTapChanger, dbsession, name="Tap changer", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class BreakerView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(BreakerView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(BreakerView, self).get_count_query()

    def __init__(self, dbsession):
        super(BreakerView, self).__init__(
            Breaker, dbsession, name="Breaker", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class SwitchView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(SwitchView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(SwitchView, self).get_count_query()

    def __init__(self, dbsession):
        super(SwitchView, self).__init__(
            Switch, dbsession, name="Switch", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class SwitchGearView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(SwitchGearView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(SwitchGearView, self).get_count_query()

    def __init__(self, dbsession):
        super(SwitchGearView, self).__init__(
            SwitchGear, dbsession, name="Switch gear", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class SynchronousMachineView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(SynchronousMachineView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(SynchronousMachineView, self).get_count_query()

    def __init__(self, dbsession):
        super(SynchronousMachineView, self).__init__(
            SynchronousMachine, dbsession,
            name="Synchronous machine", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class InductionMachineView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(InductionMachineView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(InductionMachineView, self).get_count_query()

    def __init__(self, dbsession):
        super(InductionMachineView, self).__init__(
            InductionMachine, dbsession,
            name="Induction machine", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class GasSensorView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False
    inline_models = (Transformer,)

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
        'manufacturer': {'fields': (Manufacturer.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(GasSensorView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(GasSensorView, self).get_count_query()

    def __init__(self, dbsession):
        super(GasSensorView, self).__init__(
            GasSensor, dbsession, name="Gas sensor", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

def copy_sqla_object(obj, omit_fk=True):
    """
    Given an SQLAlchemy object, creates a new object (FOR WHICH THE OBJECT
    MUST SUPPORT CREATION USING __init__() WITH NO PARAMETERS), and copies
    across all attributes, omitting PKs, FKs (by default), and relationship
    attributes.
    """
    cls = type(obj)
    mapper = class_mapper(cls)
    newobj = cls()  # not: cls.__new__(cls)
    pk_keys = set([c.key for c in mapper.primary_key])
    rel_keys = set([c.key for c in mapper.relationships])
    prohibited = pk_keys | rel_keys
    if omit_fk:
        fk_keys = set([c.key for c in mapper.columns if c.foreign_keys])
        prohibited = prohibited | fk_keys
    for k in [p.key for p in mapper.iterate_properties
              if p.key not in prohibited]:
        try:
            value = getattr(obj, k)
            setattr(newobj, k, value)
        except AttributeError:
            pass
    return newobj

class TransformerView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False
    list_template = 'admin/diagnostic/transformer.html'

    @action('clone_obj', 'Clone', 'Are you sure you want to clone ?')
    def clone_obj(self, ids):
        try:
            query = Transformer.query.filter(Transformer.id.in_(ids))

            count = 0
            for transformer in query.all():
                new_transformer = copy_sqla_object(transformer, omit_fk=False)
                self.session.add(new_transformer)
                self.session.commit()
                if new_transformer.gas_sensor is not None:
                    new_transformer.gas_sensor = copy_sqla_object(new_transformer.gas_sensor,omit_fk=False)
                new_transformer.equipment = copy_sqla_object(new_transformer.equipment,omit_fk=False)
                self.session.commit()

            flash(gettext('Transformer was cloned'))
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext('Failed to clone transformer. %(error)s', error=str(ex)), 'error')

    column_list = (
        'id', 'fluid_type',
        'gassensor_id', 'phase_number', 'sealed',
        'welded_cover', 'windings', 'fluid_volume',
        'autotransformer'
    )


    form_widget_args = {
        'phase_number': {
            'style': 'width: 50px'
        },
    }

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(TransformerView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(TransformerView, self).get_count_query()

    def __init__(self, dbsession):
        super(TransformerView, self).__init__(
            Transformer, dbsession, name="Transformer", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class LocationView(MyModelView):
    can_view_details = True
    column_hide_backrefs = False

    column_searchable_list = ('name',)
    column_sortable_list = ('id', 'name')
    
    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    column_exclude_list = ('group_id')
    form_overrides = dict(
        group_id=HiddenField
    )
    form_excluded_columns = ('children', 'equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(self.model).filter(self.model.group_id==g.user.group_id)
        else:
            return super(LocationView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(func.count('*')).filter(self.model.group_id==g.user.group_id)
        else:
            return super(LocationView, self).get_count_query()
    
    
    def create_form(self):
        form = super(MyModelView, self).create_form()
        form.group_id.data = g.user.group_id
        return form

    # inline_models = (Equipment,)
    def __init__(self, dbsession):
        super(LocationView, self).__init__(
            Location, dbsession, name="Location", category="Options"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class LabView(MyModelView):
    """
    Lab management view
    """
    # Visible columns in the list view
    # can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    column_sortable_list = (['name', 'code', 'analyser'])
    column_searchable_list = (['name', 'code', 'analyser'])

    # inline_models = (Campaign,)

    form_ajax_refs = {
        'test_result': myQueryAjaxLoader(
            'test_result',
            db.session,
            TestResult,
            fields=['remark'],
            page_size=10
        ),
    }

    def __init__(self, dbsession):
        super(LabView, self).__init__(
            Lab, dbsession, name="Laboratory", category="Campaign"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class CampaignView(MyModelView):
    """
    Campaign management view
    """
    create_modal = False
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = True

    # # List of columns that can be sorted.
    # column_sortable_list = (['equipment_id', 'lab_id', 'date', 'contract_id'])
    column_searchable_list = (['date_created', 'contract_id'])
    # inline_models = (TestResult,)
    # column_editable_list = ['created_by']

    form_excluded_columns = (
        # 'id',
        # 'location_id',z
        # 'if_rem',
        # 'if_ok',
        # 'sibling',
        # 'modifier',
        # 'data_valid',
        # 'status1',
        # 'status2',
        # 'error_state',
        # 'error_code',
    )
    column_list = (
        'date_created',
        # 'analysis_number',
        # 'equipment',
        # 'fluid_type',
        'created_by',
        # 'performed_by',
        # 'lab',
        # 'repair_date',
    )
    column_filters = [
        'date_created',
        # 'analysis_number',
        # 'equipment',
        # 'fluid_type',
        'created_by',
        # 'performed_by',
        # 'lab',
        # 'repair_date',
    ]
    form_ajax_refs = {
        'created_by': {'fields': (User.name,)},
        # 'performed_by': {'fields': (User.name,)},
        # 'recommended_by': {'fields': (User.name,)},
        # 'recommendation': {'fields': (Recommendation.name,)},
        # 'equipment': {'fields': (Equipment.equipment_number,)},
        # 'material': {'fields': (Material.name,)},
        # 'fluid_type': {'fields': (FluidType.name,)},
        # 'lab': {'fields': (Lab.name,)},
        'contract': {'fields': (Contract.name,)},
        'test_result': {'fields': (TestResult.remark,)},
        # 'lab_contract': {'fields': (Contract.name,)},
    }

    form_args = {
        'date_prelevement': {
            'label': 'Date of Sampling',
        }
    }
    column_exclude_list = ('group_id')
    form_overrides = dict(
        group_id=HiddenField
    )

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(self.model).filter(self.model.group_id==g.user.group_id)
        else:
            return super(CampaignView, self).get_query()

    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(func.count('*')).filter(self.model.group_id==g.user.group_id)
        else:
            return super(CampaignView, self).get_count_query()

    def __init__(self, dbsession):
        super(CampaignView, self).__init__(
            Campaign, dbsession, name="Campaigns", category="Campaign",
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False


class ContractView(MyModelView):
    """
    Contract management view
    """
    # Visible columns in the list view
    # can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    # column_sortable_list = ()
    column_searchable_list = (['name', 'code', 'contract_status_id'])
    column_exclude_list = ('group_id')
    form_overrides = dict(
        group_id=HiddenField
    )

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(self.model).filter(self.model.group_id==g.user.group_id)
        else:
            return super(ContractView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(func.count('*')).filter(self.model.group_id==g.user.group_id)
        else:
            return super(ContractView, self).get_count_query()
    
    def create_form(self):
        form = super(MyModelView, self).create_form()
        form.group_id.data = g.user.group_id
        return form

    def __init__(self, dbsession):
        super(ContractView, self).__init__(
            Contract, dbsession, name="Contract", category="Campaign"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class FluidProfileView(MyModelView):
    """
    FluidProfile management view
    """
    # Visible columns in the list view
    # can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    # column_sortable_list = (['name'])
    column_searchable_list = (['name'])
    column_exclude_list = (['description'])
    column_labels = {'qty_ser': 'Qty Syringe', 'pf': 'Pf 20', 'point': 'Pour Point'}

    def __init__(self, dbsession):
        super(FluidProfileView, self).__init__(
            FluidProfile, dbsession, name="Fluid profile", category="Campaign"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class TestTypeView(MyModelView):
    """
    TestType management view
    """
    # Visible columns in the list view
    # can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    # column_sortable_list = (['name', 'group_id', 'is_group'])
    column_searchable_list = (['name', 'group_id', 'is_group'])

    # inline_models = (TestResult,)
    form_excluded_columns = ('test_result')
    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
        'test_repair_note': {'fields': (TestRepairNote.remark,)},
        'test_diagnosis': {'fields': (TestDiagnosis.diagnosis_notes,)},
        'test_recommendation': {'fields': (TestRecommendation.recommendation_notes,)},
    }

    def __init__(self, dbsession):
        super(TestTypeView, self).__init__(
            TestType, dbsession, name="Test type", category="Types"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class InhibitorTypeView(MyModelView):
    """
       InhibitorType management view
       """
    # Visible columns in the list view
    # can_view_details = True
    # column_hide_backrefs = False

    # # List of columns that can be sorted.
    column_sortable_list = (['name'])
    column_searchable_list = (['name'])

    def __init__(self, dbsession):
        super(InhibitorTypeView, self).__init__(
            InhibitorType, dbsession, name="Inhibitor type", category="Types"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class TestResultView(MyModelView):
    """
    TestResult management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    # List of columns that can be sorted.
    column_sortable_list = ('date_analyse', 'test_reason_id', 'test_type_id',
                            'test_status', 'sampling_point_id', 'campaign_id')
    column_searchable_list = ('date_analyse', 'test_reason_id', 'test_type_id',
                              'test_status_id', 'sampling_point_id', 'campaign_id')

    # inline_models = (BushingTest, WindingTest, VisualInspectionTest, InsulationResistanceTest, PolymerisationDegreeTest,
    #                  TransformerTurnRatioTest, WindingResistanceTest, DissolvedGasTest, WaterTest, FuranTest,
    #                  InhibitorTest, PCBTest, ParticleTest, MetalsInOilTest, FluidTest
    #                  )
    form_excluded_columns = ('bushing_test', 'winding_test', 'insulation_resistance_test',
                             'polymerisation_degree_test', 'transformer_turn_ratio_test',
                             'winding_resistance_test', 'dissolved_gas_test',
                             'furan_test', 'pcb_test',
                             'particle_test', 'metals_in_oil_test', 'fluid_test',)
    form_ajax_refs = {
        'campaign': {'fields': (Campaign.description,)},
        'sampling_point': {'fields': (SamplingPoint.name,)},
        'equipment': {'fields': (Equipment.name,)},
        'lab_contract': {'fields': (Contract.name,)},
        'test_recommendation': {'fields': (TestRecommendation.recommendation_notes,)},
        'test_repair_note': {'fields': (TestRepairNote.remark,)},
        'test_diagnosis': {'fields': (TestDiagnosis.diagnosis_notes,)},
        'visual_inspection_test': {'fields': (VisualInspectionTest.notes,)},
        'water_test': {'fields': (WaterTest.remark,)},
        'inhibitor_test': {'fields': (InhibitorTest.remark,)},
    }
    
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.campaign_id.in_(e_ids))
        else:
            return super(TestResultView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.campaign_id.in_(e_ids))
        else:
            return super(TestResultView, self).get_count_query()

    def __init__(self, dbsession):
        super(TestResultView, self).__init__(
            TestResult, dbsession, name="Test result", category="Campaign"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class EquipmentTypeView(MyModelView):
    """
    EquipmentType management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    column_sortable_list = ('name', 'code')
    column_searchable_list = ('name', 'code')

    # inline_models = (Equipment,)

    def __init__(self, dbsession):
        super(EquipmentTypeView, self).__init__(
            EquipmentType, dbsession, name="Equipment type", category="Types"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class ElectricalProfileView(MyModelView):
    """
    ElectricalProfile management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    # column_sortable_list = ('name', 'description', 'bushing', 'winding', 'winding_double',
    #                         'insulation', 'visual', 'resistance', 'degree', 'turns')
    column_searchable_list = ('name', 'description', 'bushing', 'winding', 'insulation_pf',
                              'insulation', 'visual', 'resistance', 'degree', 'turns')

    # form_args = {'winding_double': {'label': 'Winding Doble', }}
    column_labels = {'insulation_pf': 'Insulation PF'}

    def __init__(self, dbsession):
        super(ElectricalProfileView, self).__init__(
            ElectricalProfile, dbsession, name="Electrical profile", category="Campaign"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class MaterialView(MyModelView):
    """
    Material management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    column_sortable_list = ('name', 'code')
    column_searchable_list = ('name', 'code')

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    # inline_models = (Campaign,)

    def __init__(self, dbsession):
        super(MaterialView, self).__init__(
            Material, dbsession, name="Material", category="Options"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class PowerSourceView(MyModelView):
    """
    PowerSource management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    form_ajax_refs = {
        'equipment': {'fields': (Equipment.name,)},
    }
    form_excluded_columns = ('equipment')
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(PowerSourceView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(PowerSourceView, self).get_count_query()

    def __init__(self, dbsession):
        super(PowerSourceView, self).__init__(
            PowerSource, dbsession, name="Power source", category="Equipment"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class NormView(MyModelView):
    """
    Norm management view
    """
    # Visible columns in the list view
    column_hide_backrefs = True
    can_view_details = True

    # # List of columns that can be sorted.
    column_sortable_list = ('name', )
    column_searchable_list = ('name', 'name', 'table_name')

    def is_accessible(self):
        """ Can create and edit norm tables """
        if login.current_user.is_authenticated():
            return login.current_user.has_role('expert')

        return False

    def __init__(self, dbsession):
        super(NormView, self).__init__(
            Norm, dbsession, name="Norm", category="Norms"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class RecommendationView(MyModelView):
    """
    Recommendation management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    # column_sortable_list = ('name', 'serial', 'manufacturer')
    column_searchable_list = ('name', 'code', 'description')

    # inline_models = (Campaign,)
    form_ajax_refs = {
        'test_recommendation': {'fields': (TestRecommendation.recommendation_notes,)},
    }

    def __init__(self, dbsession):
        super(RecommendationView, self).__init__(
            Recommendation, dbsession, name="Recommendation", category="Types"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class SyringeView(MyModelView):
    """
    Syringe management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    # column_sortable_list = ('name', 'serial', 'manufacturer')
    # column_sortable_list = ('name', 'serial', 'manufacturer')
    column_searchable_list = ('lab_id',)
    column_formatters = dict(_serial=lambda v, c, m, p: m.serial)

    def scaffold_form(self):
        form_class = super(SyringeView, self).scaffold_form()
        form_class.serial = TextField('Serial')
        return form_class

    def __init__(self, dbsession):
        super(SyringeView, self).__init__(
            Syringe, dbsession, name="Syringe", category="Types"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class TestStatusView(MyModelView):
    """
    TestStatus management view
    """
    # Visible columns in the list view
    # can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    column_sortable_list = (['name', 'code'])
    column_searchable_list = (['name', 'code'])
    form_excluded_columns = ('test_result')
    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def __init__(self, dbsession):
        super(TestStatusView, self).__init__(
            TestStatus, dbsession, name="Test status", category="Statuses"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False


class CampaignStatusView(MyModelView):
    """
    CampaignStatus management view
    """
    # Visible columns in the list view
    # can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    column_sortable_list = (['name', 'code'])
    column_searchable_list = (['name', 'code'])

    def __init__(self, dbsession):
        super(CampaignStatusView, self).__init__(
            CampaignStatus, dbsession, name="Campaign status", category="Statuses"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class TestScheduleView(MyModelView):
    """
    TestSchedule management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    # # List of columns that can be sorted.
    # column_sortable_list = ('equipment', 'start_date', 'assigned_to', 'description')
    column_searchable_list = ('date_start', 'assigned_to_id', 'description')

    form_ajax_refs = {
        'test_recommendation': {'fields': (TestRecommendation.recommendation_notes,)},
        'assigned_to': {'fields': (User.name,)},
    }

    def __init__(self, dbsession):
        super(TestScheduleView, self).__init__(
            TestSchedule, dbsession, name="Test schedule", category="Statuses"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') 
        return False

class TaskStatusView(MyModelView):
    """
    TaskStatus management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    def __init__(self, dbsession):
        super(TaskStatusView, self).__init__(
            TaskStatus, dbsession, name="Task status", category="Statuses"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class MySimpleView(MyModelView):
    """
    Simple models management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    # List of columns that can be sorted.
    column_sortable_list = ('name',)
    column_searchable_list = ('name',)
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class MySimpleTypesView(MySimpleView):
    def __init__(self, model_class, dbsession, **kvargs):
        super(MySimpleTypesView, self).__init__(
            model_class, dbsession, category="Types", **kvargs
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class TestReasonView(MySimpleTypesView):
    """
    TestReason management view
    """

    # inline_models = (TestResult,)
    form_excluded_columns = ('test_result')
    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def __init__(self, dbsession):
        super(TestReasonView, self).__init__(
            TestReason, dbsession, name="Test reason"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class PressureUnitView(MySimpleTypesView):
    """
    PressureUnit management view
    """

    def __init__(self, dbsession):
        super(PressureUnitView, self).__init__(
            PressureUnit, dbsession, name="Pressure unit"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class GasRelayView(MySimpleTypesView):
    """
    GasRelay management view
    """

    def __init__(self, dbsession):
        super(GasRelayView, self).__init__(
            GasRelay, dbsession, name="Gas relay"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class SamplingPointView(MySimpleTypesView):
    """
    SamplingPoint management view
    """

    # inline_models = (TestResult,)
    form_excluded_columns = ('test_result')
    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def __init__(self, dbsession):
        super(SamplingPointView, self).__init__(
            SamplingPoint, dbsession, name="Sampling point"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class EquipmentConnectionView(MySimpleView):
    """
    EquipmentConnection management view
    """
    # List of columns that can be sorted.
    column_sortable_list = ()
    column_searchable_list = ()

    form_ajax_refs = {
        'equipment': equipmentAjaxLoader(
            'equipment',
            db.session,
            Equipment,
            fields=['name'],
            page_size=10
        ),
        'parent': equipmentAjaxLoader(
            'parent',
            db.session,
            Equipment,
            fields=['name'],
            page_size=10
        )
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(EquipmentConnectionView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(EquipmentConnectionView, self).get_count_query()

    def __init__(self, dbsession):
        super(EquipmentConnectionView, self).__init__(
            EquipmentConnection, dbsession, category="Equipment", name="Equipment connection"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class SiblingView(MySimpleView):
    """
    Sibling management view
    """
    # List of columns that can be sorted.
    column_sortable_list = ()
    column_searchable_list = ()

    form_ajax_refs = {
        'equipment': equipmentAjaxLoader(
            'equipment',
            db.session,
            Equipment,
            fields=['name'],
            page_size=10
        ),
        'sibling': equipmentAjaxLoader(
            'sibling',
            db.session,
            Equipment,
            fields=['name'],
            page_size=10
        )
    }
    
    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(self.model).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(SiblingView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Equipment).filter(Equipment.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).filter(self.model.equipment_id.in_(e_ids))
        else:
            return super(SiblingView, self).get_count_query()

    def __init__(self, dbsession):
        super(SiblingView, self).__init__(
            Sibling, dbsession, category="Equipment", name="Sibling"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

# class SamplingCardView(MySimpleView):
#     """
#     SamplingCard management view
#     """
#     # List of columns that can be sorted.
#     column_sortable_list = ()
#     column_searchable_list = ()
#
#     def __init__(self, dbsession):
#         super(SamplingCardView, self).__init__(
#             SamplingCard, dbsession, category="Campaign", name="Sampling card"
#         )


class TestRecommendationView(MySimpleView):
    """
    TestRecommendation management view
    """
    # List of columns that can be sorted.
    column_sortable_list = ()
    column_searchable_list = ()

    form_ajax_refs = {
        'user': userAjaxLoader(
            'user',
            db.session,
            User,
            fields=['name'],
            page_size=10
        ),
        'test_result': myQueryAjaxLoader(
            'test_result',
            db.session,
            TestResult,
            fields=['remark'],
            page_size=10
        ),
        'recommendation': {'fields': (Recommendation.name,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(self.model).outerjoin(self.model.user).filter(User.group_id==g.user.group_id)
        else:
            return super(TestRecommendationView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            return self.session.query(func.count('*')).outerjoin(self.model.user).filter(User.group_id==g.user.group_id)
        else:
            return super(TestRecommendationView, self).get_count_query()

    def __init__(self, dbsession):
        super(TestRecommendationView, self).__init__(
            TestRecommendation, dbsession, category="Types", name="Test recommendation"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class InterruptingMediumView(MySimpleTypesView):
    def __init__(self, dbsession):
        super(InterruptingMediumView, self).__init__(
            InterruptingMedium, dbsession, name="Interrupting medium"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class InsulationView(MySimpleTypesView):
    def __init__(self, dbsession):
        super(InsulationView, self).__init__(
            Insulation, dbsession, name="Insulation"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class BreakerMechanismView(MySimpleTypesView):
    """
    Downstream management view
    """

    def __init__(self, dbsession):
        super(BreakerMechanismView, self).__init__(
            BreakerMechanism, dbsession, name="Breaker mechanism"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
        else:
            self.can_create = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class MySimpleConditionsView(MySimpleView):
    def __init__(self, model_class, dbsession, **kvargs):
        super(MySimpleConditionsView, self).__init__(
            model_class, dbsession, category="Conditions", **kvargs
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class PumpConditionView(MySimpleConditionsView):
    """
    PumpCondition management view
    """

    def __init__(self, dbsession):
        super(PumpConditionView, self).__init__(
            PumpCondition, dbsession, name="Pump condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class ValveConditionView(MySimpleConditionsView):
    """
    ValveCondition management view
    """

    def __init__(self, dbsession):
        super(ValveConditionView, self).__init__(
            ValveCondition, dbsession, name="Valve condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class GasketConditionView(MySimpleConditionsView):
    """
    GasketCondition management view
    """

    def __init__(self, dbsession):
        super(GasketConditionView, self).__init__(
            GasketCondition, dbsession, name="Gasket condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class OverallConditionView(MySimpleConditionsView):
    """
    OverallCondition management view
    """

    def __init__(self, dbsession):
        super(OverallConditionView, self).__init__(
            OverallCondition, dbsession, name="Overall condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class TapFilterConditionView(MySimpleConditionsView):
    """
    TapFilterCondition management view
    """

    def __init__(self, dbsession):
        super(TapFilterConditionView, self).__init__(
            TapFilterCondition, dbsession, name="Tap filter condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class ConnectionConditionView(MySimpleConditionsView):
    """
    ConnectionCondition management view
    """

    def __init__(self, dbsession):
        super(ConnectionConditionView, self).__init__(
            ConnectionCondition, dbsession, name="Connection condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class FoundationConditionView(MySimpleConditionsView):
    """
    FoundationCondition management view
    """

    def __init__(self, dbsession):
        super(FoundationConditionView, self).__init__(
            FoundationCondition, dbsession, name="Foundation condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class HeatingConditionView(MySimpleConditionsView):
    """
    HeatingCondition management view
    """

    def __init__(self, dbsession):
        super(HeatingConditionView, self).__init__(
            HeatingCondition, dbsession, name="Heating condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class FanConditionView(MySimpleConditionsView):
    """
    FanCondition management view
    """

    def __init__(self, dbsession):
        super(FanConditionView, self).__init__(
            FanCondition, dbsession, name="Fan condition"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class PaintTypesView(MySimpleConditionsView):
    """
    PaintTypes management view
    """

    def __init__(self, dbsession):
        super(PaintTypesView, self).__init__(
            PaintTypes, dbsession, name="Paint types"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class FluidLevelView(MySimpleConditionsView):
    """
    FluidLevel management view
    """

    def __init__(self, dbsession):
        super(FluidLevelView, self).__init__(
            FluidLevel, dbsession, name="Fluid level"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class GasLevelView(MySimpleConditionsView):
    """
    GasLevel management view
    """

    def __init__(self, dbsession):
        super(GasLevelView, self).__init__(
            GasLevel, dbsession, name="Gas level"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class TapCounterStatusView(MySimpleConditionsView):
    """
    TapCounterStatus management view
    """

    def __init__(self, dbsession):
        super(TapCounterStatusView, self).__init__(
            TapCounterStatus, dbsession, name="Tap counter status"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class MySimpleStatusesView(MySimpleView):
    def __init__(self, model_class, dbsession, **kvargs):
        super(MySimpleStatusesView, self).__init__(
            model_class, dbsession, category="Statuses", **kvargs
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class ContractStatusView(MySimpleStatusesView):
    """
    ContractStatus management view
    """

    # inline_models = (Contract,)

    def __init__(self, dbsession):
        super(ContractStatusView, self).__init__(
            ContractStatus, dbsession, name="Contract status"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') 
        return False

class MyTestView(MyModelView):
    """
    Test management view
    """
    # Visible columns in the list view
    can_view_details = True
    column_hide_backrefs = False

    def __init__(self, model_class, dbsession, **kvargs):
        super(MyTestView, self).__init__(
            model_class, dbsession, category="Tests", **kvargs
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class BushingTestView(MyTestView):
    """
    BushingTest management view
    """

    form_ajax_refs = {
        'test_result': myQueryAjaxLoader(
            'test_result',
            db.session,
            TestResult,
            fields=['remark'],
            page_size=10
        ),
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(BushingTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(BushingTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(BushingTestView, self).__init__(
            BushingTest, dbsession, name="Bushing test"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False

class WindingTestView(MyTestView):
    """
    WindingTest management view
    """

    form_ajax_refs = {
        'test_result': myQueryAjaxLoader(
            'test_result',
            db.session,
            TestResult,
            fields=['remark'],
            page_size=10
        ),
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(WindingTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(WindingTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(WindingTestView, self).__init__(
            WindingTest, dbsession, name="Winding PF"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class VisualInspectionTestView(MyTestView):
    """
    VisualInspectionTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(VisualInspectionTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(VisualInspectionTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(VisualInspectionTestView, self).__init__(
            VisualInspectionTest, dbsession, name="Visual inspection test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class InsulationResistanceTestView(MyTestView):
    """
    InsulationResistanceTest management view
    """
    
    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(InsulationResistanceTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(InsulationResistanceTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(InsulationResistanceTestView, self).__init__(
            InsulationResistanceTest, dbsession,
            name="Insulation resistance test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class PolymerisationDegreeTestView(MyTestView):
    """
    PolymerisationDegreeTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(PolymerisationDegreeTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(PolymerisationDegreeTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(PolymerisationDegreeTestView, self).__init__(
            PolymerisationDegreeTest, dbsession,
            name="Polymerisation degree test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class TransformerTurnRatioTestView(MyTestView):
    """
    TransformerTurnRatioTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(TransformerTurnRatioTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(TransformerTurnRatioTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(TransformerTurnRatioTestView, self).__init__(
            TransformerTurnRatioTest, dbsession,
            name="Transformer turn ratio test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class WindingResistanceTestView(MyTestView):
    """
    WindingResistanceTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(WindingResistanceTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(WindingResistanceTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(WindingResistanceTestView, self).__init__(
            WindingResistanceTest, dbsession, name="Winding resistance test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class DissolvedGasTestView(MyTestView):
    """
    DissolvedGasTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(DissolvedGasTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(DissolvedGasTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(DissolvedGasTestView, self).__init__(
            DissolvedGasTest, dbsession, name="Dissolved gas test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class WaterTestView(MyTestView):
    """
    WaterTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(WaterTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(WaterTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(WaterTestView, self).__init__(
            WaterTest, dbsession, name="Water test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class FuranTestView(MyTestView):
    """
    FuranTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(FuranTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(FuranTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(FuranTestView, self).__init__(
            FuranTest, dbsession, name="Furan test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class InhibitorTestView(MyTestView):
    """
    InhibitorTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(InhibitorTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(InhibitorTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(InhibitorTestView, self).__init__(
            InhibitorTest, dbsession, name="Inhibitor test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class PCBTestView(MyTestView):
    """
    PCBTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(PCBTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(PCBTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(PCBTestView, self).__init__(
            PCBTest, dbsession, name="PCB test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class ParticleTestView(MyTestView):
    """
    ParticleTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(ParticleTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(ParticleTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(ParticleTestView, self).__init__(
            ParticleTest, dbsession, name="Particle test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class MetalsInOilTestView(MyTestView):
    """
    MetalsInOilTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(MetalsInOilTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(MetalsInOilTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(MetalsInOilTestView, self).__init__(
            MetalsInOilTest, dbsession, name="Metals in oil test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class FluidTestView(MyTestView):
    """
    FluidTest management view
    """

    form_ajax_refs = {
        'test_result': {'fields': (TestResult.remark,)},
    }

    def get_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(self.model).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(FluidTestView, self).get_query()
    
    def get_count_query(self):
        if login.current_user.has_role('group_admin'):
            e_ids = [item.id  for item in self.session.query(Campaign).filter(Campaign.group_id==g.user.group_id)]
            return self.session.query(func.count('*')).join(self.model.test_result).filter(TestResult.campaign_id.in_(e_ids))
        else:
            return super(FluidTestView, self).get_count_query()

    def __init__(self, dbsession):
        super(FluidTestView, self).__init__(
            FluidTest, dbsession, name="Fluid test"
        )
    def is_accessible(self):
        if login.current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        else:
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class TestSamplingCardView(MySimpleView):
    """
    TestSamplingCard management view
    """
    # List of columns that can be sorted.
    column_sortable_list = ()
    column_searchable_list = ()

    form_ajax_refs = {
        'test_result': myQueryAjaxLoader(
            'test_result',
            db.session,
            TestResult,
            fields=['remark'],
            page_size=10
        ),
    }

    def __init__(self, dbsession):
        super(TestSamplingCardView, self).__init__(
            TestSamplingCard, dbsession, category="Campaign", name="Test sampling card"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin') or login.current_user.has_role('group_admin') or login.current_user.has_role('group_user')
        return False

class CountryView(MySimpleView):
    """
    Country management view
    """
    def __init__(self, dbsession):
        super(CountryView, self).__init__(
            Country, dbsession, category="Options", name="Country"
        )
    def is_accessible(self):
        if login.current_user.is_authenticated():
            return login.current_user.has_role('admin')
        return False
        
simple_views = [
    TestReasonView, PressureUnitView, GasRelayView, PaintTypesView,
    SamplingPointView, EquipmentConnectionView, InterruptingMediumView,
    InsulationView, BreakerMechanismView, FanConditionView, HeatingConditionView,
    FoundationConditionView, ConnectionConditionView, TapFilterConditionView,
    OverallConditionView, GasketConditionView, ValveConditionView,
    PumpConditionView, ContractStatusView, TapCounterStatusView, GasLevelView,
    FluidLevelView, TestRecommendationView, TestSamplingCardView, SiblingView,
    # SamplingCardView,
]
test_views = [
    BushingTestView, WindingTestView, VisualInspectionTestView, InsulationResistanceTestView,
    PolymerisationDegreeTestView, TransformerTurnRatioTestView, WindingResistanceTestView,
    DissolvedGasTestView, WaterTestView, PCBTestView, InhibitorTestView, FuranTestView, FluidTestView,
    MetalsInOilTestView, ParticleTestView
]
other_views = [
    EquipmentView, NormFuranView, NormPhysicView, NormIsolationView, NormGasView, AirCircuitBreakerView,
    ManufacturerView, BushingView, CableView, CapacitorView, RectifierView, NeutralResistanceView, TankView,
    LoadTapChangerView, BreakerView, SwitchView, SwitchGearView, SynchronousMachineView, InductanceView,
    InductionMachineView, TransformerView, GasSensorView, FluidTypeView, LocationView, LabView, CampaignView,
    ContractView, FluidProfileView, TestStatusView, TestTypeView, TestResultView,
    EquipmentTypeView, ElectricalProfileView, MaterialView, PowerSourceView, NormView, RecommendationView,
    SyringeView, TestScheduleView, InhibitorTypeView, CampaignStatusView, CountryView, TaskStatusView
]
admin_views = simple_views
admin_views.extend(test_views)
admin_views.extend(other_views)
