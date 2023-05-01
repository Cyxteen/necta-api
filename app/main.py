from fastapi import Depends, FastAPI
from .database import engine, get_db
from . import models
from .routers import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.routers)
