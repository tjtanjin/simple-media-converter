from telegram.ext import CommandHandler

from interactions.commands.start import execute as start_e
from interactions.commands.help import execute as help_e
from interactions.uploads.document import handle_document_input
from interactions.uploads.image import handle_image_input
from interactions.uploads.sticker import handle_sticker_input
from interactions.uploads.video import handle_video_input


def load_interactions(application):
    """
    Loads all interactions on start.
    Args:
        application: application for adding handlers to
    """
    load_commands(application)
    load_uploads(application)


def load_commands(application):
    """
    Loads all command handlers on start.
    Args:
        application: application for adding handlers to
    """
    application.add_handler(CommandHandler('start', start_e))
    application.add_handler(CommandHandler('help', help_e))


def load_uploads(application):
    """
    Loads all handlers for media uploads on start.
    Args:
        application: application for adding handlers to
    """
    # handlers for media uploads
    application.add_handler(handle_document_input())
    application.add_handler(handle_image_input())
    application.add_handler(handle_video_input())
    application.add_handler(handle_sticker_input())
