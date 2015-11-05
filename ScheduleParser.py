import requests
import sqlite3
import re

from bs4 import BeautifulSoup

def is_class_info(tag):
    if tag == '\n' or len(tag.contents) != 7:
        return False
    else:
        return True

def get_classes(classes):
    """Takes in a list, classes, and outputs a tuple (dept, num, name) of all the courses in the schedule"""

    payload = {"p_term": "FL", "p_list_all": "Y"}
    r = requests.get('http://osoc.berkeley.edu/OSOC/osoc', params=payload)

    soup = BeautifulSoup(r.text, "html.parser")
    tbody = soup.find_all(cellspacing=0)[0] #finds the enlosing tbody tag
    rows = tbody.find_all(is_class_info)
    del rows[0] #remove header row

    for tag in rows:
        if tag != '\n':
            dept = tag.contents[1].string.strip()
            num = tag.contents[3].string.strip()
            name = "" #a few department colloquiums have no name listed, so we set to empty string to avoid NoneType errors
            if tag.contents[5].string:
                name = tag.contents[5].string.rstrip('. ')

            classes.append((dept, num, name))

def get_rooms(classes, curs):
    """Takes in the list of tuples, classes, and gets the time/location of each class"""

    for row in classes:
        payload = {'p_term': 'FL', 'p_dept': row[0], 'p_course': row[1], 'p_title': row[2], 'p_print_flag': 'N', 'p_list_all': 'N'}
        r = requests.post("http://osoc.berkeley.edu/OSOC/osoc", params=payload)
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.find_all('table')
        del tables[0] #remove header and footer
        del tables[-1]

        cancelled = ['TBA', 'UNSCHED', 'NOFACILITY', 'NO FACILITY', 'CANCELLED', 'INTERNET', 'OFF CAMPUS']

        for table in tables:
            elems = table.find_all('td')
            location = elems[6].string
            c = [x in location for x in cancelled]
            if not True in c:
                parse_location(location, curs)

def parse_location(location, curs):
    paren = location.find('(')
    if paren != -1:
        location = location[:paren]
    location = location.strip()

    spl = location.split(' ', 1)
    day = spl[0]
    location = spl[1]
    spl = location.split(',', 1)
    timeslot = spl[0]
    location = spl[1]
    location = location.strip()
    spl = location.split(' ', 1)
    room = spl[0]
    if room != '':
        building = spl[1]
        days = re.findall('[A-Z][a-z]*', day)
        pm = False
        if timeslot[-1] == 'P':
            pm = True
        start = timeslot[:-1].split('-')[0]
        end = timeslot[:-1].split('-')[1]
        if start[-2:] == '30':
            start = start[:-2]
            start = int(start)
            start += .5
        else:
            start = int(start)

        if end[-2:] == '30':
            end = end[:-2]
            end = int(end)
            end += .5
        else:
            end = int(end)

        cross_noon = False
        if end < start:
            cross_noon = True

        if pm and int(end) != 12:
            end += 12
            if not cross_noon:
                start += 12

        for d in days:
            s = start
            e = end
            while s != e:
                curs.execute("INSERT INTO locations (day, timeslot, room, building) VALUES (?, ?, ?, ?)", (d, start, room, building))

def main():
    conn = sqlite3.connect('locations.db')
    curs = conn.cursor()
    curs.execute('DROP TABLE IF EXISTS locations')
    curs.execute('CREATE TABLE IF NOT EXISTS locations (day TEXT, timeslot TEXT, room TEXT, building TEXT)')

    parse_location('M 4-5P,', curs)
    # classes = []
    # get_classes(classes)
    # get_rooms(classes, curs)

if __name__ == "__main__":
    main()
