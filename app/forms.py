import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectMultipleField, IntegerField, \
    HiddenField, DecimalField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo, NumberRange
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    isadmin = BooleanField("Admin")
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])

    dob = DateField("Date of Birth", validators=[DataRequired()], format='%d/%m/%Y')
    email = StringField('Email', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class TopUpForm(FlaskForm):
    value = FloatField('Top Up Value', validators=[DataRequired()])
    submit = SubmitField('Top Up')
