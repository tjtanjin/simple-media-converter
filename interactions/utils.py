import i18n
import os

from telegram.ext import ConversationHandler

from services.media_service import purge_user_media
from services.message_service import send_message, update_message

try:
    TIMEOUT_DURATION = int(os.getenv("INTERACTION_TIMEOUT_DURATION"))
except ValueError:
    TIMEOUT_DURATION = 180


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
    await update_message(update.callback_query.message, i18n.t("interaction.cancelled"))
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
    await send_message(context, chat_id, i18n.t("interaction.timeout"))
    return ConversationHandler.END


async def handle_interaction_not_allowed(update, context):
    """
    Handles logic for when a user performs an action not allowed during an interaction
    (e.g. uploading another file while there is an existing prompt).
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    chat_id = update.message.chat_id
    await context.bot.delete_message(chat_id, update.message.message_id)
    await send_message(context, chat_id, i18n.t("interaction.not_allowed"))
