import i18n
import threading

from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from interactions.utils import TIMEOUT_DURATION, handle_interaction_timeout, handle_interaction_cancel, \
    handle_interaction_not_allowed
from services.conversion_service import convert_video
from services.media_service import VIDEO_OUTPUT_TYPES, input_media_exist, clean_up_media, DOCUMENT_VIDEO_INPUT_TYPES
from services.message_service import update_message, send_document, send_message, parse_placeholders
from ui.builder import show_conversion_options, show_animated_loader


def handle_video_input():
    """
    Handles video input from user.
    """
    return ConversationHandler(
        entry_points=[MessageHandler(filters.VIDEO, get_uploaded_video)],
        states={
            1: [CallbackQueryHandler(handle_video_output, pattern='video_(\S+)_(\S+)')],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, handle_interaction_timeout)]
        },
        fallbacks=[
            CallbackQueryHandler(handle_interaction_cancel, pattern='cancel'),
            MessageHandler(filters.ALL & (~filters.COMMAND), handle_interaction_not_allowed)
        ],
        conversation_timeout=TIMEOUT_DURATION
    )


async def get_uploaded_video(update, context):
    """
    Captures uploaded videos.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    file_id = update.message.video.file_id
    chat_id = update.message.chat_id
    input_type = update.message.video.mime_type[6:]
    if input_type not in DOCUMENT_VIDEO_INPUT_TYPES:
        await send_message(context, chat_id, i18n.t("interaction.file_not_supported"))
        return ConversationHandler.END

    await process_upload_as_video(context, chat_id, file_id, input_type)
    return 1


async def process_upload_as_video(context, chat_id, file_id, input_type):
    """
    Processes the uploaded file as a video and prompts the user for conversion type.
    Args:
        context: default telegram arg
        chat_id: id of user who uploaded the media
        file_id: id identifying uploaded file
        input_type: type of file sent
    """
    receiving_msg = await send_message(context, chat_id, i18n.t("video.detected"))
    new_file = await context.bot.get_file(file_id)
    with open(f"./input_media/{chat_id}.{input_type}", "wb") as file:
        await new_file.download_to_memory(file)
    reply_markup = show_conversion_options(VIDEO_OUTPUT_TYPES, "video", input_type)
    await update_message(receiving_msg, i18n.t("interaction.prompt_selection"), markup=reply_markup)


async def handle_video_output(update, context):
    """
    Performs conversion upon user's selection of desired output video type and returns the final result.
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
        conversion_process = threading.Thread(target=convert_video, args=(chat_id, input_type, output_type))
        conversion_process.start()
        while conversion_process.isAlive():
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


