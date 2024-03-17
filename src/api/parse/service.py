from fastapi import HTTPException
import httpx
import json

from utilities.helpers import detect_filetype

from .modality.text import Text

file_size_limit = 10000000  # 10MB


async def get_file_size(url):
    async with httpx.AsyncClient() as client:
        response = await client.head(url)
    size = response.headers.get("Content-Length")

    if size is not None:
        return int(size)
    else:
        raise HTTPException(status_code=400, detail="File size not found")


class ParseHandler:
    def __init__(self, index_id):
        self.index_id = index_id
        self.parse_classes = {"text": Text}
