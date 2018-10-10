from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Length, ValidationError, Email
from EpicCoders.models import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user



class RegistrationForm(FlaskForm):

	username = wtforms.StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
	password = wtforms.PasswordField("Password", validators=[DataRequired(), Length(min=8)])
	# confirm_password = wtforms.PasswordField("confirm Password", validators=[DataRequired()])
	first_name = wtforms.StringField("First name", validators=[DataRequired(), Length(min=2, max=10)])
	last_name = wtforms.StringField("Last name", validators=[DataRequired(), Length(min=2, max=10)])
	email = wtforms.StringField("Email", validators=[DataRequired(), Length(max=35), Email()])

	submit_button = wtforms.SubmitField("Sign Up")

	# def validate_confirm_password(self, confirm_password):

	# 	if confirm_password != self.password.data: #search how to get fields inside another field validation
	# 		raise ValidationError("passswords don't match")


	def validate_username(self, username):

		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError("اسم المستخدم مأخوذ من قبل مستخدم آخر")


class LoginForm(FlaskForm):
	UsernameOrEmail = wtforms.StringField("Username Or Email", validators=[DataRequired()])
	password = wtforms.PasswordField("Password", validators=[DataRequired()])
	remember = wtforms.BooleanField("remember me")

	submit_button = wtforms.SubmitField("Login")

	def validate_UsernameOrEmail(self, UsernameOrEmail):

		user_using_email = User.query.filter_by(email=UsernameOrEmail.data).first()
		user_using_username = User.query.filter_by(username=UsernameOrEmail.data).first()

		if user_using_email or user_using_username:
			pass
		else:
			raise ValidationError("اسم المستخدم او البريد الالكتروني خاطئ")




class UpdateUserForm(FlaskForm):
	username = wtforms.StringField("Username", validators=[Length(min=3, max=20)])
	email = wtforms.StringField("Email", validators=[Length(max=35), Email()]) 
	first_name = wtforms.StringField("First name", validators=[Length(min=2, max=10)])
	last_name = wtforms.StringField("Last name", validators=[Length(min=2, max=10)])
	picture = FileField("Update profile picture", validators=[FileAllowed(["jpg", 'png', "gif", "jpeg"])])

	submit = wtforms.SubmitField('Update')



	def validate_username(self, username):

		if current_user.username != username.data:
				user = User.query.filter_by(username=username.data).first()
				if user:
					raise ValidationError("هذا الاسم المستعار مأخوذ")


	def validate_email(self, email):

		if current_user.email != email.data:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("هذا اليميل نستخدم")



majors = [('Computer Science', 'Computer Science'), ('Quran kareem', "Quran kareem"), ('Design', 'Design')]


class CreateCourse(FlaskForm):
	course_name = wtforms.StringField("Course name", validators=[Length(min=3, max=20), DataRequired()])
	image = FileField("Course image", validators=[FileAllowed(["jpg", 'png', "gif", "jpeg"])])
	description = wtforms.StringField('Course description', validators=[DataRequired(), Length(min=3, max=150)])
	course_major = wtforms.SelectField('Course Major', choices=majors, default=None)
	course_major_another = wtforms.StringField('Other')
	course_type = wtforms.SelectField('Course Type', choices=[('public', 'Public'), ('private', 'Private')])
	subscribers = wtforms.StringField('Subscribers', validators=[Length(max=400)])

	submit = wtforms.SubmitField("Create Course")



class CreateEpisode(FlaskForm):
	episode_name = wtforms.StringField('Episode name', validators=[DataRequired(), Length(min=3, max=30)])
	picture = FileField("Episode image", validators=[FileAllowed(["jpg", 'png', "gif", "jpeg"])])
	video = wtforms.StringField('أرفق مقطع يوتيوب', validators=[Length(min=10, max=200)]) # string for youtube embeded videos
	text = wtforms.StringField('text', validators=[Length(max=3000)])
	description = wtforms.StringField('Description', validators=[Length(max=90)])

	submit = wtforms.SubmitField("Create Episode")



class DeleteCourse(FlaskForm):
	submit = wtforms.SubmitField('Delete Course')


class DeleteEpisode(FlaskForm):
	submit = wtforms.SubmitField('Delete Episode')