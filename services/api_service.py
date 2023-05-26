import aiohttp
import json
import os

API_ENDPOINT = os.getenv("API_ENDPOINT")
API_HEADERS = json.load(os.getenv("API_HEADERS"))
API_BODY = json.load(os.getenv("API_BODY"))


async def call_successful_conversion():
    """
    Makes an api call upon a successful file conversion.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_ENDPOINT, headers=API_HEADERS, data=API_BODY):
                # no need to process response
                pass
    except (Exception,):
        # in the event of an exception, don't have to do anything (i.e. ok to lose some counts).
        pass


