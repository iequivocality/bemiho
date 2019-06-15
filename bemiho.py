import json
from pprint import pprint
from bs4 import BeautifulSoup

with open('index/hinata.idols') as f:
    data = json.load(f)
    print(data[0]['blog'])
