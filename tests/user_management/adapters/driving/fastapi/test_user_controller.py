import pytest
from fastapi.testclient import TestClient
from httpx import Response

from src.app.user_management.adapters.driving.fast_api.schemas.auth_schemas import LoginSchema
from src.app.user_management.adapters.driving.fast_api.schemas.user_schemas import CreateUserSchema
from src.app.user_management.application.dtos.auth_dto import TokenDTO
from src.app.user_management.application.dtos.user_dtos import UserDTO
from tests.conftest import _DEFAULT_USER_EMAIL, _DEFAULT_USER_MOBILE, _DEFAULT_USER_PLAIN_PASSWORD

pytestmark = [pytest.mark.integration]


@pytest.fixture()
def token(client, seeded_uow) -> TokenDTO:
    return TokenDTO.model_validate(
        client.post(
            url="/auth/login",
            json=LoginSchema(
                email=_DEFAULT_USER_EMAIL.email,
                password=_DEFAULT_USER_PLAIN_PASSWORD,
            ).model_dump(),
        ).json()
    )


def test_create_user(client: TestClient, token):
    response: Response = client.post(
        "/users/",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=CreateUserSchema(
            user_mobile_number="0912873465",
            user_email="test.user@company.com",
            plain_password="test user's password",
        ).model_dump(),
    )
    assert response.status_code == 201
    assert UserDTO.model_validate(response.json())
    assert UserDTO.model_validate(response.json()).id is not None


def test_create_user_duplicate(client: TestClient, token):
    response: Response = client.post(
        "/users/",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=CreateUserSchema(
            user_mobile_number=_DEFAULT_USER_MOBILE.mobile,
            user_email=_DEFAULT_USER_EMAIL.email,
            plain_password=_DEFAULT_USER_PLAIN_PASSWORD,
        ).model_dump(),
    )
    assert response.status_code == 409


def test_create_user_not_auth(client: TestClient):
    response: Response = client.post("/users/")

    assert response.status_code == 403


def test_create_user_wrong_auth(client: TestClient):
    response: Response = client.post("/users/", headers={"Authorization": "Bearer arbitrary token"})

    assert response.status_code == 401


def test_create_user_wrong_body(client, token):
    response: Response = client.post(
        "/users/",
        json=dict(),
        headers={"Authorization": token.token_type + " " + token.access_token},
    )

    assert response.status_code == 422
