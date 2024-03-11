from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

from files.model import FileData
from files.service import FileTextExtractor

from website.service import AsyncWebScraper
from website.model import WebsiteData


import tika

tika.initVM()

app = FastAPI()


@app.post("/process/file")
async def process_file(data: FileData):
    extractor = FileTextExtractor(data.file_url)
    response, status_code = await extractor.extract_text()
    return JSONResponse(content=response, status_code=status_code)


@app.post("/process/website")
async def process_website(data: WebsiteData):
    scraper = AsyncWebScraper(data.website, data.max_depth)
    result = await scraper.scrape_data()
    return {"results": result}


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
