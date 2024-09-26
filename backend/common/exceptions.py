from typing import Optional

from fastapi import HTTPException, status

from backend.common import constants as cst
from backend.common import messages as msg


class LogError(Exception):
    """Log error."""

    pass


class UnauthorizedHttpError(HTTPException):
    """Unauthorized error."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = msg.E_API_UNAUTHORIZED
    headers = {cst.HEADER_NAME_AUTHENTICATE: cst.HEADER_TYPE_TOKEN_BEARER}

    def __init__(self, detail: Optional[str] = None):
        if detail is not None:
            self.detail = detail
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )
