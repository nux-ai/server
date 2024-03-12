from fastapi import APIRouter, HTTPException

from .models.model import GenerationResponse, GenerationRequest
from .service import generate_orchestrator


router = APIRouter()


@router.post("/", response_model=GenerationResponse)
async def generate(request: GenerationRequest) -> GenerationResponse:
    try:
        generate_request = await generate_orchestrator(request)
        return generate_request
    except Exception as e:
        # You can customize the status code and the detail message based on the exception
        raise HTTPException(status_code=500, detail=str(e))
