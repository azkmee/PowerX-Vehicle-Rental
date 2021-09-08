import app.models
from app import application
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, TopUpForm, AddAdminForm, AddVehicleForm, GetAvailableVehicles, \
    BookVehicle, SelectPayTransaction, SelectRentOutVehicle, SelectReturnVehicle
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Customer, AdminUser, Car, Van, Lorry, Vehicle, Transaction
from werkzeug.urls import url_parse
from app import db
from flask import session as ss
from app.serverlibrary import *
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, \
    IntegerField, HiddenField
from wtforms.validators import DataRequired, NumberRange, ValidationError

import sys, datetime


# Admin Routes
@application.route('/addadmin', methods=["GET", "POST"])
@login_required
def addadmin():
    user = AdminUser.query.filter_by(username=current_user.username).first()
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
    return render_template('add_admin.html', title='Balance', form=form, user=user, type=user.type)


@application.route('/removevehicle', methods=["GET", "POST"])
def remove_vehicle():
    data = request.form.to_dict()
    vid = data['id']

    Vehicle.query.filter_by(id=vid).delete()
    db.session.commit()
    print('vehicle ' + vid + ' removed', file=sys.stderr)
    return redirect('/addvehicle')


@application.route('/addvehicle', methods=["GET", "POST"])
@login_required
def addvehicle():
    user = AdminUser.query.filter_by(username=current_user.username).first()
    if user.type != 'admin':
        return redirect('/')

    vehicles = Vehicle.query.all()

    form = AddVehicleForm()
    if form.validate_on_submit():

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
    return render_template('add_vehicle.html', title='Add Vehicle',
                           form=form, type=user.type, vehicles=vehicles)

