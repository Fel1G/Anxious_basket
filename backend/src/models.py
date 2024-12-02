import os
from peewee import Model
from playhouse.postgres_ext import PostgresqlExtDatabase
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
db = PostgresqlExtDatabase(DATABASE_URL)


class BaseModel(Model):
    """Базовая модель для всех таблиц."""
    class Meta:
        database = db