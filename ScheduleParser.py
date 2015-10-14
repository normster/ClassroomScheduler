import requests
import sqlite3
from bs4 import BeautifulSoup

def is_class_info(tag):
    if tag == '\n' or len(tag.contents) != 7:
        return False
    else:
        return True

def main():
    conn = sqlite3.connect('classes.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS classes")
    c.execute("CREATE TABLE IF NOT EXISTS classes (dept TEXT, num TEXT, name TEXT)")

    payload = {"p_term": "FL", "p_list_all": "Y"}
    r = requests.get('http://osoc.berkeley.edu/OSOC/osoc', params=payload)

    soup = BeautifulSoup(r.text, "html.parser")
    tbody = soup.find_all(cellspacing=0)[0] #finds the enlosing tbody tag
    classes = tbody.find_all(is_class_info)
    del classes[0] #remove header row

    for tag in classes:
        if tag != '\n':
            dept = tag.contents[1].string.strip()
            num = tag.contents[3].string.strip()
            name = ""
            if tag.contents[5].string:
                name = tag.contents[5].string.strip()

            c.execute("INSERT INTO classes ('dept', 'num', 'name') values (?, ?, ?)", (dept, num, name))
            print(dept, num, name)


    c.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
