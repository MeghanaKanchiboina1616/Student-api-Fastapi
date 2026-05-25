import pytest

from fastapi.testclient import TestClient

from main import app
from database import get_db

from tests.database_test import (
    override_get_db,
    #stop_container
)

# Override FastAPI dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():

    with TestClient(app) as c:
        yield c

    #stop_container()