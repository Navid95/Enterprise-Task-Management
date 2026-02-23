import asyncio
import src.app.user_management.infrastructure.persistence.models
from src.app.infrastructure.persistence.db.init_db import create_tables

if __name__ == "__main__":
    asyncio.run(create_tables())
