from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from app.database import SessionLocal, get_db
from .. import schemas, models


router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUSer(user: schemas.CreateUser, db: SessionLocal = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user