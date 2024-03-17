import aiohttp
from unstructured.partition.api import partition_via_api
from config import unstructured


class TextService:
    def __init__(self, file_stream, metadata):
        self.api_key = unstructured["api_key"]
        self.metadata = metadata
        self.file_stream = file_stream
        self.chunks = []

    async def run(self):
        try:
            elements = partition_via_api(
                file=self.file_stream,
                api_key="R2cztPgpslK6wl55zoeChhUgkGbmyL",
                strategy="auto",
                pdf_infer_table_structure="true",
                metadata_filename=self.metadata["filename"],
            )
            for e in elements:
                self.chunks.append(e.to_dict())

            return {
                "status": 200,
                "message": "Success",
                "data": self.chunks,
            }
        except Exception as e:
            return {
                "status": 500,
                "message": f"An error occurred: {str(e)}",
                "data": [],
            }

# class FileTextExtractor:
#     def __init__(self, file):
#         self.file = file

#     async def extract_text(self):
#         file_stream = BytesIO(await self.file.read())
#         if file_stream:
#             try:
#                 # Extract text and metadata using Tika directly from the bytes buffer
#                 # Use getvalue() for async compatibility
#                 parsed = parser.from_buffer(file_stream.getvalue())
#                 text = parsed.get("content", "")
#                 metadata = parsed.get("metadata", {})
#                 if text:
#                     return {
#                         "status": "ok",
#                         "message": "File text extraction was successful.",
#                         "data": {
#                             "text": text.strip(),  # Strip to remove leading/trailing whitespace
#                             "metadata": metadata,
#                         },
#                     }, 200
#                 else:
#                     return {
#                         "status": "error",
#                         "message": "File downloaded but contains no text or could not be parsed.",
#                         "data": None,
#                     }, 400
#             except Exception as e:
#                 # Handle potential errors during parsing
#                 return {
#                     "status": "error",
#                     "message": f"Error parsing the file content: {e}",
#                     "data": None,
#                 }, 500
#         else:
#             return {
#                 "status": "error",
#                 "message": "Couldnt download file",
#                 "data": None,
#             }, 400
