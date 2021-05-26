from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from transaction.models import User
class RegistrationForm(FlaskForm):
	"""docstring for RegistrationForm"""
	firstname = StringField('First Name',
							validators=[DataRequired()])
	lastname = StringField('Last Name',
							validators=[DataRequired()])
	username = StringField('Username',
						validators = [DataRequired(), Length(min = 2, max = 20)])
	email = StringField('Email',
						validators = [DataRequired(), Email()])
	password = PasswordField('Password', 
						validators =[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
						validators =[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one')
		
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That Email is taken. Please choose a different one')

class LoginForm(FlaskForm):
	"""docstring for LoginForm"""
	
	email = StringField('Email',
						validators = [DataRequired(), Email()])
	password = PasswordField('Password', 
						validators =[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class ChangePassword(FlaskForm):
	"""docstring for LoginForm"""
	
	password = PasswordField('Password', 
						validators =[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
						validators =[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')
		