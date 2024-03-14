from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from generate.model import GenerationResponse, GenerationRequest
from generate.service import GenerateHandler


router = APIRouter()


@router.post("/", response_model=GenerationResponse)
async def generate(request: GenerationRequest) -> GenerationResponse:
    try:
        generate_handler = GenerateHandler(request)
        generate_request = await generate_handler._generate()
        return generate_request
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
