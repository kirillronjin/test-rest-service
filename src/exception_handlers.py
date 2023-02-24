from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from exceptions import (
    AuthServiceException,
    InternalDatabaseException,
    NoDataToUpdateException,
    NoTokenProvidedException,
    PaginationException,
    VehicleAlreadyExistsException,
    VehicleDoesNotExistException,
)


async def exception_with_location_handler(request, exception) -> ORJSONResponse:  # pylint: disable=W0613
    detail = {
        "loc": exception.location,
        "msg": exception.reason,
        "type": exception.error_type,
    }
    return ORJSONResponse(
        status_code=exception.status_code,
        content={"detail": [detail]},
    )


async def exception_without_location_handler(request, exception) -> ORJSONResponse:  # pylint: disable=W0613
    detail = {
        "msg": exception.reason,
        "type": exception.error_type,
    }
    return ORJSONResponse(
        status_code=exception.status_code,
        content={"detail": [detail]},
    )


async def validation_exception_handler(request, exception: RequestValidationError):
    details = exception.errors()
    modified_details = []
    for error in details:
        modified_details.append(
            {
                "loc": [error["loc"][1]],
                "msg": error["msg"],
                "type": error["type"],
            }
        )
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


handlers = {
    RequestValidationError: validation_exception_handler,
    VehicleDoesNotExistException: exception_with_location_handler,
    PaginationException: exception_with_location_handler,
    VehicleAlreadyExistsException: exception_with_location_handler,
    NoTokenProvidedException: exception_without_location_handler,
    InternalDatabaseException: exception_without_location_handler,
    NoDataToUpdateException: exception_without_location_handler,
    AuthServiceException: exception_without_location_handler,
}
