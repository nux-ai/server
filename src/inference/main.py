# Standard library imports
from typing import List, Optional

# Related third party imports
import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

# Local application/library specific imports
from generate.controller import router as generate_router
from embed.controller import router as embed_router

app = FastAPI(openapi_url="/docs/openapi.json", title="NUX Inference API")
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


api_router.include_router(generate_router, prefix="/generate", tags=["Generate"])
api_router.include_router(embed_router, prefix="/embed", tags=["Embed"])


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


# Include your routers here
app.include_router(api_router)
