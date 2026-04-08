from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str

    # TOKEN
    ENCRYPTION_KEY: str
    EXPIRY_DURATION: int

    # ADMIN USER
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_file_required=False,
        extra="ignore",
    )


settings = Settings()
