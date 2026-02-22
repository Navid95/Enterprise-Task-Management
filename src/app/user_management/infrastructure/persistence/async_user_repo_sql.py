from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.app.user_management.infrastructure.persistence.models import UserModel
from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.domain.value_objects.user_info import (
    UserMobileNumber,
    UserEmail,
    UserId,
)
from src.app.user_management.domain.exceptions import UserNotFound


class AsyncSQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UserId) -> User:
        user_model: UserModel | None = await self._session.get(UserModel, user_id.id)

        if user_model is None:
            raise UserNotFound(user_id=user_id)
        return user_model.to_entity()

    async def save(self, user: User):
        user_model = await self._session.get(UserModel, user.id.id)

        if user_model is None:
            user_model = UserModel.from_entity(user)
            self._session.add(user_model)
        else:
            user_model.mobile_num = user.mobile_num.mobile
            user_model.email_address = user.email_address.email
            user_model.hashed_password = user.hashed_password.hashed_password

    async def get_by_mobile(self, mobile: UserMobileNumber) -> User:
        stm = select(UserModel).where(UserModel.mobile_num == mobile.mobile)
        user_model: UserModel | None = (await self._session.execute(stm)).scalar()
        if user_model is None:
            raise UserNotFound(user_mobile=mobile)
        else:
            return user_model.to_entity()

    async def get_by_email(self, email: UserEmail) -> User:
        stm = select(UserModel).where(UserModel.email_address == email.email)
        user_model: UserModel | None = (await self._session.execute(stm)).scalar()
        if user_model is None:
            raise UserNotFound(user_email=email)
        else:
            return user_model.to_entity()

    async def exists_by_email(self, email: UserEmail) -> bool:
        stm = select(
            select(UserModel).where(UserModel.email_address == email.email).exists()
        )
        result = await self._session.execute(stm)
        return result.scalar()

    async def exists_by_mobile(self, mobile: UserMobileNumber) -> bool:
        stm = select(
            select(UserModel).where(UserModel.mobile_num == mobile.mobile).exists()
        )
        result = await self._session.execute(stm)
        return result.scalar()
