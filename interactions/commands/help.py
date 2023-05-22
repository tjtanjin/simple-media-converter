import i18n

from telegram.constants import ParseMode

from services.media_service import IMAGE_INPUT_TYPES, IMAGE_OUTPUT_TYPES, VIDEO_INPUT_TYPES, VIDEO_OUTPUT_TYPES
from services.message_service import reply


async def execute(update, context):
    """
    Lists all current conversion type information to user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await reply(update, help_message, parse_mode=ParseMode.HTML)


def build_help_message():
    """
    Builds the help message based on allowed input/output types.
    """
    message = i18n.t("help.header") + ":\n\n"

    # checks if image conversion is supported
    if image_conversion_supported():
        message += "<b>" + i18n.t("misc.images") + ":</b><pre>\n"
        message += build_types_body([i18n.t("misc.input") + ":"], [i18n.t("misc.output") + ":"]) + "\n"
        message += build_types_body(
            list(map(lambda x: "." + x, IMAGE_INPUT_TYPES)),
            list(map(lambda x: "." + x, IMAGE_OUTPUT_TYPES))
        )
        message += "</pre>\n"

    # checks if video conversion is supported
    if video_conversion_supported():
        message += "<b>" + i18n.t("misc.videos") + ":</b><pre>\n"
        message += build_types_body([i18n.t("misc.input") + ":"], [i18n.t("misc.output") + ":"]) + "\n"
        message += build_types_body(
            list(map(lambda x: "." + x, VIDEO_INPUT_TYPES)),
            list(map(lambda x: "." + x, VIDEO_OUTPUT_TYPES))
        )
        message += "</pre>\n"

    # checks if sticker conversion is supported
    if image_conversion_supported() or video_conversion_supported():
        message += "<b>" + i18n.t("misc.stickers") + ":</b><pre>\n"
        message += build_types_body([i18n.t("misc.input") + ":"], [i18n.t("misc.output") + ":"]) + "\n"
        message += build_types_body(
            [i18n.t("misc.static"), i18n.t("misc.telegram"), i18n.t("misc.stickers")],
            [i18n.t("misc.all"), i18n.t("misc.supported"), i18n.t("misc.images")]
        )
        message += "            |            \n"
        message += build_types_body(
            [i18n.t("misc.animated"), i18n.t("misc.telegram"), i18n.t("misc.stickers")],
            [i18n.t("misc.all"), i18n.t("misc.supported"), i18n.t("misc.images") + "/" + i18n.t("misc.videos")]
        )
        message += "</pre>\n"

    message += i18n.t("help.footer")
    return message


def build_types_body(input_array, output_array):
    """
    Builds the body of the message that lists the allowed input/output types.
    Args:
        input_array: list of allowed inputs
        output_array: list of allowed outputs
    """
    parsed_input = list(map(pad_input, input_array))
    parsed_output = list(map(pad_output, output_array))
    input_num = len(parsed_input)
    output_num = len(parsed_output)
    if input_num > output_num:
        while input_num > len(parsed_output):
            parsed_output.append("")
    else:
        while output_num > len(parsed_input):
            parsed_input.append("         ")
    body = ""
    for i in range(0, len(parsed_input)):
        body += parsed_input[i] + "|" + parsed_output[i] + "\n"

    return body


def pad_input(string):
    """
    Pads the allowed input type for formatting.
    Args:
        string: string to pad
    """
    string = "   " + string
    current_length = 0
    for char in string:
        if char.isascii():
            current_length += 1
        else:
            current_length += 2
    return string + ((12 - current_length) * " ")


def pad_output(string):
    """
    Pads the allowed output type for formatting.
    Args:
        string: string to pad
    """
    return "   " + string


def image_conversion_supported():
    """
    Checks if image conversion is supported.
    """
    return len(IMAGE_INPUT_TYPES) > 0 and len(IMAGE_OUTPUT_TYPES) > 0


def video_conversion_supported():
    """
    Checks if video conversion is supported.
    """
    return len(VIDEO_INPUT_TYPES) > 0 and len(VIDEO_OUTPUT_TYPES) > 0


help_message = build_help_message()
