import os
import os.path as op
# from flask import Flask
# from flask import Blueprint, request, render_template
from flask.ext.admin.contrib import sqla
from app import db, cache
from app.users.models import User, Role
from flask import flash, g, session, redirect, url_for
from flask.ext.admin.contrib.sqla import ModelView
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.admin.contrib.sqla import filters
from flask.ext.admin import helpers, expose
from flask.ext import admin, login
from wtforms import form, fields, validators
from flask import current_app
from werkzeug.security import check_password_hash
from app import admin_per
# from app import , user_per, guest_per, blogger_per
from app.tree.storage import get_tree
from app.tree.forms import TreeView
from .models import File, Image
from jinja2 import Markup
from flask_admin import BaseView
from flask import jsonify
from app.diagnostic.forms import *


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    email = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_email(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()


from .forms import *


class MyAdminIndexView(admin.AdminIndexView):
    @expose('/')
    @cache.memoize(timeout=60)
    @admin_per.require(http_exception=403)
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))

        # return redirect(url_for('campaign.index_view'))

        # popups = {
        #     'add': {
        #         'description': NewTestDescription()
        #         , 'electrical': NewTestElectrical()
        #         , 'fluid': NewTestFluid()
        #         , 'profile': NewTestProfile()
        #     },
        # }
        #
        # info = {
        #     'identification': IdentificationInfoViewForm()
        #     , 'validation': ValidationInfoViewForm()
        #     , 'nameplate': NameplateInfoViewForm()
        #     , 'bushing': BushingInfoViewForm()
        #     , 'taps': TapsInfoViewForm()
        #     , 'norms': NormsInfoViewForm()
        #     , 'loading': LoadInfoViewForm()
        #     , 'doc': DocInfoViewForm()
        # }
        #
        self._template_args['tree'] = get_tree()
        self._template_args['tree_view'] = TreeView()
        # front page views
        self._template_args['identification'] = IdentificationViewForm()
        self._template_args['test_repair'] = TestRepairViewForm()
        self._template_args['records_diagnosis'] = RecordsDiagnosticViewForm()
        self._template_args['equipment_diagnosis'] = EquipmentDiagnosisViewForm()
        # self._template_args['diagnostic'] = popups
        # self._template_args['batch'] = BatchViewForm()
        # self._template_args['report'] = EquipmentTestReportViewForm()
        # self._template_args['costumer'] = ManageCustomersViewForm()
        # self._template_args['search'] = SearchViewForm()
        # self._template_args['data'] = DataViewForm()
        # self._template_args['info'] = info
        # self._template_args['lab'] = Lab()
        #
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        link = ''
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if not user:
                link = '<p>Please contact %s</p>' % current_app.config['SUPPORT_EMAIL']
                self._template_args['link'] = link
                return redirect(url_for('.index'))

            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    @admin_per.require(http_exception=403)
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('home.home'))


class MyModelView(ModelView):
    # edit_modal = True
    # create_modal = True

    @expose('/modal/')
    def modal(self):
        """
            List view in modal form
        """
        if self.column_editable_list:
            form = self.list_form()
        else:
            form = None

        if self.can_delete:
            delete_form = self.delete_form()
        else:
            delete_form = None

        # Grab parameters from URL
        view_args = self._get_list_extra_args()

        # Map column index to column name
        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]

        # Get count and data
        count, data = self.get_list(view_args.page, sort_column, view_args.sort_desc,
                                    view_args.search, view_args.filters)

        # Calculate number of pages
        if count is not None:
            num_pages = count // self.page_size
            if count % self.page_size != 0:
                num_pages += 1
        else:
            num_pages = None

        # Various URL generation helpers
        def pager_url(p):
            # Do not add page number if it is first page
            if p == 0:
                p = None

            return self._get_list_url(view_args.clone(page=p))

        def sort_url(column, invert=False):
            desc = None

            if invert and not view_args.sort_desc:
                desc = 1

            return self._get_list_url(view_args.clone(sort=column, sort_desc=desc))

        # Actions
        actions, actions_confirmation = self.get_actions_list()

        clear_search_url = self._get_list_url(view_args.clone(page=0,
                                                              sort=view_args.sort,
                                                              sort_desc=view_args.sort_desc,
                                                              search=None,
                                                              filters=None))
        template = '/admin/diagnostic/modal_list.html'

        return self.render(
            template,
            data=data,
            form=form,
            delete_form=delete_form,

            # List
            list_columns=self._list_columns,
            sortable_columns=self._sortable_columns,
            editable_columns=self.column_editable_list,

            # Pagination
            count=count,
            pager_url=pager_url,
            num_pages=num_pages,
            page=view_args.page,
            page_size=self.page_size,

            # Sorting
            sort_column=view_args.sort,
            sort_desc=view_args.sort_desc,
            sort_url=sort_url,

            # Search
            search_supported=self._search_supported,
            clear_search_url=clear_search_url,
            search=view_args.search,

            # Filters
            filters=self._filters,
            filter_groups=self._get_filter_groups(),
            active_filters=view_args.filters,

            # Actions
            actions=actions,
            actions_confirmation=actions_confirmation,

            # Misc
            enumerate=enumerate,
            get_pk_value=self.get_pk_value,
            get_value=self.get_list_value,
            return_url=self._get_list_url(view_args),
        )

    def is_accessible(self):
        if not login.current_user.is_authenticated():
            return False

        # Prevent administration of Roles unless the
        # currently logged-in user has the "admin" role
        return login.current_user.has_role('admin')


