from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.database_models import User, Business_details, Family, Keywords


posts = [
	{
		'business': 'Garden Grove',
		'owner': 'Del-oro',
		'description': 'A gardening store',
	},
	{
		'business': 'Murdey-Green Photography',
		'owner': 'Murdey-Green',
		'description': 'A Photography company',
	}
]

@app.route('/')
@app.route('/home')
def home():
	return render_template ('home.html', posts=posts)

@app.route('/about')
def about():
	return render_template ('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'mcphelr@pedarecc.sa.edu.au' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login unsuccessful, please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)
