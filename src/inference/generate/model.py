from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class Model(BaseModel):
    model_type: str = Field(..., description="The type of the model (e.g., GPT, LLaMA).")
    """The type of the model (e.g., GPT, LLaMA)."""

    model_version: str
    """The specific model version."""


class GenerationSchema(BaseModel):
    generation_id: str
    """A unique identifier for the generation."""

    created_at: datetime
    """The timestamp of when the generation was created."""

    model: Model
    """The model used for the generation."""

    metadata: dict
    """Metadata object for the generation."""

    data: List[dict]
    """A list of generation objects"""
