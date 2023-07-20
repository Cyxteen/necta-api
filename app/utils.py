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
    
def statistics(data):
    statistics = {
        'school_name': data['school_name'], 
        'registration_number': data['registration_number'],
        'error': data['error'],
        'data': {

        }
    }

    for year, year_data in data["data"].items():
        total_students = year_data["total_students"]
        division_1 = year_data["division_1"]
        division_2 = year_data["division_2"]
        division_3 = year_data["division_3"]
        division_4 = year_data["division_4"]

        average_division_score = (division_1 + division_2 + division_3 + division_4) / 4
        pass_rate = (division_1 / total_students) * 100

        year_statistics = {
            "average_division_score": average_division_score,
            "pass_rate": round(pass_rate,1),
            "total_students": total_students
        }

        statistics['data'][year] = year_statistics

    return statistics

def check_string_in_file(file_path, search_string):
    with open(file_path, 'r') as file:
        for line in file:
            if search_string in line:
                return True
    return False