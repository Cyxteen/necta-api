from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from app.database import get_db
from .. import schemas, models, utils
from passlib.context import CryptContext
from  sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# creates an instance of the app in the main file
router = APIRouter(
    prefix="/users",
    tags=['users']
)

# route for creating a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUSer(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # hashes the password and updates the new hashed_password to the user dictionary
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
# test route for getting all users
@router.get("/", response_model= list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# update user with id
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")
    return user
