import json
import os
import re

# used to handle supported input media types
IMAGE_INPUT_TYPES = json.loads(os.getenv("IMAGE_INPUT_TYPES"))
VIDEO_INPUT_TYPES = json.loads(os.getenv("VIDEO_INPUT_TYPES"))

# used to handle supported output media types
IMAGE_OUTPUT_TYPES = json.loads(os.getenv("IMAGE_OUTPUT_TYPES"))
VIDEO_OUTPUT_TYPES = json.loads(os.getenv("VIDEO_OUTPUT_TYPES"))
STICKER_TYPES = VIDEO_OUTPUT_TYPES + IMAGE_OUTPUT_TYPES  # sticker outputs to either image/video

# used to handle mime type checks on upload (fields auto-generated from supported image/video input types to mime types)
with open("./assets/file-extension-to-mime-types.json", "r") as file:
    mimetypes = json.load(file)
DOCUMENT_IMAGE_INPUT_TYPES = list(map(lambda input_type: mimetypes["image"][input_type], IMAGE_INPUT_TYPES))
DOCUMENT_VIDEO_INPUT_TYPES = list(map(lambda input_type: mimetypes["video"][input_type], VIDEO_INPUT_TYPES))


def input_media_exist(chat_id, input_type):
    """
    Checks if an input media uploaded by user exist.
    Args:
        chat_id: id of user
        input_type: format of media
    """
    if not os.path.isfile(f"./input_media/{chat_id}.{input_type}"):
        return False
    directory, filename = os.path.split(f"./input_media/{chat_id}.{input_type}")
    return filename in os.listdir(directory)


def output_media_exist(chat_id, output_type):
    """
    Checks if an output media saved from conversion exist.
    Args:
        chat_id: id of user
        output_type: format of media
    """
    if not os.path.isfile(f"./output_media/{chat_id}.{output_type}"):
        return False
    directory, filename = os.path.split(f"./input_media/{chat_id}.{output_type}")
    return filename in os.listdir(directory)


def clean_up_media(chat_id, input_type, output_type):
    """
    Cleans up both input/output media files if they exist.
    Args:
        chat_id: use user id to identify image
        input_type: video input type
        output_type: video output type
    """
    if input_media_exist(chat_id, input_type):
        os.remove(f"./input_media/{chat_id}.{input_type}")
    if output_media_exist(chat_id, output_type):
        os.remove(f"./output_media/{chat_id}.{output_type}")


def purge_user_media(media_dir, chat_id):
    """
    Purges all media from a user in given directory (used to handle cleanup during timeouts with untracked media types).
    Args:
        media_dir: directory where media is (input/output)
        chat_id: id of user to purge
    """
    for f in os.listdir(media_dir):
        if re.search(str(chat_id) + ".*", f):
            os.remove(os.path.join(media_dir, f))
