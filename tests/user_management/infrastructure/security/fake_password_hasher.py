from src.app.user_management.application.ports.password_hasher import IPasswordHasher
from src.app.user_management.domain.value_objects.user_info import HashedPassword


class FakePasswordHasher(IPasswordHasher):
    def verify(self, plain_password: str, hashed_password: HashedPassword) -> bool:
        return self.hash_password(plain_password) == hashed_password

    def hash_password(self, plain_password: str) -> HashedPassword | None:
        return HashedPassword(hashed_password=plain_password.upper())
