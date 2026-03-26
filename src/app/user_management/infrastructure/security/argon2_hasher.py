from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from src.app.user_management.application.ports.password_hasher import IPasswordHasher
from src.app.user_management.domain.value_objects.user_info import HashedPassword


class Argon2PasswordHasher(IPasswordHasher):

    def __init__(self):
        self.hasher = PasswordHasher()

    def hash_password(self, plain_password: str) -> HashedPassword:
        return HashedPassword(hashed_password=self.hasher.hash(plain_password))

    def verify(self, plain_password: str, hashed_password: HashedPassword) -> bool:
        try:
            return self.hasher.verify(hashed_password.hashed_password, plain_password)
        except VerifyMismatchError:
            return False
