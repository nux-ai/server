from fastapi import APIRouter, HTTPException, Body, Depends, Request, Path

from .model import ParseFileRequest, SupportedModalities
from .service import ParseHandler

router = APIRouter()


@router.post("/{modality}")
async def parse_file(
    request: Request,
    request_body: ParseFileRequest,
    modality: SupportedModalities = Path(...),
):
    parse_handler = ParseHandler(request.index_id)

    if len(request_body.file_urls) == 0:
        raise HTTPException(status_code=400, detail="No file_urls provided")

    if len(request_body.file_urls) > 1:
        raise HTTPException(
            status_code=400, detail="Multiple file_urls are not supported yet"
        )
    try:
        return await parse_handler.run_handler_once(
            modality=modality, file_url=request_body.file_urls[0]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
