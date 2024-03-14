import httpx
from generate.model import GenerationRequest, GenerationResponse
from fastapi.encoders import jsonable_encoder

from _exceptions import BadRequestError, NotFoundError, InternalServerError

from config import inference_url


class GenerateHandler:
    def __init__(self, index_id, generation_request):
        self.index_id = index_id
        # TODO: credit handler for index_id
        self.generation_request = generation_request
        # TODO: handler for other models
        self.api_url = f"{inference_url}/generate/"

    async def _generate(self) -> GenerationResponse:
        async with httpx.AsyncClient() as client:
            request_dict = jsonable_encoder(self.generation_request)
            response = await client.post(self.api_url, json=request_dict)

            if response.status_code == 400:
                raise BadRequestError(response.json())
            elif response.status_code == 404:
                raise NotFoundError(response.json())
            elif response.status_code == 500:
                raise InternalServerError(response.json())

            response.raise_for_status()
            generation_response = GenerationResponse(**response.json())
            return generation_response
