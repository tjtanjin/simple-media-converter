import i18n
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
i18n.load_path.append('./assets/lang')
i18n.set('file_format', 'json')
i18n.set('filename_format', '{locale}.{format}')
i18n.set('locale', os.getenv("LANGUAGE"))
i18n.set('fallback', 'en-US')
from telegram.ext import Application
from interactions.loader import load_interactions


def main():
	"""
	Handles the initial launch of the program (entry point).
	"""
	token = os.getenv("BOT_TOKEN")
	application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
	load_interactions(application)
	print("Simple Media Converter instance started!")
	application.run_polling()


if __name__ == '__main__':
	main()
