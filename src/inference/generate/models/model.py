from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict


class Model(BaseModel):
    type: str = Field(..., description="The type of the model (e.g., GPT, LLaMA).")
    version: str = Field(..., description="The specific model version.")


class Message(BaseModel):
    role: str = Field(
        ...,
        description="The role of the message, either 'system' or 'user' or 'assistant'.",
    )
    content: str = Field(..., description="The content of the message.")


class Settings(BaseModel):
    system_prompt: Optional[str] = Field(
        None, description="System prompt to prepend to each message."
    )
    temperature: Optional[float] = Field(
        None, description="Sampling temperature to use."
    )
    max_tokens: Optional[int] = Field(
        None, description="Maximum number of tokens to generate."
    )
    stop: Optional[List[str]] = Field(
        None, description="Sequence where the API will stop generating further tokens."
    )
    top_p: Optional[float] = Field(None, description="Nucleus sampling parameter.")
    frequency_penalty: Optional[float] = Field(
        None, description="Penalty for new tokens based on their frequency."
    )
    presence_penalty: Optional[float] = Field(
        None, description="Penalty for new tokens based on their presence."
    )

    class Config:
        json_schema_extra = {
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
        default={"type": "GPT", "version": "gpt-3.5-turbo"},
        description="The model configuration, specifying the type and version of the model.",
    )
    response_format: Optional[Dict] = Field(
        None, description="Optional JSON schema specifying the format of the response from the LLM"
    )
    context: Optional[str] = Field(
        None,
        description="Optional string providing context for the generation request.",
    )
    messages: List[Message] = Field(
        ..., description="List of messages involved in the generation context."
    )
    settings: Optional[Settings] = Field(
        None, description="Optional settings to control the generation process."
    )


class Metadata(BaseModel):
    runtime: Optional[float] = Field(
        ..., description="The runtime of the generation process in milliseconds."
    )
    output_token_count: Optional[int] = Field(
        ..., description="The number of tokens generated in the response."
    )
    content_type: Optional[str] = Field(
        ..., description="The content type of the generated response."
    )


class GenerationResponse(BaseModel):
    generation_id: str = Field(
        ..., description="A unique identifier for the generation."
    )
    created_at: datetime = Field(
        ..., description="The timestamp of when the generation was created."
    )
    model: Model = Field(..., description="The model used for the generation.")
    metadata: Optional[Metadata] = Field(..., description="Metadata object for the generation.")
    data: List[dict] = Field(..., description="A list of generation objects")
    error: Optional[dict] = Field(
        None,
        description="Optional field to capture any errors that occurred during the generation process.",
    )
    status: int = Field(
        ..., description="HTTP status code representing the outcome of the generation."
    )
