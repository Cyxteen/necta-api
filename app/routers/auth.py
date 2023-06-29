from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db

# the tags argument is to be used in the API documentations
router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/verify-email", status_code=status.HTTP_202_ACCEPTED)
async def validateUserEmail(request: schemas.EmailVerification, db: Session = Depends(get_db)):
    email = request.email
    verification_code = request.verification_code
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if verification_code != user.activation_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Code")
    
    user.activation_status = 1

    db.commit()
    
    return {"message": "Email verified"}

# login path, the response models checks if the format matches the ones that are described in the schemas table
@router.post("/login", response_model=schemas.Token)
async def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    id = user.id
    # check the user status
    check_status = utils.check_status(id, db)
    # print(check_status)
    if not check_status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")
    # checks if the user is present in the database
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid username or password")
    verified = utils.verify_password(user_creds.password, user.password)
    # if the user is present, this checks the password if its also correct
    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid username or password")
    
    # creates Token with the user_id
    access_token = oauth2.create_token(data = {"user_id": user.id})
    # returns the Token
    return {"access_token": access_token, "token_type": "bearer"}