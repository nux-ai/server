from fastapi import APIRouter, HTTPException, Body, Depends, Request
from typing import List

from .model import WorkflowCreateRequest, WorkflowMinimalResponse, WorkflowSchema
from .service import WorkflowSyncService

from db_internal.model import PaginationParams

router = APIRouter()


@router.post("/", response_model=WorkflowSchema)
async def create_workflow(
    request: Request,
    workflow_request: WorkflowCreateRequest = Body(...),
    pagination: PaginationParams = Depends(),
):
    workflow_service = WorkflowSyncService(request.index_id)
    return workflow_service.create(workflow_request)


# @router.get('/', response_model=List[WorkflowMinimalResponse])
# def list_workflows(
#     request: Request,
#     pagination: PaginationParams = Depends()
# ):

#     wb_service = WorkflowSyncService(
#         index_id,
#         version_id="latest",
#         scope=scope
#     )
#     try:
#         return wb_service.list(limit=pagination.limit, offset=pagination.offset)
#     except:
#         raise HTTPException(status_code=400, detail="Couldn't list workbooks.")


# @router.get("/{workflow_id}")
# async def get_workflow(
#     request: Request,
# ):

#     return {"message": "Listener created"}


# @router.put("/{workflow_id}")
# async def update_workflow(
#     request: Request,
# ):

#     return {"message": "Listener created"}


# @router.delete("/{workflow_id}")
# async def delete_workflow(
#     request: Request,
# ):
#     return {"message": "Listener created"}
