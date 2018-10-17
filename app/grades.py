from bs4 import BeautifulSoup,NavigableString
import html2text
import socket
import ssl
import robobrowser
import http
import requests
from requests import Session
import json

requests.packages.urllib3.disable_warnings()

session = Session()
session.verify = False # Skip SSL verification
session.proxies = {'http': 'http://proxy22.iitd.ac.in/'} # Set default proxies
session.headers.update()
ACADEMICS_URL = 'https://academics1.iitd.ac.in/Academics/'

class AuthenticationError(Exception):
    pass

def get_gradesheet(username,password):

    # Browser
    br = robobrowser.RoboBrowser(session=session, parser='lxml')

    # The site we will navigate into, handling it's session
    br.open(ACADEMICS_URL)


    # Select the second (index one) form (the first form is a search query box)
    form = br.get_form(action='index.php?page=tryLogin')

    br.session.headers['Referer'] = ACADEMICS_URL

    # User credentials
    form['username'] = username
    form['password'] = password

    # Login
    br.submit_form(form)
    soup = BeautifulSoup(str(br.select),"lxml")
    current_grades_link=None
    past_grades_link=None
    for i in soup.find_all('a'):
        if 'vgrd' in str(i.get('href')):
            current_grades_link=i.get('href')
        if 'grade' in str(i.get('href')):
            past_grades_link=i.get('href')

    if (current_grades_link is None) and (past_grades_link is None):
        # Invalid Credentials
        raise AuthenticationError("Invalid Login Credentials")

    def remove_attrs(soup):
        for tag in soup.findAll(True):
            tag.attrs = None
        return soup

    grades_str = '' 
    if not(past_grades_link is None):

        br.open(ACADEMICS_URL+past_grades_link)

        soup = BeautifulSoup(str(br.select),"html5lib")

        soup_without_attributes=remove_attrs(soup)
        final_soup =soup_without_attributes.findAll('table')[0].findAll('table')[1].findAll('table')
        for div in final_soup:
            for x in div.find_all():
                if len(x.text) == 0:
                    x.extract()

    final_soup = final_soup[1].findAll('table')
    data = []
    idx = 0
    while idx < len(final_soup):
        semester = {}
        semester_number = final_soup[idx].findAll('strong')[1].string[-1]
        idx = idx+1
        tr = 1
        grades = {}
        table_rows = final_soup[idx].findAll('tr')
        idx = idx+1
        while tr < len(table_rows)-1:
            course = {}
            table_data = table_rows[tr].findAll('td')
            course_code = table_data[1].string
            course['course_name'] = table_data[2].string
            course['course_category'] = table_data[3].string
            course['course_credits'] = int(table_data[4].string[-1])
            course['course_grade'] = table_data[5].string
            grades[course_code] = course
            tr = tr+1
        semester_data = final_soup[idx].findAll('strong')
        semester['grades'] = grades
        semester['sgpa'] = float(semester_data[0].string[-5:])
        semester['cgpa'] = float(semester_data[1].string[-5:])
        semester['earned_credits'] = float(semester_data[2].string[-2:])
        semester['total_credits'] = float(semester_data[3].string[-2:])
        # data[semester_number] = semester
        data.append(semester)
        idx=idx+1

    return data


def getGrades(username,password):

    # def connect(self):      #some code to deal with certificate validation
    #         sock = socket.create_connection((self.host, self.port),
    #                             self.timeout, self.source_address)
    #         if self._tunnel_host:
    #             self.sock = sock
    #             self._tunnel()

    #         self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)


    # httplib.HTTPSConnection.connect = connect
    # Browser
    # Browser
    br = robobrowser.RoboBrowser(session=session)

    # The site we will navigate into, handling it's session
    br.open(ACADEMICS_URL)


    # Select the second (index one) form (the first form is a search query box)
    form = br.get_form(action='index.php?page=tryLogin')

    br.session.headers['Referer'] = ACADEMICS_URL

    # User credentials
    form['username'] = username
    form['password'] = password

    # Login
    br.submit_form(form)
    soup = BeautifulSoup(str(br.select),"lxml")
    current_grades_link=None
    past_grades_link=None
    for i in soup.find_all('a'):
        if 'vgrd' in str(i.get('href')):
            current_grades_link=i.get('href')
        if 'grade' in str(i.get('href')):
            past_grades_link=i.get('href')

    if (current_grades_link is None) and (past_grades_link is None):
        return (True,"Invalid Login Credentials")

    def remove_attrs(soup):
        for tag in soup.findAll(True):
            tag.attrs = None
        return soup

    grades_str = '' 

    if not(current_grades_link is None):
        
        gradesheet=br.open("https://academics1.iitd.ac.in/Academics/"+current_grades_link).read()

        soup = BeautifulSoup(gradesheet,"html5lib")
        soup_without_attributes=remove_attrs(soup)
        final_soup =soup_without_attributes.findAll('table')[0].findAll('table')[1].findAll('table')[2]

        for x in final_soup.find_all():
            if len(x.text) == 0:
                x.extract()

        grades_str += str(final_soup)

    return grades_str


# if __name__ == "__main__":
#     print(get_gradesheet("xxx ", "xxx"))
