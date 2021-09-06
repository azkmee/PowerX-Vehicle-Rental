from app import application
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, TopUpForm, AddAdminForm, AddVehicleForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Customer, AdminUser, Car, Van, Lorry, Vehicle
from werkzeug.urls import url_parse
from app import db
from flask import request 
from app.serverlibrary import * 
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, IntegerField, HiddenField
from wtforms.validators import DataRequired, NumberRange, ValidationError

import sys


#Public Route
@application.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)

	return render_template('login.html', title='Sign In', form=form, type=None)

@application.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@application.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = Customer(username=form.username.data)
		user.set_password(form.password.data)

		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user.')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form, type=None)


#Private Route
@application.route('/')
@application.route('/index')
@login_required
def index():
	user = Customer.query.filter_by(username = current_user.username).first()
	print(user,file=sys.stderr)
	
	return render_template('index.html', title='Home', type=user.type)
# write down your handler for the routes here


# Customer Routes
@application.route('/balance', methods=["GET","POST"])
@login_required
def balance():
	user = Customer.query.filter_by(username = current_user.username).first()

	form=TopUpForm()

	if form.validate_on_submit():
		value = form.value.data
		print(value, file=sys.stderr)
		user.add_balance(float(value))
		db.session.commit()
		return redirect('/balance')

    
	return render_template('balance.html', title='Balance',
	 balance=user.balance, form=form, user=user, type=user.type)

@application.route('/topup', methods=["GET","POST"])
def topUp():
	if request.method == 'POST':
		user = User.query.filter_by(username = current_user.username).first()
		req = request.form
		value = req['value']
		
		new_balance = user.add_balance(float(value))
		db.session.commit()
		print(new_balance, file=sys.stderr)
		return redirect('/balance')

@application.route('/deduct', methods=["GET","POST"])
def deduct():
	if request.method == 'POST':
		user = User.query.filter_by(username = current_user.username).first()
		req = request.form
		value = req['value']
		
		new_balance = user.deduct_balance(float(value))
		db.session.commit()
		
		# return redirect('/balance')

#Admin Routes

@application.route('/addadmin', methods=["GET","POST"])
@login_required
def addadmin():
	user = AdminUser.query.filter_by(username = current_user.username).first()
	if user.type != 'admin':
		return redirect('/')

	form = AddAdminForm()
	# print(user.admin, file=sys.stderr)

	if form.validate_on_submit():
		admin_username = form.username.data
		admin_password = form.password.data
		new_admin = user.add_admin_user([admin_username, admin_password])
		db.session.add(new_admin)
		db.session.commit()
		return redirect('/addadmin')
	return render_template('add_admin.html', title='Balance',form=form, user=user, type=user.type)
	
@application.route('/addvehicle', methods=["GET","POST"])
@login_required
def addvehicle():
	user = AdminUser.query.filter_by(username = current_user.username).first()
	if user.type != 'admin':
		return redirect('/')

	vehicles = Vehicle.query.all()


	form = AddVehicleForm()
	if form.validate_on_submit():
		print('validating', file=sys.stderr)
		type = form.vehicleType.data
		vehicle_num = form.vehicleNum.data
		modelNumber = form.modelNumber.data
		# purchaseDate = form.purchaseDate.data
		odometer = form.odometer.data

		if type == 'Car':
			vehicle = Car()

		elif type == 'Van':
			vehicle = Van()

		elif type == 'Lorry':
			vehicle = Lorry()
		else:
			return redirect('/')

		vehicle.vehicle_num = vehicle_num
		vehicle.model_number = modelNumber
		# vehicle.purchase_date = purchaseDate
		vehicle.odometer = odometer

		db.session.add(vehicle)
		db.session.commit()

		print(vehicle, file=sys.stderr)

		return redirect('/addvehicle')
	return render_template('add_vehicle.html', title='Add Vehicle',form=form, type=user.type, vehicles=vehicles)



	# vehicleType = RadioField('Vehicle Type', choices = [('Car', 'Car'),('Lorry','Lorry'),('Van','Van')])
	# vehicleNum = StringField('Vehicle Number', validators=[DataRequired()])
	# modelNumber = StringField('Model Number', validators=[DataRequired()])
	# purchaseDate = DateField('Purchase Date', validators=[DataRequired()])
	# odometer = DecimalField('Odometer', validators= [DataRequired()] )
	# submit = SubmitField('Add Vehicle')

