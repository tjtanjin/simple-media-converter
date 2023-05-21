from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from interactions.utils import TIMEOUT_DURATION, handle_interaction_timeout, handle_interaction_cancel
from services.conversion_service import IMAGE_TYPES, convert_image, input_media_exist, clean_up_media
from services.message_service import send_message, update_message, send_document
from ui.builder import show_conversion_options


def handle_image_input():
    """
    Handles image input from user.
    """
    return ConversationHandler(
        entry_points=[MessageHandler(filters.PHOTO, get_uploaded_image)],
        states={
            1: [CallbackQueryHandler(handle_image_output, pattern='image_(\S+)_(\S+)')],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, handle_interaction_timeout)]
        },
        fallbacks=[CallbackQueryHandler(handle_interaction_cancel, pattern='cancel')],
        conversation_timeout=TIMEOUT_DURATION
    )


async def get_uploaded_image(update, context):
    """
    Captures uploaded images.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    chat_id = update.message.chat_id
    file_id = update.message.photo[-1].file_id
    await send_message(context, chat_id, "You sent your image as a photo. If you run into conversion issues, "
                                         "try sending your image as a file instead.")

    # if sent as photo, no way to detect file name to parse type - hence defaults to jpg and users are encouraged to
    # send images as a file if conversion result is less than desirable
    await process_upload_as_image(context, chat_id, file_id, "jpg")
    return 1


async def process_upload_as_image(context, chat_id, file_id, input_type):
    """
    Processes the uploaded file as an image and prompts the user for conversion type.
    Args:
        context: default telegram arg
        chat_id: id of user who uploaded the media
        file_id: id identifying uploaded file
        input_type: type of file sent
    """
    receiving_msg = await send_message(context, chat_id, "Image file detected. Preparing file...")
    new_file = await context.bot.get_file(file_id)
    with open(f"./input_media/{chat_id}.{input_type}", "wb") as file:
        await new_file.download_to_memory(file)
    reply_markup = show_conversion_options(IMAGE_TYPES, "image", input_type)
    await update_message(receiving_msg, "Please select the file type to convert to:", markup=reply_markup)


async def handle_image_output(update, context):
    """
    Performs conversion upon user's selection of desired output image type and returns the final result.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await context.bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    chat_id = update.callback_query.message.chat.id

    # update user on progress of conversion and send converted media on success
    try:
        match_file = data.split("_")
        input_type, output_type = match_file[1], match_file[2]
        if not input_media_exist(chat_id, input_type):
            await send_message(context, chat_id, "File not found, please upload again.")
            return ConversationHandler.END

        processing_msg = await send_message(context, chat_id, f"Converting {input_type} file to {output_type}...")
        convert_image(chat_id, input_type, output_type)
        await update_message(processing_msg, f"Converted to {output_type} format. Retrieving file...")
        await send_document(context, chat_id, f"./output_media/{chat_id}.{output_type}", "Here is your file!")
    # throw error on failure
    except Exception as ex:
        await update_message(processing_msg,
                             'An error has occurred. Please open an issue at our <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!',
                             parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        print(ex)
    # remove all media files at the end
    finally:
        clean_up_media(chat_id, input_type, output_type)
    return ConversationHandler.END
