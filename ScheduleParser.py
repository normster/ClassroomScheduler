import requests

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

def get_rooms(classes):
    """Takes in the list of tuples, classes, and gets the time/location of each class"""

    for row in classes:
        payload = {'p_term': 'FL', 'p_dept': row[0], 'p_course': row[1], 'p_title': row[2], 'p_print_flag': 'N', 'p_list_all': 'N'}
        r = requests.post("http://osoc.berkeley.edu/OSOC/osoc", params=payload)
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.find_all('table')
        print(row[2])
        del tables[0] #remove header and footer
        del tables[-1]


        for table in tables:
            elems = table.find_all('td')
            location = elems[6].string
            print(location)

def main():
    classes = []
    get_classes(classes)
    get_rooms(classes)

if __name__ == "__main__":
    main()
