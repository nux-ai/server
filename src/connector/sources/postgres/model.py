from pydantic import BaseModel
from typing import Optional


class PostgresConnection(BaseModel):
    table_name: str
    db: str
    host: str
    port: Optional[int] = 5432
    user: str
    password: str
