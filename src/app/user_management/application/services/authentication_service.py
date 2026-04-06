from src.app.user_management.application.commands.login_command import LoginCommand
from src.app.user_management.application.dtos.auth_dto import TokenDTO
from src.app.user_management.application.exceptions.auth import AuthenticationError
from src.app.user_management.application.ports.auth_token_service import IAuthTokenService
from src.app.user_management.application.ports.password_hasher import IPasswordHasher
from src.app.user_management.domain.exceptions import UserNotFound
from src.app.user_management.domain.ports.driven.unit_of_work import UnitOfWork
from src.app.user_management.domain.value_objects.user_info import UserEmail


class AuthenticationService:
    def __init__(self, token_service: IAuthTokenService, passwd_hasher: IPasswordHasher):
        self._token_service = token_service
        self._password_hasher = passwd_hasher

    async def login(self, login_command: LoginCommand, uow: UnitOfWork) -> TokenDTO:
        user_email = UserEmail(email=login_command.email)
        try:
            async with uow:
                user = await uow.user_repo.get_by_email(email=user_email)
        except UserNotFound:
            raise AuthenticationError(reason="Invalid_Email")

        if self._password_hasher.verify(login_command.password, user.hashed_password):
            token = self._token_service.generate_token(user.id.id)
            return TokenDTO(access_token=token)
        else:
            raise AuthenticationError(reason="Invalid_Password")
