from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(unhashed_password: str):
    hashed_password = pwd_context.hash(unhashed_password)

    return hashed_password