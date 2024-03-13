from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from utilities.helpers import unique_name


class ListenerSettings(BaseModel):
    requirements: List[str] = Field(default_factory=list)
    python_version: Optional[str] = "python3.10"


class ListenerSchema(BaseModel):
    index_id: str
    created_at: datetime
    provider_id: str
    code_as_string: str
    listener_name: str
    metadata: dict
    settings: ListenerSettings


class ProviderInformation(BaseModel):
    webhook_url: str
    metadata: Optional[dict] = {}


class ListenerCreateRequest(BaseModel):
    provider_id: str
    provider_information: ProviderInformation
    code_as_string: str
    listener_name: Optional[str] = Field(default_factory=unique_name)
    metadata: Optional[dict] = {}
    settings: Optional[ListenerSettings] = {}
