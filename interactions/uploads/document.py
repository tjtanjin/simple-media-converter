import i18n

from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from interactions.uploads.image import handle_image_output, process_upload_as_image
from interactions.uploads.video import handle_video_output, process_upload_as_video
from interactions.utils import TIMEOUT_DURATION, handle_interaction_timeout, \
    handle_interaction_cancel, handle_interaction_not_allowed
from services.media_service import DOCUMENT_IMAGE_INPUT_TYPES, DOCUMENT_VIDEO_INPUT_TYPES
from services.message_service import reply


def handle_document_input():
    """
    Handles document input from user.
    """
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Document.ALL, get_uploaded_document)],
        states={
            1: [CallbackQueryHandler(handle_video_output, pattern='video_(\S+)_(\S+)')], # noqa
            2: [CallbackQueryHandler(handle_image_output, pattern='image_(\S+)_(\S+)')], # noqa
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, handle_interaction_timeout)]
        },
        fallbacks=[
            CallbackQueryHandler(handle_interaction_cancel, pattern='cancel'),
            MessageHandler(filters.ALL & (~filters.COMMAND), handle_interaction_not_allowed)
        ],
        conversation_timeout=TIMEOUT_DURATION
    )


async def get_uploaded_document(update, context):
    """
    Captures uploaded documents that are media files and processes based on detected media type.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    chat_id = update.message.chat_id
    file_id = update.message.document.file_id
    input_type = update.message.document.mime_type[6:]
    if input_type in DOCUMENT_VIDEO_INPUT_TYPES:
        await process_upload_as_video(context, chat_id, file_id, input_type)
        return 1
    elif input_type in DOCUMENT_IMAGE_INPUT_TYPES:
        await process_upload_as_image(context, chat_id, file_id, input_type)
        return 2
    else:
        await reply(update, i18n.t("interaction.file_not_supported"))
        return ConversationHandler.END
