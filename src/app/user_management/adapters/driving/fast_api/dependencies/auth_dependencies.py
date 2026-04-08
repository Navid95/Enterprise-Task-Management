from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer()


def get_authentication_service(request: Request):
    return request.app.container.get_auth_service()


def current_user(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer)
) -> UUID:
    return request.app.container.get_token_service().verify(credentials.credentials)
