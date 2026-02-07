from fastapi.exceptions import HTTPException
from src.app.core.exceptions import DomainError
from src.app.user_management.domain.exceptions import (
    NotTeamManagerError,
    MemberAlreadyInTeamError,
    MemberNotInTeamError,
    DuplicateUserInformation,
    UserNotFound,
)


class APIException(HTTPException):
    def __init__(
        self,
        status_code: int = 500,
        error_type: str = "",
        message: str = "",
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "status_code": status_code,
                "error_type": error_type,
                "message": message,
            },
        )


_HTTP_ERRORS: dict[int, str] = {
    # 4xx – Client errors
    400: "Bad request",
    401: "Authentication required",
    403: "You do not have permission to perform this action",
    404: "Resource not found",
    409: "Request conflicts with the current state of the resource",
    422: "Request is semantically invalid",
    # 5xx – Server / infrastructure errors
    500: "Internal server error",
    502: "Bad gateway",
    503: "Service temporarily unavailable",
}

_DOMAIN_TO_HTTP: dict[type(DomainError), int] = {
    NotTeamManagerError: 409,
    MemberAlreadyInTeamError: 409,
    MemberNotInTeamError: 409,
    DuplicateUserInformation: 409,
    UserNotFound: 404,
}


def exc_mapper(exc: DomainError):
    status_code = _DOMAIN_TO_HTTP.get(type(exc), 500)
    return APIException(
        status_code=status_code,
        error_type=str(exc.__class__.__name__),
        message=_HTTP_ERRORS.get(status_code),
    )
