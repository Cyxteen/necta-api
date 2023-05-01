from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(unashed_password: str):
    hashed_password = pwd_context.hash(unashed_password)
    
    return hashed_password