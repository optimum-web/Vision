from app.users import constants as USER
from app import db, app
from app.group.models import Group
from hashlib import md5
from sqlalchemy import event, select, func
from sqlalchemy.sql import text
from sqlalchemy.orm import class_mapper, ColumnProperty
import datetime
from flask.ext.security import RoleMixin, UserMixin
from flask.ext.security.utils import verify_password
from itsdangerous import (JSONWebSignatureSerializer
as Serializer, BadSignature, SignatureExpired)

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app.diagnostic.helpers import AESCipher


ENCRYPT_KEY = app.config['SECURITY_DB_ENCRYPT']

# Define models
users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users_user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Role(db.Model, RoleMixin):
    """
    Class Role
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role %r>' % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'id': self.id,
                'name': self.name,
                'description': self.description
                }


class User(db.Model, UserMixin):
    """
    Class User

    """
    __tablename__ = 'users_user'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column('name', db.String(250), unique=False)
    alias = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    roles = db.relationship(
        'Role', secondary=users_roles,
        backref=db.backref('users_user', lazy='dynamic')
    )
    status = db.Column(db.SmallInteger, default=USER.NEW)
    address = db.Column(db.String(255))
    mobile = db.Column(db.String(50))
    website = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    description = db.Column(db.UnicodeText())
    active = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime())
    created = db.Column('created', db.DateTime, default=datetime.datetime.now)
    updated = db.Column('updated', db.DateTime, default=datetime.datetime.now)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"))
    country = db.relationship('Country', backref='users_user')
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    group = db.relationship('Group', backref='users_user')

    def __unicode__(self):
        return u"%s" % (self.name)

    def __init__(self, *args, **kwargs):
        fields = [prop.key for prop in class_mapper(self.__class__).iterate_properties if
                  isinstance(prop, ColumnProperty)]
        for arg, val in kwargs.items():
            if arg in fields or arg == 'name':
                print('---', arg, val)
                setattr(self, arg, val)

    @property
    def initials(self):
        if not self.name:
            return ""
        return ("".join([x[:1] for x in self.name.split()])).upper()

    def getStatus(self):
        return USER.STATUS[self.status]

    def get_role(self):
        return USER.ROLE[self.roles]

    def __repr__(self):
        return '<User %r>' % (self.name)

    def is_confirmed(self):
        return self.confirmed

    def is_active(self):
        return self.active

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + \
               md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    # API authentication
    def verify_password(self, password):
        return verify_password(password, self.password)

    def generate_auth_token(self):
        # TODO: Token should expire
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        return User.query.get(data['id'])

    @hybrid_property
    def name(self):
        # can be called for InstrumentedAttribute
        if type(self._name) not in (unicode, str):
            return self._name

        if self._name:
            cipher = AESCipher(ENCRYPT_KEY)
            msg = cipher.decrypt(self._name)
            return msg.encode('utf-8')
        else:
            return None

    @name.setter
    def name(self, val):
        print('setter', val)
        cipher = AESCipher(ENCRYPT_KEY)
        msg = cipher.encrypt(val)
        self._name = msg

    @hybrid_method
    def contains(self, val):
        cipher = AESCipher(ENCRYPT_KEY)
        msg = cipher.encrypt(val)
        msg = msg.encode('utf-8')
        return self._name.ilike(msg)

    @name.expression
    def name(cls):
        return User._name

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'id': self.id,
                'name': self.name,
                'alias': self.alias,
                'email': self.email,
                # 'password': self.password,
                'roles': [ item.serialize() for item in self.roles],
                'status': self.status,
                'address': self.address,
                'mobile': self.mobile,
                'website': self.website,
                'country_id': self.country_id,
                'country': self.country and self.country.serialize(),
                'group_id': self.group_id,
                'group': self.group and self.group.serialize(),
                'photo': self.photo,
                'description': self.description,
                'active': self.active,
                'confirmed': self.confirmed,
                'confirmed_at': dump_datetime(self.confirmed_at),
                'created': dump_datetime(self.created),
                'updated': dump_datetime(self.updated),
                }


