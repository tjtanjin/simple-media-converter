import i18n

from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from interactions.utils import TIMEOUT_DURATION, handle_interaction_timeout, handle_interaction_cancel, \
    handle_interaction_not_allowed
from services.conversion_service import convert_sticker
from services.media_service import IMAGE_OUTPUT_TYPES, STICKER_TYPES, input_media_exist, clean_up_media
from services.message_service import update_message, send_document, send_message, parse_placeholders
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
        fallbacks=[
            CallbackQueryHandler(handle_interaction_cancel, pattern='cancel'),
            MessageHandler(filters.ALL & (~filters.COMMAND), handle_interaction_not_allowed)
        ],
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
    receiving_msg = await send_message(context, chat_id, i18n.t("sticker.detected"))
    new_file = await context.bot.get_file(file_id)
    with open(f"./input_media/{chat_id}.{input_type}", "wb") as file:
        await new_file.download_to_memory(file)
    if update.message.sticker.is_animated:
        reply_markup = show_conversion_options(STICKER_TYPES, "sticker", input_type)
    else:
        reply_markup = show_conversion_options(IMAGE_OUTPUT_TYPES, "sticker", input_type)
    await update_message(receiving_msg, i18n.t("interaction.prompt_selection"), markup=reply_markup)
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
        if not input_media_exist(chat_id, input_type):
            await send_message(context, chat_id, i18n.t("interaction.file_not_found"))
            return ConversationHandler.END

        processing_msg = await send_message(context, chat_id, parse_placeholders(i18n.t("conversion.in_progress"),
                                                                                 ["%input_type%", "%output_type%"],
                                                                                 [input_type, output_type]))
        convert_sticker(chat_id, input_type, output_type)
        await update_message(processing_msg, parse_placeholders(i18n.t("conversion.complete"),
                                                                ["%input_type%", "%output_type%"],
                                                                [input_type, output_type]))
        await send_document(context, chat_id, f"./output_media/{chat_id}.{output_type}", i18n.t("conversion.send_file"))
    # throw error on failure
    except Exception as ex:
        await update_message(processing_msg, i18n.t("misc.error"), parse_mode=ParseMode.HTML)
        print(ex)
    # remove all media files at the end
    finally:
        clean_up_media(chat_id, input_type, output_type)
    return ConversationHandler.END