from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from exceptions import (
    EntitySubordinationException,
    InternalDatabaseException,
    PaginationException,
    EntityAlreadyExistException,
    EntityNotFoundException,
    DatabaseException
)


async def exception_handler(request, exception) -> ORJSONResponse:  # pylint: disable=W0613
    content = {
        "code": exception.status_code,
        "message": exception.reason,
        "details": exception.details
    }
    return ORJSONResponse(
        status_code=exception.status_code,
        content=content,
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
    EntityNotFoundException: exception_handler,
    PaginationException: exception_handler,
    EntityAlreadyExistException: exception_handler,
    InternalDatabaseException: exception_handler,
    DatabaseException: exception_handler,
    EntitySubordinationException: exception_handler,
}
