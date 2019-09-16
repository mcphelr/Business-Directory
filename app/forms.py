from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.database_models import User
class RegistrationForm(FlaskForm):
	username = StringField('Owner', validators=[DataRequired(), Length(min=2, max=16)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()	#Checks to see if there is any instance of this username in the database
		if user:	#If there is an instance, user will exist and therefore, a validation error will occur
			raise ValidationError('Username is taken.')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('Email is taken.')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('Owner', validators=[DataRequired(), Length(min=2, max=16)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Change Profile Picture', validators = [FileRequired(), FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update Account')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError('Username is taken.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('Email is taken.')
		
class BusinessForm(FlaskForm):
	business_name = StringField('Business name', validators=[DataRequired()])
	contact_phone_number = StringField('Contact Number', validators=[DataRequired()])
	contact_email_address = StringField('Contact Email', validators=[DataRequired()])
	business_address = StringField('Business Street Address')
	web_address = StringField('Web Address')
	business_description = TextAreaField('Business Description', validators=[DataRequired()])
	business_photo = FileField('Business Photo', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Add Business')
