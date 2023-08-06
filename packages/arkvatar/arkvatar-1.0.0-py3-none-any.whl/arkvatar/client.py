import aiohttp
import json


class Client:
    async def get(self, endpoint: str, headers: dict = {}):
        async with aiohttp.ClientSession(headers=headers) as session:
            request = await session.get(f"{endpoint}")
            response = await request.read()
            return json.loads(response)

    async def post(self, endpoint: str, data: dict = {}, headers:  dict = {}):
        async with aiohttp.ClientSession(headers=headers) as session:
            request = await session.post(f"{endpoint}", json=data)
            response = await request.read()
            return json.loads(response)
