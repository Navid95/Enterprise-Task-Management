import pytest
from fastapi.testclient import TestClient
from httpx import Response

from src.app.user_management.adapters.driving.fast_api.schemas.auth_schemas import LoginSchema
from src.app.user_management.application.dtos.auth_dto import TokenDTO
from tests.conftest import _DEFAULT_USER_EMAIL, _DEFAULT_USER_PLAIN_PASSWORD

pytestmark = [pytest.mark.integration]


def test_login(client: TestClient, seeded_uow):
    response: Response = client.post(
        url="/auth/login",
        json=LoginSchema(
            email=_DEFAULT_USER_EMAIL.email,
            password=_DEFAULT_USER_PLAIN_PASSWORD,
        ).model_dump(),
    )

    assert response.status_code == 200
    assert TokenDTO.model_validate(response.json())


def test_login_wrong_password(client: TestClient, seeded_uow):
    response: Response = client.post(
        url="/auth/login",
        json=LoginSchema(
            email=_DEFAULT_USER_EMAIL.email,
            password=_DEFAULT_USER_PLAIN_PASSWORD + "wrong password",
        ).model_dump(),
    )
    assert response.status_code == 401


def test_login_wrong_email(client: TestClient, seeded_uow):
    response: Response = client.post(
        url="/auth/login",
        json=LoginSchema(
            email="wrongemail@company.com",
            password=_DEFAULT_USER_PLAIN_PASSWORD,
        ).model_dump(),
    )

    assert response.status_code == 401


def test_login_missing_fields(client: TestClient):
    response = client.post(url="/auth/login", json={})

    assert response.status_code == 422
