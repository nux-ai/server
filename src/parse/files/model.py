from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile


class FileData(BaseModel):
    file_url: str
