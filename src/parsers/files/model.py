from pydantic import BaseModel, Field, root_validator, ValidationError
from typing import Optional
from fastapi import UploadFile


class FileData(BaseModel):
    file_url: Optional[str] = None
    contents: Optional[str] = None

    # @root_validator
    # def check_file_data(cls, values):
    #     file_url, contents = values.get("file_url"), values.get("contents")
    #     if file_url is None and contents is None:
    #         raise ValidationError("Either 'file_url' or 'contents' must be provided.")
    #     if file_url is not None and contents is not None:
    #         raise ValidationError(
    #             "Only one of 'file_url' or 'contents' can be provided."
    #         )
    #     return values
