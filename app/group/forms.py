from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, ValidationError
from wtforms import TextAreaField, FileField, HiddenField
from wtforms.validators import Required, EqualTo, Email, Length, Optional
from app.users.utils import check_password

class RegisterForm(Form):
    group = TextField('Company Name', [Required()])
    name = TextField('Full Name', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])
    accept_tos = BooleanField('', [Required()])

    # recaptcha = RecaptchaField()

    @staticmethod
    def validate_password(form, field):
        """docstring for validate_password"""
        strength = check_password(field.data)
        if strength not in ['Medium', 'Strong', 'Very Strong']:
            raise ValidationError(
                'Your password is %s, it should be > 6 '
                'chars and contain at least one digit' % strength)

