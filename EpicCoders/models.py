from EpicCoders import db, login_manager
from flask_login import UserMixin


# the idea for making a many to many relation is simply to create a new table (model) that has a ForeignKey relation
#with both of the tables that you want many to many reltion between them 
#and then you can instansiate the table with the same rows many times

user_course_many_to_many = db.Table("user_course_many_to_many",
									 db.Column('user_id', db.Integer, db.ForeignKey('user.id')), 
									 db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
									 )




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
	course_name = db.Column(db.String(20), nullable=False)
	image = db.Column(db.String(20), nullable=False)
	description = db.Column(db.String(150), nullable=False) 
	course_field = db.Column(db.String(60), nullable=False)
	course_accessibility = db.Column(db.String(20), nullable=False, default='public')
	course_unique_string = db.Column(db.String(20), nullable=False, unique=True)
	creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	episodes = db.relationship('Episode', backref='course', cascade="all,delete", lazy=True)
	subscribers = db.relationship('User', secondary=user_course_many_to_many, 
		backref=db.backref('subscribed_to_courses', lazy=True), lazy='subquery')



class Episode(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	episode_name = db.Column(db.String(30), nullable=False)
	image = db.Column(db.String(20), nullable=True, default='default.jpg')
	video = db.Column(db.String(200), nullable=True)
	text = db.Column(db.String(3000), nullable=True)
	description = db.Column(db.String(90), nullable=True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)






	