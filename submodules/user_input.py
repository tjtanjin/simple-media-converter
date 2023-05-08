from telegram.constants import ParseMode
from submodules import media_processor as mp
from submodules import miscellaneous as mc
import os, re, json

# used to handle supported videos/images types
video_types = json.loads(os.getenv("VIDEO_TYPES"))
image_types = json.loads(os.getenv("IMAGE_TYPES"))

# used to handle videos/images sent as documents
video_types_format_name = ["gif", "x-msvideo", "webm", "mp4", "x-flv", "mov", "x-matroska"]
image_types_format_name = ["png", "jpg", "jpeg", "tiff", "webp", "vnd.microsoft.icon", "heif"]

sticker_types = video_types + image_types

async def start(update, context):
    """
    The function welcomes the user and prompts user to input files.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await update.message.reply_text("Hello there! Drop your media here to start conversion! (supports video, image and sticker conversions)")

async def get_document(update, context):
    """
    This function captures non-mp4 format documents.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    input_type = update.message.document.mime_type[6:]
    if input_type in video_types_format_name:
        await get_video(update, context)
    elif input_type in image_types_format_name:
        await get_photo(update, context)
    else:
        await update.message.reply_text("Unsupported file uploaded. Do /help to see supported file formats.")
    return None

async def get_photo(update, context):
    """
    The function get_photo takes image input from the user and processes it
    to return it as the type specified by the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    # accounts for different file format of user input
    chat_id = update.message.chat_id
    try:
        file_id = update.message.document.file_id
        input_type = update.message.document.mime_type[6:]
    except:
        try:
            file_id = update.message.photo[-1].file_id
            context.bot.send_message(chat_id=chat_id, text="You sent your image as a photo. If you run into conversion issues, send your image as a file instead.")
        except:
            file_id = update.message.sticker.file_id
        input_type = "jpg"

    receiving_msg = await context.bot.send_message(chat_id=chat_id, text="Image file detected. Preparing file...")
    newFile = await context.bot.get_file(file_id)
    with open('./input_media/{}.{}'.format(chat_id, input_type), "wb") as file:
        await newFile.download_to_memory(file)
    reply_markup = mc.show_options(len(image_types), image_types, "photo", input_type)
    await receiving_msg.edit_text(text="Please select the file type to convert to:", reply_markup=reply_markup)
    return None

async def get_sticker(update, context):
    """
    This function captures telegram stickers.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    file_id = update.message.sticker.file_id
    input_type = "tgs"
    chat_id = update.message.chat_id
    receiving_msg = await context.bot.send_message(chat_id=chat_id, text="Sticker detected. Preparing file...")
    newFile = await context.bot.get_file(file_id)
    with open('./input_media/{}.{}'.format(chat_id, input_type), "wb") as file:
        await newFile.download_to_memory(file)
    if update.message.sticker.is_animated:
        reply_markup = mc.show_options(len(sticker_types), sticker_types, "sticker", input_type)
    else:
        reply_markup = mc.show_options(len(image_types), image_types, "sticker", input_type)
    await receiving_msg.edit_text(text="Please select the file type to convert to:", reply_markup=reply_markup)
    return None

