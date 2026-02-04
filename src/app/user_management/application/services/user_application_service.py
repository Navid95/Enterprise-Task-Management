from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserMobileNumber,
    HashedPassword,
)
from src.app.user_management.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from src.app.user_management.application.commands.create_user_command import (
    CreateUserCommand,
)
from src.app.user_management.application.dtos.user_dtos import UserDTO


class UserApplicationService:
    def __init__(self, create_user_uc: CreateUserUseCase):
        self.create_user_uc = create_user_uc

    def create_user(self, create_user_command: CreateUserCommand) -> UserDTO:
        user_email = UserEmail(email=create_user_command.user_email)
        user_mobile_number = UserMobileNumber(
            mobile=create_user_command.user_mobile_number
        )
        # TODO: hash port needed, for now plain password is used
        hashed_password = HashedPassword(
            hashed_password=create_user_command.plain_password
        )
        user = self.create_user_uc.execute(
            user_mobile_number, user_email, hashed_password
        )
        return UserDTO.from_entity(user)
