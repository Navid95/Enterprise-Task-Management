import pytest

from src.app.user_management.application.commands.login_command import LoginCommand
from src.app.user_management.application.exceptions.auth import AuthenticationError
from tests.conftest import _DEFAULT_USER_EMAIL, _DEFAULT_USER_PLAIN_PASSWORD


@pytest.mark.asyncio
async def test_login(authentication_service, seeded_user_repo):
    login_command = LoginCommand(
        user_email=_DEFAULT_USER_EMAIL.email,
        password=_DEFAULT_USER_PLAIN_PASSWORD
    )

    user_token = await authentication_service.login(login_command, seeded_user_repo)

    assert user_token is not None


@pytest.mark.asyncio
async def test_login_wrong_credentials(authentication_service, seeded_user_repo):
    login_command1 = LoginCommand(
        user_email="ABC" + _DEFAULT_USER_EMAIL.email,
        password=_DEFAULT_USER_PLAIN_PASSWORD
    )

    with pytest.raises(AuthenticationError):
        await authentication_service.login(login_command1, seeded_user_repo)

    login_command2 = LoginCommand(
        user_email=_DEFAULT_USER_EMAIL.email,
        password="abc" + _DEFAULT_USER_PLAIN_PASSWORD
    )

    with pytest.raises(AuthenticationError):
        await authentication_service.login(login_command2, seeded_user_repo)
