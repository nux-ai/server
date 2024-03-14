from typing import Optional


class NuxException(Exception):
    def __init__(
        self,
        success: bool,
        status: int,
        error: Optional[dict] = None,
        response: Optional[dict] = None,
    ):
        self.success = success
        self.status = status
        self.error = error
        self.response = response
        super().__init__(self.error)


class InternalServerError(NuxException):
    def __init__(self, error: Optional[dict] = None, response: Optional[dict] = None):
        super().__init__(
            success=False,
            status=500,
            error=error or {"message": "Internal Server Error"},
            response=response,
        )


class NotFoundError(NuxException):
    def __init__(self, error: Optional[dict] = None, response: Optional[dict] = None):
        super().__init__(
            success=False,
            status=404,
            error=error or {"message": "Not Found"},
            response=response,
        )


class BadRequestError(NuxException):
    def __init__(self, error: Optional[dict] = None, response: Optional[dict] = None):
        super().__init__(
            success=False,
            status=400,
            error=error or {"message": "Bad Request"},
            response=response,
        )
