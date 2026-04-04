from src.app.user_management.application.commands.login_command import LoginCommand
from src.app.user_management.application.exceptions.auth import AuthenticationError
from src.app.user_management.application.ports.auth_token_service import IAuthTokenService
from src.app.user_management.application.ports.password_hasher import IPasswordHasher
from src.app.user_management.domain.exceptions import UserNotFound
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.domain.value_objects.user_info import UserEmail


class AuthenticationService:
    def __init__(self, token_service: IAuthTokenService, passwd_hasher: IPasswordHasher):
        self._token_service = token_service
        self._password_hasher = passwd_hasher

    async def login(self, login_command: LoginCommand, user_repo: UserRepository) -> str:
        user_email = UserEmail(email=login_command.user_email)
        try:
            user = await user_repo.get_by_email(email=user_email)
        except UserNotFound:
            raise AuthenticationError(reason="Invalid_Email")

        if self._password_hasher.verify(login_command.password, user.hashed_password):
            token = self._token_service.generate_token(user.id.id)
            return token
        else:
            raise AuthenticationError(reason="Invalid_Password")
