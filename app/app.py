from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b2649b0d7c71121421a0226c4458b680'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):					#Creates a database class for the user
	id = db.Column(db.Integer, primary_key=True)		#Creates the primary key for the database which is unique
	role = db.Column(db.String(30), nullable=False)		#Creates a role column in the database, where each entry needs to have an input for this
	username = db.Column(db.String(30), unique=True, nullable=False)	#Creates the username column, where each entry needs to be unique to other entries in this column.
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.role}', '{self.username}', '{self.email}', '{self.password}')"

class Business_details(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	keywords = db.Relationship('Keywords', backref='keyword', lazy=True)
	family_name = db.Relationship('Family', backref='Family_name', lazy=True)
	creator = db.Relationship('User', backref='Entry_creator', lazy=True)
	phone_number = db.Column(db.String(12), nullable = False)
	email = db.Column(db.String(50), nullable=False)
	address = db.Column(db.String(60), nullable=False)
	display_photo = db.Column(db.String(20))
	web_address = db.Column(db.String(60), nullable=False)
	company_name = db.Column(db.String(60), nullable=False)
	description = db.Column(db.String(120), nullable=False)
	
class Family(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40), unique=True, nullable=False)
	workplace = db.Column(db.String(40), nullable=False)
	email = db.Column(db.String(40), unique=True, nullable=True)
	phone_number = db.Column(db.String(12), nullable=True, unique=True)

class Keywords(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	keyword = db.Column(db.String(20), unique=True, nullable=False)




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

if __name__ == "__main__":
	app.run(debug=True)