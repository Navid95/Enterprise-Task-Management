from src.app.core.settings import Settings
from src.app.infrastructure.persistence.base import BaseModel
from src.app.infrastructure.persistence.db.session import (
    close_engine,
    get_engine,
    init_engine,
)


async def create_tables() -> None:
    setting = Settings()
    init_engine(setting)
    assert get_engine() is not None

    async with get_engine().begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    await close_engine()
