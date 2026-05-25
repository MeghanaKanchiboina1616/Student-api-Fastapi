from unittest.mock import MagicMock

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from models import Student
from schemas import studentCreate
from services.student_service import create_student, get_students


def test_get_students(test_session):
    # SETUP
    # PROCESS AND ASSERT
    # CLEANUP
    try:
        student = Student(
            name="John",
            age=18,
            branch="CSM"
        )
        test_session.add(student)
        test_session.flush()
        result = get_students(test_session)
        assert len(result) == 1
        assert result[0].name == "John"
        assert result[0].age == 18
        assert result[0].branch == "CSM"
    except Exception as E:
        raise Exception(f"Failed to test get students: {E}")


def test_create_student(test_session):
    student_data = studentCreate(
        name="Mia",
        age=22,
        branch="ECE"
    )

    result = create_student(test_session, student_data)

    assert result.name == "Mia"
    assert result.age == 22
    assert result.branch == "ECE"


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
