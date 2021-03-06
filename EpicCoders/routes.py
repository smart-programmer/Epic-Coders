from EpicCoders import app, db, bcrypt
from flask import render_template, redirect, url_for, request, flash
from EpicCoders.forms import (RegistrationForm, LoginForm, UpdateUserForm, CreateCourse, CreateEpisode,
 DeleteWithName, Subscribe, InputField)
from EpicCoders.models import User, Course, Episode
from flask_login import current_user, login_user, logout_user, login_required
from EpicCoders.utils import save_image, perfect_list, generate_unique_token_hex, generate_slug
import os
import random




@app.route('/')
def Home(): 
	courses = Course.query.filter_by(course_accessibility='public').limit(4).all()
	return render_template("Home.html", is_Home=True, without_background=True, courses=courses)


@app.route('/register', methods=["GET", "POST"])
def register(): 
	if current_user.is_authenticated:
		redirect(url_for("Home"))

	form = RegistrationForm()

	if form.validate_on_submit():
		password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		if form.username.data == 'ammar' or form.username.data == 'homsi':
			user_type = 'super_user'
		else:
			user_type = 'user'
		user = User(username=form.username.data, password=password,
		 first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
		  user_type=user_type)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("Home"))

	return render_template("register.html", form=form, is_registration_form=True, no_bootstrab=True)


@app.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		redirect(url_for("Home"))

	login_form = LoginForm()

	if login_form.validate_on_submit():
		user_using_username = User.query.filter_by(username=login_form.UsernameOrEmail.data).first()
		user_using_email = User.query.filter_by(email=login_form.UsernameOrEmail.data).first()

		if user_using_username:
			if bcrypt.check_password_hash(user_using_username.password, login_form.password.data):
				login_user(user_using_username, remember=login_form.remember.data)
				next_page = request.args.get("next") # next is set on login_required views

				return redirect(next_page) if next_page else redirect(url_for("Home"))
			else:
				return redirect(url_for('Home'))
		elif user_using_email:
			if bcrypt.check_password_hash(user_using_email.password, login_form.password.data):
				login_user(user_using_email, remember=True) # login_form.remember.data
				next_page = request.args.get("next") # next is set on login_required views

				return redirect(next_page) if next_page else redirect(url_for("Home"))
			else:
				return redirect(url_for('Home'))
		else:
			flash("فشل تسجيل الدخول يرجى التحقق من المعلومات المدخلة", 'danger')
			redirect(url_for("Home"))

	return render_template("login.html", form=login_form, is_login_form=True, no_bootstrab=True)


@app.route('/logut', methods=["GET", "POST"])
def logout():
	logout_user()
	return redirect(url_for("Home"))


@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
	form = UpdateUserForm()

	if form.validate_on_submit():
		if form.picture.data:
			image_name = save_image(form.picture.data, 'static/images/profile_pics', 'account')
			current_user.picture = image_name

		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		db.session.commit()
		flash("Your account has been updated successfuly", "success")

		return redirect(url_for('account'))

	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name

	image_file = url_for('static', filename=f'images/profile_pics/{current_user.picture}')
	return render_template("account.html", is_account=True, without_background=True, image_file=image_file, form=form)


@app.route('/developers_page')
def developers_page():

	return render_template('developers_page.html', is_developers_page=True)



@app.route('/courses')
def courses():
	courses = Course.query.all()
	
	return render_template('courses.html', courses=courses, is_courses=True)


@app.route('/my_courses/<username>/')
def user_courses(username):
	user_username = username

	empty = True
	subscribed_to_courses = current_user.subscribed_to_courses
	courses_created = current_user.courses

	courses = subscribed_to_courses + courses_created

	if courses:
		empty = False

	return render_template('my_courses.html',  courses=courses, empty=empty, is_courses=True)




@app.route('/course/<course_id>/', methods=['GET', 'POST'])
@login_required
def course(course_id):
	courseId = course_id
	course = Course.query.get(courseId)
	course_slug = generate_slug(course.course_name)

	if not course:
		return redirect(url_for('Home'))
	
	image_file = url_for('static', filename=f'images/courses/{course.image}')

	episodes = course.episodes

	episode_image_file = None

	subscribe_form = None
	delete_course_form = None

	does_own_course = False
	form = None

	if course.creator == current_user:
		does_own_course = True

	if does_own_course:		
		form = CreateEpisode()
		delete_course_form = DeleteWithName()
		delete_course_form.name.label.text = 'Enter course name to delete it'
		if form.validate_on_submit() and len(form.episode_name.data) > 0:
			episode_name = form.episode_name.data
			text = form.text.data
			description = form.description.data
			image_name = save_image(form.picture.data, 'static/images/episodes', 'course')
			video = form.video.data
		

			episode = Episode(episode_name=episode_name,
				text=text,
				description=description, image=image_name, video=video, course_id=courseId)

			db.session.add(episode)
			db.session.commit()

			return redirect(url_for("course", course_id=course.id))

		elif delete_course_form.validate_on_submit() and delete_course_form.name.data:
			if delete_course_form.name.data == course.course_name:
				db.session.delete(course)
				db.session.commit()
				return redirect(url_for('user_courses', username=current_user.username))

	else:
		subscribe_form = Subscribe()
		# here i'm doing the validation twice so i can set the subscribe button to display the correct thing
		if current_user in course.subscribers:
			subscribe_form.submit.label.text = "Unsubscribe"
			if subscribe_form.validate_on_submit():
				course.subscribers.remove(current_user)
				db.session.commit()
				return redirect(url_for('course', course_id=course.id))
		else:
			subscribe_form.submit.label.text = "Subscribe"
			if subscribe_form.validate_on_submit():
				course.subscribers.append(current_user)
				db.session.commit()
				return redirect(url_for('course', course_id=course.id))


	images_file = url_for('static', filename='images/episodes')

	return render_template('course.html', course=course, is_course=True, image_file=image_file, form=form
		, episode_image_file=episode_image_file, episodes=episodes, images_file=images_file,
		 without_background=True, users=course.subscribers, delete_course_form=delete_course_form,
		 subscribe_form=subscribe_form, does_own_course=does_own_course, 
		 course_slug=course_slug)


