from fastapi import status


class CustomException(Exception):
    error_type: str = ""
    reason: str = ""
    status_code: int = status.HTTP_400_BAD_REQUEST


class NoTokenProvidedException(CustomException):
    error_type = "NoTokenProvidedException"
    reason = "no token provided"
    status_code = status.HTTP_401_UNAUTHORIZED


class VehicleAlreadyExistsException(CustomException):
    error_type = "VehicleAlreadyExistsException"
    reason = "vehicle with similar vehicle_id is already exists"
    location = ["vehicle_id"]
    status_code = status.HTTP_412_PRECONDITION_FAILED


class VehicleDoesNotExistException(CustomException):
    error_type = "VehicleDoesNotExistException"
    reason = "vehicle doesn't exist"
    location = ["vehicle_id"]
    status_code = status.HTTP_404_NOT_FOUND


class AuthServiceException(CustomException):
    error_type = "AuthServiceException"
    reason = "auth service exception"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class PaginationException(CustomException):
    error_type = "PaginationException"
    reason = "invalid pagination values(page or per_page are non-positive)"
    location = ["page", "per_page"]
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class NoDataToUpdateException(CustomException):
    error_type = "NoDataToUpdateException"
    reason = "no data to update"
    status_code = status.HTTP_412_PRECONDITION_FAILED


class InternalDatabaseException(CustomException):
    def __init__(self, reason: str | None = None):
        super().__init__()
        self.error_type = "InternalDatabaseException"
        if reason:
            self.reason = reason
        else:
            self.reason = "something goes wrong with database"

        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
