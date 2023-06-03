from fastapi import Depends, APIRouter, HTTPException, status
from app.database import get_db
from .. import schemas, models, utils, oauth2
from passlib.context import CryptContext
from  sqlalchemy.orm import Session
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# creates an instance of the app in the main file
router = APIRouter(
    prefix="/user",
    tags=['User']
)

# route for creating a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUSer(user: schemas.CreateUser, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # for some reason the user_id returns a dict
    id = user_id.id
    # check if the email already exists in the database
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    # hashes the password and updates the new hashed_password to the user dictionary
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    # generate email acivation codes
    activation_code = secrets.token_urlsafe(16)

    new_user = models.User(**user.dict(), activation_code=activation_code)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# route for getting a user
@router.get("/profile", response_model=schemas.UserProfile)
def get_user(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # for some reason the user_id returns a dict
    id = user_id.id
    user = db.query(models.User).filter(models.User.id == id).first()
    # check the user status
    check_status = utils.check_status(id, db)
    # print(check_status)
    if not check_status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


# update route for updating a user
@router.patch("/profile", response_model=schemas.UserProfile, status_code=status.HTTP_200_OK)
def update_user(user: schemas.UpdateUser, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # for some reason the user_id returns a dict
    id = user_id.id
    user_update = db.query(models.User).filter(models.User.id == id)
    # returns the first user
    db_user = user_update.first()
    # checks if the user is present
    # check the user status
    check_status = utils.check_status(id, db)
    # print(check_status)
    if not check_status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")
    if db_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    # if present updates the users row and commits the changes
    user_update.update(user.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    # returns the updated user
    updated_user = user_update.first()
    return updated_user