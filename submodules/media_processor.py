import ffmpy, os

def convert_video(chat_id, input_type, output_type):
	"""
	The function video of one type to another.
	Args:
		chat_id: unique identification for video name
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
