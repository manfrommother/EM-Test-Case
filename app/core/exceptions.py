from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NoAvailableCopiesException(BadRequestException):
    def __init__(self):
        super().__init__(detail='No available copies of this book')
