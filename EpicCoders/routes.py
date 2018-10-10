from EpicCoders import app, db, bcrypt
from flask import render_template, redirect, url_for, request, flash
from EpicCoders.forms import (RegistrationForm, LoginForm, UpdateUserForm, CreateCourse, CreateEpisode,
 DeleteCourse, DeleteEpisode)
from EpicCoders.models import User, Course, Episode
from flask_login import current_user, login_user, logout_user, login_required
from EpicCoders.utils import save_image, perfect_list
import os
import random




@app.route('/')
def Home(): 
	
	return render_template("Home.html", is_Home=True, without_background=True)


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
		elif user_using_email:
			if bcrypt.check_password_hash(user_using_email.password, login_form.password.data):
				login_user(user_using_email, remember=True) # login_form.remember.data
				next_page = request.args.get("next") # next is set on login_required views

			return redirect(next_page) if next_page else redirect(url_for("Home"))
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
	# instansiate empty list
	courses_list = []
	
	# add public courses to list
	for course in Course.query.filter_by(course_type='public'):
		courses_list.append(course)

	# add private courses that the user is subscribed to
	for course in Course.query.filter_by(course_type='private'):
		for subscriber in course.subscribers:
			if subscriber == current_user:
				courses_list.append(course)

	# shuffle the list to make the page look random
	random.shuffle(courses_list)
	
	return render_template('courses.html', courses=courses_list, is_courses=True)


@app.route('/course/<course_id>/', methods=['GET', 'POST'])
@login_required
def course(course_id):
	courseId = course_id
	course = Course.query.get(courseId)

	if not course:
		return redirect(url_for('Home'))
	
	image_file = url_for('static', filename=f'images/courses/{course.image}')

	episodes = Episode.query.filter_by(course_id=courseId)
	episode_image_file = None

	does_own_course = False
	form = None

	if course.creator == current_user:
		does_own_course = True

	if does_own_course:		
		form = CreateEpisode()
		delete_course_form = DeleteCourse()
		if form.validate_on_submit():
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

			return redirect(url_for("Home"))

		elif delete_course_form.validate_on_submit():
			db.session.delete(course)
			db.session.commit()
			return redirect(url_for('account'))

	images_file = url_for('static', filename='images/episodes')

	return render_template('course.html', course=course, is_course=True, image_file=image_file, form=form
		, episode_image_file=episode_image_file, episodes=episodes, images_file=images_file,
		 without_background=True, users=course.subscribers, delete_course_form=delete_course_form)


@app.route('/course_create', methods=['GET', 'POST'])
@login_required
def create_course():
	# if current_user.username != 'ammar':
	# 	return redirect(url_for("warning"))

	form = CreateCourse()

	if form.validate_on_submit():
		subscribers_list = []
		if form.subscribers.data:
			subscribers_list = perfect_list(form.subscribers.data)
			
		course_name = form.course_name.data
		image_name = save_image(form.image.data, 'static/images/courses', 'create_course')
		description = form.description.data
		# because course major has two fields one is select field the other is for other majors this logic needs to be here
		course_major = form.course_major.data
		course_major_another = form.course_major_another.data
		if course_major_another:
			course_major = course_major_another
			
		course_type = form.course_type.data
		course = Course(course_name=course_name, creator_id=current_user.id,
		 image=image_name, description=description, course_major=course_major, course_type=course_type)

		for subscriber in subscribers_list:
			user = User.query.filter_by(username=subscriber).first()
			if user:
				course.subscribers.append(user)

		db.session.add(course)
		db.session.commit()
		return redirect(url_for('Home'))

	
	return render_template("create_course.html", form=form)






@app.route('/<course_name>/episode/<episode_id>')
@login_required
def episode(course_name, episode_id):
	episode = Episode.query.get(episode_id)
	if not episode:
		return redirect(url_for('Home'))
		
	image_file = url_for('static', filename=f'images/episodes/{episode.image}')

	delete_episode_form = DeleteEpisode()
	if delete_episode_form.validate_on_submit():
			db.session.delete(episode)
			db.session.commit()
			return redirect(url_for('account'))
	# video_file = url_for('static', filename=f'videos/episodes/{episode.video}')
	# video_extention = os.path.splitext(episode.video)
	# if 'mp4' in video_extention:
	# 	video_extention = 'mp4'
	# elif 'wmv' in video_extention:
	# 	video_extention = 'wmv' 

	return render_template('episode.html', episode=episode, image_file=image_file, is_episode=True,
	 delete_episode_form=delete_episode_form)



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