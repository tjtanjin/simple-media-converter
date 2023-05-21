import ffmpy
import json
import os
import pyheif
import re
from rlottie_python import LottieAnimation
from PIL import Image

# used to handle support lottie conversion types from telegram stickers
LOTTIE_SUPPORTED_TYPES = ["png", "tiff", "pdf", "webp", "gif"]

# used to handle supported conversion (output) types
VIDEO_TYPES = json.loads(os.getenv("VIDEO_TYPES"))
IMAGE_TYPES = json.loads(os.getenv("IMAGE_TYPES"))
STICKER_TYPES = VIDEO_TYPES + IMAGE_TYPES


def convert_video(chat_id, input_type, output_type):
    """
    Converts video of one type to another.
    Args:
        chat_id: use user id to identify video
        input_type: video input type
        output_type: video output type
    """
    inputs = {f"./input_media/{chat_id}.{input_type}": None}
    if output_type == "gif":
        outputs = {f"./output_media/{chat_id}.{output_type}": '-t 3 -vf "fps=30,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0'}
    else:
        outputs = {f"./output_media/{chat_id}.{output_type}": None}
    ff = ffmpy.FFmpeg(
        inputs=inputs,
        outputs=outputs
    )
    ff.run()
    return None


def convert_sticker(chat_id, input_type, output_type):
    """
    Converts sticker to an image/video.
    Args:
        chat_id: use user id to identify sticker
        input_type: sticker type (.tgs)
        output_type: image/video output type
    """
    try:
        if output_type in LOTTIE_SUPPORTED_TYPES:
            anim = LottieAnimation.from_tgs(f"./input_media/{chat_id}.{input_type}")
            anim.save_animation(f"./output_media/{chat_id}.{output_type}")
            return None

        if output_type in VIDEO_TYPES:
            anim = LottieAnimation.from_tgs(f"./input_media/{chat_id}.{input_type}")
            anim.save_animation(f"./input_media/{chat_id}.gif")
            convert_video(chat_id, "gif", output_type)
            os.remove(f"./input_media/{chat_id}.gif")
        else:
            anim = LottieAnimation.from_tgs(f"./input_media/{chat_id}.{input_type}")
            anim.save_animation(f"./input_media/{chat_id}.png")
            convert_image(chat_id, "png", output_type)
            os.remove(f"./input_media/{chat_id}.png")
    except (Exception,):
        # if all else fails, convert sticker straight to image type
        convert_image(chat_id, "tgs", output_type)
    return None


def convert_image(chat_id, input_type, output_type):
    """
    Converts image of one type to another.
    Args:
        chat_id: use user id to identify image
        input_type: video input type
        output_type: video output type
    """
    if input_type == "heif":
        heif_file = pyheif.read(f"./input_media/{chat_id}.{input_type}")
        img = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride)
    else:
        img = Image.open(f"./input_media/{chat_id}.{input_type}")
    if output_type == "jpg" or ((input_type == "tiff" or input_type == "png") and output_type == "pdf"):
        img = img.convert('RGB')
    elif output_type == "ico":
        icon_size = [(32, 32)]
        img.save(f"./output_media/{chat_id}.{output_type}", sizes=icon_size)
        return None
    img.save(f"./output_media/{chat_id}.{output_type}", quality=95, optimize=True)
    return None


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

