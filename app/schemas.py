from pydantic import EmailStr, BaseModel


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

class SingleStudent(BaseModel):
    division: str | None = None
    exam_number: str | None = None
    gender: str | None = None
    point: str | None = None
    school_name: str | None = None
    subjects: list = []
    url: str | None = None
