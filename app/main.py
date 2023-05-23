from fastapi import Depends, FastAPI
from .database import engine
from . import models
from .routers import users, auth
# created the database tables before alembic installation
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)