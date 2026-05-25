from unittest.mock import MagicMock

from database_test import get_session_maker
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from testcontainers.postgres import PostgresContainer
from utils.container_utils import get_postgres_container

from schemas import studentCreate
from services.student_service import create_student, get_students


@pytest.fixture(scope="module")
def test_session():
    try:
        with get_postgres_container() as container:
            url = container.get_connection_url()
            test_session = get_session_maker(url)
            yield test_session
    finally:
        test_session.close()

def test_get_students(test_session):
    try:
        # Insert John
        result = get_students(test_session)
        assert result[0]["name"] == "John"
    finally:
        # Erase John

def test_create_student():
    mock_db = MagicMock()

    student_data = studentCreate(
        name="John",
        age=20,
        branch="CSE"
    )

    result = create_student(mock_db, student_data)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.name == "John"

def test_create_duplicate_student():
    mock_db = MagicMock()

    mock_db.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=None
    )

    student_data = studentCreate(
        name="John",
        age=20,
        branch="CSE"
    )

    try:
        create_student(mock_db, student_data)

    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Student already exists"

    mock_db.rollback.assert_called_once()