class RoleAdmin(MyModelView):
    def __init__(self, dbsession):
        super(RoleAdmin, self).__init__(Role, dbsession, name="User role", category='CMS')


class UserAdmin(MyModelView):
    """
    User management view
    """
    # Visible columns in the list view
    column_hide_backrefs = False
    form_excluded_columns = (
        'password',
        'confirmed_at',
        'created',
        'updated',
        'status',
    )
    column_exclude_list = [
        'password',
        'confirmed_at',
        'updated',
        'photo',
        'address',
        'mobile',
        'website',
        'country'
    ]

    # # List of columns that can be sorted.
    column_sortable_list = ('name', 'email', 'alias')

    # # rename column names
    column_labels = dict(
        name='Full Name',
        alias='Username',
    )

    column_searchable_list = ('alias', 'name', 'email', 'id')

    def __init__(self, dbsession):
        super(UserAdmin, self).__init__(User, dbsession, name="User", category='CMS')


from sqlalchemy.event import listens_for
from flask_admin.form import ImageUploadField, FileUploadField, thumbgen_filename

PROJECT = 'vision'
env_dir = '/home/%s/www' % PROJECT
file_path = env_dir + '/app/static/img/uploads/'


class FileView(ModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'path': FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'path': {
            'label': 'File',
            'base_path': file_path,
            'allow_overwrite': False
        }
    }

    def __init__(self, dbsession):
        super(FileView, self).__init__(File, dbsession, name="File", category='CMS')


class ImageView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        prefix = 'img/uploads/'
        return Markup('<img src="%s">' % url_for('static', filename=thumbgen_filename(prefix + model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': ImageUploadField('Image', base_path=file_path, thumbnail_size=(100, 100, True))
    }

    def __init__(self, dbsession):
        super(ImageView, self).__init__(Image, dbsession, name="Image", category='CMS')


@listens_for(File, 'after_delete')
def del_file(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              thumbgen_filename(target.path)))
        except OSError:
            pass


from .storage import *
from .forms import MenuViewForm
from app.pages.models import Pages
from app.tree.storage import get_locale


class MenuView(BaseView):
    # @expose.before_app_request
    # def before_request():
    #     set_locale()

    @expose('/')
    @admin_per.require(http_exception=403)
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('users.login'))

        form = MenuViewForm()

        # myChoices = [ ('' , '...') ]
        # for page in Pages.query.order_by(Pages.updated_on.desc()).all():
        #     myChoices.append( (page.translations[page.get_locale()].title , page.translations[get_locale()].title) )

        myChoices = [(0, '...')] + [(page.id, page.translations[get_locale()].title) for page in
                                    Pages.query.order_by(Pages.updated_on.desc()).all()]
        form.page_view.choices = myChoices

        self._template_args['menu'] = get_menu()
        self._template_args['menu_view'] = form
        # print get_menu()
        return self.render('admin/menu.html')

    @expose('/create/', methods=['POST'])
    def create(self):
        if request.is_xhr:
            id = None
            if admin_per.require().can():
                if request.form['parent']:
                    id = create_node(parent=request.form['parent'], text=request.form['text'],
                                     type=request.form['type'])
            return jsonify({'id': id})
        else:
            # redirect to home
            return redirect(url_for('.index'))

    @expose('/delete/', methods=['POST'])
    def delete(self):
        if request.is_xhr:
            id = None
            if admin_per.require().can():
                if request.form['id']:
                    id = delete_node(id=request.form['id'])

            return jsonify({'id': id})
        else:
            # redirect to home
            return redirect(url_for('.index'))

    @expose('/rename/', methods=['POST'])
    def rename(self):
        if request.is_xhr:
            success = False
            if admin_per.require().can():
                if request.form['id']:
                    success = rename_node(id=request.form['id'], text=request.form['text'])

            return jsonify({'success': success})
        else:
            # redirect to home
            return redirect(url_for('.index'))

    @expose('/move/', methods=['POST'])
    def move(self):
        if request.is_xhr:
            status = "NOK"
            if request.form['node_id']:
                res = move_node(request.form['node_id'], request.form['parent_id'])
                if res is not None:
                    status = "OK"
            return jsonify({'status': status})
        else:
            # redirect to home
            return redirect(url_for('.index'))

    @expose('/copy/', methods=['POST'])
    def copy(self):
        pass

    @expose('/getview/', methods=['POST'])
    def getview(self):
        if request.is_xhr:
            retview = 0
            if admin_per.require().can():
                if request.form['node_id']:
                    res = get_view_by_id(request.form['node_id'])
                    if res is not None:
                        retview = res

            return jsonify({'view': retview})
        else:
            # redirect to home
            return redirect(url_for('.index'))

    @expose('/update/', methods=['POST'])
    def update(self):
        if request.is_xhr:
            status = "NOK"
            ret_id = 0
            if admin_per.require().can():
                form = MenuViewForm(request.form)

                myChoices = [('0', '...')] + [(str(page.id), page.translations[get_locale()].title) for page in
                                              Pages.query.order_by(Pages.updated_on.desc()).all()]
                form.page_view.choices = myChoices

                if form.validate():
                    res = update_node(request.form['node_id'], request.form['page_view'])
                    if res is not None:
                        ret_id = request.form['node_id']
                        status = "OK"
                else:
                    data = []
                    for field, errors in form.errors.items():
                        for error in errors:
                            data.append((getattr(form, field).label.text, error))

                    status = data
            return jsonify({'status': status, 'id': ret_id})

        else:
            # redirect to home
            return redirect(url_for('.index'))
