from src.app.infrastructure.persistence.base import BaseModel
from src.app.infrastructure.persistence.db.session import (
    close_engine,
    get_engine,
    init_engine,
)


async def create_tables() -> None:
    init_engine()
    assert get_engine() is not None

    async with get_engine().begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    await close_engine()
