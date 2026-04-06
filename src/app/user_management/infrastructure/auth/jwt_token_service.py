from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError

from src.app.user_management.application.exceptions.auth import AuthenticationError
from src.app.user_management.application.ports.auth_token_service import IAuthTokenService


class JWTTokenService(IAuthTokenService):
    def __init__(self, enc_key: str, expiry_minutes: int):
        self._enc_key = enc_key
        self._expiry_minutes = expiry_minutes

    def generate_token(self, user_id: UUID) -> str:
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(minutes=self._expiry_minutes)
        token = jwt.encode(
            payload={"sub": user_id.hex, "iat": iat.timestamp(), "exp": exp.timestamp()},
            key=self._enc_key,
            algorithm="HS256",
        )
        return token

    def verify_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(key=self._enc_key, jwt=token, algorithms=["HS256"])
        except InvalidTokenError:
            raise AuthenticationError(reason="Invalid Token")

        try:
            user_id = UUID(payload.get("sub"))
        except Exception:
            raise AuthenticationError(reason="Invalid user_id format")

        return user_id
