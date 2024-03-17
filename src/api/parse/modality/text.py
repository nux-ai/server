from config import parser_url
import time
import json
import httpx
import io


class Text:
    def __init__(self, file_bytes, file_type):
        self.url = f"{parser_url}/process/file"
        self.file_bytes = file_bytes
        self.file_type = file_type
        self.response_object = {
            "response": None,
            "error": None,
            "status": 500,
            "metadata": {"content_type": "application/json"},
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def _extract_text(self, file_bytes: bytes):
        tmp_filename = f"file.{self.file_type['mime_type']}"

        files = [
            (
                "file",
                (tmp_filename, io.BytesIO(file_bytes), self.file_type["mime_type"]),
            )
        ]

        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, files=files)
            print(response.text)
        return response.json()

    async def run(self):
        print("parsing_text")
        start_time = time.time() * 1000

        try:
            parser_response = await self._extract_text(self.file_bytes)

            print(parser_response)

            if parser_response["status"] == "ok":
                self.response_object["response"] = parser_response["data"]["text"]
                self.response_object["status"] = 200

            else:
                self.response_object["error"] = parser_response["message"]
                self.response_object["status"] = 500

        except Exception as e:
            self.response_object["error"] = f"Failed to call Parser: {e}"
            self.response_object["status"] = 500

        self.response_object["metadata"] = {
            "runtime": (time.time() * 1000) - start_time,
            "file_type": self.file_type,
        }

        return self.response_object
