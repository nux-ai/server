from pydantic import BaseModel
from typing import List, Union
from enum import Enum


class SupportedModalities(str, Enum):
    text = "text"
    image = "image"
    audio = "audio"
    video = "video"


class ParseFileRequest(BaseModel):
    file_url: str
