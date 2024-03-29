# necessary imports
from bs4 import BeautifulSoup
import requests

def multiple_years(name_of_school:str, type_of_exam:str, school_reg_number:str, new_year:int):
    year_str = str(new_year)
    if school_reg_number != "":
        # check if exam level is advanced level or secondary level
        if type_of_exam == "acsee":
            url = f"https://onlinesys.necta.go.tz/results/{new_year}/acsee/results/{school_reg_number}.htm"

        elif type_of_exam == "csee":
            if new_year > 2014:
                url = f"https://onlinesys.necta.go.tz/results/{new_year}/csee/results/{school_reg_number}.htm"
            else:
                url = f"https://onlinesys.necta.go.tz/results/{new_year}/csee/{school_reg_number}.htm"
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # check for 200 response code if yes page is ok else 'not found'
            if response.status_code == 200:
                # calculates all students that sat for the exam
                # for school results later than >2014 (2019, 20 and 21)
                if type_of_exam == 'csee':
                    if new_year >= 2019:
                        # performance summary in table format
                        division_one = int((soup.find('table').find_all('tr')[
                                            3].find_all('p')[1:][1]).text)
                        division_two = int((soup.find('table').find_all('tr')[
                                            3].find_all('p')[1:][2]).text)
                        division_three = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][3]).text)
                        division_four = int((soup.find('table').find_all('tr')[
                                            3].find_all('p')[1:][4]).text)
                        division_zero = int((soup.find('table').find_all('tr')[
                                            3].find_all('p')[1:][5]).text)

                        total_students = division_one + division_two + \
                            division_three + division_four + division_zero

                        # calculates number of all absentees
                        total_absentees = len(
                            soup.body.findAll(text='ABS'))

                        # calculates number of all students who withdrew
                        total_withheld = len(
                            soup.body.findAll(text='*W'))

                        p = 6
                        # extracts the first exam number
                        first_exam_number = soup.find_all('tr')[
                            p].font.text
                        total_students = total_students + 5 + total_absentees + total_withheld

                    # for school results later than >2014 (2015, 16, 17 and 18)
                    elif new_year > 2014:
                        # performance summary in paragraph format
                        division_one = int(soup.find('h3').find(
                            'p').find('h3').text.split(' ')[2].strip(';'))
                        division_two = int(soup.find('h3').find(
                            'p').find('h3').text.split(' ')[6].strip(';'))
                        division_three = int(soup.find('h3').find(
                            'p').find('h3').text.split(' ')[10].strip(';'))
                        division_four = int(soup.find('h3').find(
                            'p').find('h3').text.split(' ')[14].strip(';'))
                        division_zero = int(soup.find('h3').find(
                            'p').find('h3').text.split(' ')[18].strip(';'))

                        # total number of all students(without absentees and withheld)
                        total_students = division_one + division_two + \
                            division_three + division_four + division_zero

                        # calculates number of all absentees
                        total_absentees = len(
                            soup.body.findAll(text='ABS'))

                        # calculates number of all students who withdrew
                        total_withheld = len(
                            soup.body.findAll(text='*W'))

                        p = 1
                        # extracts the first exam number
                        first_exam_number = soup.find_all('tr')[
                            p].font.text

                        # total number of all students(with absentees and withheld)
                        total_students = total_students + total_withheld + total_absentees
                    # for advanced results
                elif type_of_exam == 'acsee':
                    if new_year > 2019:
                        # performance summary in table format
                        try:
                            division_one = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][1]).text)
                            division_two = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][2]).text)
                            division_three = int((soup.find('table').find_all('tr')[
                                                    3].find_all('p')[1:][3]).text)
                            division_four = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][4]).text)
                            division_zero = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][5]).text)

                            total_students = division_one + division_two + \
                                division_three + division_four + division_zero

                            # calculates number of all absentees
                            total_absentees = len(
                                soup.body.findAll(text='ABS'))

                            # calculates number of all students who withdrew
                            total_withheld = len(
                                soup.body.findAll(text='*W'))

                            p = 6
                            # extracts the first exam number
                            first_exam_number = soup.find_all('tr')[
                                p].font.text
                            total_students = total_students + 5 + total_absentees + total_withheld
                        except ValueError:
                            # performance summary in paragraph format
                            division_one = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[2].strip(';'))
                            division_two = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[6].strip(';'))
                            division_three = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[10].strip(';'))
                            division_four = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[14].strip(';'))
                            division_zero = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[18].strip(';'))

                            # total number of all students(without absentees and withheld)
                            total_students = division_one + division_two + \
                                division_three + division_four + division_zero

                            # calculates number of all absentees
                            total_absentees = len(
                                soup.body.findAll(text='ABS'))

                            # calculates number of all students who withdrew
                            total_withheld = len(
                                soup.body.findAll(text='*W'))

                            p = 1
                            # extracts the first exam number
                            first_exam_number = soup.find_all('tr')[
                                p].font.text

                            # total number of all students(with absentees and withheld)
                            total_students = total_students + total_withheld + total_absentees

                        except AttributeError:
                            # performance summary in paragraph format
                            division_one = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[2].strip(';'))
                            division_two = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[6].strip(';'))
                            division_three = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[10].strip(';'))
                            division_four = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[14].strip(';'))
                            division_zero = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[18].strip(';'))

                            # total number of all students(without absentees and withheld)
                            total_students = division_one + division_two + \
                                division_three + division_four + division_zero

                            # calculates number of all absentees
                            total_absentees = len(
                                soup.body.findAll(text='ABS'))

                            # calculates number of all students who withdrew
                            total_withheld = len(
                                soup.body.findAll(text='*W'))

                            p = 1
                            # extracts the first exam number
                            first_exam_number = soup.find_all('tr')[
                                p].font.text

                            # total number of all students(with absentees and withheld)
                            total_students = total_students + total_withheld + total_absentees

                        # for school results later than >2013 (2014, 15, 16, 17 and 18)
                    elif new_year > 2013:
                        # performance summary in paragraph format
                        try:
                            division_one = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[2].strip(';'))
                            division_two = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[6].strip(';'))
                            division_three = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[10].strip(';'))
                            division_four = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[14].strip(';'))
                            division_zero = int(soup.find('h3').find(
                                'p').find('h3').text.split(' ')[18].strip(';'))

                            # total number of all students(without absentees and withheld)
                            total_students = division_one + division_two + \
                                division_three + division_four + division_zero

                            # calculates number of all absentees
                            total_absentees = len(
                                soup.body.findAll(text='ABS'))

                            # calculates number of all students who withdrew
                            total_withheld = len(
                                soup.body.findAll(text='*W'))

                            p = 1
                            # extracts the first exam number
                            first_exam_number = soup.find_all('tr')[
                                p].font.text

                            # total number of all students(with absentees and withheld)
                            total_students = total_students + total_withheld + total_absentees
                        except ValueError:
                            division_one = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][1]).text)
                            division_two = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][2]).text)
                            division_three = int((soup.find('table').find_all('tr')[
                                                    3].find_all('p')[1:][3]).text)
                            division_four = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][4]).text)
                            division_zero = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][5]).text)

                            total_students = division_one + division_two + \
                                division_three + division_four + division_zero

                            # calculates number of all absentees
                            total_absentees = len(
                                soup.body.findAll(text='ABS'))

                            # calculates number of all students who withdrew
                            total_withheld = len(
                                soup.body.findAll(text='*W'))

                            p = 6
                            # extracts the first exam number
                            first_exam_number = soup.find_all('tr')[
                                p].font.text
                            total_students = total_students + 5 + total_absentees + total_withheld
                        except AttributeError:
                            division_one = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][1]).text)
                            division_two = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][2]).text)
                            division_three = int((soup.find('table').find_all('tr')[
                                                    3].find_all('p')[1:][3]).text)
                            division_four = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][4]).text)
                            division_zero = int((soup.find('table').find_all('tr')[
                                                3].find_all('p')[1:][5]).text)

                            total_students = division_one + division_two + \
                                division_three + division_four + division_zero

                            # calculates number of all absentees
                            total_absentees = len(
                                soup.body.findAll(text='ABS'))

                            # calculates number of all students who withdrew
                            total_withheld = len(
                                soup.body.findAll(text='*W'))

                            p = 6
                            # extracts the first exam number
                            first_exam_number = soup.find_all('tr')[
                                p].font.text
                            total_students = total_students + 5 + total_absentees + total_withheld
                data = {
                    year_str:{
                        'total_students': total_students,
                        'total_withheld': total_withheld,
                        'absentees': total_absentees,
                        'division_1': division_one,
                        'division_2': division_two,
                        'division_3': division_three,
                        'division_4': division_four,
                        'division_0': division_zero
                    }
                }
                # print(data)
                return data
                
        except requests.ConnectionError:
            return {
                year_str:{
                    'error':'internet connetion is down'
                }
            }

    else:
        return {
            year_str:{
                'error':'results not found'
            }
        }

