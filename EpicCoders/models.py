from EpicCoders import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	first_name = db.Column(db.String(10), nullable=False)
	last_name = db.Column(db.String(10), nullable=False)
	email = db.Column(db.String(35), nullable=False, unique=True)
	picture = db.Column(db.String(300), nullable=False, default='default.jpg')
	user_type = db.Column(db.String(33), nullable=False, default='user')
	courses = db.relationship('Course', backref='creator', lazy=True)

	def __repr__(self):
		return f"{self.username}"



class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	course_name = db.Column(db.String(20), unique=True, nullable=False)
	image = db.Column(db.String(20), nullable=False)
	description = db.Column(db.String(150), nullable=False) 
	creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	episode = db.relationship('Episode', backref='course', lazy=True)


class Episode(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	episode_name = db.Column(db.String(30), nullable=False)
	image = db.Column(db.String(20), nullable=True, default='default.jpg')
	video = db.Column(db.String(200), nullable=True)
	text = db.Column(db.String(3000), nullable=True)
	description = db.Column(db.String(90), nullable=True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)






	