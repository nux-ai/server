from fastapi import APIRouter, HTTPException, Body, Depends, Request, Path
from typing import Optional, Dict, Any


from .model import ParseFileRequest
from .service import ParseHandler

router = APIRouter()


@router.post("/")
async def parse_file(
    request: Request,
    parser_request: ParseFileRequest,
    should_chunk: Optional[bool] = True,
):
    parse_handler = ParseHandler(request.index_id)
    payload = {
        "file_url": parser_request.file_url,
        # "contents": getattr(request_body.contents, "contents", None),
        "index_id": request.index_id,
    }
    try:
        response = await parse_handler.send_to_parser(payload, should_chunk)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
