from src.app.user_management.application.commands.create_user_command import (
    CreateUserCommand,
)
from src.app.user_management.application.dtos.user_dtos import UserDTO
from src.app.user_management.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from src.app.user_management.domain.ports.driven.unit_of_work import UnitOfWork
from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserMobileNumber,
)
from src.app.user_management.application.ports.password_hasher import IPasswordHasher


class UserApplicationService:
    def __init__(self, passwd_hasher: IPasswordHasher):
        self.create_user_uc = CreateUserUseCase()
        self.password_hasher = passwd_hasher

    async def create_user(self, uow: UnitOfWork, create_user_command: CreateUserCommand) -> UserDTO:
        user_email = UserEmail(email=create_user_command.user_email)
        user_mobile_number = UserMobileNumber(mobile=create_user_command.user_mobile_number)
        hashed_password = self.password_hasher.hash_password(create_user_command.plain_password)
        async with uow:
            user = await self.create_user_uc.execute(
                uow.user_repo, user_mobile_number, user_email, hashed_password
            )
            await uow.commit()
        return UserDTO.from_entity(user)
