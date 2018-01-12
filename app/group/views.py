import os
import md5
import hashlib
import base64
from flask import Blueprint, request, render_template
from flask import flash, g, session, redirect, url_for
from flask import make_response
from flask import current_app
from flask_mail import Message
from werkzeug import secure_filename
from app import db
from app import mail
from app.mail_utility import send_email
from app.group.forms import RegisterForm
from app.users.constants import UPLOAD_FOLDER
from app.users.models import User, Role, users_roles
from app.group.models import Group
from app.users.utils import allowed_image_file
from app.users.decorators import login_required, templated
from itsdangerous import URLSafeTimedSerializer
from flask.ext.babel import gettext
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity

from app import guest_per, user_per, blogger_per, admin_per

mod = Blueprint('group', __name__, url_prefix='/group')


def authorize(user):
    session['user_id'] = user.id


def is_logged():
    return g.user


@mod.before_app_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


import base64
import string
@mod.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration Form
    """
    form = RegisterForm(request.form)
    if request.args.get('group'):
        form.group.data = 'tmp'
    if form.validate_on_submit():
        # create an user instance not yet stored in the database
        # check if email exists
        try:
            exists = db.session.query(User).filter(
                User.email == form.email.data).first()

            if exists:
                flash(
                    gettext(
                        u'User with this e-mail was registered already.'
                        u' If you forgot your password click ' +
                        u'<a href="%s">remind password</a>' % url_for(
                            'users.forgot')
                    ))
                # redirect user to the 'home' method of the user module.
                return redirect(url_for('users.register'))
        except Exception as e:
            current_app.logger.exception(e)

        alias = ''.join(e for e in form.name.data if e.isalnum())
        try:
            alias_exists = db.session.query(User).filter(
                User.alias == alias).one()
        except Exception as e:
            current_app.logger.exception(e)
            alias_exists = None

        if alias_exists:
            alias = hashlib.md5(form.email.data).hexdigest()

        if request.args.get('group'):
            group_id = string.replace(base64.b64decode(request.args.get('group')), "group|", "")
        else:
            group_id = 0
        user = User(
            name=form.name.data,
            email=form.email.data,
            alias=alias,
            password=encrypt_password(form.password.data),
            group_id=group_id
        )

        # add default
        userRole = db.session.query(Role).filter(Role.name == "group_user").first()
        if userRole is not None:
            # createUserRole =  users_roles( user_id = user.id
            #     , role_id = userRole.id );
            # adminRole =  db.session.query(Role).filter(Role.name == "admin").first()
            # user.roles.append(adminRole)
            user.roles.append(userRole)

        if group_id == 0:
            # add company_admin
            userRole = db.session.query(Role).filter(Role.name == "group_admin").first()
            if userRole is not None:
                # createUserRole =  users_roles( user_id = user.id
                #     , role_id = userRole.id );
                # adminRole =  db.session.query(Role).filter(Role.name == "admin").first()
                # user.roles.append(adminRole)
                user.roles.append(userRole)

            group = Group(
                name=form.group.data
            )
            db.session.add(group)
            db.session.flush()
            db.session.commit()
            user.group_id = group.id
        else:
            user.group_id = group_id
        
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        

        

        # Log the user in, as he now has an id
        authorize(user)

        try:
            os.mkdir(os.path.join(UPLOAD_FOLDER, str(user.id)), 0775)
        except OSError as e:
            current_app.logger.exception(e)

        db.session.commit()
        email_recipients = [item.email for item in db.session.query(User).all()
                            if item.has_role(Role.query.get(1))
                            ]
        msg = 'A new user with login {} was created'.format(user.name)

        if current_app.config['SEND_EMAILS'] == True:
            try:
                send_email(email_recipients, msg)
            except Exception as e:
                pass

        # flash will display a message to the user
        flash(gettext(u'Thanks for registering'))
        # redirect user to the 'home' method of the user module.
        if not user.is_confirmed():
            return redirect(url_for('users.pleaseconfirm', next=url_for('users.home')))
    if request.args.get('group'):
        group_id = True
    else:
        group_id = False
    print group_id
    return render_template('company/register.html', form=form, group_id=group_id)

