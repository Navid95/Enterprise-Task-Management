from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.exceptions import (
    DuplicateUserInformation,
)
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.domain.value_objects.user_info import (
    HashedPassword,
    UserEmail,
    UserId,
    UserMobileNumber,
)


class CreateUserUseCase:
    async def execute(
        self,
        user_repo: UserRepository,
        user_mobile_number: UserMobileNumber,
        user_email: UserEmail,
        hashed_password: HashedPassword,
    ) -> User:
        if await user_repo.exists_by_mobile(user_mobile_number):
            raise DuplicateUserInformation(user_mobile=user_mobile_number)
        if await user_repo.exists_by_email(user_email):
            raise DuplicateUserInformation(user_email=user_email)

        user = User(
            id=UserId(),
            mobile_num=user_mobile_number,
            email_address=user_email,
            hashed_password=hashed_password,
        )

        await user_repo.save(user)
        return user
