from pydantic import BaseModel, confloat
from typing import Optional, List
from datetime import datetime


class ListenerSchema(BaseModel):
    index_id: str
    workbook_id: str
    author_id: str
    comment_id: str
    comment: str
    created_at: datetime
    metadata: Optional[dict] = None
    replied_to: Optional[str] = None


# class CommentRequest(BaseModel):
#     workbook_id: str
#     author_id: str
#     comment: str
#     metadata: Optional[dict] = None
#     replied_to: Optional[str] = None
