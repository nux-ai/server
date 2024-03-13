from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from utilities.helpers import unique_name, generate_uuid


class WorkflowSettings(BaseModel):
    requirements: List[str] = Field(default_factory=list)
    python_version: Optional[str] = "python3.10"


class WorkflowSchema(BaseModel):
    index_id: str
    created_at: datetime
    workflow_id: str
    code_as_string: str
    workflow_name: Optional[str]
    metadata: Optional[dict] = {}
    settings: WorkflowSettings


class WorkflowCreateRequest(BaseModel):
    workflow_id: Optional[str] = Field(default_factory=lambda: generate_uuid())
    code_as_string: str
    metadata: Optional[dict] = {}
    settings: WorkflowSettings
    workflow_name: Optional[str] = Field(default_factory=unique_name)


class WorkflowMinimalResponse(BaseModel):
    workflow_id: str
    workflow_name: Optional[str]
    created_at: datetime
    metadata: Optional[dict] = {}
