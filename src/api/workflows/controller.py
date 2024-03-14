from fastapi import APIRouter, HTTPException, Body, Depends, Request
from typing import List, Optional

from utilities.helpers import generate_uuid, current_time

from .model import WorkflowCreateRequest, WorkflowMinimalResponse, WorkflowSchema
from .service import WorkflowSyncService, WorkflowRunService

from db_internal.model import PaginationParams, QueryParamsSchema

router = APIRouter()


@router.post("/", response_model=WorkflowSchema)
async def create_workflow(
    request: Request,
    workflow_request: WorkflowCreateRequest = Body(...),
    pagination: PaginationParams = Depends(),
):
    workflow_service = WorkflowSyncService(request.index_id)
    return workflow_service.create(workflow_request)


@router.post("/{workflow_id}/run")
async def run_workflow(
    request: Request,
    workflow_id: str,
    parameters: Optional[QueryParamsSchema] = None,
    websocket_id: Optional[str] = None,
):
    workflow_service = WorkflowRunService(request.index_id)

    workflow = workflow_service.get(workflow_id)
    if not workflow:
        raise HTTPException(
            status_code=404, detail=f"Workflow {workflow_id} not found."
        )
    if workflow.get("metadata", {}).get("serverless_function_name") is None:
        raise HTTPException(
            status_code=400,
            detail=f"Workflow {workflow_id} has no serverless function.",
        )

    # run orchestrator
    task = await workflow_service.run(
        workflow=workflow,
        run_id=generate_uuid(),
        websocket_id=websocket_id,
        request_parameters=parameters,
    )

    workflow_service.update({"last_run": current_time()})

    # remove objectId
    task.pop("_id")
    return task


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
