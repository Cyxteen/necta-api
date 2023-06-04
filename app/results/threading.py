# necessary imports
import threading
from .multiple_years import multiple_years


def process_year(name_of_school, type_of_exam, year, curr_path):
    # gets a single result from each year
    file = f'{curr_path}/total-schools/{type_of_exam.upper()}-{year}.text'
    try:
        file2 = open(file, 'r')
    except FileNotFoundError:
        pass
    for word in file2:
        if name_of_school.upper() == word[5:].strip():
            school_reg_number = (word[0:5]).lower()
            break
        else:
            school_reg_number = ''
    multiple_years_results = multiple_years(name_of_school, type_of_exam, school_reg_number, year)
    return {year: multiple_years_results}

def process_multiple_years(name_of_school, type_of_exam, start_year, end_year, curr_path):
    # Calculate the number of years to process
    diff = int(end_year) - int(start_year)

    # Create a list to hold the threads
    threads = []

    # Create a dictionary to hold the results
    results_dict = {}
    final_results_dict = {}

    # Create a thread for each year's data
    for i in range(diff+1):
        year = int(start_year) + i
        t = threading.Thread(target=lambda: results_dict.update(process_year(name_of_school, type_of_exam, year, curr_path)))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Convert the results to JSON and return
    for year in results_dict:
        final_results_dict.update(results_dict[year])
    
    # sort the dictionary by keys
    sorted_dict = dict(sorted(final_results_dict.items()))
    try:
        iterating_year = start_year
        for year in sorted_dict:
            if(sorted_dict[year]["error"]):
                error = sorted_dict[year]["error"]
            iterating_year+=1
    except:
        pass
    # gets a single result from each year
    file = f'{curr_path}/total-schools/{type_of_exam.upper()}-{year}.text'
    try:
        error = None
        file2 = open(file, 'r')
    except FileNotFoundError:
        pass
    for word in file2:
        if name_of_school.upper() == word[5:].strip():
            school_reg_number = (word[0:5]).lower()
            break
        else:
            school_reg_number = None
    final_dict = {
        'school_name': name_of_school,
        'registration_number': school_reg_number,
        'error': error,
        'data': sorted_dict
    }
    # print(final_dict)
    return final_dict
