from unittest.mock import MagicMock

import pytest
from database_test import get_sessionmaker
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from testcontainers.postgres import PostgresContainer

from models import Student
from schemas import studentCreate
from services.student_service import create_student, get_students
from utils.container_utils import get_postgres_container


@pytest.fixture(scope="module")
def postgres_container():
    with get_postgres_container() as container:
        yield container

@pytest.fixture(scope="module")
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

def test_get_students(test_session):
    try:
        student = Student(
            name="John",
            age=18,
            branch="CSM"
        )
        test_session.add(student)
        test_session.flush()
        result = get_students(test_session)
        print(result)
        assert result[0].name == "John"
        test_session.reset()

    finally:
        # We don't have to Erase John, Since session is not Commited
        pass
# def test_create_student():
#     mock_db = MagicMock()

#     student_data = studentCreate(
#         name="John",
#         age=20,
#         branch="CSE"
#     )

#     result = create_student(mock_db, student_data)

#     mock_db.add.assert_called_once()
#     mock_db.commit.assert_called_once()
#     mock_db.refresh.assert_called_once()

#     assert result.name == "John"

# def test_create_duplicate_student():
#     mock_db = MagicMock()

#     mock_db.commit.side_effect = IntegrityError(
#         statement=None,
#         params=None,
#         orig=None
#     )

#     student_data = studentCreate(
#         name="John",
#         age=20,
#         branch="CSE"
#     )

#     try:
#         create_student(mock_db, student_data)

#     except HTTPException as e:
#         assert e.status_code == 400
#         assert e.detail == "Student already exists"

#     mock_db.rollback.assert_called_once()
