from uuid import UUID

from src.app.user_management.application.ports.auth_token_service import IAuthTokenService


class FakeTokenService(IAuthTokenService):
    def generate_token(self, user_id: UUID) -> str:
        return user_id.hex

    def verify_token(self, token: str) -> UUID:
        return UUID(token)
