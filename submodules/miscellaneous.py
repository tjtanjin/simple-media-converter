from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

def build_menu(buttons, header_buttons=None, footer_buttons=None):
    """
    Function to build the menu buttons to show users.
    """
    menu = [buttons[i] for i in range(0, len(buttons))]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def show_options(n_rows, text, input_type):
    """
    Function that takes in button text and callback data to generate the view.
    Args:
        n_rows: rows for button
        text: list of texts to show
        input_type: format of video
    """
    button_list = []
    for i in range(0,n_rows):
        button_list.append([InlineKeyboardButton(text[i], callback_data="video_" + input_type + "_" + text[i])])
    reply_markup = InlineKeyboardMarkup(build_menu(button_list))
    return reply_markup

def check_exist_media(chat_id, input_type):
    """
    Function to check if media exist.
    Args:
        chat_id: id of user
        input_type: format of video
    """
    #checks if media exist by looking for file with user's username
    if not os.path.isfile("./input_media/{}.{}".format(str(chat_id), input_type)): 
        return False
    directory, filename = os.path.split("./input_media/{}.{}".format(str(chat_id), input_type))
    return filename in os.listdir(directory)