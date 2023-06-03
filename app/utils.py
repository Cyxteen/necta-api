from passlib.context import CryptContext
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(unhashed_password: str):
    hashed_password = pwd_context.hash(unhashed_password)

    return hashed_password

def verify_password(unhashed_password: str, hashed_password: str):
    verified = pwd_context.verify(unhashed_password, hashed_password)

    return verified

def check_status(user_id: int, db):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    # return user.activation_status
    if user.activation_status == "0":
        return False
    else:
        return True