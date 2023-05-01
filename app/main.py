from fastapi import Depends, FastAPI
from .database import engine, get_db
from . import models
from  sqlalchemy.orm import Session
from .routers import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
