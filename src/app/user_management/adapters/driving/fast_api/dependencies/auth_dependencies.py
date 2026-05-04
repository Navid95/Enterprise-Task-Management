from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED


class JWTBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


bearer = JWTBearer()


def get_authentication_service(request: Request):
    return request.app.container.get_auth_service()


def current_user(
        request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer)
) -> UUID:
    return request.app.container.get_token_service().verify_token(credentials.credentials)
