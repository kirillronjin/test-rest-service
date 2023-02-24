from exceptions import CustomException


def generate_additional_responses(exceptions: list[CustomException]) -> dict:
    responses_schemas = {}
    for exp in exceptions:
        detail = {
            "loc": [
                "location",
            ],
            "msg": exp.reason,
            "type": exp.error_type,
        }
        response = {
            exp.status_code: {
                "description": "Unprocessable Entity",
                "content": {
                    "application/json": {"example": {"detail": [detail]}},
                },
            }
        }

        responses_schemas.update(response)

    return responses_schemas
