import cgi
import httpx
from io import BytesIO
from magika import Magika
import time

from .utils import generate_filename_from_url, get_filename_from_cd
from .text.service import TextService

from _exceptions import InternalServerError, NotFoundError, BadRequestError
from _utils import create_json_response

files = {
    "text": ["pdf", "docx", "txt", "md", "html", "xml"],
    "image": ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"],
    "audio": ["mp3", "wav", "ogg", "flac", "m4a", "wma", "aac"],
    "video": ["mp4", "mkv", "webm", "avi", "mov", "wmv", "flv"],
}


class FileHandler:
    def __init__(self, file_url):
        self.file_url = file_url

    async def download_into_memory(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.file_url)
                if response.status_code == 200:
                    filename = get_filename_from_cd(
                        response.headers.get("content-disposition")
                    )
                    if not filename:
                        filename = generate_filename_from_url(self.file_url)
                    else:
                        raise ValueError("Filename not found")
                    return response.content, filename
                else:
                    raise BadRequestError(
                        error={
                            "message": f"Error downloading file: {response.status_code}"
                        }
                    )

        except Exception as e:
            raise InternalServerError(error={"message": f"Error downloading file: {e}"})

    def detect_filetype(self, contents):
        try:
            m = Magika()
            res = m.identify_bytes(contents)
            # {
            #     "label": "pdf",
            #     "description": "PDF document",
            #     "mime_type": "application/pdf",
            #     "group": "document",
            # }
            data = {
                "label": res.output.ct_label,
                "description": res.output.description,
                "mime_type": res.output.mime_type,
                "group": res.output.group,
            }
            return data
        except Exception as e:
            raise InternalServerError(
                error={"message": "Error occurred while detecting filetype"}
            )

    async def parse_file(self):
        # Download file into memory
        contents, filename = await self.download_into_memory()
        stream = BytesIO(contents)

        # Detect file type
        metadata = self.detect_filetype(stream.getvalue())
        metadata["filename"] = filename
        metadata["start_time"] = time.time() * 1000

        text_service = TextService(stream, metadata)

        if metadata["label"] == "pdf":
            return await text_service.run_pdf()
        else:
            raise BadRequestError(error={"message": "File type not supported"})
