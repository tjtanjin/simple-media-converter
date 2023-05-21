from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from interactions.uploads.image import handle_image_output, process_upload_as_image
from interactions.uploads.video import handle_video_output, process_upload_as_video
from interactions.utils import TIMEOUT_DURATION, handle_interaction_timeout, handle_interaction_cancel
from services.message_service import reply

# supported media types sent as documents
video_types_format_name = ["gif", "x-msvideo", "webm", "mp4", "x-flv", "mov", "x-matroska"]
image_types_format_name = ["png", "jpg", "jpeg", "tiff", "webp", "vnd.microsoft.icon", "heif"]


def handle_document_input():
    """
    Handles document input from user.
    """
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Document.ALL, get_uploaded_document)],
        states={
            1: [CallbackQueryHandler(handle_video_output, pattern='video_(\S+)_(\S+)')],
            2: [CallbackQueryHandler(handle_image_output, pattern='image_(\S+)_(\S+)')],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, handle_interaction_timeout)]
        },
        fallbacks=[CallbackQueryHandler(handle_interaction_cancel, pattern='cancel')],
        conversation_timeout=TIMEOUT_DURATION
    )


async def get_uploaded_document(update, context):
    """
    Captures uploaded documents that are media files and processes them based on detected media type.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    chat_id = update.message.chat_id
    file_id = update.message.document.file_id
    input_type = update.message.document.mime_type[6:]
    if input_type in video_types_format_name:
        await process_upload_as_video(context, chat_id, file_id, input_type)
        return 1
    elif input_type in image_types_format_name:
        await process_upload_as_image(context, chat_id, file_id, input_type)
        return 2
    else:
        await reply(update, "Unsupported file uploaded. Do /help to see supported file formats.")
        return ConversationHandler.END
