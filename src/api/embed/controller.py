from fastapi import APIRouter, HTTPException, Body, Depends, Request

router = APIRouter()


@router.post("/")
async def embed_input(request: Request):
    return "ok"
