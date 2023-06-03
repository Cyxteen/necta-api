from fastapi import Depends, APIRouter, HTTPException, status
from app.database import get_db
from .. import schemas, oauth2, models, utils
from passlib.context import CryptContext
from  sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# creates an instance of the app in the main file
router = APIRouter(
    prefix="/results",
    tags=['Results']
)

# get results for school
@router.get("/single-student", status_code=status.HTTP_200_OK)
def getStudent(user: schemas.GetResult, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
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