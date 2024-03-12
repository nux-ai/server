from fastapi import APIRouter, HTTPException
from typing import List

from .models.model import GenerationResponse, GenerationRequest, Model
from .service import generate_orchestrator


router = APIRouter()


@router.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    generate_request = await generate_orchestrator(request)
    generate_request.pop("_id", None)  # Safely remove "_id" if exists
    return generate_request
