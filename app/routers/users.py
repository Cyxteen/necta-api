from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from app.database import SessionLocal, get_db
from .. import schemas, models, utils
from passlib.context import CryptContext
from  sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


routers = APIRouter()

@routers.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUSer(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@routers.get("/users", response_model= list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@routers.put("/users", response_model= list[schemas.UserOut])
def update_user(db: Session = Depends(get_db)):
    pass