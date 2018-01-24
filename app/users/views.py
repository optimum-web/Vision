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
from app.users.forms import RegisterForm, LoginForm, ProfileForm, ForgotForm
from app.users.constants import UPLOAD_FOLDER
from app.users.models import User, Role, users_roles
from app.users.utils import allowed_image_file
from app.users.decorators import login_required, templated
from itsdangerous import URLSafeTimedSerializer
from flask.ext.babel import gettext
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity

from app import guest_per, user_per, blogger_per, admin_per

mod = Blueprint('users', __name__, url_prefix='/users')


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


@mod.route('/dashboard')
@mod.route('/home')
@user_per.require(http_exception=403)
def home():
    return render_template(
        "users/me.html", user=g.user
    )


@mod.route('/pleaseconfirm')
def pleaseconfirm():
    if g.user:
        send_confirmation()
    return render_template("users/pleaseconfirm.html", user=g.user)


@mod.route("/confirm/<string:token>", methods=['GET', 'POST'])
def confirm(token):
    """docstring for confirm"""
    try:
        email = confirm_token(token)
    except:
        flash(gettext(u'The confirmation link is invalid or has expired.'), 'danger')

    user = User.query.filter_by(email=email).first_or_404()

    if user.is_confirmed():
        flash(gettext(u'Account already confirmed. Please login.'), 'success')
    else:
        user.confirmed = True
        user.active = True
        db.session.commit()
        flash(gettext(u'You have confirmed your account. Thanks!'), 'success')

    return redirect("/admin") #url_for('users.home')


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


@mod.route("/reconfirm/<string:alias>", methods=['GET', 'POST'])
def reconfirm(alias):
    """docstring for reconfirm"""
    if g.user:
        send_confirmation()
    return redirect(url_for('users.home'))


def send_confirmation():
    """docstring for send_confirmation"""

    token = generate_confirmation_token(str(g.user.get_email()))
    lnk = url_for('users.confirm', token=token, _external=True)
    conflnk_html = '<a href="%s">%s</a>' % (lnk, lnk)

    msg = Message(
        gettext(u"Please confirm your account at vision website"),
        sender=current_app.config['NOREPLY_EMAIL'],
        recipients=[g.user.get_email()]
    )
    msg.body = "\nWelcome\n\n"
    msg.body += "\nPlease confirm your account by clicking this link:\n"
    msg.body += "\n%s" % lnk
    msg.body += "\nFuture notifications will be sent to this email address."
    msg.body += "\nThank you,"
    msg.body += "\n\nTeam."

    html = "Hi, Welcome"
    html += "<br><br>Please confirm your account by clicking this link:"
    html += "\n%s" % conflnk_html
    html += "<br>Future notifications will be sent to this email address."
    html += "<br>Thank you,"
    html += "<br><br>Team."
 
 
    if current_app.config['SEND_EMAILS'] == "1":
        #mail.send(msg)
        send_email([g.user.get_email()], html, u"Please confirm your account at vision website")


# @mod.route('/forgot-password', methods=['GET', 'POST'])
# def forgot():
#     if 'user_id' in session:
#         return redirect(url_for('users.home'))
#
#     form = ForgotForm(request.form)
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             user = User.query.filter_by(email=form.email.data).first()
#             if user:
#                 return user
#
#     # make sure data are valid, but doesn't validate password is right
#     return render_template("users/forgot.html", form=form)



@mod.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    if 'user_id' in session:
        return redirect(url_for('users.home'))

    form = LoginForm(request.form)

    # make sure data are valid, but doesn't validate password is right
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            # we use werzeug to validate user's password
            if user and verify_password(form.password.data, user.password):
                # the session can't be modified as it's signed,
                # it's a safe place to store the user id
                authorize(user)
                # Tell Flask-Principal the identity changed
                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(user.id))

                flash(gettext(u'Welcome') + " " + user.name)
                if not user.is_confirmed():
                    return redirect(url_for('users.pleaseconfirm', next=url_for('home.home')))
                return redirect(url_for('home.home'))
        flash(gettext(u'Wrong email or password'), 'error-message')

    return render_template('users/login.html', form=form)


@mod.route('/logout', methods=['GET'])
def logout():
    """ Logout action.  """
    if 'user_id' in session:
        del session['user_id']
        g.user = None

        # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    response = make_response(redirect(url_for('users.login')))
    response.set_cookie('sc', '', expires=0)
    return response


@mod.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration Form
    """
    form = RegisterForm(request.form)
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

        user = User(
            name=form.name.data,
            email=form.email.data,
            alias=alias,
            password=encrypt_password(form.password.data)
        )

        # add default
        userRole = db.session.query(Role).filter(Role.name == "user").first()
        if userRole is not None:
            # createUserRole =  users_roles( user_id = user.id
            #     , role_id = userRole.id );
            # adminRole =  db.session.query(Role).filter(Role.name == "admin").first()
            # user.roles.append(adminRole)
            user.roles.append(userRole)

        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.flush()

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

    return render_template('users/register.html', form=form)


@mod.route("/profile", methods=['GET', 'POST'])
@user_per.require(http_exception=403)
@templated('users/profile.html')
def profile():
    user = g.user
    form = ProfileForm(request.form, obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.mobile = form.mobile.data
        user.website = form.website.data
        user.description = form.description.data

        if 'photo' in request.files:
            # remove user photo and thumbs
            mfile = request.files['photo']

            if mfile and allowed_image_file(mfile.filename):

                # if file reuploaded
                if user.photo and len(user.photo) > 0:
                    photo = os.path.join(
                        UPLOAD_FOLDER, str(user.id), user.photo
                    )
                    try:
                        os.remove(photo)
                    except Exception as e:
                        print ("removing %s" % photo)
                        current_app.logger.exception(e)

                    fufile = str(photo.split('.')[0])

                    for basewidth in [200, 245]:
                        thumb = fufile + '_thumb%s.png' % basewidth
                        try:
                            os.remove(thumb)
                        except Exception as e:
                            print ("removing %s" % thumb)
                            current_app.logger.exception(e)

                    user.photo = ''

                filename = secure_filename(mfile.filename)
                ext = filename.rsplit('.', 1)[1]
                fname = '%s_%s' % (g.user.id, g.user.email)
                newfn = '%s.%s' % (base64.b64encode(fname), ext)
                photo = os.path.join(
                    UPLOAD_FOLDER, str(user.id), newfn
                )

                mfile.save(photo)
                user.photo = newfn

        db.session.commit()
        flash(gettext(u'Profile updated'))

        return redirect(url_for("users.profile"))

    return dict(form=form, user=user)


@mod.route("/profile/change-password", methods=['GET', 'POST'])
@user_per.require(http_exception=403)
@templated('users/change-password.html')
def change_password():
    user = User.query.get(session['user_id'])
    form = ProfileForm(request.form, obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.country_id = form.country_id.data
        user.address = form.address.data
        user.mobile = form.mobile.data
        user.website = form.website.data
        db.session.commit()
        flash(gettext(u"Profile updated"))
        return redirect(url_for("users.home"))

    return dict(form=form, user=user)

@mod.route("/invite/", methods=[ 'POST'])
def invite_user():
    user = User.query.get(session['user_id'])
    return dict(user=user)
