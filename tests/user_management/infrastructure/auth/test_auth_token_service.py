
from uuid import UUID, uuid4
import pytest

from src.app.user_management.application.exceptions.auth import AuthenticationError
from src.app.user_management.application.ports.auth_token_service import IAuthTokenService
from src.app.user_management.infrastructure.auth.jwt_token_service import JWTTokenService

_TEST_UUID: UUID = uuid4()


@pytest.fixture(scope="module")
def auth_token_service() -> IAuthTokenService:
    return JWTTokenService(enc_key="test_key", expiry_minutes=1)


@pytest.fixture()
def auth_token_service_expired() -> IAuthTokenService:
    return JWTTokenService(enc_key="test_key", expiry_minutes=0)


def test_generate_token(auth_token_service: IAuthTokenService):
    token = auth_token_service.generate_token(user_id=_TEST_UUID)
    assert isinstance(token, str)


def test_verify_token(auth_token_service: IAuthTokenService):
    token = auth_token_service.generate_token(user_id=_TEST_UUID)
    user_id = auth_token_service.verify_token(token)
    assert user_id == _TEST_UUID


def test_verify_token_expired(auth_token_service_expired: IAuthTokenService):
    token = auth_token_service_expired.generate_token(user_id=_TEST_UUID)
    with pytest.raises(AuthenticationError):
        auth_token_service_expired.verify_token(token)

