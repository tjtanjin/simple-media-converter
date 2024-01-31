import i18n
import os

from dotenv import load_dotenv
from health_ping import HealthPing
from telegram.ext import Application
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
i18n.load_path.append('./assets/lang')
i18n.set('file_format', 'json')
i18n.set('filename_format', '{locale}.{format}')
i18n.set('locale', os.getenv("LANGUAGE"))
i18n.set('fallback', 'en-US')

from interactions.loader import load_interactions # noqa

if os.getenv("HEALTHCHECKS_ENDPOINT"):
    HealthPing(url="https://hc-ping.com/613b74f2-e71b-49de-95e5-f8b617d23525",
               schedule="1 * * * *",
               retries=[60, 300, 720]).start()


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
