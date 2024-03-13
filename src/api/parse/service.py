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


async def download_file_to_bytes(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        return response.content
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading file")


class ParseHandler:
    def __init__(self, index_id):
        self.index_id = index_id
        self.parse_classes = {"text": Text}

    async def run_handler_once(self, modality, file_url):
        if modality.lower() in self.parse_classes:

            # ensure doesn't exceed filesize limit
            size = await get_file_size(file_url)
            if size > file_size_limit:
                raise HTTPException(
                    status_code=400, detail="File size exceeds 10MB limit"
                )

            # download file
            file_bytes = await download_file_to_bytes(file_url)

            # detect file type
            provided_filetype = detect_filetype(file_bytes)
            with open("supported_filetypes.json", "r") as f:
                supported_filetypes = json.load(f)

            if provided_filetype["label"] not in supported_filetypes:
                raise HTTPException(status_code=400, detail="File type not supported")

            # parse file
            parse_handler_class = self.parse_classes[modality](
                file_bytes, provided_filetype
            )
            async with parse_handler_class as instance:
                return await instance.run()
        else:
            raise HTTPException(status_code=400, detail="parse class not found")

    async def run_handler_many(self, modality, file_urls):
        # TODO implement queuing for multiple file_urls
        raise NotImplementedError
