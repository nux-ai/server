from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union
from datetime import datetime

from utilities.helpers import generate_api_key
from enum import Enum

# requests


class CreateOrgRequest(BaseModel):
    email: EmailStr
    org_metadata: Optional[dict] = {}
    user_metadata: Optional[dict] = {}


class SecretRequest(BaseModel):
    name: str
    value: str


# responses


class OrgIndexResponse(BaseModel):
    indexes: List[str] = []


# schema
class CodePermissions(BaseModel):
    memory_size: int = Field(default=1024)
    timeout: int = Field(default=60)
    packages_allowed: List[str] = ["requests"]


class ModelPermissions(BaseModel):
    pass


class DataPermissions(BaseModel):
    memory_size: int = Field(default=1024)
    timeout: int = Field(default=60)
    types_allowed: List[str] = Field(default_factory=list)


class Permissions(BaseModel):
    rate_limit: str = Field(default="10/minute")  # requests per minute


class PricingTier(str, Enum):
    free = "free"
    deluxe = "deluxe"
    premium = "premium"
    startup = "startup"
    enterprise = "enterprise"


class UsagePricing(BaseModel):
    credits: int = Field(default=1000)
    pricing_tier: PricingTier = Field(default=PricingTier.free)
    # credit_usage_history: List[dict] = Field(default_factory=list)
    # last_credit_recharge_date: Optional[datetime] = None
    # credit_recharge_history: List[dict] = Field(default_factory=list)


class Index(BaseModel):
    index_id: str = Field(default_factory=lambda: "ix-" + generate_api_key())


class ApiKey(BaseModel):
    name: str = Field(default="default")
    key: str = Field(default_factory=lambda: "sk-" + generate_api_key())


class User(BaseModel):
    email: EmailStr
    creation_date: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)
    scope: str = Field(default="organization")


class Secret(BaseModel):
    name: str
    value: bytes


class ApiKeyScope(BaseModel):
    user_ids: Optional[List[str]] = None


class ApiKey(BaseModel):
    name: str
    key: str = Field(default_factory=lambda: "sk-" + generate_api_key())
    scope: ApiKeyScope = Field(default_factory=ApiKeyScope)
    indexes: List[str] = Field(default_factory=list)


class OrganizationBase(BaseModel):
    org_id: str = Field(default_factory=lambda: "org-" + generate_api_key())
    indexes: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    creation_date: datetime = Field(default_factory=datetime.now)
    secrets: List[Secret] = Field(default_factory=list)
    api_keys: List[ApiKey] = Field(default_factory=list)
    users: List[User] = Field(default_factory=list)

    permissions: Permissions
    usage: UsagePricing


class TrustedUserResponse(BaseModel):
    email: EmailStr
    creation_date: datetime
    metadata: dict
    scope: str


class TrustedOrgResponse(BaseModel):
    org_id: str
    indexes: List[str]
    metadata: dict
    creation_date: datetime

    users: List[TrustedUserResponse]

    permissions: Permissions
    usage: UsagePricing
