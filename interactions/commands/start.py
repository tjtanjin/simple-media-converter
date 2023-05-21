from services.message_service import reply


async def execute(update, context):
    """
    Welcomes the user and prompts user to input files.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await reply(update, "Hello there! Drop your media here to start conversion! (supports video, image and sticker conversions)")
