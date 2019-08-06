from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):					#Creates a database class for the user
	id = db.Column(db.Integer, primary_key=True)		#Creates the primary key for the database which is unique
	role = db.Column(db.String(30), nullable=False)		#Creates a role column in the database, where each entry needs to have an input for this
	username = db.Column(db.String(30), unique=True, nullable=False)	#Creates the username column, where each entry needs to be unique to other entries in this column.
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	creator_id = db.Column(db.Integer, db.ForeignKey('business_details.id'))

	def __repr__(self):
		return f"User('{self.role}', '{self.username}', '{self.email}', '{self.password}')"

class Business_details(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	keywords = db.relationship('Keywords', backref='keyword_selection', lazy=True)
	family_name = db.relationship('Family', backref='Family_name', lazy=True)
	creator = db.relationship('User', backref='Entry_creator', lazy=True)
#Error Here: sqlalchemy.exc.NoForeignKeysError:
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
	family_name_id = db.Column(db.Integer, db.ForeignKey('business_details.id'))

class Keywords(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	keyword = db.Column(db.String(20), unique=True, nullable=False)
	keyword_id = db.Column(db.Integer, db.ForeignKey('business_details.id'))