import asyncio
import ffmpy
import os
import pyheif

from rlottie_python import LottieAnimation
from PIL import Image, UnidentifiedImageError

from services.api_service import call_successful_conversion
from services.media_service import VIDEO_OUTPUT_TYPES

# used to handle support lottie conversion types from telegram stickers
LOTTIE_SUPPORTED_TYPES = ["png", "tiff", "pdf", "webp", "gif"]

# check if api service is enabled
API_SERVICE_ENABLED = os.getenv("API_SERVICE_ENABLED")


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
    if API_SERVICE_ENABLED:
        asyncio.run(call_successful_conversion())
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
            if API_SERVICE_ENABLED:
                asyncio.run(call_successful_conversion())
            return None

        if output_type in VIDEO_OUTPUT_TYPES:
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
    try:
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
    except UnidentifiedImageError:
        return None
    if output_type == "jpg" or ((input_type == "tiff" or input_type == "png") and output_type == "pdf"):
        img = img.convert('RGB')
    elif output_type == "ico":
        icon_size = [(32, 32)]
        img.save(f"./output_media/{chat_id}.{output_type}", sizes=icon_size)
        if API_SERVICE_ENABLED:
            asyncio.run(call_successful_conversion())
        return None
    img.save(f"./output_media/{chat_id}.{output_type}", quality=95, optimize=True)
    if API_SERVICE_ENABLED:
        asyncio.run(call_successful_conversion())
    return None

