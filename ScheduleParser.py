import requests
from bs4 import BeautifulSoup

def is_class_tr(tag):


payload = {"p_term": "FL", "p_list_all": "Y"}
r = requests.get('http://osoc.berkeley.edu/OSOC/osoc', params=payload)

soup = BeautifulSoup(r.text, "html.parser"
tag = soup.find_all(cellpadding=0)
