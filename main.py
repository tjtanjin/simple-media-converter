import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

from telegram.ext import Application
from interactions.loader import load_interactions


def main():
	token = os.getenv("BOT_TOKEN")
	application = Application.builder().token(token).read_timeout(30).write_timeout(30).build()
	load_interactions(application)
	print("Simple Media Converter instance started!")
	application.run_polling()


if __name__ == '__main__':
	main()
