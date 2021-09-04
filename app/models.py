from app import db
from app import login
from datetime import datetime 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# example of how to create association table
#association_table = db.Table('association', 
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'))
#)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	# balance = db.relationship('Balance',backref='user',lazy='dynamic')
	balance = db.Column(db.Float(64))
	# questions = db.relationship('Question', backref='from_user', 
	# 							lazy='dynamic')
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def check_balance(self):
		return self.balance
	
	def deduct_balance(self, value):
		self.balance = self.balance - value
		return self.balance
	
	def add_balance(self, value):
		self.balance = self.balance + value
		return self.balance

	def __repr__(self):
		return f'<User {self.username:}>'

# class Balance(db.Model):
# 	__tablename__ = 'balance'
# 	id = db.Column(db.Integer, primary_key=True)

# 	balance = db.Column(db.Float(64))
# 	uid = db.Column(db.Integer, db.ForeignKey(User.id))

class Vehicle(db.Model):
	__tablename__ = 'vehicle'
	id = db.Column(db.Integer, primary_key=True)


# create your model for the database here

