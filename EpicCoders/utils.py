import secrets
import os
from flask_login import current_user
from EpicCoders import app
from PIL import Image



def save_image(image_file, path, view):
	if image_file:

		# create random string
		random_string = secrets.token_hex(9)

		# get image extention
		_, extention = os.path.splitext(image_file.filename)

		# create image_name
		image_filename = random_string + extention

		# path to save in
		image_path = os.path.join(app.root_path, path, image_filename)

		# resize image and save it to specified path 
		if view == "account":
			new_size = (125, 125)
			image = Image.open(image_file)
			image.thumbnail(new_size)
			image.save(image_path)
		else:
			image_file.save(image_path) # <- this is saving the image without resizing

		return image_filename

	return current_user.picture



def save_video(video_file, path, view):
	if video_file:

		# create random string
		random_string = secrets.token_hex(9)

		# get video extention
		_, extention = os.path.splitext(video_file.filename)

		# create video_name
		video_filename = random_string + extention

		# path to save in
		video_path = os.path.join(app.root_path, path, video_filename)

		# save video to specified path 
	
		video_file.save(video_path)

		return video_filename

	return None



# this function takes names seperated bu commas and puts them in a list for example ammar, ahmad, khalid will be ['ammar', 'ahmad', 'khalid']
def perfect_list(string):
	new_list = []
	sub_string = None
	current_position = 0
	till_position = 0
	loop_count = 0
	keep_for_last_till = till_position
	while True:
		till_position = string.find(',', current_position)
		if till_position == -1:
			if loop_count > 0:
				sub_string = string[keep_for_last_till + 1: len(string)]
			else:
				sub_string = string[keep_for_last_till: len(string)]
			sub_string = sub_string.strip()
			new_list.append(sub_string)
			break

		sub_string = string[current_position:till_position]
		sub_string = sub_string.strip()
		new_list.append(sub_string)
		current_position = till_position + 1
		keep_for_last_till = till_position
		loop_count += 1
	return new_list


def generate_unique_token_hex(courses):
	token = secrets.token_hex(5)

	while True:
		unique = True
		for course in courses:
			if token == course.course_unique_string:
				token = secrets.token_hex(5)
				unique = False
		
		if unique:
			break
			

	return token



def generate_slug(title):

	title = title.replace(' ', '-')
	title = title.replace(',', '-')
	title = title.replace('(', '-')
	title = title.replace(')', '-')
	title = title.replace('?', '-qmark-')
	title = title.replace('؟', '-qmark-')
	title = title.replace(':', '-')
	title = title.replace(';', '-')
	title = title.replace('|', '-')
	title = title.replace('~', '-')
	title = title.replace('`', '-')
	title = title.replace('*', '-')
	title = title.replace('&', '-')
	title = title.replace('^', '-')
	title = title.replace('%', '-')
	title = title.replace('+', '-')
	title = title.replace('=', '-')
	title = title.replace('$', '-')
	title = title.replace('#', '-')
	title = title.replace('@', '-')
	title = title.replace('!', '-')
	title = title.replace('<', '-')
	title = title.replace('>', '-')
	title = title.replace('/', '-')
	title = title.replace('"', '-')
	title = title.replace("'", '-')


	

	return title

