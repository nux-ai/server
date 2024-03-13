# Standard library imports
from typing import List, Optional

# Related third party imports
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

# Local application/library specific imports
from auth.service import get_index_id

# Local application/library specific imports
from listener.controller import router as listener_router
from organization.controller import router as organization_router
from parse.controller import router as parse_router
from workflow.controller import router as workflow_router


api_router = APIRouter()


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)


# unauthenticated
api_router.include_router(
    organization_router, prefix="/organizations", tags=["Organization"]
)

# authenticated
# fmt: off
api_router.include_router(listener_router, prefix="/listeners", tags=["Listener"], dependencies=[Depends(get_index_id)])
api_router.include_router(parse_router, prefix="/parse", tags=["Parse"], dependencies=[Depends(get_index_id)])
api_router.include_router(workflow_router, prefix="/workflows", tags=["Workflow"], dependencies=[Depends(get_index_id)])

@api_router.get("/", include_in_schema=False)
def hello_world():
    return {"message": "welcome to the NUX api, check out the docs for more: docs.nux.ai"}


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
