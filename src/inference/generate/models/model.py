from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict


class Model(BaseModel):
    model_type: str
    """The type of the model (e.g., GPT, LLaMA)."""

    model_version: str
    """The specific model version."""


class Message(BaseModel):
    role: str
    """"The role of the message, either 'system' or 'user' or 'assistant'."""

    content: str
    """The content of the message."""


class Settings(BaseModel):
    system_prompt: Optional[str] = None
    """System prompt to prepend to each message."""

    temperature: Optional[float] = None
    """Sampling temperature to use."""

    max_tokens: Optional[int] = None
    """Maximum number of tokens to generate."""

    stop: Optional[List[str]] = None
    """Sequence where the API will stop generating further tokens."""

    top_p: Optional[float] = None
    """Nucleus sampling parameter."""

    frequency_penalty: Optional[float] = None
    """Penalty for new tokens based on their frequency."""

    presence_penalty: Optional[float] = None
    """Penalty for new tokens based on their presence."""

    class Config:
        schema_extra = {
            "example": {
                "system_prompt": "You are a helpful assistant.",
                "temperature": 0.7,
                "max_tokens": 150,
                "stop": ["\n"],
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            }
        }


class GenerationRequest(BaseModel):
    model: Model = Field(
        default={"model_type": "GPT", "model_version": "gpt-3.5-turbo"}
    )
    """The model configuration, specifying the type and version of the model."""

    response_format: Optional[Dict] = None
    """Optional dictionary specifying the format of the response."""

    context: Optional[str] = None
    """Optional string providing context for the generation request."""

    messages: List[Message] = []
    """List of messages involved in the generation context."""

    settings: Optional[Settings] = None
    """Optional settings to control the generation process."""


class GenerationResponse(BaseModel):
    generation_id: str
    """A unique identifier for the generation."""

    created_at: datetime
    """The timestamp of when the generation was created."""

    model: Model
    """The model used for the generation."""

    metadata: dict
    """Metadata object for the generation."""

    data: List[dict] = []
    """A list of generation objects"""

    error: dict = None
    """Optional field to capture any errors that occurred during the generation process."""
