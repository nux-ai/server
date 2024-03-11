from enum import Enum
from pydantic import BaseModel
from typing import Optional


class Modality(Enum):
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"
    TEXT = "text"


class DimensionRequest(BaseModel):
    modality: Optional[Modality] = None
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingRequest(BaseModel):
    input: Optional[str] = None
    modality: Optional[Modality] = None
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingResponse(BaseModel):
    embedding: float


class DimensionsResponse(BaseModel):
    dimensions: int
