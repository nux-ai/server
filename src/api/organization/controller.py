import pprint
from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from typing import Optional, Union, cast

from auth.service import get_index_id
from db.model import PaginationParams

from organization.clerk_model import (
    ClerkOrganizationCreatedData,
    ClerkOrganizationDeletedData,
    ClerkOrganizationMembershipData,
    ClerkUserCreatedData,
    WebhookClerkEvent,
)
from workbook.service import WorkbookSyncService
from .model import (
    CreateOrgRequest,
    OrganizationBase,
    TrustedOrgResponse,
    SecretRequest,
)
from .service import OrganizationSyncService
from fastapi import Request, Response, status

from svix.webhooks import Webhook, WebhookVerificationError
from config import clerk_credentials

router = APIRouter()


@router.post("/")
def create_organization(request: CreateOrgRequest, response_model=OrganizationBase):

    org_service = OrganizationSyncService()

    try:
        org = org_service.create_organization(
            request.org_metadata,
        )
        return org
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=Union[TrustedOrgResponse, OrganizationBase])
def get_organization(
    index_id: str = Depends(get_index_id), keys: Optional[bool] = None
):
    org_service = OrganizationSyncService()

    try:
        if keys:
            # Call a different method when keys is provided
            org = org_service.get_by_index_id(index_id)
            return OrganizationBase.parse_obj(org)
        else:
            org = org_service.get_for_frontend(index_id)
            return TrustedOrgResponse.parse_obj(org)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/secrets")
def add_secret(secret: SecretRequest, index_id: str = Depends(get_index_id)):
    organization_service = OrganizationSyncService()

    try:
        organization_service.add_secret(index_id, secret.name, secret.value)
        return {"message": "Secret added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/secrets")
def delete_secret(secret_name: str, index_id: str = Depends(get_index_id)):
    organization_service = OrganizationSyncService()

    try:
        organization_service.delete_secret(index_id, secret_name)
        return {"message": "Secret deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
