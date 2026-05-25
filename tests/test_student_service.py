from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from services.student_service import (
    get_students,
    create_student
)

from schemas import studentCreate

def test_get_students():
    mock_db = MagicMock()

    mock_db.query.return_value.all.return_value = [
        {"name": "John", "age": 20, "branch": "CSE"}
    ]

    result = get_students(mock_db)

    assert result[0]["name"] == "John"

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