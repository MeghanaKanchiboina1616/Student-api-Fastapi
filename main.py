from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import studentCreate

from services.student_service import (
    create_student,
    get_students
)

app = FastAPI()


@app.post("/students/")
def create_stud(
    st: studentCreate,
    db: Session = Depends(get_db)
):

    return create_student(db, st)


@app.get("/students/")
def get_stud(
    db: Session = Depends(get_db)
):

    return get_students(db)