import pytest
from database_test import get_sessionmaker
from fastapi.testclient import TestClient

from database import get_db
from main import app
from tests.database_test import (
    override_get_db,
    #stop_container
)
from utils.container_utils import get_postgres_container

# Override FastAPI dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():

    with TestClient(app) as c:
        yield c

    #stop_container()

@pytest.fixture(scope="session")
def postgres_container():
    with get_postgres_container() as container:
        yield container

@pytest.fixture()
def test_session(postgres_container):
    try:
        test_session = None
        url = postgres_container.get_connection_url()
        session_maker = get_sessionmaker(url)
        test_session = session_maker()
        yield test_session
    finally:
        if test_session:
            test_session.close()
