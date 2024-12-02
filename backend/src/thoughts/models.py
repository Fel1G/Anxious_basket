from models import BaseModel
from peewee import IntegerField, TextField, DateTimeField, AutoField
from datetime import datetime


class ThoughtModel(BaseModel):
    id = AutoField()
    user_id = IntegerField()
    text = TextField()
    datetime = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'thoughts'