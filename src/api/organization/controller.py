from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Union, cast

from auth.service import get_index_id
from db_internal.model import PaginationParams

from .model import (
    CreateOrgRequest,
    OrganizationBase,
    TrustedOrgResponse,
    SecretRequest,
)
from .service import OrganizationSyncService
from fastapi import Request, Response, status

router = APIRouter()


@router.post("/")
def create_organization(request: CreateOrgRequest):
    org_service = OrganizationSyncService()
    return org_service.create_organization(email=request.email)


# @router.get("/", response_model=Union[TrustedOrgResponse, OrganizationBase])
# def get_organization(
#     index_id: str = Depends(get_index_id), keys: Optional[bool] = None
# ):
#     org_service = OrganizationSyncService()

#     try:
#         if keys:
#             # Call a different method when keys is provided
#             org = org_service.get_by_index_id(index_id)
#             return OrganizationBase.model_validate(org)
#         else:
#             org = org_service.get_for_frontend(index_id)
#             return TrustedOrgResponse.model_validate(org)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @router.post("/secrets")
# def add_secret(secret: SecretRequest, index_id: str = Depends(get_index_id)):
#     organization_service = OrganizationSyncService()

#     try:
#         organization_service.add_secret(index_id, secret.name, secret.value)
#         return {"message": "Secret added successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @router.delete("/secrets")
# def delete_secret(secret_name: str, index_id: str = Depends(get_index_id)):
#     organization_service = OrganizationSyncService()

#     try:
#         organization_service.delete_secret(index_id, secret_name)
#         return {"message": "Secret deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
