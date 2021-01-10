import ffmpy, os
from PIL import Image

def convert_video(chat_id, input_type, output_type):
	"""
	The function converts video of one type to another.
	Args:
		chat_id: unique identification for video
		input_type: video input type
		output_type: video output type
	"""
	inputs = {'./input_media/{}.{}'.format(chat_id, input_type): None}
	if output_type == "gif":
		outputs = {'./output_media/{}.{}'.format(chat_id, output_type): '-t 3 -vf "fps=30,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0'}
	else:
		outputs = {'./output_media/{}.{}'.format(chat_id, output_type): None}
	ff = ffmpy.FFmpeg(
	    inputs=inputs,
	    outputs=outputs
	)
	ff.run()
	return None

def convert_image(chat_id, input_type, output_type):
	"""
	The function converts image of one type to another.
	Args:
		chat_id: unique identification for image
		input_type: video input type
		output_type: video output type
	"""
	img = Image.open('./input_media/{}.{}'.format(chat_id, input_type))
	if output_type == "jpg" or ((input_type == "tiff" or input_type == "png") and output_type == "pdf"):
		img = img.convert('RGB')
	elif output_type == "ico":
		icon_size = [(32, 32)]
		img.save('./output_media/{}.{}'.format(chat_id, output_type), sizes=icon_size)
		return None
	img.save('./output_media/{}.{}'.format(chat_id, output_type), quality=95, optimize=True)
	return None
