from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_menu(buttons, header_buttons=None, footer_buttons=None):
    """
    Serves as a helper for building the menu buttons to show users.
    """
    menu = [buttons[i] for i in range(0, len(buttons))]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def show_conversion_options(text, media_type, input_type):
    """
    Generates conversion option buttons for users from a list of button texts and callback data.
    Args:
        text: list of texts to show
        media_type: currently supports videos and images
        input_type: format of video
    """
    button_list = []
    for i in range(0, len(text)):
        button_list.append([InlineKeyboardButton(text[i], callback_data=media_type + "_" + input_type + "_" + text[i])])

    # append a final cancel button for users to cancel conversion
    button_list.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
    reply_markup = InlineKeyboardMarkup(build_menu(button_list))
    return reply_markup
