from contextlib import asynccontextmanager
from fastapi import FastAPI
from thoughts.router import router as thoughtsRouter
from thoughts.models import ThoughtModel
from models import db

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not db.table_exists('thoughts'):
        db.create_tables([ThoughtModel])
    yield  
    

app.router.lifespan_context = lifespan
app.include_router(thoughtsRouter, prefix="/thoughts")
