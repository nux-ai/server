from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uvicorn


from sources.postgres.service import PostgresService
from sources.postgres.model import PostgresConnection


app = FastAPI()


@app.post("/postgres/setup")
async def setup_notify(connection_info: PostgresConnection):
    pg = PostgresService(connection_info)
    pg.create_notifier(connection_info.table_name)
    return pg.invoke_notifier(connection_info.table_name)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
