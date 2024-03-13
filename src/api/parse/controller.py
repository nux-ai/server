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

    # one single file_url provided
    if isinstance(request_body.file_url, str):
        return await parse_handler.run_handler_once(
            modality=modality, file_url=request_body.file_url
        )

    # multiple file_urls provided
    elif isinstance(request_body.file_url, list):
        raise NotImplementedError