async def get_video(update, context):
    """
    The function get_video takes video input from the user and processes it
    to return it as the type specified by the user.
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
    receiving_msg = await context.bot.send_message(chat_id=chat_id, text="Video file detected. Preparing file...")
    newFile = await context.bot.get_file(file_id)
    with open('./input_media/{}.{}'.format(chat_id, input_type), "wb") as file:
        await newFile.download_to_memory(file)
    reply_markup = mc.show_options(len(video_types), video_types, "video", input_type)
    await receiving_msg.edit_text(text="Please select the file type to convert to:", reply_markup=reply_markup)
    return None

async def output_video_type(update, context):
    """
    This function triggers upon user's selection of desired output video type.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await context.bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    chat_id = update.callback_query.message.chat.id

    # update user on progress of conversion and send converted media on success
    try:
        match_file = re.match(r'video_(\S+)_(\S+)', data)
        input_type, output_type = match_file.group(1), match_file.group(2)
        if mc.check_exist_media(chat_id, input_type):
            processing_msg = await context.bot.send_message(chat_id=chat_id, text="Converting {} file to {}...".format(input_type, output_type))
            mp.convert_video(chat_id, input_type, output_type)
            await processing_msg.edit_text(text="Converted to {} format. Retrieving file...".format(output_type))
            await context.bot.send_document(chat_id=chat_id, document=open('./output_media/{}.{}'.format(chat_id, output_type), 'rb'), caption="Here is your file!")
        else:
            await context.bot.send_message(chat_id=chat_id, text="File not found, please upload again.")
            return None
    # throw error on failure
    except Exception as ex:
        await processing_msg.edit_text('An error has occurred. Please open an issue at our <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        print(ex)
    # remove all media files at the end
    finally:
        os.remove("./input_media/{}.{}".format(chat_id, input_type))
        os.remove("./output_media/{}.{}".format(chat_id, output_type))
    return None

async def output_sticker_type(update, context):
    """
    This function triggers upon user's selection of desired output sticker type.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await context.bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    chat_id = update.callback_query.message.chat.id

    # update user on progress of conversion and send converted media on success
    try:
        match_file = re.match(r'sticker_(\S+)_(\S+)', data)
        input_type, output_type = match_file.group(1), match_file.group(2)
        if mc.check_exist_media(chat_id, input_type):
            processing_msg = await context.bot.send_message(chat_id=chat_id, text="Converting {} file to {}...".format(input_type, output_type))
            mp.convert_sticker(chat_id, input_type, output_type)
            await processing_msg.edit_text(text="Converted to {} format. Retrieving file...".format(output_type))
            await context.bot.send_document(chat_id=chat_id, document=open('./output_media/{}.{}'.format(chat_id, output_type), 'rb'), caption="Here is your file!")
        else:
            await context.bot.send_message(chat_id=chat_id, text="File not found, please upload again.")
            return None
    # throw error on failure
    except Exception as ex:
        await processing_msg.edit_text('An error has occurred. Please open an issue at our <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        print(ex)
    # remove all media files at the end
    finally:
        os.remove("./input_media/{}.{}".format(chat_id, input_type))
        os.remove("./output_media/{}.{}".format(chat_id, output_type))
    return None

async def output_photo_type(update, context):
    """
    This function triggers upon user's selection of desired output photo type.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await context.bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    chat_id = update.callback_query.message.chat.id

    # update user on progress of conversion and send converted media on success
    try:
        match_file = re.match(r'photo_(\S+)_(\S+)', data)
        input_type, output_type = match_file.group(1), match_file.group(2)
        if mc.check_exist_media(chat_id, input_type):
            processing_msg = await context.bot.send_message(chat_id=chat_id, text="Converting {} file to {}...".format(input_type, output_type))
            mp.convert_image(chat_id, input_type, output_type)
            await processing_msg.edit_text(text="Converted to {} format. Retrieving file...".format(output_type))
            await context.bot.send_document(chat_id=chat_id, document=open('./output_media/{}.{}'.format(chat_id, output_type), 'rb'), caption="Here is your file!")
        else:
            await context.bot.send_message(chat_id=chat_id, text="File not found, please upload again.")
            return None
    # throw error on failure
    except Exception as ex:
        await processing_msg.edit_text('An error has occurred. Please open an issue at our <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        print(ex)
    # remove all media files at the end
    finally:
        os.remove("./input_media/{}.{}".format(chat_id, input_type))
        os.remove("./output_media/{}.{}".format(chat_id, output_type))
    return None

async def show_help(update, context):
    """
    Function to show current conversion type information to users.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await update.message.reply_text("""Here are the currently available conversion types:\n
    <b>Videos:</b><pre>
        Input:   |   Output:
        .mp4     |   .mp4
        .webm    |   .webm
        .gif     |   .gif
        .avi     |   .avi
        .flv     |   .flv
        .mov     |   .mov
        .mkv     |   .mkv\n
    </pre>
    <b>Images:</b><pre>
        Input:   |   Output:
        .png     |   .png
        .jpg     |   .jpg
        .tiff    |   .tiff
        .webp    |   .webp
        .ico     |   .ico
        .heif    |   .pdf\n
    </pre>
    <b>Stickers:</b><pre>
        Input:   |   Output:
        Static   |   All
        Telegram |   Supported
        Sticker  |   Images
                 |
        Animated |   All
        Telegram |   Supported
        Sticker  |   Images/Videos
    </pre>
Drop a video or image to start your file conversion today! Have ideas and suggestions for this mini project? Head over to the <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!""", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    return None
