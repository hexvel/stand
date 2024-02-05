import typing

import aiohttp
from typing import Literal


class Request:

    @staticmethod
    async def request(url: str, data: dict):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=data) as resp:
                return await resp.json()