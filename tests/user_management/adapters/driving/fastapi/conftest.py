import pytest
from fastapi.testclient import TestClient

from src.app.core.settings import Settings
from src.app.main import create_app
from tests.conftest import TEST_DIR

settings = Settings(_env_file=f"{TEST_DIR}/.env")


@pytest.fixture(scope="session")
def client(engine):
    with TestClient(create_app(settings)) as test_client:
        yield test_client
