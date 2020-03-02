from telegram import ParseMode
from submodules import media_processor as mp
from submodules import miscellaneous as mc
import os, re

def start(update, context):
    """
    The function welcomes the user and prompts user to input files.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    update.message.reply_text("Hello there! Drop your media here to start conversion! (currently only supports video conversions)")

def get_document(update, context):
    """
    This function captures non-mp4 format documents.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    input_type = update.message.document.mime_type[6:]
    if input_type == "gif" or input_type == "avi" or input_type == "webm" or input_type == "mp4":
        get_video(update, context)
    else:
        pass
    return None

def get_video(update, context):
    """
    The function get_video takes video input from the user and processes it
    to return it as a gif to the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    # accounts for different file format of user input
    try:
        file_id = update.message.video.file_id
        input_type = update.message.video.mime_type[6:]
    except:
        file_id = update.message.document.file_id
        input_type = update.message.document.mime_type[6:]

    chat_id = update.message.chat_id
    receiving_msg = context.bot.send_message(chat_id=chat_id, text="Receiving file...")
    newFile = context.bot.get_file(file_id, timeout=None)
    newFile.download('./input_media/{}.{}'.format(chat_id, input_type))
    reply_markup = mc.show_options(4, ["gif", "avi", "webm", "mp4"], input_type)
    receiving_msg.edit_text(text="Please select the file type to convert to:", reply_markup=reply_markup)
    return None

def output_type(update, context):
    """
    This function triggers upon user's selection of desired output video type.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    context.bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    chat_id = update.callback_query.message.chat.id

    # update user on progress of conversion and send converted media on success
    try:
        match_file = re.match(r'(\S+)_(\S+)', data)
        input_type, output_type = match_file.group(1), match_file.group(2)
        if mc.check_exist_media(chat_id, input_type):
            context.bot.send_message(chat_id=chat_id, text="Processing file...")
            mp.convert_video(chat_id, input_type, output_type)
            context.bot.send_document(chat_id=chat_id, document=open('./output_media/{}.{}'.format(chat_id, output_type), 'rb'), caption="Conversion successful!")
        else:
            context.bot.send_message(chat_id=chat_id, text="File not found, please upload again.")
            return None
    # throw error on failure
    except Exception as ex:
        context.bot.send_message(chat_id=chat_id, text='An error has occurred. Please open an issue at our <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        print(ex)
    # remove all media files at the end
    finally:
        os.remove("./input_media/{}.{}".format(chat_id, input_type))
        os.remove("./output_media/{}.{}".format(chat_id, output_type))


    return None

def show_help(update, context):
    """
    Function to show current conversion type information to users.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    update.message.reply_text("""Here are the currently available conversion types:\n
        <b>.mp4</b>
        <b>.webm</b>
        <b>.gif</b>
        <b>.avi</b>\n
Drop a video to start your file conversion today! Have ideas and suggestions for this mini project? Head over to the <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!""", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    return None