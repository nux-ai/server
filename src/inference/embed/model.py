from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class Modality(Enum):
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"
    TEXT = "text"


class DimensionRequest(BaseModel):
    modality: Optional[Modality] = "text"
    model: Optional[str] = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingRequest(BaseModel):
    input: str
    modality: Optional[Modality] = "text"
    model: str = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    elapsed_time: float


class DimensionsResponse(BaseModel):
    dimensions: int
    elapsed_time: float
