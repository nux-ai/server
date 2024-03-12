from fastapi import APIRouter, HTTPException, Body, Depends, Request

# from .model import ListenerSchema
# from .service import ListenerAsyncService

router = APIRouter()


@router.post("/{provider_id}")
def receive_payload(request: Request):
    print(request.index_id)
    return {"message": "received"}
