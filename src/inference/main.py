# Related third party imports
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Local application/library specific imports
from generate.controller import router as generate_router
from embed.controller import router as embed_router
from _exceptions import InternalServerError, NotFoundError, BadRequestError
from _utils import create_json_response

app = FastAPI(openapi_url="/docs/openapi.json", title="NUX Inference API")
api_router = APIRouter()


api_router = APIRouter(default_response_class=JSONResponse)


@app.exception_handler(InternalServerError)
async def internal_server_exception_handler(request: Request, exc: InternalServerError):
    return create_json_response(exc.success, exc.status, exc.error, exc.response)


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return create_json_response(exc.success, exc.status, exc.error, exc.response)


@app.exception_handler(BadRequestError)
async def bad_request_exception_handler(request: Request, exc: BadRequestError):
    return create_json_response(exc.success, exc.status, exc.error, exc.response)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return create_json_response(False, 422, exc.errors(), None)


api_router.include_router(generate_router, prefix="/generate", tags=["Generate"])
api_router.include_router(embed_router, prefix="/embed", tags=["Embed"])


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


# Include your routers here
app.include_router(api_router)
