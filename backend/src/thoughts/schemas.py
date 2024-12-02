from pydantic import BaseModel
from datetime import datetime

class ThoughtCreate(BaseModel):
    user_id: int
    text: str
    datetime: datetime

class ThoughtResponse(BaseModel):
    id: int
    user_id: int
    text: str
    datetime: datetime
