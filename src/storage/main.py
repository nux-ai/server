# Related third party imports
from fastapi import APIRouter


api_router = APIRouter()


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
