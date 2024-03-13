from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging

# from .extensions import configure_extensions
# from .logger import configure_logging

from api import api_router

# from rate_limiter import limiter

log = logging.getLogger(__name__)

# we configure the logging level and format
# configure_logging()

app = FastAPI(openapi_url="/docs/openapi.json", title="NUX API")


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    # sentry_sdk.capture_exception(traceback.print_exc())
    return JSONResponse(
        status_code=500,
        content={
            "detail": "We made a mistake, email info@nux.ai or submit an issue on GitHub"
        },
    )


# # Add the limiter as a middleware
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(api_router)
