from app.users import constants as USER
from app import db, app
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



class Group(db.Model, UserMixin):
    """
    Class Group

    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(250), unique=False)

    def __unicode__(self):
        return u"%s" % (self.name)

    def __init__(self, *args, **kwargs):
        fields = [prop.key for prop in class_mapper(self.__class__).iterate_properties if
                  isinstance(prop, ColumnProperty)]
        for arg, val in kwargs.items():
            if arg in fields or arg == 'name':
                print('---', arg, val)
                setattr(self, arg, val)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'id': self.id,
                'name': self.name}

