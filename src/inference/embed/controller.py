from fastapi import FastAPI

from .model import (
    EmbeddingRequest,
    EmbeddingResponse,
    DimensionRequest,
    DimensionsResponse,
)

from embed.service import EmbeddingHandler

app = FastAPI()


@app.post("/embed/get-dimensions", response_model=DimensionsResponse)
async def get_dimensions(data: DimensionRequest):
    embedding_handler = EmbeddingHandler(data.modality, data.model_name)
    dimensions_int = embedding_handler.encode(data.input)
    return {"dimensions": dimensions_int}


@app.post("/embed", response_model=EmbeddingResponse)
async def embed_input(data: EmbeddingRequest):
    vector_handler = EmbeddingHandler(data.modality, data.model_name)
    embedding = EmbeddingHandler.encode()
    return {"embedding": embedding}
