import requests
from bs4 import BeautifulSoup

def is_class_info(tag):
    if tag == '\n' or len(tag.contents) != 7:
        return False
    else:
        return True


payload = {"p_term": "FL", "p_list_all": "Y"}
r = requests.get('http://osoc.berkeley.edu/OSOC/osoc', params=payload)

soup = BeautifulSoup(r.text, "html.parser")
tbody = soup.find_all(cellspacing=0)[0] #finds the enlosing tbody tag
classes = tbody.find_all(is_class_info)
del classes[0] #remove header row
print(classes[0].string)
