from fastapi import APIRouter, Request
from typing import List

from .model import GenerationSchema, Model
from .service import generate_orchestrator
from utilities.methods import generate_uuid

router = APIRouter()


@router.post("/generate", response_model=GenerationSchema)
async def generate(
    request: Request,
    model: Model = {"model_type": "GPT", "model_version": "gpt-3.5-turbo"},
    response_format: dict = None,
    context: str = None,
    messages: List[dict] = [],
    settings: dict = None,
):

    generate_request = await generate_orchestrator(
        model,
        response_format,
        context,
        messages,
        settings,
    )

    # remove object_id
    generate_request.pop("_id")

    return generate_request
