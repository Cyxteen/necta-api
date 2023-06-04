# imports
import os
from .single_year import single_year
from .threading import process_multiple_years

# gets the current path the file is located
curr_path = os.path.dirname(os.path.abspath(__file__))


def compare(name_of_school: str, type_of_exam: str, start_year: int, end_year=0):
    # change argument to low case
    name_of_school = name_of_school.lower()
    type_of_exam = type_of_exam.lower()

    # checks if only oney year is passed
    if end_year == 0:
        single_year_results = single_year(name_of_school, type_of_exam, start_year, curr_path)
        return single_year_results
    
    else:
        return process_multiple_years(name_of_school, type_of_exam, start_year, end_year, curr_path)

