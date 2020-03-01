from telegram import ParseMode
from submodules import media_processor as mp
import os

def get_video(update, context):
    """
    The function get_video takes video input from the user and processes it
    to return it as a gif to the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    chat_id = update.message.chat_id
    file_id = update.message.video.file_id
    newFile = context.bot.get_file(file_id, timeout=None)
    newFile.download('./media/{}.mp4'.format(chat_id))
    update.message.reply_text("Received file and processing...")
    mp.video_to_gif(chat_id)
    context.bot.send_document(chat_id=chat_id, document=open('./media/{}.gif'.format(chat_id), 'rb'))
    context.bot.send_message(chat_id=chat_id, text="Conversion successful.")
    os.remove("./media/{}.mp4".format(chat_id))
    os.remove("./media/{}.gif".format(chat_id))
    return None

def show_help(update, context):
    """
    Function to show help options to users.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    update.message.reply_text("""Here are the currently available commands:\n
        <b>/help</b> - displays the available commands\n
Have ideas and suggestions for this mini project? Head over to the <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!""", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    return None