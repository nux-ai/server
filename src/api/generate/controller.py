from fastapi import APIRouter, Request, Body
from _exceptions import BadRequestError, InternalServerError, NotFoundError

from .model import GenerationResponse, GenerationRequest
from .service import GenerateHandler


router = APIRouter()


@router.post("/", response_model=GenerationResponse)
async def generate(
    request: Request,
    generation_request: GenerationRequest = Body(...),
):
    try:
        generate_handler = GenerateHandler(request.index_id, generation_request)
        return await generate_handler._generate()
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)
    except Exception as e:
        print("ERROR: ", e)
        raise InternalServerError(error="Internal Server Error")
