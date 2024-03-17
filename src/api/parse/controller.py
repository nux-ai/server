from fastapi import APIRouter, HTTPException, Body, Depends, Request, Path

from .model import ParseFileRequest
from .service import ParseHandler

router = APIRouter()


# @router.post("/{modality}")
# async def parse_file(
#     request: Request,
#     request_body: ParseFileRequest
# ):
