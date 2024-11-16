from typing import Any

from fastapi import status
from starlette.exceptions import HTTPException


class BaseException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Any = 'Internal server error',
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class InternalServerErrorException(BaseException):
    def __init__(self, detail: Any = 'Internal server error') -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class NotFoundException(BaseException):
    def __init__(self, detail: str = 'Not found') -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
