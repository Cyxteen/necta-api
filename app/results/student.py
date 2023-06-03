# imports
from bs4 import BeautifulSoup
import requests

# main function
def get_student(year, school_number, exam_number, exam_type):
    url = ''
    # converts the year into an integer
    year = int(year)
    if year < 2014:
        return {"error": "results before 2014 are not available"}
    # converts the exam number and the exam type
    exam_number = exam_number.lower()
    exam_type = exam_type.lower()
    # stringfy the exam number
    exam_number = f'{school_number}/{exam_number}'

    # check if exam level is advanced level or secondary level
    if exam_type == "acsee":
        url = f"https://onlinesys.necta.go.tz/results/{year}/acsee/results/{school_number}.htm"

    elif exam_type == "csee":
        if year > 2014:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/results/{school_number}.htm"
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/{school_number}.htm"

    try:
        # checks for response from the site if no then terminate after 3 tries
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # check for 200 response code if yes page is ok else 'not found'
        if response.status_code == 200:
             # calculates all students that sat for the exam
            # for school results later than >2014 (2019, 20 and 21)
            if exam_type =='csee':
                if year >= 2019:
                    # performance summary in table format
                    range_1 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][1]).text)
                    range_2 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][2]).text)
                    range_3 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][3]).text)
                    range_4 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][4]).text)
                    range_5 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][5]).text)
                    
                    # get total students
                    total_students = range_1 + range_2 + range_3 + range_4 + range_5

                    # calculates number of all absentees
                    total_absentees = len(soup.body.findAll(text='ABS'))

                    # calculates number of all students who withdrew
                    total_withheld = len(soup.body.findAll(text='*W'))
                    
                    i=6
                    # extracts the first exam number
                    first_exam_number = soup.find_all('tr')[i].font.text
                    total_students = total_students + 5 + total_absentees + total_withheld
                
                # for school results later than >2014 (2015, 16, 17 and 18)
                elif year > 2014:
                    # performance summary in paragraph format
                    range_1 = int(soup.find('h3').find('p').find('h3').text.split(' ')[2].strip(';'))
                    range_2 = int(soup.find('h3').find('p').find('h3').text.split(' ')[6].strip(';'))
                    range_3 = int(soup.find('h3').find('p').find('h3').text.split(' ')[10].strip(';'))
                    range_4 = int(soup.find('h3').find('p').find('h3').text.split(' ')[14].strip(';'))
                    range_5 = int(soup.find('h3').find('p').find('h3').text.split(' ')[18].strip(';'))
                
                    # total number of all students(without absentees and withheld)
                    total_students = range_1 + range_2 + range_3 + range_4 + range_5
                    
                    # calculates number of all absentees
                    total_absentees = len(soup.body.findAll(text='ABS'))

                    # calculates number of all students who withdrew
                    total_withheld = len(soup.body.findAll(text='*W'))
                    
                    i=1
                    # extracts the first exam number
                    first_exam_number = soup.find_all('tr')[i].font.text

                    # total number of all students(with absentees and withheld)
                    total_students = total_students + total_withheld + total_absentees
            # for advanced results
            elif exam_type == 'acsee':
                if year > 2019:
                    # performance summary in table format
                    range_1 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][1]).text)
                    range_2 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][2]).text)
                    range_3 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][3]).text)
                    range_4 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][4]).text)
                    range_5 = int((soup.find('table').find_all('tr')[3].find_all('p')[1:][5]).text)

                    total_students = range_1 + range_2 + range_3 + range_4 + range_5

                    # calculates number of all absentees
                    total_absentees = len(soup.body.findAll(text='ABS'))
                    
                    # calculates number of all students who withdrew
                    total_withheld = len(soup.body.findAll(text='*W'))
                    
                    i=6
                    # extracts the first exam number
                    # first_exam_number = soup.find_all('tr')[i].font.text
                    total_students = total_students + 5 + total_absentees + total_withheld
                
                # for school results later than >2013 (2014, 15, 16, 17 and 18)
                elif year > 2013:
                    # performance summary in paragraph format
                    range_1 = int(soup.find('h3').find('p').find('h3').text.split(' ')[2].strip(';'))
                    range_2 = int(soup.find('h3').find('p').find('h3').text.split(' ')[6].strip(';'))
                    range_3 = int(soup.find('h3').find('p').find('h3').text.split(' ')[10].strip(';'))
                    range_4 = int(soup.find('h3').find('p').find('h3').text.split(' ')[14].strip(';'))
                    range_5 = int(soup.find('h3').find('p').find('h3').text.split(' ')[18].strip(';'))
                
                    # total number of all students(without absentees and withheld)
                    total_students = range_1 + range_2 + range_3 + range_4 + range_5
                    
                    # calculates number of all absentees
                    total_absentees = len(soup.body.findAll(text='ABS'))

                    # calculates number of all students who withdrew
                    total_withheld = len(soup.body.findAll(text='*W'))
                    
                    i=1
                    # extracts the first exam number
                    first_exam_number = soup.find_all('tr')[i].font.text

                    # total number of all students(with absentees and withheld)
                    total_students = total_students + total_withheld + total_absentees

            while i <= total_students:
                if (exam_number).upper() == soup.find_all('tr')[i].font.text:
                    
                    # uncleaned_school_name = soup.select_one("h3").p
                    cleaned_one = soup.find_all('h3')[0].p.text

                    # cleaned school name
                    cleaned_school_name = cleaned_one.split('\n')[0].strip()

                    name = soup.find_all('tr')[i]
                    # student_exam_number = name.find_all('p')[0].text
                    student_gender = name.find_all('p')[1].text
                    student_points = name.find_all('p')[2].text.strip(" ")
                    student_division = name.find_all('p')[3].text
                    subject_length = len(name.find_all('p')[4].text.split('  '))

                    # creates subjects list for storing subjects
                    subjects = []
                    for a in range(subject_length-1):
                        subjects.append(name.find_all('p')[4].text.split('  ')[a].strip(' '))

                    subject_dict = {}
                    for subject in subjects:
                        subject_parts = subject.split("-")
                        subject_code = subject_parts[0].strip()
                        grade = subject_parts[1].strip()
                        subject_dict[subject_code] = grade.strip("'")
                    
                    return_json = {
                        'status' : 200,
                        'school_name' : cleaned_school_name[6:],
                        'url' : url,
                        'exam_number' :  exam_number.upper(),
                        'gender' : student_gender,
                        'division' : student_division,
                        'point': student_points,
                        'subjects': subject_dict,
                        'error': None
                    }

                    return return_json
                else:
                    if i == total_students:
                        return {'error': "Exam number does not exist"}
                    i+=1

        else:
            return {'error': "An error occured"}
    
    # checks for connection(internet) error
    except:
        return {'error': "An error occured"}
    
   