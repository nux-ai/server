from fastapi import APIRouter, HTTPException, Body, Depends, Request, Path

from .model import ParseFileRequest
from .service import ParseHandler

router = APIRouter()


@router.post("/")
async def parse_file(request: Request, parser_request: ParseFileRequest):
    parse_handler = ParseHandler(request.index_id)
    payload = {
        "file_url": parser_request.file_url,
        # "contents": getattr(request_body.contents, "contents", None),
        "index_id": request.index_id,
    }
    try:
        response = await parse_handler.send_to_parser(payload)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
