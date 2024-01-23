import i18n
import threading

from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from interactions.utils import TIMEOUT_DURATION, handle_interaction_timeout, handle_interaction_cancel, \
    handle_interaction_not_allowed
from services.conversion_service import convert_image
from services.media_service import IMAGE_OUTPUT_TYPES, input_media_exist, clean_up_media, IMAGE_INPUT_TYPES
from services.message_service import send_message, update_message, send_document, parse_placeholders
from ui.builder import show_conversion_options, show_animated_loader


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
        fallbacks=[
            CallbackQueryHandler(handle_interaction_cancel, pattern='cancel'),
            MessageHandler(filters.ALL & (~filters.COMMAND), handle_interaction_not_allowed)
        ],
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

    # images sent to telegram are by default received as jpg so a specific check is done here
    if "jpg" not in IMAGE_INPUT_TYPES:
        await send_message(context, chat_id, i18n.t("interaction.file_not_supported"))
        return ConversationHandler.END

    # if sent as photo, no way to detect file name to parse type - hence defaults to jpg and users are encouraged to
    # send images as a file if conversion result is less than desirable
    await send_message(context, chat_id, i18n.t("image.advise"))

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
    receiving_msg = await send_message(context, chat_id, i18n.t("image.detected"))
    try:
        new_file = await context.bot.get_file(file_id)
    except BadRequest:
        await update_message(receiving_msg, i18n.t("interaction.file_too_large"))
        return ConversationHandler.END

    with open(f"./input_media/{chat_id}.{input_type}", "wb") as file:
        await new_file.download_to_memory(file)
    reply_markup = show_conversion_options(IMAGE_OUTPUT_TYPES, "image", input_type)
    await update_message(receiving_msg, i18n.t("interaction.prompt_selection"), markup=reply_markup)


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
            await send_message(context, chat_id, i18n.t("interaction.file_not_found"))
            return ConversationHandler.END

        selection_msg = update.callback_query.message
        processing_msg = await update_message(selection_msg, parse_placeholders(i18n.t("conversion.in_progress"),
                                                                                    ["%input_type%", "%output_type%"],
                                                                                    [input_type, output_type]))
        conversion_process = threading.Thread(target=convert_image, args=(chat_id, input_type, output_type))
        conversion_process.start()
        while conversion_process.is_alive():
            await show_animated_loader(processing_msg)
        await update_message(processing_msg, parse_placeholders(i18n.t("conversion.complete"),
                                                                ["%input_type%", "%output_type%"],
                                                                [input_type, output_type]))
        await send_document(context, chat_id, f"./output_media/{chat_id}.{output_type}", i18n.t("conversion.send_file"))
    # throw error on failure
    except (Exception,):
        await update_message(selection_msg, i18n.t("misc.error"), parse_mode=ParseMode.HTML)
    # remove all media files at the end
    finally:
        clean_up_media(chat_id, input_type, output_type)
    return ConversationHandler.END
