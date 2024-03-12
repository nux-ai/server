from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ListenerSettings(BaseModel):
    requirements: List[str] = Field(default_factory=list)
    python_version: Optional[str] = "python3.10"


class ListenerCreateRequest(BaseModel):
    index_id: str
    created_at: datetime
    provider_id: str
    code_as_string: str
    listener_name: Optional[str]
    metadata: Optional[dict] = None
    settings: Optional[ListenerSettings] = None
