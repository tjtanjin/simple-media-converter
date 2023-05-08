import ffmpy, os, pyheif, json
from rlottie_python import LottieAnimation
from PIL import Image

# used to handle support lottie conversion types from telegram stickers
lottie_supported_types = ["png", "tiff", "pdf", "webp", "gif"]

# used to handle supported videos/images types
video_types = json.loads(os.getenv("VIDEO_TYPES"))

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

def convert_sticker(chat_id, input_type, output_type):
	"""
	The function converts video of one type to another.
	Args:
		chat_id: unique identification for video
		input_type: video input type
		output_type: video output type
	"""
	try:
		if output_type in lottie_supported_types:
			anim = LottieAnimation.from_tgs('./input_media/{}.{}'.format(chat_id, input_type))
			anim.save_animation('./output_media/{}.{}'.format(chat_id, output_type))
			return None
	
		if output_type in video_types:
			anim = LottieAnimation.from_tgs('./input_media/{}.{}'.format(chat_id, input_type))
			anim.save_animation('./input_media/{}.{}'.format(chat_id, "gif"))
			convert_video(chat_id, "gif", output_type)
			os.remove("./input_media/{}.{}".format(chat_id, "gif"))
		else:
			anim = LottieAnimation.from_tgs('./input_media/{}.{}'.format(chat_id, input_type))
			anim.save_animation('./input_media/{}.{}'.format(chat_id, "png"))
			convert_image(chat_id, "png", output_type)
			os.remove("./input_media/{}.{}".format(chat_id, "png"))
	except:
		# if all else fails, convert sticker straight to image type
		convert_image(chat_id, "tgs", output_type)
	return None

def convert_image(chat_id, input_type, output_type):
	"""
	The function converts image of one type to another.
	Args:
		chat_id: unique identification for image
		input_type: video input type
		output_type: video output type
	"""
	if (input_type == "heif"):
		heif_file = pyheif.read('./input_media/{}.{}'.format(chat_id, input_type))
		img = Image.frombytes(
		    heif_file.mode, 
		    heif_file.size, 
		    heif_file.data,
		    "raw",
		    heif_file.mode,
		    heif_file.stride)
	else:
		img = Image.open('./input_media/{}.{}'.format(chat_id, input_type))
	if output_type == "jpg" or ((input_type == "tiff" or input_type == "png") and output_type == "pdf"):
		img = img.convert('RGB')
	elif output_type == "ico":
		icon_size = [(32, 32)]
		img.save('./output_media/{}.{}'.format(chat_id, output_type), sizes=icon_size)
		return None
	img.save('./output_media/{}.{}'.format(chat_id, output_type), quality=95, optimize=True)
	return None
