import json
from fastapi import Depends, APIRouter, HTTPException, status
from app.database import get_db
from app import schemas, oauth2, utils, models
from app.results import student
from app.results.school import compare
from passlib.context import CryptContext
from  sqlalchemy.orm import Session
import datetime

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

    # Check if the desired data is available in the cache
    cache_key = f"student_{school_registration}_{exam_number}_{exam_type}_{year_completed}"
    cached_data = db.query(models.CachedData).filter_by(cache_key=cache_key).first()

    if cached_data:
        # Return the data from the cache
        return json.loads(cached_data.data)
    
    result = student.get_student(year_completed, school_registration, exam_number, exam_type)

    new_cached_data = models.CachedData(cache_key=cache_key, data=json.dumps(result))
    db.add(new_cached_data)
    db.commit()

    return result

# get total results for school in a year
@router.get("/school", response_model=schemas.SchoolResults,status_code=status.HTTP_200_OK)
def getSchool(school: schemas.SchoolIn, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
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

    if start > end:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error in format")
    
    # Check if the desired data is available in the cache
    cache_key = f"school_{school_name}_{school_level}_{start}_{end}"
    cached_data = db.query(models.CachedData).filter_by(cache_key=cache_key).first()

    if cached_data:
        # Return the data from the cache
        return json.loads(cached_data.data)

    school_results = compare(school_name, school_level, start, end)

    # Store the retrieved data in the cache table
    new_cached_data = models.CachedData(cache_key=cache_key, data=json.dumps(school_results))
    db.add(new_cached_data)
    db.commit()

    return school_results

# compare school(two) results
@router.get("/compare", response_model=schemas.CombinedSchoolResults, status_code=status.HTTP_200_OK)
def getSchools(schools: schemas.SchoolsIn, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    id = user_id.id
    # check the user status if it's activated
    check_status = utils.check_status(id, db)
    if not check_status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized")

    school_one_name = schools.school_one_name
    school_two_name = schools.school_two_name
    level = schools.level
    year = int(schools.year)
    default_year = 2022

    if year == 0 or year > 9:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="an error occured: the format provided is not correct")
    
    start_year = default_year - year
    end_year = default_year

    # print(year)
    # Check if the desired data is available in the cache
    cache_key = f"schools_{school_one_name}_{school_two_name}_{level}_{year}"
    cached_data = db.query(models.CachedData).filter_by(cache_key=cache_key).first()

    if cached_data:
        # Return the data from the cache
        return json.loads(cached_data.data)

    school_one_results = compare(school_one_name, level, start_year, end_year)
    school_two_results = compare(school_two_name, level, start_year, end_year)

    # Combine the results for both schools
    combined_results = {
        school_one_name: school_one_results,
        school_two_name: school_two_results
    }

    # Store the retrieved data in the cache table
    new_cached_data = models.CachedData(cache_key=cache_key, data=json.dumps(combined_results))
    db.add(new_cached_data)
    db.commit()
    
    return combined_results


# get school statistics
@router.get("/statistics", response_model=schemas.Statistics,status_code=status.HTTP_200_OK)
def schoolStatistics(school: schemas.SchoolIn, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
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
    school_statistics = utils.statistics(school_results)

    return school_statistics