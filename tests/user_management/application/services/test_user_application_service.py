from src.app.user_management.application.commands.create_user_command import (
    CreateUserCommand,
)
from src.app.user_management.application.dtos.user_dtos import UserDTO


def test_create_user(user_application_service):
    command = CreateUserCommand(
        user_mobile_number="0123456789",
        user_email="johnDoe@example.com",
        plain_password="JohnsPlainPassword",
    )

    user_dto: UserDTO = user_application_service.create_user(command)

    assert user_dto.id is not None
    assert user_dto.mobile_num == command.user_mobile_number
    assert user_dto.email_address == command.user_email
