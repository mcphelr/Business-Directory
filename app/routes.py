import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, BusinessForm
from app.database_models import User, Business_details, Family, Keywords
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
	posts = Business_details.query.all()
	return render_template ('home.html', posts=posts)

@app.route('/about')
def about():
	return render_template ('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():		#If the form was valid
		password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email = form.email.data, password=password_hash)	#Creates a variable user which holds the data for an entry to the database
		db.session.add(user)			#Adds the user variable, which is set
		db.session.commit()
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:	#If the user is already logged in, send them to the home page
		return redirect(url_for('home'))
	form = LoginForm()		#Declares the variable form as the login form in forms.py
	if form.validate_on_submit():	#If the form is valid
		user = User.query.filter_by(email = form.email.data).first()	#Checks to see if the email matches one in the database
		if user and bcrypt.check_password_hash(user.password, form.password.data):	#If there is an email that matches and the password hashes are for the same password
			login_user(user, remember=form.remember.data)	#Logs in the user
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login unsuccessful, please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_profile_picture(form_picture):
	random_hex = secrets.token_hex(8)		#Creates a random hex to add to the file name so that it does not conflict with present photos in the db
	_, f_ext = os.path.splitext(form_picture.filename)	#Returns the extension of the file
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/Photos/profile_pictures', picture_fn)
	

	output_size = (125, 125)	# Changing size of the photos
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	i.save(picture_path)	#Saving the picture

	return picture_fn	# Returns the file name of the photo so it can be accessed


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()			
	if form.validate_on_submit():
		if form.picture.data:		#If there is data in this field.
			picture_file = save_profile_picture(form.picture.data)	#Having problem here, saying form is not defined
			current_user.profile_picture = picture_file		#Should change the current users profile picture to the one added in the form.
		current_user.username = form.username.data	#Updates other information
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	profile_picture = url_for('static', filename='Photos/profile_pictures/'+current_user.profile_picture)
	return render_template('account.html', title ='Account', profile_picture=profile_picture, form=form)

def save_business_picture(form_picture):
	random_hex = secrets.token_hex(8)		#Creates a random hex to add to the file name so that it does not conflict with present photos in the db
	_, f_ext = os.path.splitext(form_picture.filename)	#Returns the extension of the file
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/Photos/business_photos', picture_fn)
	

	output_size = (125, 125)	# Changing size of the photos
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	i.save(picture_path)	#Saving the picture

	return picture_fn	# Returns the file name of the photo so it can be accessed

@app.route('/business/new', methods=['GET', 'POST'])
@login_required
def new_business():
	form = BusinessForm()
	if form.validate_on_submit():
		if form.business_photo.data:
			business_photo_file = save_business_picture(form.business_photo.data)
			business = Business_details(business_name=form.business_name.data, 
				phone_number=form.contact_phone_number.data,
				email=form.contact_email_address.data,
				address=form.business_address.data,
				business_photo=business_photo_file,
				web_address=form.web_address.data,
				description=form.business_description.data,
				Entry_creator=current_user)
		else:
			business = Business_details(business_name=form.business_name.data, 
				phone_number=form.contact_phone_number.data,
				email=form.contact_email_address.data,
				address=form.business_address.data,
				web_address=form.web_address.data,
				description=form.business_description.data,
				Entry_creator=current_user)
		db.session.add(business)
		db.session.commit()
		flash('Your business has been added', 'success')
		return redirect(url_for('home'))
	#business_photo = url_for('static', filename='Photos/profile_pictures'+)

	return render_template('create_business.html', title ='Business', form=form, business_picture=Business_details.business_photo)	#Add the business_photo soon

@app.route("/business/<int:business_id>")
def business(business_id):
	business = Business_details.query.get_or_404(business_id)
	return render_template('business.html', title=business.business_name, business=business)
