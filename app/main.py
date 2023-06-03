from fastapi import FastAPI
from .routers import users, auth, results
from fastapi.middleware.cors import CORSMiddleware
# created the database tables before alembic installation
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(results.router)