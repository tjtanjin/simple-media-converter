import ffmpy

def video_to_gif(chat_id):
	"""
	The function video_to_gif converts a given video to gif.
	Args:
		chat_id: unique identification for video name
	"""
	inputs = {'./media/{}.mp4'.format(chat_id): None}
	outputs = {'./media/{}.gif'.format(chat_id): '-t 3 -vf "fps=30,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0'}
	ff = ffmpy.FFmpeg(
	    inputs=inputs,
	    outputs=outputs
	)
	ff.run()
	return None
