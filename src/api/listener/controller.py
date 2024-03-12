from fastapi import APIRouter, HTTPException, Body, Depends, Request

from .model import ListenerCreateRequest
from .service import ListenerAsyncService

router = APIRouter()


@router.post("/")
async def create_listener(
    request: Request,
    listener: ListenerCreateRequest = Body(...),
):
    listener_service = ListenerAsyncService(request.index_id)

    if await listener_service.get_listener(
        listener.provider_id, listener.listener_name
    ):
        raise HTTPException(
            status_code=400,
            detail="Listener with this provider and name already exists",
        )

    resp = await listener_service.create_listener(listener.model_dump(by_alias=True))

    return {"message": "Listener created", "data": resp}


@router.post("/{provider_id}")
def receive_payload(request: Request):
    # check if the provider_id exists in index_id
    # if not, return 404
    # check if provider_id has a serverless function
    # if it does, run it
    # if it doesn't return 404
    return {"message": "received"}
