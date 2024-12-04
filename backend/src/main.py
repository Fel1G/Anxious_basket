from contextlib import asynccontextmanager
from fastapi import FastAPI
from thoughts.router import router as thoughtsRouter
from thoughts.models import ThoughtModel
from models import db

app = FastAPI(title="Anxious basket",
              description="API сервиса для применения техники \"Worry Time\"",
              version="1.0.0",
              openapi_tags=[
                  {"name": "thoughts", "description": "Операции с мыслями"}
              ]
              )

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not db.table_exists('thoughts'):
        db.create_tables([ThoughtModel])
    yield  
    

app.router.lifespan_context = lifespan
app.include_router(thoughtsRouter, prefix="/thoughts", tags=["thoughts"])
