from pydantic import BaseModel, Field

class studentCreate(BaseModel):

    name: str = Field(..., min_length=1)

    age: int = Field(..., gt=0)

    branch: str = Field(..., min_length=1)