@app.route('/course_create', methods=['GET', 'POST'])
@login_required
def create_course():

	form = CreateCourse()

	if form.validate_on_submit():
		subscribers_list = []
		if form.subscribers.data:
			subscribers_list = perfect_list(form.subscribers.data)
			
		course_name = form.course_name.data
		image_name = save_image(form.image.data, 'static/images/courses', 'create_course')
		description = form.description.data
		# because course major has two fields one is select field the other is for other majors this logic needs to be here
		course_field = form.course_field.data
		course_field_another = form.course_field_another.data
		if course_field_another:
			course_field = course_field_another
			
		course_accessibility = form.course_accessibility.data
		course_unique_token = generate_unique_token_hex(Course.query.all())

		course = Course(course_name=course_name, creator_id=current_user.id,
		 image=image_name, description=description, course_field=course_field,
		  course_accessibility=course_accessibility, course_unique_string=course_unique_token)

		for subscriber in subscribers_list:
			user = User.query.filter_by(username=subscriber).first()
			if user:
				course.subscribers.append(user)

		db.session.add(course)
		db.session.commit()
		return redirect(url_for('Home'))

	
	return render_template("create_course.html", form=form)






@app.route('/<course_name>/episode/<episode_id>', methods=['GET', 'POST'])
@login_required
def episode(course_name, episode_id):
	episode = Episode.query.get(episode_id)
	if not episode:
		return redirect(url_for('Home'))

	course = Course.query.get(episode.course_id)
	is_owner = current_user == Course.query.get(episode.course_id).creator
	delete_episode_form = None

		
	image_file = url_for('static', filename=f'images/episodes/{episode.image}')

	if is_owner:
		delete_episode_form = DeleteWithName()
		delete_episode_form.name.label.text = 'Enter episode name to delete it'
		if delete_episode_form.validate_on_submit() and delete_episode_form.name.data:
			if delete_episode_form.name.data == episode.episode_name:
				db.session.delete(episode)
				db.session.commit()
				return redirect(url_for('course', course_id=course.id))
	else:
		# this will prevent people from typing the url for an episode and watching it without subscribing
		if course not in current_user.subscribed_to_courses:
			return redirect(url_for('Home'))

	if len(episode.video) == 0:
		episode.video = 'No video with this episode'
	if len(episode.text) == 0:
		episode.text = 'No text with this episode'
	if len(episode.description) == 0:
		episode.description = 'No description for this episode'


	return render_template('episode.html', episode=episode, image_file=image_file, is_episode=True,
	 delete_episode_form=delete_episode_form)




@app.route('/courses/subscribe_by_course_token', methods=['GET', 'POST'])
def token_hex_input():
	form = InputField()
	form.field.label.text = 'Token'
	form.submit.label.text = 'Subscribe'

	if form.validate_on_submit():
		course = Course.query.filter_by(course_unique_string=form.field.data).first()
		if course and course not in current_user.subscribed_to_courses:
			course.subscribers.append(current_user)
			db.session.commit()
			return redirect(url_for('user_courses', username=current_user.username))
		else:
			return redirect(url_for('Home'))


	return render_template('token_hex_input.html', form=form, is_token_hex_input=True)



# @app.route('/warning')
# def warning():
# 	return render_template('warning.html')



# @app.route('/private_page')
# def warning_private():

# 	return render_template('private_page.html')



# make a warning sysytem from one view that you'll pass the type of warnning in the url 













# @app.route('/episode_create')
# def episode_create():
# 	form = CreateEpisode()
# 	does_own_course = False
# 	if form.validate_on_submit():
# 		course_name = form.course_name.data
# 		for course in Course.query.filter_by(creator_id=current_user.id)
# 			if course.course_name = course_name:
# 				does_own_course = True
# 		if does_own_course:
# 			episode_name = form.episode_name.data
# 			text = form.text.data
# 			description = form.description.data

# 			episode = Episode(course_name=course_name, 
# 				episode_name=episode_name,
# 				text=text,
# 				description=description)

# 			db.session.add(episode)
# 			db.session.commit()

# 			return url_for("courses") 
		
# 	return render_template('episode_create.html')




# elif delete_course_form.validate_on_submit():
		# 	db.session.delete(course)
		# 	db.session.commit()
		# 	return redirect(url_for('user_courses', username=current_user.username))






# deside wich form is valid depending on the data