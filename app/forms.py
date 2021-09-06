from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, RadioField, DateField, SelectMultipleField, IntegerField, HiddenField
from wtforms.validators import DataRequired, ValidationError, EqualTo, NumberRange
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', 
							   validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

class TopUpForm(FlaskForm):
	value = DecimalField('Top Up Value', validators= [NumberRange(min=0, max=100, message='bla')] )
	submit = SubmitField('Top Up')

class AddAdminForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Add admin')
	
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')


class AddVehicleForm(FlaskForm):
	vehicleType = RadioField('Vehicle Type', choices = [('Car', 'Car'),('Lorry','Lorry'),('Van','Van')], validators=[DataRequired()])
	vehicleNum = StringField('Vehicle Number', validators=[DataRequired()])
	modelNumber = StringField('Model Number', validators=[DataRequired()])
	# purchaseDate = DateField('Purchase Date', validators=[DataRequired()]) 
	odometer = DecimalField('Odometer', validators= [DataRequired()] )
	submit = SubmitField('Add Vehicle')

