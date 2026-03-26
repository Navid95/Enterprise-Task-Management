import pytest

from src.app.user_management.domain.value_objects.user_info import HashedPassword
from src.app.user_management.infrastructure.security.argon2_hasher import Argon2PasswordHasher


@pytest.fixture()
def hasher() -> Argon2PasswordHasher:
    return Argon2PasswordHasher()


def test_hash_returns_hashed_password_value_object(hasher):
    result = hasher.hash_password("secret")

    assert isinstance(result, HashedPassword)


def test_hash_does_not_store_plain_password(hasher):
    result = hasher.hash_password("secret")

    assert result.hashed_password != "secret"


def test_verify_returns_true_for_correct_password(hasher):
    hashed = hasher.hash_password("secret")

    assert hasher.verify("secret", hashed) is True


def test_verify_returns_false_for_wrong_password(hasher):
    hashed = hasher.hash_password("secret")

    assert hasher.verify("wrong", hashed) is False


def test_same_password_produces_different_hashes(hasher):
    first = hasher.hash_password("secret")
    second = hasher.hash_password("secret")

    assert first != second
