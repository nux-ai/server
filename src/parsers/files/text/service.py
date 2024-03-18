import aiohttp
from unstructured.partition.api import partition_via_api
from config import unstructured

from _exceptions import InternalServerError


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
                api_key=self.api_key,
                strategy="auto",
                pdf_infer_table_structure="true",
                metadata_filename=self.metadata["filename"],
            )
            for e in elements:
                self.chunks.append(e.to_dict())

            return {
                "success": True,
                "status": 200,
                "error": None,
                "response": self.chunks,
            }, 200
        except Exception as e:
            error = {"message": str(e)}
            raise InternalServerError(error)
