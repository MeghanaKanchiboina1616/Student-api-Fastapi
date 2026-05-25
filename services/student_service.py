from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from models import Student


def create_student(db, st):

    new_stud = Student(
        name=st.name,
        age=st.age,
        branch=st.branch
    )

    db.add(new_stud)

    try:
        db.commit()
        db.refresh(new_stud)

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Student already exists"
        )

    return new_stud


def get_students(db):

    return db.query(Student).all()
