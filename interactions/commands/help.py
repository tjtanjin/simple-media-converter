from telegram.constants import ParseMode

from services.message_service import reply


async def execute(update, context):
    """
    Lists all current conversion type information to user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    await reply(update, """Here are the currently available conversion types:\n
    <b>Videos:</b><pre>
        Input:   |   Output:
        .mp4     |   .mp4
        .webm    |   .webm
        .gif     |   .gif
        .avi     |   .avi
        .flv     |   .flv
        .mov     |   .mov
        .mkv     |   .mkv\n
    </pre>
    <b>Images:</b><pre>
        Input:   |   Output:
        .png     |   .png
        .jpg     |   .jpg
        .tiff    |   .tiff
        .webp    |   .webp
        .ico     |   .ico
        .heif    |   .pdf\n
    </pre>
    <b>Stickers:</b><pre>
        Input:   |   Output:
        Static   |   All
        Telegram |   Supported
        Sticker  |   Images
                 |
        Animated |   All
        Telegram |   Supported
        Sticker  |   Images/Videos
    </pre>
Drop a video or image to start your file conversion today! Have ideas and suggestions for this mini project? Head over to the <a href="https://github.com/tjtanjin/simple-media-converter">Project Repository</a>!""", parse_mode=ParseMode.HTML)
