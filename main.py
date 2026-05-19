from database import engine
from models import Base
Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
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
    db.commit()
    return{
        "message":"New Student Created"
    }

@app.get("/students/")
def get_stud():
    db=SessionLocal()
    students=db.query(Student).all()
    return students