from fastapi import Depends, APIRouter, HTTPException, status
from app.database import get_db
from .. import schemas, oauth2, models, utils
from ..results import student
from ..results.school import compare
from passlib.context import CryptContext
from  sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# creates an instance of the app in the main file
router = APIRouter(
    prefix="/results",
    tags=['Results']
)

# get results for student(single)
@router.get("/student", response_model=schemas.SingleStudentOut, status_code=status.HTTP_200_OK)
def getStudent(student_creds: schemas.SingleStudentIn, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # for some reason the user_id returns a dict
    id = user_id.id
    # check the user status
    check_status = utils.check_status(id, db)
    if not check_status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")
    
    year_completed = student_creds.year_completed
    school_registration = student_creds.school_registration_number
    exam_number = student_creds.student_exam_number
    exam_type = student_creds.student_level
    result = student.get_student(year_completed, school_registration, exam_number, exam_type)
    return result

# get total results for school
@router.get("/school", response_model=schemas.SchoolResults,status_code=status.HTTP_200_OK)
def getStudent(school: schemas.SchoolIn, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # for some reason the user_id returns a dict
    id = user_id.id
    # check the user status
    check_status = utils.check_status(id, db)
    if not check_status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")
    
    school_name = school.school_name
    school_level = school.school_level
    start = school.start_year
    end = school.end_year
    school_results = compare(school_name, school_level, start, end)
    return school_results