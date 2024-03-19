from _exceptions import NotFoundError, BadRequestError, InternalServerError
import httpx
import json

from config import parser_url

file_size_limit = 10000000  # 10MB


async def get_file_size(url):
    async with httpx.AsyncClient() as client:
        response = await client.head(url)
    size = response.headers.get("Content-Length")

    if size is not None:
        return int(size)
    else:
        raise NotFoundError({"error": "File not found"})


class ParseHandler:
    def __init__(self, index_id):
        self.index_id = index_id
        self.url = f"{parser_url}/file"

    async def send_to_parser(self, payload, should_chunk):
        # if await get_file_size(payload["file_url"]) > file_size_limit:
        #     raise BadRequestError({"error": "File too large"})

        payload["index_id"] = self.index_id

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url + "?should_chunk=" + str(should_chunk),
                json=payload,
            )
            return response.json()
