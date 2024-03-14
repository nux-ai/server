import httpx
from .model import GenerationRequest, GenerationResponse
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from config import inference_url


class GenerateHandler:
    def __init__(self, request: GenerationRequest):
        self.request = request
        self.api_url = "{inference_url}/generate"

    async def _generate(self) -> GenerationResponse:
        try:
            async with httpx.AsyncClient() as client:
                request_dict = jsonable_encoder(self.request)
                response = await client.post(self.api_url, json=request_dict)
                response.raise_for_status()
                generation_response = GenerationResponse(**response.json())
                return generation_response
        except httpx.HTTPStatusError as http_err:
            raise HTTPException(
                status_code=http_err.response.status_code, detail=str(http_err)
            )
        except httpx.RequestError as req_err:
            raise HTTPException(
                status_code=503, detail=f"Request error: {str(req_err)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unexpected error occurred: {str(e)}"
            )
