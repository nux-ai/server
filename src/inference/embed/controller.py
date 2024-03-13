from fastapi import APIRouter  # Import APIRouter instead of FastAPI

from .model import (
    EmbeddingRequest,
    EmbeddingResponse,
    DimensionRequest,
    DimensionsResponse,
)

from embed.service import EmbeddingHandler

router = APIRouter()


@router.get("/dimensions", response_model=DimensionsResponse)
async def get_dimensions(data: DimensionRequest):
    embedding_handler = EmbeddingHandler(data.modality, data.model)
    return embedding_handler.get_dimensions()


@router.get("/", response_model=EmbeddingResponse)
async def embed_input(data: EmbeddingRequest):
    embedding_handler = EmbeddingHandler(data.modality, data.model)
    return embedding_handler.encode(data.input)
