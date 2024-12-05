from pydantic import BaseModel
from datetime import datetime

class Thought(BaseModel):
    user_id: int
    text: str
    datetime: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "text": "This is my anxious thought",
                    "datetime": '2024-12-05T12:34:56' 
                }
            ]
        }
    }

class ThoughtResponse(BaseModel):
    id: int
    user_id: int
    text: str
    datetime: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'id': 1,
                    'user_id': 1,
                    'text': 'This is my example anxious response thought',
                    'datetime': '2024-12-05T12:34:56' 
                }
            ]
        }
    }