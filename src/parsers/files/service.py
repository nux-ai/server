import httpx
from tika import parser
from io import BytesIO


class FileTextExtractor:
    def __init__(self, file):
        self.file = file

    async def extract_text(self):
        file_stream = BytesIO(await self.file.read())
        if file_stream:
            try:
                # Extract text and metadata using Tika directly from the bytes buffer
                # Use getvalue() for async compatibility
                parsed = parser.from_buffer(file_stream.getvalue())
                text = parsed.get("content", "")
                metadata = parsed.get("metadata", {})
                if text:
                    return {
                        "status": "ok",
                        "message": "File text extraction was successful.",
                        "data": {
                            "text": text.strip(),  # Strip to remove leading/trailing whitespace
                            "metadata": metadata,
                        },
                    }, 200
                else:
                    return {
                        "status": "error",
                        "message": "File downloaded but contains no text or could not be parsed.",
                        "data": None,
                    }, 400
            except Exception as e:
                # Handle potential errors during parsing
                return {
                    "status": "error",
                    "message": f"Error parsing the file content: {e}",
                    "data": None,
                }, 500
        else:
            return {
                "status": "error",
                "message": "Couldnt download file",
                "data": None,
            }, 400
