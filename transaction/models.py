from datetime import datetime
from transaction import db, login_manager
from flask_login import UserMixin
from pytz import timezone

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	"""docstring for User"""
	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(20), nullable = False)
	lastname = db.Column(db.String(20), nullable = False)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	password = db.Column(db.String(60), nullable = False)
	date = db.Column(db.DateTime, default=datetime.now(
            timezone("Asia/Kolkata")).replace(microsecond=0))
	user_transaction = db.relationship('Transaction', backref = "transaction", lazy = True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"
		


class Transaction(db.Model):
	"""docstring for Transaction"""
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)
	card_type = db.Column(db.String(100), nullable = False)
	card_number = db.Column(db.Integer, nullable = False)
	amount_withdrawal = db.Column(db.Integer, nullable = False)
	amount_remaining = db.Column(db.Integer, nullable = False)
	wallet_balance = db.Column(db.Integer, nullable = False)
	transaction_date = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

	def __repr__(self):
		return f"Transaction('{self.name}', '{self.card_type}', '{self.card_number}', '{self.amount_withdrawal}', '{self.amount_remaining}', '{self.wallet_balance}')"