from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from interactions.utils import TIMEOUT_DURATION, handle_interaction_timeout, handle_interaction_cancel
from services.conversion_service import IMAGE_TYPES, STICKER_TYPES, convert_sticker, input_media_exist, clean_up_media
from services.message_service import update_message, send_document, send_message
from ui.builder import show_conversion_options


def handle_sticker_input():
    """
    Handles sticker input from user.
    """
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Sticker.ALL, get_uploaded_sticker)],
        states={
            1: [CallbackQueryHandler(handle_sticker_output, pattern='sticker_(\S+)_(\S+)')],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, handle_interaction_timeout)]
        },
        fallbacks=[CallbackQueryHandler(handle_interaction_cancel, pattern='cancel')],
        conversation_timeout=TIMEOUT_DURATION
    )


async def get_uploaded_sticker(update, context):
    """
    Captures sent telegram stickers.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    file_id = update.message.sticker.file_id
    input_type = "tgs"
    chat_id = update.message.chat_id
    receiving_msg = await send_message(context, chat_id, "Sticker detected. Preparing file...")
    new_file = await context.bot.get_file(file_id)
    with open(f"./input_media/{chat_id}.{input_type}", "wb") as file:
        await new_file.download_to_memory(file)
    if update.message.sticker.is_animated:
        reply_markup = show_conversion_options(len(STICKER_TYPES), STICKER_TYPES, "sticker", input_type)
    else:
        reply_markup = show_conversion_options(len(IMAGE_TYPES), IMAGE_TYPES, "sticker", input_type)
    await update_message(receiving_msg, "Please select the file type to convert to:", markup=reply_markup)
    return 1


async def handle_sticker_output(update, context):
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
        match_file = data.split("_")
        input_type, output_type = match_file[1], match_file[2]
        if input_media_exist(chat_id, input_type):
            processing_msg = await send_message(context, chat_id, f"Converting {input_type} file to {output_type}...")
            convert_sticker(chat_id, input_type, output_type)
            await update_message(processing_msg, f"Converted to {output_type} format. Retrieving file...")
            await send_document(context, chat_id, f"./output_media/{chat_id}.{output_type}", "Here is your file!")
        else:
            await send_message(context, chat_id, "File not found, please upload again.")
            return ConversationHandler.END
    # throw error on failure
    except Exception as ex:
        await update_message(processing_msg, 'An error has occurred. Please open an issue at our <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        print(ex)
    # remove all media files at the end
    finally:
        clean_up_media(chat_id, input_type, output_type)
    return ConversationHandler.END