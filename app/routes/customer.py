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



# Private Route
@application.route('/')
@application.route('/index')
@login_required
def index():
    user = Customer.query.filter_by(username=current_user.username).first()
    print(user, file=sys.stderr)

    return render_template('index.html', title='Home', type=user.type)


# write down your handler for the routes here


# Customer Routes
@application.route('/balance', methods=["GET", "POST"])
@login_required
def balance():
    user = Customer.query.filter_by(username=current_user.username).first()

    form = TopUpForm()

    if form.validate_on_submit():
        value = form.value.data
        print(value, file=sys.stderr)
        user.add_balance(float(value))
        db.session.commit()
        return redirect('/balance')
    return render_template('balance.html', title='Balance',
                           balance=user.balance, form=form, user=user, type=user.type)


@application.route('/topup', methods=["GET", "POST"])
def topUp():
    if request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()
        req = request.form
        value = req['value']

        new_balance = user.add_balance(float(value))
        db.session.commit()
        print(new_balance, file=sys.stderr)
        return redirect('/balance')

@application.route('/selectpaytransaction', methods=["GET", "POST"])
@login_required
def selectPayTransaction():
    qry1 = db.session.query(Transaction, Vehicle) \
        .join(Vehicle, Transaction.vid == Vehicle.id) \
        .filter(Transaction.cid == current_user.id) \
        .filter(Transaction.state == "Booked") \
        .all()

    print(qry1)
    print([(t[0].id, t[1].id, t[1].vehicle_num, t[0].start_date, t[0].end_date) for t in qry1])
    choices = [(str(t[0].id), str(t[0].id)) for t in qry1]

    form = SelectPayTransaction()
    form.tid.choices = choices

    if form.validate_on_submit():
        tid = int(form.tid.data)
        # print(form.tid.data)
        qry2 = db.session.query(Transaction).filter(Transaction.id == tid).first()
        print(qry2, type(qry2), "$", qry2.amount)

        customer = db.session.query(Customer).filter(Customer.id == current_user.id).first()
        print(customer, type(customer), "$", customer.check_balance())

        # Check if user has enough money
        if customer.check_balance() < qry2.amount:
            print("INSUFFICIENT FUNDS")
            flash("Insufficient funds in your wallet. Please top up.")
            return redirect(url_for("balance"))
        else:
            amt = qry2.amount
            customer.deduct_balance(float(amt))
            qry2.state = "Paid"
            db.session.commit()
            flash("Successfully Paid!")
            return render_template("select_paytransaction.html", transvehicle=qry1, form=form, type='customer')

    return render_template("select_paytransaction.html", transvehicle=qry1, form=form, type='customer')


# @application.route('/paytransaction', methods=["GET", "POST"])
# @login_required
# def payTransaction():
#     pass


@application.route('/selectrentout', methods=["GET", "POST"])
@login_required
def selectRentOutVehicle():
    qry1 = db.session.query(Transaction, Vehicle) \
        .join(Vehicle, Transaction.vid == Vehicle.id) \
        .filter(Transaction.cid == current_user.id) \
        .filter(Transaction.state == "Paid") \
        .all()

    print(qry1)
    print([(t[0].id, t[1].id, t[1].vehicle_num, t[0].start_date, t[0].end_date) for t in qry1])
    choices = [(str(t[0].id), t[1].vehicle_num) for t in qry1]

    form = SelectRentOutVehicle()
    form.vehicleNum.choices = choices
    print(form.validate_on_submit())

    if form.validate_on_submit():
        tid = int(form.vehicleNum.data)
        print("ID", type(tid), tid)
        vl = [t for t in qry1 if t[0].id == tid]
        print("VL", vl)
        selectedVehicle = vl[0]
        print("NOLIST", selectedVehicle)

        qry2 = db.session.query(Transaction).filter(Transaction.id == selectedVehicle[0].id).first()
        print(qry2, type(qry2), "$", qry2.state)
        qry2.state = "Dispatch"
        qry2.start_odo = selectedVehicle[1].odometer

        db.session.commit()
        flash("Successfully dispatched your vehicle!")
        return redirect(url_for("index"))
    return render_template("select_rentout.html", transvehicle=qry1, form=form, type='customer')



@application.route('/selectreturn', methods=["GET", "POST"])
@login_required
def selectReturnVehicle():
    qry1 = db.session.query(Transaction, Vehicle) \
        .join(Vehicle, Transaction.vid == Vehicle.id) \
        .filter(Transaction.cid == current_user.id) \
        .filter(Transaction.state == "Dispatch") \
        .all()

    print(qry1)
    print([(t[0].id, t[1].id, t[1].vehicle_num, t[0].start_date, t[0].end_date) for t in qry1])
    choices = [(str(t[0].id), t[1].vehicle_num) for t in qry1]

    form = SelectReturnVehicle()
    form.vehicleNum.choices = choices
    print(form.validate_on_submit())

    if form.validate_on_submit():
        tid = int(form.vehicleNum.data)
        odo = form.odo.data
        dateReturn = form.datereturn.data
        print("ID ODO DATE", type(tid), tid, type(odo), odo, type(dateReturn), dateReturn)
        vl = [t for t in qry1 if t[0].id == tid]
        print("VL", vl)
        selectedVehicle = vl[0]
        print("NOLIST", selectedVehicle)

        qry2 = db.session.query(Transaction).filter(Transaction.id == selectedVehicle[0].id).first()
        print(qry2, type(qry2), qry2.state)
        qry2.state = "Complete"
        qry2.end_date = dateReturn
        qry2.end_odo = odo
        print(qry2, type(qry2), qry2.state, qry2.end_odo)

        qry3 = db.session.query(Vehicle).filter(Vehicle.id == selectedVehicle[1].id).first()
        print(qry3, type(qry3), qry3.odometer)
        qry3.update_odo(odo)
        print(qry3, type(qry3), qry3.odometer)

        db.session.commit()
        flash("Successfully returned your vehicle!")
        return redirect(url_for("index"))

    return render_template("select_return.html", transvehicle=qry1, form=form, type='customer')


