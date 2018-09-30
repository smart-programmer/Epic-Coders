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