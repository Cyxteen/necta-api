from typing import Dict, Optional, TypedDict
from pydantic import EmailStr, BaseModel, Field


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    activation_code: str

    class Config:
        orm_mode = True

class UserProfile(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class GetResult(BaseModel):
    school_registration_number: str
    student_exam_number: str
    student_level: str
    year_completed: str

class SingleStudentIn(BaseModel):
    school_registration_number: str
    student_exam_number: str
    student_level: str
    year_completed: int

class SingleStudentOut(BaseModel):
    school_name: str | None = None
    exam_number: str | None = None
    gender: str | None = None
    division: str | None = None
    point: str | None = None
    subjects: Dict[str, str] | None = None
    url: str | None = None
    error: str | None = None

class SchoolIn(BaseModel):
    school_name: str
    school_level: str
    start_year: int
    end_year: int | None = None


class YearData(BaseModel):
    division_1: int | None=None
    division_2: int | None=None
    division_3: int | None=None
    division_4: int | None=None
    division_0: int | None=None

class SchoolResults(BaseModel):
    school_name: Optional[str]
    registration_number: Optional[str]
    error: Optional[str]
    data: Dict[str, YearData] | None=None
