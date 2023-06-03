from fastapi import Depends, APIRouter, HTTPException, status
from app.database import get_db
from .. import schemas, oauth2, models, utils
from ..results import student
from passlib.context import CryptContext
from  sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# creates an instance of the app in the main file
router = APIRouter(
    prefix="/results",
    tags=['Results']
)

# get results for school
@router.post("/student", response_model=schemas.SingleStudentOut, status_code=status.HTTP_200_OK)
def getStudent(user: schemas.SingleStudentIn, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # for some reason the user_id returns a dict
    id = user_id.id
    # check the user status
    check_status = utils.check_status(id, db)
    if not check_status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")
    
    year_completed = user.year_completed
    school_registration = user.school_registration_number
    exam_number = user.student_exam_number
    exam_type = user.student_level
    result = student.get_student(year_completed, school_registration, exam_number, exam_type)
    return result