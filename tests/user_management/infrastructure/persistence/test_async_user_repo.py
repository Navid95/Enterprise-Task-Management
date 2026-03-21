import pytest

from sqlalchemy.exc import IntegrityError

from src.app.user_management.domain.value_objects.user_info import (
    UserId,
    UserEmail,
    UserMobileNumber,
)
from src.app.user_management.domain.exceptions import UserNotFound
from src.app.user_management.infrastructure.persistence.async_user_repo_sql import (
    AsyncSQLUserRepository,
)
from src.app.user_management.domain.entities.users import User
from tests.conftest import (
    _DEFAULT_USER_EMAIL,
    _DEFAULT_USER_MOBILE,
    _DEFAULT_USER_HASHED_PASSWORD,
)


@pytest.mark.asyncio
async def test_save_success(user_repo):
    await user_repo.save(
        User(
            id=UserId(),
            mobile_num=_DEFAULT_USER_MOBILE,
            email_address=_DEFAULT_USER_EMAIL,
            hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
        )
    )


@pytest.mark.asyncio
async def test_save_fail_duplicate_mobile(seeded_user_repo: AsyncSQLUserRepository):
    with pytest.raises(IntegrityError) as e:
        await seeded_user_repo.save(
            User(
                id=UserId(),
                mobile_num=_DEFAULT_USER_MOBILE,
                email_address=UserEmail(email="some@persistance.com"),
                hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
            )
        )
        await seeded_user_repo._session.flush()


@pytest.mark.asyncio
async def test_save_fail_duplicate_email(seeded_user_repo: AsyncSQLUserRepository):
    with pytest.raises(IntegrityError) as e:
        await seeded_user_repo.save(
            User(
                id=UserId(),
                mobile_num=UserMobileNumber(mobile="123456789012"),
                email_address=_DEFAULT_USER_EMAIL,
                hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
            )
        )
        await seeded_user_repo._session.flush()


@pytest.mark.asyncio
async def test_get_by_mobile_success(seeded_user_repo: AsyncSQLUserRepository):
    user = await seeded_user_repo.get_by_mobile(_DEFAULT_USER_MOBILE)
    assert user is not None
    assert user.mobile_num == _DEFAULT_USER_MOBILE


@pytest.mark.asyncio
async def test_get_by_mobile_fail_not_found(seeded_user_repo: AsyncSQLUserRepository):
    mobile_num = UserMobileNumber(mobile="00000000000")
    with pytest.raises(UserNotFound) as e:
        user = await seeded_user_repo.get_by_mobile(mobile_num)
    assert e.value.context.get("user_mobile") == mobile_num


@pytest.mark.asyncio
async def test_get_by_email_success(seeded_user_repo: AsyncSQLUserRepository):
    user = await seeded_user_repo.get_by_email(_DEFAULT_USER_EMAIL)
    assert user is not None
    assert user.email_address == _DEFAULT_USER_EMAIL


@pytest.mark.asyncio
async def test_get_by_email_fail_not_found(seeded_user_repo: AsyncSQLUserRepository):
    email_address = UserEmail(email="notfound@company.com")
    with pytest.raises(UserNotFound) as e:
        user = await seeded_user_repo.get_by_email(email_address)
    assert e.value.context.get("user_email") == email_address


@pytest.mark.asyncio
async def test_exists_by_email_success(seeded_user_repo: AsyncSQLUserRepository):
    result = await seeded_user_repo.exists_by_email(_DEFAULT_USER_EMAIL)
    assert result is True


@pytest.mark.asyncio
async def test_exists_by_email_fail(seeded_user_repo: AsyncSQLUserRepository):
    email_address = UserEmail(email="notfound@company.com")
    result = await seeded_user_repo.exists_by_email(email_address)
    assert result is False


@pytest.mark.asyncio
async def test_exists_by_mobile_success(seeded_user_repo: AsyncSQLUserRepository):
    result = await seeded_user_repo.exists_by_mobile(_DEFAULT_USER_MOBILE)
    assert result is True


@pytest.mark.asyncio
async def test_exists_by_mobile_fail(seeded_user_repo: AsyncSQLUserRepository):
    mobile_num = UserMobileNumber(mobile="00000000000")
    result = await seeded_user_repo.exists_by_mobile(mobile_num)
    assert result is False
