from fastapi.responses import JSONResponse
from typing import Optional


def create_json_response(
    success: bool, status: int, error: str, response: Optional[str]
):
    return JSONResponse(
        content={
            "success": success,
            "status": status,
            "error": error,
            "response": response,
        },
        status_code=status,
    )
