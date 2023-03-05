from fastapi import status


class CustomException(Exception):
    error_type: str = ""
    reason: str = ""
    status_code: int = status.HTTP_400_BAD_REQUEST


class EntityAlreadyExistException(CustomException):
    def __init__(self, reason: str = "reason", details: dict = None):
        self.reason = reason
        self.details = details

    error_code = "EntityAlreadyExistException"
    status_code = status.HTTP_409_CONFLICT


class EntityNotFoundException(CustomException):
    def __init__(self, reason: str = "reason", details: dict = None):
        self.reason = reason
        self.details = details

    error_code = "EntityNotFoundException"
    status_code = status.HTTP_404_NOT_FOUND


class EntitySubordinationException(CustomException):

    def __init__(self, reason: str = "reason", details: dict = None):
        self.reason = reason
        self.details = details

    error_type = "EntitySubordinationException"
    status_code = status.HTTP_400_BAD_REQUEST


class PaginationException(CustomException):
    error_type = "PaginationException"
    reason = "invalid pagination values(page or per_page are non-positive)"
    location = ["page", "per_page"]
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class DatabaseException(CustomException):
    def __init__(self, reason: str = "reason", details: dict = None):
        self.reason = reason
        self.details = details

    error_type = "DatabaseException"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class InternalDatabaseException(CustomException):
    def __init__(self, reason: str | None = None):
        super().__init__()
        self.error_type = "InternalDatabaseException"
        if reason:
            self.reason = reason
        else:
            self.reason = "something goes wrong with database"

        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
