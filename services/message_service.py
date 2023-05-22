from telegram.constants import ParseMode


async def reply(update, text, markup=None, parse_mode=ParseMode.HTML):
    """
    Replies a user with the given message.
    Args:
        update: default telegram arg
        text: text message to reply to user with
        markup: markup for showing buttons, defaults to none
        parse_mode: mode to parse the string, defaults to HTML
    """
    return await update.message.reply_text(text, reply_markup=markup, disable_web_page_preview=True,
                                           parse_mode=parse_mode)


async def send_message(context, user_id, text, markup=None, parse_mode=ParseMode.HTML):
    """
    Sends a message to the user with the given id.
    Args:
        context: default telegram arg
        user_id: id of user to send message to
        text: text message to send user
        markup: markup for showing buttons, defaults to none
        parse_mode: mode to parse the string, defaults to HTML
    """
    return await context.bot.send_message(user_id, text, reply_markup=markup, disable_web_page_preview=True,
                                          parse_mode=parse_mode)


async def update_message(message, text, markup=None, parse_mode=ParseMode.HTML):
    """
    Updates an existing message with the user.
    Args:
        message: message to edit
        text: text to edit the message with
        markup: markup for showing buttons, defaults to none
        parse_mode: mode to parse the string, defaults to HTML
    """
    return await message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True, parse_mode=parse_mode)


async def send_document(context, user_id, document_path, caption):
    """
   Sends a document to the user with the given id.
   Args:
       context: default telegram arg
       user_id: id of user to send document to
       document_path: path to the document being sent
       caption: text message to accompany the document
   """
    return await context.bot.send_document(chat_id=user_id, document=open(document_path, 'rb'), caption=caption)


def parse_placeholders(string, keys, values):
    """
    Parses placeholders within a string.
    Args:
        keys: placeholder keys being used
        values: values to replaced the keys with
    """
    for i in range(0, len(keys)):
        string = string.replace(keys[i], values[i])
    return string
