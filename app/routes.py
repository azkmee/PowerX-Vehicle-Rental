from app import application
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm 
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User 
from werkzeug.urls import url_parse
from app import db
from flask import request 
from app.serverlibrary import * 
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, IntegerField, HiddenField
from wtforms.validators import DataRequired, NumberRange, ValidationError

import sys

@application.route('/')
@application.route('/index')
@login_required
def index():
	return render_template('index.html', title='Home')

# write down your handler for the routes here


@application.route('/users')
@login_required
def users():
	users = User.query.all()	
	# mergesort(users, lambda item: item.username)
	usernames = [u.username for u in users]
	return render_template('users.html', title='Users',
							users=usernames)

class TopUpForm(FlaskForm):
	value = DecimalField('Top Up Value', validators= [NumberRange(min=0, max=10, message='bla')] )
	submit = SubmitField('Top Up')

@application.route('/balance', methods=["GET","POST"])
@login_required
def balance():
	user = User.query.filter_by(username = current_user.username).first()

	form=TopUpForm()

	if form.validate_on_submit():
		value = form.value.data
		print(value, file=sys.stderr)
		user.add_balance(float(value))
		db.session.commit()
		return redirect('/balance')

    
	return render_template('balance.html', title='Balance', balance=user.balance, form=form)

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
		print(new_balance, file=sys.stderr)
		# return redirect('/balance')

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
	return render_template('login.html', title='Sign In', form=form)

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
		user = User(username=form.username.data, balance = 0)
		user.set_password(form.password.data)

		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user.')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

