import os

from telegram.ext import ConversationHandler

from services.conversion_service import purge_user_media
from services.message_service import send_message

try:
    TIMEOUT_DURATION = int(os.getenv("INTERACTION_TIMEOUT_DURATION"))
except ValueError:
    TIMEOUT_DURATION = 300


async def handle_interaction_cancel(update, context):
    """
    Handles logic for when user uploads a media but decides to cancel the conversion.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await context.bot.answer_callback_query(update.callback_query.id)
    chat_id = update.callback_query.message.chat.id
    purge_user_media("./input_media/", chat_id)
    await send_message(context, chat_id, "Ok! Your attempt to convert has been cancelled!")
    return ConversationHandler.END


async def handle_interaction_timeout(update, context):
    """
    Handles logic for when a user interaction timeouts.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    chat_id = update.message.chat_id
    purge_user_media("./input_media/", chat_id)
    purge_user_media("./output_media/", chat_id)
    await send_message(context, chat_id, "It seems you are no longer interested :( Hope to see you again!")
    return ConversationHandler.END
