from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from submodules import user_input as ui
import json

def main():
	print("Running...")
	with open("./config/token.json", "r") as file:
		token = json.load(file)["token"]
	updater = Updater(token, use_context=True, workers=4)
	dp = updater.dispatcher
	dp.add_handler(MessageHandler(Filters.video, ui.get_video))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
