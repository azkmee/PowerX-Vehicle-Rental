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


# Public Route
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

# vehicleType = RadioField('Vehicle Type', choices = [('Car', 'Car'),('Lorry','Lorry'),('Van','Van')])
# vehicleNum = StringField('Vehicle Number', validators=[DataRequired()])
# modelNumber = StringField('Model Number', validators=[DataRequired()])
# purchaseDate = DateField('Purchase Date', validators=[DataRequired()])
# odometer = DecimalField('Odometer', validators= [DataRequired()] )
# submit = SubmitField('Add Vehicle')

# ref: https://stackoverflow.com/questions/17057191/redirect-while-passing-arguments
# ref: https://stackoverflow.com/questions/8895208/sqlalchemy-how-to-filter-date-field
@application.route('/select', methods=["GET", "POST"])
# @login_required
def selectVehicle():
    if current_user.is_anonymous:
        class UserAnon:
            type=None
        user = UserAnon()
    else:
        user = User.query.filter_by(username=current_user.username).first()
    selectionForm = GetAvailableVehicles()
    bookingForm = None
    vehicles = None
    if selectionForm.validate_on_submit():
        startDate = selectionForm.startDate.data
        endDate = selectionForm.endDate.data
        vt = selectionForm.vehicleType.data
        print(startDate, endDate)
        print(vt)
        # qry = db.session.query(Vehicle).filter_by(vehicle_type=vehicletype)
        # qry = db.session.query(Vehicle).all()
        #####qry = db.session.query(Vehicle).filter_by(vehicle_type = vt)
        # qry = Vehicle.query().filter(Vehicle.vehicle_type == vt).all()
        qry = db.session.query(Vehicle).filter(Vehicle.vehicle_type == vt).all()
        print("QRY", qry)
        vehicles = [v for v in qry]
        print([(v.id, v.vehicle_type) for v in vehicles])
        # ss["vid"] = [v.id for v in vehicles]
        ss["start"] = startDate.strftime("%d/%m/%Y")
        ss["end"] = endDate.strftime("%d/%m/%Y")
        # dictparams = {"start": startDate, "end": endDate}
        # return redirect(url_for("bookVehicle", vehicles='.'.join([str(v.id) for v in vehicles]),
        #                         startDate=startDate, endDate=endDate))

        """
        Algorithm: 
        1) Check if either transaction start date or (start + duration) is within our start and end date
        2) If either case, then if it is Booked or Dispatch, Reject the vehicle
        """
        qry2 = db.session.query(Transaction) \
            .filter(db.and_(db.or_(Transaction.start_date.between(startDate, endDate),
                                   (Transaction.start_date + Transaction.book_duration)
                                   .between(startDate, endDate)),
                            Transaction.state.in_(["Booked", "Dispatch", "Paid"]))) \
            .all()

        rejectedVid = [t.vid for t in qry2]
        print("Rejected Vehicles", rejectedVid)

        qry3 = db.session \
            .query(Vehicle).filter(Vehicle.vehicle_type == vt) \
            .filter(~Vehicle.id.in_(rejectedVid)) \
            .all()
        filteredVehicles = [v for v in qry3]
        print("QRY3", qry3)
        print([(v.id, v.vehicle_type) for v in filteredVehicles])
        ss["vid"] = [v.id for v in filteredVehicles]

        return redirect(url_for("bookVehicle"))

        # return render_template("select_vehicle.html", selectionForm=selectionForm, bookingForm=bookingForm, vehicles=vehicles)

    # elif bookingForm is not None:
    #     print("Booking Form not none")
    #     if bookingForm.validate_on_submit():
    #         print("Booked")
    #         print(bookingForm.vehicleNum.data)
    #         #REDIRECT
    #         return render_template("select_vehicle.html", selectionForm=selectionForm, bookingForm=bookingForm, vehicles=vehicles)

    return render_template("select_vehicle.html", selectionForm=selectionForm, type=user.type)


@application.route('/book', methods=["GET", "POST"])
# @login_required
def bookVehicle():
    if current_user.is_anonymous:
        class UserAnon:
            type=None
        user = UserAnon()
    else:
        user = User.query.filter_by(username=current_user.username).first()
    vid = ss["vid"]
    startDate = ss["start"]
    endDate = ss["end"]
    vehicles = db.session.query(Vehicle).filter(Vehicle.id.in_(vid)).all()
    form = BookVehicle()
    form.vehicleNum.choices = [(str(v.id), v.vehicle_num) for v in vehicles]

    if form.validate_on_submit():
        s = int(form.vehicleNum.data)
        selectedVehicle = db.session.query(Vehicle).filter(Vehicle.id == s).first()
        bookdays = (datetime.datetime.strptime(endDate, "%d/%m/%Y")
                    - datetime.datetime.strptime(startDate, "%d/%m/%Y")).days + 1

        r = Transaction(vid=selectedVehicle.id,
                        cid=current_user.id,
                        start_date=datetime.datetime.strptime(startDate, "%d/%m/%Y"),
                        book_duration=bookdays,
                        state="Booked",
                        amount=selectedVehicle.unit_price * bookdays)
        db.session.add(r)
        db.session.commit()
        flash(f"You have booked {selectedVehicle.vehicle_num} from {startDate} to {endDate}.")

        return redirect(url_for("selectPayTransaction"))

    return render_template("book_vehicle.html", startDate=startDate,
                           endDate=endDate, vehicles=vehicles, bookingForm=form, type=user.type)

