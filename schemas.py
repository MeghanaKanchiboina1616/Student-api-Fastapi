from pydantic import BaseModel
class studentCreate(BaseModel):
    name:str
    age:int
    branch:str

