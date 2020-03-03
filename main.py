from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from submodules import user_input as ui
import json

def main():
	print("Running...")
	with open("./config/token.json", "r") as file:
		token = json.load(file)["token"]
	updater = Updater(token, use_context=True, workers=4)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('start', ui.start))
	dp.add_handler(CommandHandler('help', ui.show_help))
	dp.add_handler(MessageHandler(Filters.document, ui.get_document))
	dp.add_handler(MessageHandler(Filters.photo, ui.reject_photo))
	dp.add_handler(MessageHandler(Filters.video, ui.get_video))
	dp.add_handler(CallbackQueryHandler(ui.output_photo_type, pattern='photo_(\S+)_(\S+)'))
	dp.add_handler(CallbackQueryHandler(ui.output_video_type, pattern='video_(\S+)_(\S+)'))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
