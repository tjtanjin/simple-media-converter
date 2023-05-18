import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from submodules import user_input as ui

def main():
	print("Simple Media Converter instance started!")
	token = os.getenv("BOT_TOKEN")
	application = Application.builder().token(token).read_timeout(30).write_timeout(30).build()
	application.add_handler(CommandHandler('start', ui.start))
	application.add_handler(CommandHandler('help', ui.show_help))
	application.add_handler(MessageHandler(filters.Document.ALL, ui.get_document))
	application.add_handler(MessageHandler(filters.PHOTO, ui.get_photo))
	application.add_handler(MessageHandler(filters.VIDEO, ui.get_video))
	application.add_handler(MessageHandler(filters.Sticker.ALL, ui.get_sticker))
	application.add_handler(CallbackQueryHandler(ui.output_photo_type, pattern='photo_(\S+)_(\S+)'))
	application.add_handler(CallbackQueryHandler(ui.output_video_type, pattern='video_(\S+)_(\S+)'))
	application.add_handler(CallbackQueryHandler(ui.output_sticker_type, pattern='sticker_(\S+)_(\S+)'))
	application.run_polling()

if __name__ == '__main__':
	main()
