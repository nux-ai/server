from fastapi import APIRouter
from _exceptions import BadRequestError, InternalServerError, NotFoundError

from generate.model import GenerationResponse, GenerationRequest
from generate.service import GenerateHandler


router = APIRouter()


@router.post("/", response_model=GenerationResponse)
async def generate(request: GenerationRequest) -> GenerationResponse:
    try:
        generate_handler = GenerateHandler(request)
        generate_request = await generate_handler._generate()
        return generate_request
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)
    except Exception as e:
        print("ERROR: ", e)
        raise InternalServerError(error="Internal Server Error")
