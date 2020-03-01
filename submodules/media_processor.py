import ffmpy

def video_to_gif(chat_id):
	"""
	The function video_to_gif converts a given video to gif.
	Args:
		chat_id: unique identification for video name
	"""
	ff = ffmpy.FFmpeg(
	    inputs={'./media/{}.mp4'.format(chat_id): None},
	    outputs={'./media/{}.gif'.format(chat_id): None}
	)
	ff.run()
	return None
