import sys

from app import application
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, TopUpForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db
from flask import request
from app.serverlibrary import *


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
    # usernames = [u.username for u in users]
    return render_template('users.html', title='Users',
                           users=users)


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
        print(current_user)
        print(current_user.wallet)
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
        # user = Admin(username=form.username.data) if form.isadmin.data else Customer(username=form.username.data)
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.usertype = "Admin" if form.isadmin.data else "Customer"
        user.dob = form.dob.data
        user.email = form.email.data
        user.mobile = form.mobile.data
        user.address = form.address.data
        user.wallet = 0
        user.isactive = True
        # print(user.__repr__())

        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@application.route('/topup', methods=["GET", "POST"])
@login_required
def topUp():
    form = TopUpForm()
    if form.validate_on_submit():
        print("################inside if")
        #user = User(username=current_user.username)
        user = User.query.filter_by(username=current_user.username).first()
        db.session.delete(user)
        print(user)
        w = form.value.data
        print(w, user.wallet)
        user.wallet = user.wallet + w
        print("ADDED WALLED")
        print(user.address)
        print(user.wallet)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('topUp'))
    return render_template('balance.html', form=form)



