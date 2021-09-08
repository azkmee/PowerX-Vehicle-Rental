from werkzeug import useragents
from app import db
from app import login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# example of how to create association table
# association_table = db.Table('association',
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'))
# )

# have a master user that can create a admin user
# normal user register normally


# have a master user that can create a admin user
# normal user register normally


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	type = db.Column(db.String)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def __repr__(self):
		return f'<User {self.username:}>'

class Customer(User):
	balance = db.Column(db.Float(64))
	transaction = db.relationship('Transaction', backref='customer',lazy='dynamic')
	
	def __init__(self, username):
		self.balance = 0
		self.type = 'customer'
		self.username = username

	def check_balance(self):
		return self.balance
	
	def deduct_balance(self, value):
		self.balance = self.balance - value
		return self.balance
	
	def add_balance(self, value):
		self.balance = self.balance + value
		return self.balance
	
class AdminUser(User):
	def __init__(self, username):
		self.type = 'admin'
		self.username=username

	def add_admin_user(self, user_details):
		username = user_details[0]
		password = user_details[1]
		new_admin = AdminUser(username=username)
		new_admin.set_password(password)
		return new_admin

class Vehicle(db.Model):
	__tablename__ = 'vehicle'
	id = db.Column(db.Integer, primary_key=True)
	vehicle_num = db.Column(db.String(64))
	model_number = db.Column(db.String(64))
	# purchase_date = db.Column(db.String(64))
	odometer = db.Column(db.Float(64))
	vehicle_type = db.Column(db.String(64))
	unit_price = db.Column(db.Float(64))
	transaction = db.relationship('Transaction', backref='vehicle', lazy='dynamic')
	# update odo

	def update_odo(self, new_odo):
		self.odometer = new_odo
		

class Car(Vehicle):
	def __init__(self):
		self.unit_price = 90.0
		self.vehicle_type = 'car'

class Van(Vehicle):
	def __init__(self):
		self.unit_price = 100.0
		self.vehicle_type = 'van'

class Lorry(Vehicle):
	def __init__(self):
		self.unit_price = 120.0
		self.vehicle_type = 'Lorry'
	

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    vid = db.Column(db.Integer, index=True)
    cid = db.Column(db.Integer, index=True)
    book_duration = db.Column(db.Integer)  # User will book
    start_date = db.Column(db.Date)  # User will book
    end_date = db.Column(db.Date)  # Updates when User returns
    start_odo = db.Column(db.Float())
    end_odo = db.Column(db.Float())
    amount = db.Column(db.Float())
    additional_fee = db.Column(db.Float())
    state = db.Column(db.String(10))
