import aiohttp
import asyncio


async def send(endpoint, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=payload) as response:
            return await response.text()
