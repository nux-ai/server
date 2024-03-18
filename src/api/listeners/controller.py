from fastapi import APIRouter, HTTPException, Body, Depends, Request

from .model import ConnectionInformation
from .service import ListenerAsyncService

router = APIRouter()

connection_info = {
    "db": "postgres",
    "user": "postgres.ajbmxtlpktvtcbtxxikl",
    "password": "qQbj2eAbTXHAfzOQ",
    "host": "aws-0-us-east-1.pooler.supabase.com",
    "table_name": "documents",
    # "port": 5434,
}

listener_id = "123"

listener_info = {
    "table_name": "my_table_name",
    "filters": {"status": "processing"},
    "embedding": {
        "model": "sentence-transformers/all-MiniLM-L6-v2",
        "field": "file_url",
        "embed_type": "url",  # url or in-place
    },
}


@router.post("/")
async def create_listener(
    request: Request,
    # connection_info: ConnectionInformation = Body(...),
):
    # init listener service
    listener_service = ListenerAsyncService(request.index_id)
    listener_service.init_client(request.api_key)

    resp = await listener_service.create_listener(connection_info)

    return {"message": "Listener created", "data": resp}


@router.post("/{provider_id}")
def receive_payload(request: Request):
    print(request)
    return {"message": "received"}
