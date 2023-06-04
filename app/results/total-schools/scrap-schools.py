"""
----------------------------------------
        PYTHON API Version 1.0.0        
----------------------------------------
works with results from 2014
"""
# imports
from bs4 import BeautifulSoup
import requests
import os

# gets the current path the file is located
curr_path = os.path.dirname(os.path.abspath(__file__))


def total_school_that_year(year: int, type_of_exam: str):
    # for advanced schools only
    # currently works with advanced results from 2015
    if type_of_exam == 'acsee':
        if year == 2022:
            base_url = f'https://matokeo.necta.go.tz/{type_of_exam.lower()}{year}/index.htm'
        elif year >= 2020:
            base_url = f'https://onlinesys.necta.go.tz/results/{year}/{type_of_exam.lower()}/index.htm'
        elif year == 2016:
            base_url = f'https://maktaba.tetea.org/exam-results/{type_of_exam.upper()}{year}/index.htm'
        else:
            base_url = f'https://onlinesys.necta.go.tz/results/{year}/{type_of_exam}/{type_of_exam}.htm'

    # file name
    file = f'{type_of_exam.upper()}-{year}.text'

    # check for file existence
    file_exists = os.path.exists(file)
    if file_exists:
        print(f'{file}: file already exists')
        pass
    else:
        # Creating a file at specified location
        with open(os.path.join(curr_path, file), 'w') as fp:
            pass

        try:
            # sends a get request to the url provided
            response = requests.get(base_url)
            # from the response sent above beautifulsoup parses the data received
            soup = BeautifulSoup(response.text, 'html.parser')

            # checks if the year is 2014 for secondary results
            if year == 2014 and type_of_exam == 'csee':
                total_schools = len(soup.find_all('table')[0].find_all('a'))

                existing_file = open(file, 'w')
                for i in range(0, (total_schools)):
                    school_no = soup.find_all('table')[0].find_all('a')[i].text
                    existing_file.write(school_no)
                    i += 1

                print('done')
                total_school_that_year((year-1), 'csee')

            # for advanced results
            elif year == 2015 and type_of_exam == 'acsee':
                total_schools = len(soup.find_all('table')[0].find_all('a'))

                existing_file = open(file, 'w')
                for i in range(0, (total_schools)):
                    school_no = soup.find_all('table')[0].find_all('a')[i].text
                    existing_file.write(school_no)
                    i += 1
            else:
                total_schools = len(soup.find_all('table')[2].find_all('a'))

                existing_file = open(file, 'w')
                for i in range(0, (total_schools)):
                    school_no = soup.find_all('table')[2].find_all('a')[i].text
                    existing_file.write(school_no)
                    i += 1

                # print(f'{year}-done')
                # if year >= 2015:
                #     total_school_that_year((year-1), 'acsee')
        except KeyboardInterrupt:
            print(curr_path)
            print('....Exiting')


total_school_that_year(2020, 'acsee')
