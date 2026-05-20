from database import engine
from models import Base
from sqlalchemy.exc import IntegrityError
Base.metadata.create_all(bind=engine)

from fastapi import FastAPI,HTTPException
from schemas import studentCreate
from database import SessionLocal
from models import Student

app=FastAPI()
@app.post("/students/")
def create_stud(st:studentCreate):
    db=SessionLocal()
    new_stud=Student(
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

@app.get("/students/")
def get_stud():
    db=SessionLocal()
    students=db.query(Student).all()
    return students